import random

card_accounts = []
card_pins = []

def options():
    print("1. Create an account")
    print("2. Log into account")
    print("0. Exit")

def logged_in():
    print("1. Balance")
    print("2. Log out")
    print("0. Exit")

def create_card_number():
    card_value = "400000" + str(random.randint(1000000000, 9999999999))
    card_value_final = str(card_value)
    card_accounts.append(card_value_final)
    return card_value_final

def create_pin():
    pin_first = random.randint(0, 9)
    pin_second = random.randint(0, 9)
    pin_third = random.randint(0, 9)
    pin_fourth = random.randint(0, 9)
    pin = str(pin_first) + str(pin_second) + str(pin_third) + str(pin_fourth)
    card_pins.append(pin)
    return pin

stopped = False
while stopped != True:
    options()
    user_input = input()
    if user_input == "1":
        print()
        print("Your card has been created")
        print("Your card number:")
        card_number = create_card_number()
        print(card_number)
        print("Your card PIN:")
        pin = create_pin()
        print(pin)
        print()
    elif user_input == "2":
        print()
        print("Enter your card number:")
        card_input = input()
        print("Enter your PIN:")
        pin_input = input()

        if pin_input in card_pins:
            position_value = card_pins.index(pin_input)
            if card_input == card_accounts[position_value]:
                print()
                print("You have successfully logged in!")
                print()
                logged_in()
                stopped_two = False
                while stopped_two != True:
                    user_input_two = input()
                    if user_input_two == "1":
                        print()
                        print("Balance: 0")
                        print()
                        logged_in()
                    elif user_input_two == "2":
                        print()
                        print("You have successfully logged out!")
                        print()
                        stopped_two = True
                    else:
                        stopped_two = True
                        stopped = True
                        print()
                        print("Bye!")
            else:
                print()
                print("Wrong card number or PIN!")
                print()
        elif card_input in card_accounts:
            position_value = card_accounts.index(card_input)
            if pin_input == card_pins[position_value]:
                print()
                print("You have successfully logged in!")
                print()
                logged_in()
                stopped_two = False
                while stopped_two != True:
                    user_input_two = input()
                    if user_input_two == "1":
                        print()
                        print("Balance: 0")
                        print()
                        logged_in()
                    elif user_input_two == "2":
                        print()
                        print("You have successfully logged out!")
                        print()
                        stopped_two = True
                    else:
                        stopped_two = True
                        stopped = True
                        print()
                        print("Bye!")
            else:
                print()
                print("Wrong card number or PIN!")
                print()
        else:
            print()
            print("Wrong card number or PIN!")
            print()
    else:
        stopped = True
        print()
        print("Bye!")






