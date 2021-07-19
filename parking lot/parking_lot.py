class ParkingLot:
    def __init__(self):
        self.slot_number = {}

        self.color_to_registration_number = {}

        self.color_to_slot_number = {}

        self.registration_number_to_slot_number = {}

    def add(self, slot, Car):
        registration = Car.registration
        color = Car.color
        if color not in self.color_to_registration_number:

            self.slot_number[slot] = [registration, color]

            self.color_to_registration_number[color] = [registration]

            self.color_to_slot_number[color] = [slot]

            self.registration_number_to_slot_number[registration] = slot

        else:
            self.slot_number[slot] = [registration, color]

            self.color_to_registration_number[color].append(registration)

            self.color_to_slot_number[color].append(slot)

            self.registration_number_to_slot_number[registration] = slot

    def remove(self, slot):
        registration = self.slot_number[slot][0]
        color = self.slot_number[slot][1]

        self.color_to_registration_number[color].remove(registration)

        self.color_to_slot_number[color].remove(slot)

        self.registration_number_to_slot_number.pop(registration)

        self.slot_number.pop(slot)
