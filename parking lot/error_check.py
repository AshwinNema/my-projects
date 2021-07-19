class ErrorCheck:
    def check_money(self, money):
        if money == "YES" or money == "NO":
            return True

        return False

    def check_amount(self, amount):
        for i in range(len(amount)):
            if 48 <= ord(amount[i]) <= 57:
                continue

            else:
                return False

        return True

    def check_car(self, count):
        if count == "YES" or count == "NO":
            return True

        return False

    def check_start(self, start):
        start = start.split()
        if len(start) != 2 or start[0] != "create_parking_lot":
            return False

        for i in range(len(start[1])):
            if i == 0 and 49 <= ord(start[1][i]) <= 57:
                continue

            elif 48 <= ord(start[1][i]) <= 57:
                continue

            else:
                return False

        start[1] = int(start[1])

        if start[1] == 0:
            return False

        return start[1]

    def check_leave(self, leave, spots):
        if leave[0] != "leave" or len(leave) != 2:
            return False

        for i in range(len(leave[1])):
            if i == 0 and 49 <= ord(leave[1][0]) <= 57:
                continue

            elif 48 <= ord(leave[1][i]) <= 57 and i != 0:
                continue

            else:
                return False

        slot = int(leave[1])
        if slot > len(spots):
            return False

        elif spots[slot - 1] is False:
            return str(slot)

        else:
            return slot