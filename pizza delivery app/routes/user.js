const express = require('express')
const { verify_email, verify_mobile_number, verifydistance } = require('../middlewares/verification')
require('dotenv').config()
const { checkinglastordertime } = require('../middlewares/miscellaneous')
const UserModel = require('../models/User')
const user_router = express.Router()
user_router.use(express.urlencoded({ extended: true }))
const session = require('express-session')
const MongoDBStore = require('connect-mongodb-session')(session)
const { DATABASE, SESSIONSECRET, SESSION } = process.env
const bcrypt = require('bcrypt')
const axios = require('axios')
const OrderModel = require('../models/order')
const store = new MongoDBStore({
    uri: DATABASE,
    collection: SESSION
})

user_router.use(session({
    secret: SESSIONSECRET,
    resave: false,
    saveUninitialized: false,
    store: store
}))

//Renders the home page
user_router.get('/', async (req, res) => {
    req.session.gotanorder = false
    let edit_order = {edit:true}
    let can_edit_order = await checkinglastordertime(req.session.user, Date.now()) 
    if (can_edit_order) {
        res.render('home',{...req.session.user,...edit_order})
        return
    } 
    else {
        req.session.editorder = false
    }
    res.render('home', req.session.user)

})

//Renders login page if user has not been logged in,else redirects to home page
user_router.get('/login', async (req, res) => {
    req.session.gotanorder = false
    if (req.session.isloggedin) {
        res.redirect("/")
        return
    }
    res.render('login')
})

//Renders signup page if user has not been logged in,else redirects to home page
user_router.get('/signup', (req, res) => {
    req.session.gotanorder = false
    if (req.session.isloggedin) {
        res.redirect("/")
        return
    }
    res.render("signup")
})

//Checks that the user details provided during signup are correct,then redirects user to home page
user_router.post('/signup', async (req, res) => {
    req.session.gotanorder = false
    req.session.editorder = false
    req.session.orderprice = null
    req.session.ordertype = null
    if (req.session.isloggedin) {
        res.redirect("/")
        return
    }

    const verifyemail = await verify_email(req.body.email)
    const verifynumber = await verify_mobile_number(req.body.mobile_number)
    if (!verifyemail || !verifynumber || req.body.password != req.body.confirmpassword) {
        res.render("signuperror")
        return
    }
    delete req.body.confirmpassword
    try {
        const salt = await bcrypt.genSalt(10)
        const hash = await bcrypt.hash(req.body.password, salt)
        req.body.password = hash
        const newuser = new UserModel(req.body)
        const finaluser = await newuser.save()
        req.session.isloggedin = true
        req.session.user = { _id: finaluser._id, name: finaluser.name, mobile_number: finaluser.mobile_number, email: finaluser.email}
        res.redirect("/")
        return
    } catch (error) {
        console.log(error)
    }
    res.render("signuperror")
})

//Checks login details of the user then redirects to home page
user_router.post('/login', async (req, res) => {
    req.session.editorder = false
    req.session.orderprice = null
    req.session.ordertype = null
    req.session.gotanorder = false
    if (!req.session.isloggedin) {
        try {
            const user = await UserModel.findOne({ email: req.body.email })
            const isMatching = await bcrypt.compare(req.body.password, user.password)
            if (user != null && isMatching) {
                req.session.isloggedin = true
                req.session.user = { _id: user._id, name: user.name, mobile_number: user.mobile_number, email: user.email}
                res.redirect("/")
                return
            }
        } catch (error) {
            console.log(error)
        }
        res.render('loginerror')
    } else {
        res.redirect("/")
    }
})

//Logs out user then redirects to home page
user_router.post('/logout', async (req, res) => {
    req.session.gotanorder = false
    req.session.isloggedin = false
    req.session.user = null
    req.session.orderprice = null
    req.session.ordertype = null
    req.session.editorder = null
    res.redirect("/")
})

// Renders edit profile page if user has signed in else redirects to home page

user_router.post("/editprofile", async (req, res) => {
    req.session.gotanorder = false
    if (req.session.isloggedin) {
        res.render('updateuser')
        return
    }
    res.redirect("/")
})

// Checks that details provided ny the user during update are correct or not then redirects user to the home page

user_router.post('/updateuser', async (req, res) => {
    req.session.gotanorder = false
    if (req.session.isloggedin) {
        if (req.body.password != req.body.confirmpassword) {
            res.render('updateusererror')
            return
        }
        const newobject = {}
        if (req.body.name) {
            newobject.name = req.body.name
            req.session.user.name = req.body.name
        }

        if (req.body.email && verify_email(req.body.email)) {
            newobject.email = req.body.email
            req.session.user.email = req.body.email
        }

        if (req.body.mobile_number && verify_mobile_number(req.body.mobile_number)) {
            newobject.mobile_number = req.body.mobile_number
            req.session.user.mobile_number = req.body.mobile_number
        }

        if (req.body.password) {
            newobject.password = req.body.password
            req.session.user.password = req.body.password
        }

        if (Object.keys(newobject).length != 0) {
            await UserModel.updateOne({ _id: req.session.user._id }, { $set: newobject })
        }
        res.redirect("/")
    } else {
        res.redirect("/")
    }
})

// If the user has been logged in then user account is deleted after this redirects to main page

user_router.post("/deleteuser", async (req, res) => {
    if (req.session.isloggedin) {
        req.session.isloggedin = false
        await UserModel.deleteOne({ _id: req.session.user._id })
        await OrderModel.deleteMany({Customer: req.session.user._id})
        req.session.destroy()
    }
    res.redirect("/")
})

// Saves user location if user has been logged in, then redirects user to home page

user_router.post('/savelocation',async (req, res) => {
    req.session.gotanorder = false
    if (req.session.isloggedin) {
        if (verifydistance(req.body.latitude, req.body.longtitude)) {
            await UserModel.updateOne({ _id: req.session.user._id }, {location:[req.body.latitude, req.body.longtitude]})
        }
        res.json({ redirectUrl: "/" })
        return
    }
    res.redirect("/")
})

module.exports = user_router