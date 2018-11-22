def sign_choose(value, positive, zero, negative):
    if value < 0:
        return negative
    elif value == 0:
        return zero
    else:
        return positive
