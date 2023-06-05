from django import template

register = template.Library()


@register.filter
def subtract(value, arg):
    return value - arg

@register.filter
def percent(value, arg):
    return (arg/100)*value

@register.filter
def stockstate(value, arg):
    final_stock = value
    stock_level_security = arg
    if final_stock <  stock_level_security:
        return "Satisfactory level"
    elif final_stock >  stock_level_security:
        return "Resupply"