from error_check import ErrorCheck

from execution import Execution


class DisplayOutput:
    def __init__(self):
        self.review = ErrorCheck()

    def display_header(self):
        print("-"*90)
        print()
        print(" "*33, "WELCOME TO PARKATO", " "*40)
        print()
        print("-"*90)
        print()
        print("Do you want to earn money through your your parking lot?")
        print()
        print("If yes, then type YES")
        print()
        print("If not, then type NO")
        print()

    def money(self):
        flag = False
        money = input()
        print()

        if self.review.check_money(money):
            if money == "YES":
                charge = "Enter amount you want to charge each customer:"
                print(charge, end=" ")
                amount = input()

                if self.review.check_amount(amount):
                    amount = int(amount)
                    flag = amount
                    print()

                else:
                    print("Invalid Input")
                    print()

        else:
            print("Invalid Input")
            print()

        return flag

    def cars(self):
        flag = False

        print("Do you want to know how many cars", end=" ")
        print("will be parked in your parking lot?")
        print()
        print("If yes, then type YES")
        print()
        print("If not, then type NO")
        print()

        count = input()
        print()
        if self.review.check_car(count):
            if count == "YES":
                flag = True

        else:
            print("Invalid Input")
            print()

        return flag

    def mode_execution(self, money, cars):
        print("Please select the mode of input")
        print()
        print("Press 1 for providing input through command prompt", end="")
        print(" based shell where commands can be typed in")
        print("Press 2 to accept a filename as a parameter ", end="")
        print("at the command prompt and read the commands from that file")
        print()

        mode = input()

        if mode == "1":
            print()
            self.interactive_mode(money, cars)

        elif mode == "2":
            print()
            self.user_file_mode(money, cars)

        else:
            print("Invalid Input")

    def display_money(self, money, income):
        if money:
            print("Total income = ", end="")
            print(income)
            print()

    def display_cars(self, cars, count):
        if cars:
            print("Total number of vehicles ", end="")
            print("that were parked in the parking lot = ", end="")
            print(count)

    def interactive_mode(self, money, cars):
        command = input()

        start = self.review.check_start(command)

        if not(start):
            print("Invalid Input")

        else:
            print(f"Created a parking lot with {start} slots")

            if money:
                user = Execution(start, money)

            else:
                user = Execution(start)

            while command != "exit":
                command = input().strip()

                if command != "exit":
                    user.execute(command)

            print()
            self.display_money(money, user.spots.income)
            self.display_cars(cars, user.spots.count)

    def user_file_mode(self, money, cars):
        print("Please enter the source of file:", end=" ")
        source = input()
        print()

        import os
        path = f"{os.path.dirname(os.path.abspath(__file__))}/{source}"
        file = open(path)
        output = 1

        for content in file:
            if output == 1:
                start = self.review.check_start(content)

                if not(start):
                    print("Invalid Input")

                else:
                    print(f"Created a parking lot with {start} slots")

                    if money:
                        user = Execution(start, money)

                    else:
                        user = Execution(start)

                output += 1

            elif start:
                content = content.strip()
                user.execute(content)

        file.close()
        if start:
            print()
            self.display_money(money, user.spots.income)
            self.display_cars(cars, user.spots.count)
