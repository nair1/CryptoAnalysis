#from yahoofinancials import YahooFinancials as yf
import yfinance as yf
from datetime import date, datetime

class Asset:
    # option_type
    # S - Stock
    # M - Money
    # C - Call
    # P - Put

    def __init__(self, amount, ticker=None, date=None, strike=None, option_type=None, override_price=None):
        self.amount = amount
        self.ticker = ticker
        self.date = date
        self.strike = strike
        self.option_type = option_type
        self.override_price = override_price
    
    def get_value(self):
        if (self.override_price != None): # Return if override price is provided
            return self.amount * self.override_price

        if (self.ticker == None): # Return amount if Asset is cash
            return self.amount

        if (self.date == None): # Return amount if Asset is stock
            return self.amount * get_stock_price(self.ticker)
        
        #Return if asset is option
        return self.amount * get_option_price(self.ticker, self.date, self.strike, self.option_type)

def format_option(stock, date, strike, option_type='C'):
    month = date[5:7]
    day = date[8:]
    year = date[2:4]

    if (len(strike) == 3):
        extra_letters = '00'
    else:
        extra_letters = '000'
    
    return stock + year + month + day + option_type + '000' + strike + extra_letters

def get_option_price(ticker, date, strike, option_type='C'):
    
    strike = strike.replace('.', '')

    option_chain = yf.Ticker(ticker).option_chain(date).calls.values

    if (option_type == 'P'):
        option_chain = yf.Ticker(ticker).option_chain(date).puts.values
    
    option_string = format_option(ticker, date, strike)

    for option in option_chain:
        if (option[0] == option_string):
            return option[3]*100
        
    return None

def get_stock_price(ticker):
    stock = yf.Ticker(ticker)

    stock_price = stock.history(period='1d')['Close'][0]

    #stock_price = (stock.get('ask') + stock.get('bid'))/2
    return round(stock_price, 2)

def get_portfolio_value(assets):
    sum = 0

    for asset in assets:
        sum += asset.get_value()
    
    return sum

def get_annualized_return(current_val, starting_val, days):
    return round(100 * pow(current_val/starting_val, 365/days) - 100, 3)

def get_days_since_ytd():
    todays_year = datetime.now().year
    todays_month = datetime.now().month
    todays_day = datetime.now().day
    start_date = date(2021, 2, 26)
    return (date(todays_year, todays_month, todays_day) - start_date).days

starting_portfolio_value = 3767.14
starting_spy_value = 380.36 # As of 2021-02-26

current_portfolio = [
    Asset(88, 'PLTR'), 
    Asset(100, 'TLRY'), 
    Asset(-1, 'TLRY', '2021-04-16', '21.5', 'C'), 
    Asset(9.75)
]

current_portfolio_value = round(get_portfolio_value(current_portfolio), 2)
current_spy_price = get_stock_price('SPY')
days_since_ytd = get_days_since_ytd()
current_profit = round(current_portfolio_value - starting_portfolio_value, 2)
current_return = round((100*current_portfolio_value/starting_portfolio_value)-100, 3)
spy_return = round((100*current_spy_price/starting_spy_value)-100, 3)
annualized_return = get_annualized_return(current_portfolio_value, starting_portfolio_value, days_since_ytd)
annualized_return_spy = get_annualized_return(current_spy_price, starting_spy_value, days_since_ytd)

print('\n\nStarting Portfolio Value: $' + str(starting_portfolio_value) + '   Starting SPY Value: $' + str(starting_spy_value))
print('Current Portfolio Value:  $' + str(current_portfolio_value) + '   Starting SPY Value: $' + str(round(current_spy_price, 2)))

print('\n\nStart Date: 2021-02-26 (' + str(days_since_ytd) + ' days)')
print('\nCurrent YTD Profit:    $' + str(current_profit))
print('Current YTD Profit:     ' + str(current_return) + '%')

print('\nAnnualized YTD Profit:  ' + str(annualized_return) + '%')
print('Annualized SPY Profit:  ' + str(annualized_return_spy) + '%\n\n')

