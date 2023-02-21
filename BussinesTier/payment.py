from dataclasses import dataclass


def validate_credit_card(card_number: str):
    sum_odd_digits = 0
    sum_even_digits = 0

    # Remove all the spaces and dashes from the card number
    card_number = card_number.replace('-', '')
    card_number = card_number.replace(' ', '')

    '''
    The card number is reversed to make it easier to work with it
    We need to do this because the card number is read from right to left
    '''
    card_number = card_number[::-1]

    '''
    We iterate through the card number and we add the odd digits to the sum_odd_digits variable
    '''
    for num in card_number[::2]:
        sum_odd_digits += int(num)

    # We check if the sum of the odd digits is greater than 9

    '''
    We will multiply the even digits by 2 and we will add the digits of the result to the sum_even_digits variable
    '''
    for num in card_number[1::2]:
        num = int(num) * 2
        if num >= 10:
            sum_even_digits += (1 + (num % 10))
        else:
            sum_even_digits += num

    # We add the sum of the odd digits and the sum of the even digits
    total = sum_odd_digits + sum_even_digits

    '''
    If the total is divisible by 10, the card number is valid
    '''
    if total % 10 == 0:
        print('The card number is valid')
        return True
    else:
        print('The card number is not valid')
        return False


@dataclass()
class Payment:
    card_number: str

    def __init__(self, card_number):
        self.card_number = card_number
        validate_credit_card(self.card_number)
