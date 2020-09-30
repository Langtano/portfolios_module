from dateutil.relativedelta import relativedelta
from copy import deepcopy
from datetime import date


def times_per_year(period):
    #Returns how many periods are in a year
    
    if period == "week":
        delta = 52
    elif period == "fortnight":
        delta = 24
    elif period == "month":
        delta = 12

    return delta 


def periods(period):
    #Transform the period string in delta-time object.

    if period == "day":
        delta = relativedelta(days=+1)
    elif period == "week":
        delta = relativedelta(days=+7)
    elif period == "fortnight":
        delta = relativedelta(days=+15)
    elif period == "month":
        delta = relativedelta(months=+1)

    return delta 

def number_of_periods(date_1,date_2,period):
    #Returns the number of periods between two dates.

    delta = periods(period=period)
    number_of_periods = 0
    date = deepcopy(date_1) + delta
    while date<=date_2:	

        date += delta
        number_of_periods += 1

    return number_of_periods


def number_of_months(date_1,date_2):
    #Returns the number of months between two dates.

    num_months = (date_2.year-date_1.year) * 12 + (date_2.month-date_1.month)
    
    return num_months


def transaction_list(amount,period,number_of_periods,startdate):
    """
    Returns a list with transactions [amount,date] according to
    the period ('week','fortnight',month'), the number of periods
    chosen and the amount, this last one will be constant in each
    transaction.

    Example:
        >>>l = transaction_list(1_000,period='month',
                            number_of_periods=12,
                            startdate=dt.date(2019,1,1))
        >>>print(l)
        
        [[1000, datetime.date(2019, 1, 1)], 
        [1000, datetime.date(2019, 2, 1)], 
        [1000, datetime.date(2019, 3, 1)], 
        [1000, datetime.date(2019, 4, 1)],  
        .
        .
        .
        [1000, datetime.date(2019, 12, 1)]]

    """
    now = startdate
    transactions=[]

    if period == 'month':
        transactions = [ 
                    [amount,now + relativedelta(months=+i)] 
                    for i in range(number_of_periods)
                    ] 
  
    elif period == 'fortnight':
        transactions = [ 
                    [amount,now + dt.timedelta(days=i*15)] 
                    for i in range(number_of_periods+1)
                    ]
    
    elif period == 'week':
        transactions = [ 
                    [amount,now + dt.timedelta(weeks=i)] 
                    for i in range(number_of_periods+1)
                    ]
        
    return transactions


