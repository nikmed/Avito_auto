def base62encode(number):
    if not isinstance(number, (int, int)):
        raise TypeError('number must be an integer')
    if number < 0:
        raise ValueError('number must be positive')

    alphabet, base62 = ['0123456789AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz', '']

    while number:
        number, i = divmod(number, 62)
        base62 = alphabet[i] + base62

    return base62 or alphabet[0]


def base62decode(number):
    res = 0
    alphabet, base62 = ['0123456789AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz', '']
    len_number = len(number)
    for i in range(len_number):
        res += alphabet.index(str(number[len_number - i - 1])) * pow(62, i)
    return res
