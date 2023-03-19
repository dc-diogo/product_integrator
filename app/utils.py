def isFloat(num):
    try:
        float(num)
        return True
    except ValueError:
        return False


def get_double_price(price_string):
    plano = re.search(r'[0-9]*(\.[0-9]{3})*,([0-9]{2})?', price_string)

    if price_string is not '':
        if isFloat(price_string):
            return price_string
        else:
            money = plano.group(0)
            value = float(money.replace(".", "").replace(",", "."))
            return value
    else:
        return -1