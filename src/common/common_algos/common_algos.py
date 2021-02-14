'''Python file for common algorithms

Mainly used to store algorithms written to make usage more convenient
'''

def bin_to_decimal(s: str):
    '''
    Helper function that takes in a binary string and returns the converted decimal number
    '''
    for c in s:
        assert c in set(['.', '1', '0'])
    decimal_value = 0
    frac = False
    frac_power = 1
    for c in s:
        if c == '.':
            frac = True
            continue
        else:
            parsed_c = int(c)
        if not frac:
            decimal_value *= 2
            decimal_value += parsed_c
        else:
            decimal_value += parsed_c * (2**(-frac_power))
            frac_power += 1
    return decimal_value

def hex_to_decimal(s: str):
    '''
    Helper function that takes in a hexadecimal string and returns the converted decimal number
    '''
    a_ord = ord('A')
    for c in s:
        assert c in set(['.'] + [str(num) for num in range(10)] + [chr(a_ord + offset) for offset in range(6)])
    decimal_value = 0
    frac = False
    frac_power = 1
    for c in s:
        if c == '.':
            frac = True
            continue
        else:
            if c in set([str(num) for num in range(10)]):
                parsed_c = int(c)
            elif c in set([chr(a_ord + offset) for offset in range(6)]):
                parsed_c = 10 + ord(c) - a_ord
        if not frac:
            decimal_value *= 16
            decimal_value += parsed_c
        else:
            decimal_value += parsed_c * (16**(-frac_power))
            frac_power += 1
    return decimal_value


if __name__ == '__main__':
    print(bin_to_decimal('1101'))
    print(bin_to_decimal('1101.1101'))

    print(hex_to_decimal('91ABF.FFF'))
