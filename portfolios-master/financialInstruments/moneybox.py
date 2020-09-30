import numpy as np
import pandas as pd
import datetime as dt
from copy import deepcopy
from dateutil.relativedelta import relativedelta


class MoneyBox:
    
    #WARNING. There is no withdrawal in this code

    """
    The moneybox financial product. it's a kind of portfolio
    with multiples transactions to invest. The revenues are
    calculated according to the days elapsed between the date
    the transaction was generated and the cut off date given.
    The plan it makes references to the amount and period in
    which it is deposited every transaction.
    
    Attributes
    ==========

        amount:
            FLOAT. The amount that the client deposited 
            each period. This amount it is constant and
            it depends of the hired plan.

        period:
            STRING. The period of the transactions:
            'month','fortnight','week'.
        
        startdate:
            DATE OBJECT. The start date of the plan.

        transaction_list:
            It is a list of every transaction made, ordered
            chronologically. A transaction looks like:
            [amount,date] -> [1_000,date(2020,1,1)]

        matrix:
            A dictionaty with the data of amortized table.
            Values are:
                transactions,
                dates,
                revenues,
                days_column

    Example
    =======
        from utils.periods import transaction_list

        l = transaction_list(1_000,period='month',number_of_periods=12,startdate=dt.date(2019,1,1))
        mb = MoneyBox(1_000,'month',startdate=dt.date(2019,1,1),transactions=l)
        print(mb.amortize(dt.date(2020,7,29)).to_dataframe())

            Transaction Date  Transaction  Revenues   Days     Total
        1           2019-01-01       1000.0    157.53  575.0   1157.53
        2           2019-02-01       1000.0    149.04  544.0   1149.04
        3           2019-03-01       1000.0    141.37  516.0   1141.37
        4           2019-04-01       1000.0    132.88  485.0   1132.88
        5           2019-05-01       1000.0    124.66  455.0   1124.66
        6           2019-06-01       1000.0    116.16  424.0   1116.16
        7           2019-07-01       1000.0    107.95  394.0   1107.95
        8           2019-08-01       1000.0     99.45  363.0   1099.45
        9           2019-09-01       1000.0     90.96  332.0   1090.96
        10          2019-10-01       1000.0     82.74  302.0   1082.74
        11          2019-11-01       1000.0     74.25  271.0   1074.25
        12          2019-12-01       1000.0     66.03  241.0   1066.03
        Total              NaN      12000.0   1343.02    NaN  13343.02

    """

    def __init__(self,amount,period,startdate,transactions):
        self.amount = amount
        self.period = period
        self.startdate = startdate
        self.transaction_list = transactions
        self.matrix = {}
        
    
    def amortize(self,cutoffDate):
        
        transaction_list = deepcopy(self.transaction_list)
        transactions = [
                round(transaction[0],2) 
                for transaction in transaction_list
                ]
        dates = [
                transaction[1] 
                for transaction in transaction_list
                ]
        revenues = list(
                    map(
                        lambda transaction:
                        round(transaction[0]*0.1/365*(cutoffDate-transaction[1]).days,2) 
                            if (transaction[0]>0 and (cutoffDate-transaction[1]).days>0) 
                            else 0,transaction_list
                        )
                    ) 
        days_column = [
                    (cutoffDate-transaction[1]).days 
                    for transaction in transaction_list
                    ]
        
        self.matrix['transactions']=transactions
        self.matrix['dates']=dates
        self.matrix['revenues']=revenues
        self.matrix['days_column']=days_column

        return self


    def to_dataframe(self):
        
        df = pd.DataFrame({
                    'Transaction Date':self.matrix['dates'],
                    'Transaction':self.matrix['transactions'],
                    'Revenues':self.matrix['revenues'],
                    'Days':self.matrix['days_column']
                    })
        df['Total']=df['Transaction'] + df['Revenues']
        sum_row=df[['Revenues','Transaction','Total']].sum(axis=0)
        total_row = pd.DataFrame([sum_row], index = ["Total"])
        df.index = np.arange(1, len(df)+1)
        df = pd.concat([df,total_row])

        return df




