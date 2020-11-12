from exceptions import ValidationError

def validate_products_is_sold(is_sold):
    if is_sold is not None:
        if is_sold != '0' and is_sold != '1':
            raise ValidationError('V001')
    return is_sold

def validate_products_is_displayed(is_displayed):
    if is_displayed is not None:
        if is_displayed != 0 and is_displayed != 1:
            raise ValidationError('V002')
    return is_displayed

