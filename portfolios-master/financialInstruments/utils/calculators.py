from copy import deepcopy
from datetime import date
from dateutil.relativedelta import relativedelta

ISR = 1.45/100

def goal_amount(amount,product,isr=False):

    """
    Returns the date when the desired amount is reached
    if this amount were invested. When isr = True, 
    it takes into consideration this tax in the revenues.

    As a parameter we must put a product, this is
    a dictionaty with the next structure:

        product = {
            'category': 'fixed',
            'amount':1000,
            'rate':0.1,
            'startdate': date(2020,1,1),
        }
    
    At the moment category key it's not relevant.
    An example with this product could be:

        >>>print(goal_amount(10_000,product=product,isr=False))

        2028-11-15
    """

    initial_capital = product['amount']
    revenues = 0
    days = 1
    date = deepcopy(product['startdate'])
    rate = product['rate']

    while (initial_capital + revenues) < amount:
        if isr:
            revenues=amount*(rate-ISR)/360*days
        else:
            revenues=amount*rate/360*days
        days+=1
   
    delta = relativedelta(days=+days)
    goal_date = date + delta
    
    return goal_date


def goal_date(date,product,isr=False):

    """
    Returns the total amount accumulated when the given date
    is reached if this amount were invested untill the date.

    Example:
        
        >>>print(goal_date(date(2021,1,1),product=product,isr=False))

        101.39

    """
    
    amount = product['amount']
    revenues = 0
    days = 1
    startdate = deepcopy(product['startdate'])
    rate = product['rate']
    delta = relativedelta(days=+days)

    while startdate + delta < date:
        if isr:
            revenues=amount*(rate-ISR)/360*days
        else:
            revenues=amount*rate/360*days
        days+=1
        delta = relativedelta(days=+days)

    return round(revenues,2)
    



