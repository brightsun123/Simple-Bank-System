import sqlite3
import random

conn = sqlite3.connect('card.s3db')
cur = conn.cursor()
cur.execute("DROP TABLE IF EXISTS card;") # can use to remove table; to keep data - comment out this statement
cur.execute("""CREATE TABLE IF NOT EXISTS card (
        id INTEGER PRIMARY KEY AUTOINCREMENT, 
        number TEXT, 
        pin TEXT, 
        balance INTEGER DEFAULT 0
        );""")
conn.commit()
# card_accounts = []
# card_pins = []
card_counter = 0

def options():
    print("1. Create an account")
    print("2. Log into account")
    print("0. Exit")

def logged_in():
    print("1. Balance")
    print("2. Add income")
    print("3. Do transfer")
    print("4. Close account")
    print("5. Log out")
    print("0. Exit")

def create_card_number():
    global card_counter
    card_value = "400000" + str(random.randint(100000000, 999999999))
    card_value_list = list(card_value)
    card_value_list = list(map(int, card_value_list))
    check_sum = 0
    sum_value = 0
    for i in range(len(card_value_list)):
        if (i + 1) % 2 == 1:
            card_value_list[i] *= 2
    for num in card_value_list:
        if num > 9:
            index = card_value_list.index(num)
            card_value_list[index] -= 9
    for num_value in card_value_list:
        sum_value += num_value
    total_sum = sum_value
    while total_sum % 10 != 0:
        check_sum += 1
        total_sum += 1
    card_value_final = str(card_value) + str(check_sum)
    # card_accounts.append(card_value_final)
    cur.execute("INSERT INTO card (number) VALUES (?);", (card_value_final,))
    conn.commit()
    card_counter += 1
    return card_value_final

def luhn_algorithm(card_value):
    card_value_check = list(map(int, card_value))
    last_digit = card_value_check[-1]
    card_value_check.pop()
    sum_check = 0
    for i in range(len(card_value_check)):
        if (i + 1) % 2 == 1:
            card_value_check[i] *= 2
    for num in card_value_check:
        if num > 9:
            index = card_value_check.index(num)
            card_value_check[index] -= 9
    for num_value in card_value_check:
        sum_check += num_value
    sum_check += last_digit
    if sum_check % 10 == 0:
        return True
    else:
        return False

def in_system(card_match_input):
    cur.execute("SELECT number FROM card WHERE number = ?", (card_match_input,))
    card_match = cur.fetchall()
    if not card_match:
        return False
    else:
        return True
def create_pin():
    pin_first = random.randint(0, 9)
    pin_second = random.randint(0, 9)
    pin_third = random.randint(0, 9)
    pin_fourth = random.randint(0, 9)
    pin = str(pin_first) + str(pin_second) + str(pin_third) + str(pin_fourth)
    # card_pins.append(pin)
    cur.execute("UPDATE card SET pin = ? WHERE id = ?;", (pin, card_counter))
    conn.commit()
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
        cur.execute("SELECT number FROM card WHERE pin = ?", (pin_input,))
        pin_match = cur.fetchall()
        if not pin_match:
            print()
            print("Wrong card number or PIN!")
            print()
        else:
            pin_match_card = pin_match[0][0]
            if pin_match_card == card_input:
                print()
                print("You have successfully logged in!")
                print()
                logged_in()
                stopped_two = False
                while stopped_two != True:
                    user_input_two = input()
                    if user_input_two == "1":
                        print()
                        cur.execute("SELECT balance FROM card WHERE pin = ?", (pin_input,))
                        conn.commit()
                        balance_value = cur.fetchall()[0][0]
                        print("Balance: " + str(balance_value))
                        print()
                        logged_in()
                    elif user_input_two == "2":
                        print()
                        print("Enter income:")
                        add_value = int(input())
                        cur.execute("UPDATE card SET balance = balance + ? WHERE number = ?;", (add_value, card_input))
                        conn.commit()
                        print("Income was added!")
                        print()
                        logged_in()
                    elif user_input_two == "3":
                        print()
                        print("Transfer")
                        print("Enter card number:")
                        card_input_transfer = input()
                        luhn_check = luhn_algorithm(card_input_transfer)
                        if luhn_check:
                            if in_system(card_input_transfer):
                                print("Enter how much money you want to transfer:")
                                transfer_money = int(input())
                                cur.execute("SELECT balance FROM card WHERE number = ?", (card_input,))
                                conn.commit()
                                balance_before_transfer = cur.fetchall()[0][0]
                                if balance_before_transfer >= transfer_money:
                                    cur.execute("UPDATE card SET balance = balance - ? WHERE number = ?;",
                                                (transfer_money, card_input))
                                    conn.commit()
                                    cur.execute("UPDATE card SET balance = balance + ? WHERE number = ?;",
                                                (transfer_money, card_input_transfer))
                                    conn.commit()
                                    print("Success!")
                                    print()
                                    logged_in()
                                else:
                                    print("Not enough money!")
                                    print()
                                    logged_in()
                            else:
                                print("Such a card does not exist.")
                                print()
                                logged_in()
                        else:
                            print("Probably you made a mistake in the card number. Please try again!")
                            print()
                            logged_in()

                    elif user_input_two == "4":
                        print()
                        cur.execute("DELETE FROM card WHERE number = ?", (card_input,))
                        conn.commit()
                        print("The account has been closed!")
                        stopped_two = True
                        print()
                    elif user_input_two == "5":
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
                options()
    else:
        stopped = True
        print()
        print("Bye!")