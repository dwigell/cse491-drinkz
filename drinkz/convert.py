def convert_ml(amount):
    total = 0.0

    amt, unit = amount.split()

    amt = float(amt)
    
    if unit == "oz":
        total += amt * 29.5735
    elif unit == "gallon" or unit == "gallons":
        total += amt * 3785.41
    elif unit == "liter" or unit == "liters":
        total += amt * 1000
    else:
        total += amt

    return total


