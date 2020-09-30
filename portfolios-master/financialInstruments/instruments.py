from datetime import date
from dateutil.relativedelta import relativedelta
from copy import deepcopy
from random import gauss
from financialInstruments.utils.periods import periods
from financialInstruments.utils.periods import number_of_periods
from financialInstruments.utils.periods import times_per_year
from financialInstruments.utils.periods import number_of_months

import pandas as pd


class Portfolio:
    """
    A Portfolio with fixed or variable rate. It can be dynamic or not. If it is dynamic,
    the first and the last row of the dataframe change according to the remaining days 
    between the start date and the firts day of the subsequent month. This is because
    when a portfolio is dynamic, the cut off date for revenues is the first day of each
    month. Then, the last row will have more days, the corresponding days between one
    month and other, and those from the first day of the last month to the due date.

    Attributes
    ==========

        category:
            STRING. It can be 'fixed' or 'variable'.

        startdate:
            DATE OBJECT. The initial date of the contract.

        enddate:
            DATE OBJECT. The cut off date of the contract.
        
        amount:
            FLOAT>0. The amount to invest.

        rate:
            FLOAT>0. The anual rate of investment. If the category
            is variable, then the rate will be the anual rate mean.

        matrix:
            A list of list. With columns = ['Cut off Date',
            'Initial Capital','Anual Rate','Revenues','ISR',
            'Accumulated Revenues'] And as a rows every transaction
            generating acording to the period.

    Example
    =======

        fo=date(2020,1,16) #start date
        fc=date(2021,1,16) #cut off date

        p=Portfolio(category='fixed',startdate=fo,enddate=fc,
                        amount=1_000_000,rate=16)
        print(p.amortize(period='month',dynamic=False).to_dataframe())
    """


    def __init__(self,category,startdate,enddate,amount,rate):

        self.category = category
        self.startdate = startdate
        self.enddate = enddate
        self.amount = amount
        self.rate = rate
        self.matrix = []
        self.period = None
        self.isr = 1.45/100 if startdate >= date(2020,1,1) else 1.04/100

    @property
    def revenues_before_tax(self):
        days_elapsed = (self.enddate - self.startdate).days
        revenues = self.amount*self.rate/360*days_elapsed
        return round(revenues,2)

    @property
    def revenues(self):
        days_elapsed = (self.enddate - self.startdate).days
        revenues = self.amount*(self.rate-self.isr)/360*days_elapsed
        return round(revenues,2)
    
    
    def amortize(self,period,dynamic=False):
        """
        Generates the amortization table stored in self.matrix as a list.
        The period can be 'week','fortnight' or 'week'.
        """
        
        self.period = period
        self.matrix = []
        revenues = 0
        delta = periods(period=period)
        date = deepcopy(self.startdate) + delta
        accumulated_revenues = 0
        n = number_of_periods(self.startdate,self.enddate,period)
        times = times_per_year(period=self.period)
        counter = 1

        if dynamic:
            try:
                if self.period=="month":
                    date = date.replace(day=1)
                    surplus_days = self.startdate.day 
                    if surplus_days == 31:
                        remaining_days = 0  
                    else: 
                        remaining_days = 30 - surplus_days
                elif self.period != "month":
                    raise Exception
                
            except Exception as e:
                print(f'There is not portfolio dynamic with {self.period} as period')      
            
        while date<=self.enddate:	
            
            if self.category == 'variable': 
                rate = round(gauss(mu=self.rate,sigma=2)/100,2)
            elif self.category == 'fixed':
                rate = self.rate/100
            
            if dynamic:
                if counter == 1:
                    revenues = round(self.amount*rate/360*remaining_days,2)
                elif counter == n:
                    revenues = round(self.amount*rate/360*(surplus_days+30),2)
                else:
                    revenues = round(self.amount*rate/times,2)
                counter+=1
            else:
                revenues = round(self.amount*rate/times,2)
       
            
            isr = round(self.amount*self.isr/times,2)
            accumulated_revenues += (revenues - isr)
            self.matrix.append([date,
                                self.amount,
                                rate,
                                revenues,
                                isr,
                                accumulated_revenues])
            date += delta

        return self

    def to_dataframe(self,total = ['Revenues','ISR']):
        """
        It turns the self.matrix into a dataframe object. The total
        parameter is a list containing those columns that will be sumed 
        as a total in the last row. It returns this dataframe.
        """
        
        dataframe = pd.DataFrame(self.matrix,
                            columns = ['Cut off Date',
                                        'Initial Capital',
                                        'Anual Rate',
                                        'Revenues',
                                        'ISR',
                                        'Accumulated Revenues'])
        
        sum_row=dataframe[total].sum(axis=0)
        total_row = pd.DataFrame([sum_row], index = ["Total"])
        df = pd.concat([dataframe,total_row])

        return df


