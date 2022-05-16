from random import randrange, seed


MIN_VALUE_CODE = 100000
MAX_VALUE_CODE = 999999


def code_gen():
    seed()
    return str(randrange(MIN_VALUE_CODE, MAX_VALUE_CODE))
