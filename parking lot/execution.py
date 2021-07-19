from parking_lot import ParkingLot
from car import Car
from error_check import ErrorCheck
from slots import Slots


class Execution:
    def __init__(self, capacity, charge=0):
        self.charge = charge
        self.spots = Slots(capacity, self.charge)
        self.parking = ParkingLot()
        self.review = ErrorCheck()

    def execute(self, act):
        act = act.split()
        assign = {"park": self.park(act), "leave": self.leave(act),
                  "status": self.status(act),
                  "registration_numbers_for_cars_with_colour":
                  self.registration_numbers_for_cars_with_colour(act),
                  "slot_numbers_for_cars_with_colour":
                  self.slot_numbers_for_cars_with_colour(act),
                  "slot_number_for_registration_number":
                  self.slot_number_for_registration_number(act)}

        if assign.get(act[0]) is None or assign.get(act[0]) is False:
            print("Invalid Input")

    def park(self, act):
        if act[0] != "park" or len(act) != 3:
            return False

        if self.parking.registration_number_to_slot_number.get(act[1]) is None:
            check = self.spots.add()

            if check:
                Vehicle = Car(act[1], act[2])
                self.parking.add(check, Vehicle)

                print("Allocated slot number " + str(check))

            else:
                print("Sorry, parking lot is full")

        else:
            print("Sorry, car of this registration number is already parked")
        return True

    def leave(self, act):
        slot = self.review.check_leave(act, self.spots.register)

        if not(slot):
            return False

        elif type(slot) == str:
            print("Slot number " + slot + " was already free")

        else:
            self.spots.remove(slot)
            self.parking.remove(slot)
            print(f"Slot number {slot} is free")

        return True

    def status(self, act):
        if act[0] != "status" or len(act) != 1:
            return False

        if len(self.parking.slot_number) > 0:
            print("Slot No. Registration No Colour")
            for key in self.parking.slot_number.keys():
                registration = self.parking.slot_number[key][0]
                color = self.parking.slot_number[key][1]
                print(key, registration, color)
        else:
            print("Parking lot is empty")

        return True

    def registration_numbers_for_cars_with_colour(self, act):
        check = "registration_numbers_for_cars_with_colour"
        if len(act) != 2 or act[0] != check:
            return False

        value = self.parking.color_to_registration_number.get(act[1])

        if value is None or value == []:
            print("Not found")

        else:
            print(*value, sep=", ")

        return True

    def slot_numbers_for_cars_with_colour(self, act):
        if act[0] != "slot_numbers_for_cars_with_colour" or len(act) != 2:
            return False

        value = self.parking.color_to_slot_number.get(act[1])

        if value is None or value == []:
            print("Not found")

        else:
            print(*value, sep=", ")

        return True

    def slot_number_for_registration_number(self, act):
        if len(act) != 2 or act[0] != "slot_number_for_registration_number":
            return False

        value = self.parking.registration_number_to_slot_number.get(act[1])

        if value is None or value == []:
            print("Not found")

        else:
            print(value)

        return True