class StarterPortfolio(Portfolio):

    """ 
    A demo portfolio to try dynamic or classic type. Its duration it's
    only 1, 2,..., untill 6 months, but not longer. There aren't controls about
    this time period in the code. So keep that in mind and do not enter
    dates that have more than 3 months difference. In order to make the
    code more readable, the parameter cutoffdate was changed to enddate.

    Example
    =======

        fo=date(2020,1,16) #start date
        fc=date(2020,4,16) #end date

        p=StarterPortfolio(category='fixed',startdate=fo,enddate=fc,amount=1_000_000,dynamic=True,period='month')
        print(p.amortize().to_dataframe())

    """


    def __init__(self,category,startdate,enddate,amount,dynamic,period):
        super().__init__(category,startdate,enddate,amount,rate=None)
        self.dynamic = dynamic
        self.period = period
        self.reinvestment = False

        if self.dynamic:
            self.rate = 7
        else:
            if self.amount < 500_000:
                self.rate = 10
            else: self.rate = 12

    def amortize(self):
        super().amortize(period=self.period,dynamic=self.dynamic)
        return self


class ClassicPortfolio(Portfolio):

    """ 
    The classic portfolio with a duration of more than 1 year. 

    Example
    =======

        fo=date(2020,1,16) #start date
        fc=date(2025,1,16) #end date

        p=ClassicPortfolio(category='fixed',startdate=fo,enddate=fc,
                        amount=1_000_000,dynamic=True,period='month')
        print(p.amortize().to_dataframe())

    """

    def __init__(self,category,startdate,enddate,amount,dynamic,
                period):
        super().__init__(category=category,startdate=startdate,
                            enddate=enddate,amount=amount,rate=None)
        self.dynamic = dynamic
        self.period = period
        self.number_of_months = number_of_months(startdate,enddate)
        self.reinvestment = True

        if self.dynamic:
            self.rate = 7
        else:
            if 12<=self.number_of_months<=36:
                if self.amount < 500_000:
                    self.rate = 10
                else: self.rate = 12
            elif 36<self.number_of_months<=60:
                if self.amount < 500_000:
                    self.rate = 12
                else: self.rate = 14
            elif 60<self.number_of_months:
                if self.amount < 500_000:
                    self.rate = 14
                else: self.rate = 16
            else:
                print("Classic portfolio doesnt have that period")

    def amortize(self):
        super().amortize(period=self.period,dynamic=self.dynamic)
        return self


class FlexiblePortfolio(Portfolio):

    """ 
    A portfolio with duration between 1 and 12 months. 

    Example
    =======

        fo=date(2020,1,16) #start date
        fc=date(2021,1,16) #end date

        p=FlexiblePortfolio(category='fixed',startdate=fo,enddate=fc,
                        amount=1_000_000,dynamic=False,period='month')
        print(p.amortize().to_dataframe())

    """

    def __init__(self,category,startdate,enddate,amount,dynamic,
                period):
        super().__init__(category=category,startdate=startdate,
                            enddate=enddate,amount=amount,rate=None)
        self.dynamic = dynamic
        self.period = period
        self.number_of_months = number_of_months(startdate,enddate)
        self.reinvestment = True

        if self.dynamic:
            self.rate = 4
        else:
            self.rate = 5

    def amortize(self):
        super().amortize(period=self.period,dynamic=self.dynamic)
        return self











