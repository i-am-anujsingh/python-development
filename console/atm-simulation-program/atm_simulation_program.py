'''------- ATM SIMULATION PROGRAM -------'''
import os

def menu():
    '''FUNCTION TO DISPLAY MENU OF ATM SIMULATION'''
    print('\n\tMENU\n\t\b——————')
    print('1. Display Balance\n2. Change PIN\n3. Withdrawl\n4. Deposit\n5. Cancel')


def card_entry():
    '''FUNTION TO ENTER CARD NUMBER, AND VALIDATE THE USRE'''
    try:
        cardNum = input('\nEnter Card Number: ')
        assert cardNum.isdigit(), 'CARD NUM MUST BE OF DIGIT!!'
        assert len(cardNum) == 12, 'INVALID CARD NUMBER LENGTH, CARD NUMBER LENGTH MUST BE OF 12.'

    except AssertionError as ae:
        print(ae)

    else:
        try:
            print('\n Welcome!', users[cardNum][0])

        except KeyError:
            print('INVALID CARD DETAIL.')

        else:
            return (cardNum)


def pin_entry(cn, fn):
    '''FUNCTION TO ENTER CARD PIN, AND VALIDATE THE USER'''
    pin_attempts=3
    while True:
        if(pin_attempts<=0):
            print("OUT OF ATTEMPTS! PLEASE TRY AFTER SOME TIME.")
            input("\nPRESS ENTER TO GO BACK TO THE MENU.")
            clear_screen()
            break
        try:
            pin = int(input('Enter pin: '))
            assert (pin > 999 and pin < 10000), 'INVALID PIN LENGTH, PIN LENGTH MUST BE OF 4.'

        except ValueError:
            print('PIN MUST BE A 4 DIGIT NUMBER.')

        except AssertionError as ae:
            print(ae)

        else:
            if (pin == users[cn][1]):
                fn(cn)
                break

            else:
                print('INVALID PIN.')
            
            pin_attempts-=1


def print_user(cn):
    '''FUNCTION TO PRINT USER DETAILS'''
    print('\n—————User Details—————\n')
    print('Name :', users[cn][0])
    print('Balance :', users[cn][2])


def change_pin(cn):
    '''FUNCTION TO CHANGE PIN'''
    try:
        newPin = int(input('Enter new 4 digit PIN:'))
        assert (newPin > 999 and newPin < 10000), 'INVALID PIN LENGTH, PIN LENGTH MUST BE OF 4.'
        users[cn][1] = newPin
        print("New Changed PIN is", users[cn][1])

    except ValueError:
        print('NEW PIN MUST BE A 4 DIGIT NUMBER.\n')

    except AssertionError as ae:
        print(ae)


def withdrawl(cn):
    '''FUNCTION TO WITHDRAW CASH'''
    try:
        amount = int(input('Enter Amount to be Withdrawl: '))

        if ((users[cn][2] < amount) or (amount <= 0)):
            print('WITHDRAWL MUST BE LESS THAN BALANCE. AND AMOUNT CAN NOT BE IN NEGATIVE OR ZERO.')

        elif (amount > 10000):
            print('WITHDRAWL LIMIT IS 10000.')

        else:
            users[cn][2] -= amount
            print('Withdrawl amount is:', amount)
            print('Balance after withdrawl is:', users[cn][2])

    except ValueError as ve:
        print('AMOUNT MUST BE A NUMBER.')


def deposite(cn):
    '''FUNCTION TO DEPOSITE CASH'''
    try:
        r500 = int(input('Enter Number of ₹500 Note to be deposite: '))
        r200 = int(input('Enter Number of ₹200 Note to be deposite: '))
        r100 = int(input('Enter Number of ₹100 Note to be deposite: '))
        
        if(r100<0 or r200<0 or r500<0):
            print('NOTES CAN NOT BE NEGATIVE.')
            return
		
        amount = ((500 * r500) + (200 * r200) + (100 * r100))

        if((100 > amount ) or (amount > 20000)) :
            print('DEPOSITE AMOUNT MUST BE LESS THAN 20000 AND MORE THAN OR EQUAL TO 100. AND AMOUNT CAN NOT BE IN NEGATIVE OR ZERO.')

        else:
            users[cn][2] += amount
            print('Deposited amount is:', amount)
            print('Balance after deposite is:', users[cn][2])

    except ValueError as ve:
        print('AMOUNT MUST BE AN INTEGER NUMBER.')


users = {
    '123456789101': ['ABC User', 1001, 18000],
    '999999999999': ['XYZ User', 1234, 5000]
}


def clear_screen():
	if os.name == 'nt':
		pass
		os.system('cls')

	else:
		pass
		os.system('clear')


while True:
    print(__doc__)

    while True:
        cardNumber = card_entry()

        if (cardNumber):
            break

    while True:
        try:
            print('—' * 22)
            menu()
            opt = int(input("\nEnter Operation: "))

            if (5 == opt):
                break

            elif (1 == opt):
                pin_entry(cardNumber, print_user)

            elif (2 == opt):
                pin_entry(cardNumber, change_pin)

            elif (3 == opt):
                pin_entry(cardNumber, withdrawl)

            elif (4 == opt):
                pin_entry(cardNumber, deposite)

        except ValueError:
            print('OPTION MUST BE IN INTEGER, RESPECTIVE TO OPERATION.')

    clear_screen()