import re

# (pdv_name, product, category, subcategory)
def is_date_prod_extracted_biggest_than_last_prod_in_history(history_product, date):
    is_last_item_older = True

    for price_history in history_product['price_history']:
        if price_history["date"] < date:
            continue
        else:
            is_last_item_older = False

    return is_last_item_older


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


def transform_name(name):
    name = name.replace("1litro ", "1 litro ")
    name = name.replace("1l ", "1 litro ")
    name = name.replace("1l", "1 litro ")
    name = name.replace("1,0l ", "1 litro ")
    name = name.replace("1,0l", "1 litro ")
    name = name.replace("1,0 litro ", "1 litro ")
    name = name.replace("1 l ", "1 litro ")
    name = name.replace("1kg", "1 kg ")
    name = name.replace("1kg ", "1 kg ")
    name = name.replace("0k ", "0 kg ")
    name = name.replace("2kg", "2 kg ")
    name = name.replace("2kg ", "2 kg ")
    name = name.replace("0k ", "0 kg ")
    name = name.replace("1l", "1 litro ")
    name = name.replace("1,0l ", "1 litro ")
    name = name.replace("1,0l", "1 litro ")
    name = name.replace("1,0 litro ", "1 litro ")
    name = name.replace("1 l ", "1 litro ")
    name = name.replace("0gramas", "0 gramas ")
    name = name.replace("0gr", "0 gramas ")
    name = name.replace("0gr ", "0 gramas ")
    name = name.replace("0g", "0 gramas ")
    name = name.replace("0g ", "0 gramas ")
    name = name.replace("0kg", "0 kg ")
    name = name.replace("0kg ", "0 kg ")
    name = name.replace("0ml ", "0 ml ")
    name = name.replace("0ml", "0 ml ")
    name = name.replace("pct ", "pacote ")
    name = name.replace("cx ", "caixa ")
    name = name.replace("achoc ", "achocolatado ")
    name = name.replace("choc ", "chocolate ")
    name = name.replace("ferm ", "fermentado ")
    name = name.replace("sorv ", "sorvete ")
    name = name.replace("0kg ", "0 kg")
    name = name.replace("0kg", "0 kg")

    return name

