"""
stocktrader -- A Python module for virtual stock trading

Contains functions normaliseDate, loadStock, loadPortfolio , H, L, DateCheck,
valuatePortfolio, addTransaction, savePortfolio, sellAll, loadAllStocks, Q-buy
and tradeStrategy1.

This functions allow you with the correct format files to modify a portfolio,
using some of the functions listed above. Some functions will just evaluate the
portfolio or some criteria and other will make changes to the portfolio.

In order to work properly you should load the corresponding portfolio
 with the loadPortfolio() function before using functions such as valuatePortfolio
 , addTransaction and tradeStrategy1.


Full name: Pedro Fermín Martínez Pan
StudentId: 10498001
Email: pedro.martinezpan@student.manchester.ac.uk
"""
import re
import os



class TransactionError(Exception):
    pass

class DateError(Exception):
    pass

stocks = {}
portfolio = {}
transactions = []


def normaliseDate(s):
    """
    Takes as input a string s and returns a date string of the form YYYY-MM-DD.
    
    Accepts the following input formats: YYYY-MM-DD, YYYY/MM/DD and DD.MM.YYYY, 
    where DD and MM are integers with one or two digits and YYYY is a 
    four-digit integer.
    
    The function converts all of these formats to 
    YYYY-MM-DD.
    
    If the conversion of the format fails function raises a DateError exception.
    
    The function does not check if dates exist.
    """
    if type(s) != str:
        raise DateError(" Argument should be a string ")
    
    dates = re.findall('\d+', s) # Learnt how to use this function for minitest2
    
    if len(dates) > 3 or len(dates) < 3 :
        raise DateError(" 3 integers have to be inputed, check your date!!!")
    
    
    if "." in s:
        dates.reverse()
    
    # How can i make this simpler?
    if len(dates[1]) < 2:
        dates[1] = "0" + dates[1]
    
    if len(dates[2]) < 2:
        dates[2] = "0" + dates[2]

    
    x = "-".join(dates)
    
    
    if len(dates[0])<4 or len(dates[0])>4:
        raise DateError(" We are looking for 4 digit year input")
    
    if int(dates[1])>12:
        raise DateError(" There are no more than 12 months, check your date!!! ")
        
    if int(dates[2])>31:
        raise DateError(" A month has got only 31 days, chek your date!!!")
    
    
    return(x)


def loadStock(symbol):
    """
    Takes as input a string symbol (example 'EZJ.csv', then loadStock('EZJ'),
    and loads the historic stock data from the corresponding CSV file into the
    dictionary stocks.
    
    CSV files should follow this format:
        
        -The first line is the header and will be ignored
        
        -Every following line should be of the comma-separated form 
        Date,Open,High,Low,Close,AdjClose,Volume, where Date is in any of the 
        formats accepted by the function normaliseDate(), and all other entries 
        should be floating point numbers corresponding to prices and trading 
        volumes.
    
    The function does not return anything as as the dictionary stocks is in 
    the outer namespace.
    
    If the file given by symbol cannot be opened as it is not found,
    a FileNotFoundError exception will be raised.

    If a line in the CSV file is of an invalid format, a ValueError exception 
    will be raised.
    """
    try:
        stockname = symbol + ".csv"
        f = open(stockname, mode='r')
        f.readline()
        d = dict()
        for line in f:
            line = line.split(",")
            k, v = normaliseDate(line[0]), line[1:5] # Saw this on stackoverflow
            d[k] = v
            for values in v:
                try:
                    float(values)
                except ValueError:
                    raise ValueError("Looks like your file is of the wrong format")
        stocks[symbol] = d
    except DateError:
        raise ValueError("Looks like your file is of the wrong format")


def loadPortfolio(fname='portfolio.csv'):
    """
    
    Takes as input a string fname corresponding to the name of a CSV file.
    The function loads the data from the file and assigns them to the 
    portfolio dictionary. Loads by default 'portfolio.csv'.
    
    Portfolio dictionary and the list transactions are emptied before new data
    is loaded into them.
   
    The CSV file shoul have strings date, cash, and arbitrarily many symbols in
    coma separated with the volume of each symbol. In that order.
    
    The function does not return anything as as the dictionary portfolio is in 
    the outer namespace.
    
    If the file given by fname cannot be opened as it is not found,
    a FileNotFoundError exception will be raised.
    
    If a line in the CSV file is of an invalid format, a ValueError exception 
    will be raised.
    
    """
    global portfolio
    transactions.clear()
    portfolio = {}
    try:
        f = open(fname, mode = 'r')
        count = 0
        for line in f:
            count += 1
            if count == 2:
                line = line.split()
                portfolio['cash'] = float(line[0])
                continue
            if count >= 3:
                line = line.rstrip("\n").split(",") #Saw the rstrip online
                loadStock(line[0])
                portfolio[line[0]]= float(line[1])
                continue
            line = line.split()
            portfolio['date'] = normaliseDate(line[0])
    except DateError:
        portfolio = {}
        raise ValueError("Looks like your file is of the wrong format")
    except IndexError:
        portfolio = {}
        raise ValueError("Looks like your file is of the wrong format")
    

def H(s,j):
    """
    Takes as inputs a symbol s and a trading day j and returns the high price 
    of the stock on that day.
    """
    H = stocks.get(s).get(j)
    return float(H[1])

def L(s,j):
    """
    Takes as inputs a symbol s and a trading day j and returns the low price 
    of the stock on that day.
    """
    H = stocks.get(s).get(j)
    return float(H[2])        


def DateCheck(date1,date2):
    """
    Cheks if date1 is earlier than date2 and returns Boolean True or False.
    
    Dates should be of a valid format accepted by normaliseDate().
    """
    date1 = normaliseDate(date1)
    date2 = normaliseDate(date2)
    dates1 = re.findall('\d+', date1)
    dates2 = re.findall('\d+', date2)
    if float(dates2[0]) < float(dates1[0]):
        return False
    if float(dates2[0]) == float(dates1[0]) and float(dates2[1]) < float(dates1[1]):
        return False
    if float(dates2[0]) == float(dates1[0]) and float(dates2[1]) == float(dates1[1]) and float(dates2[2]) < float(dates1[2]) :
        return False
    
    return True


def valuatePortfolio(date = None , verbose = False):
    """
    Takes input parameters date and verbose.
    
    The function valuates the portfolio at a given date and returns a 
    floating point number corresponding to its total value. 
    
    The parameter date is any string accepted by the normaliseDate() function 
    and when it is not provided, the date of the portfolio is used.
    
    The parameter verbose is a Boolean value which is False by default. 
    When the function is called with verbose=True it will still return the 
    total value of the portfolio but also print to the console a table of all 
    capital with the current low prices of all shares, as well as the 
    total value.
    
    For the valuation we use the low prices of stock on the date.
    
    A call to valuatePortfolio(date) will raise DateError exceptions in 
    two cases:
        
        -When date is earlier than the date of the portfolio.
        
        -When date is not a trading day.
    
    """
    if date == None:
        date = portfolio.get('date')
        
    if DateCheck(portfolio.get('date'),date) == False:
        raise DateError("Valuation day is earlier than portfolio date")
    try:
        if verbose == False:
            date = normaliseDate(date)
            value = 0
            count = 0
            for asset in portfolio:
                count += 1
                if count == 1:
                    continue
                if count == 2:
                    value += portfolio.get(asset)
                    continue
                if count >= 3:
                    value += portfolio.get(asset) * L(asset,date)
                    continue
            return float("{: .2f}".format(value)) #Saw this formatting on the internet
    
        if verbose == True:
            count = 0
            value = 0
            date = normaliseDate(date)
            print( "Your portfolio on " + date+":") # Used a similar table formatting I found on the internet
            print( "[* share values based on the lowest price on " + date + "]" )
            print("                                       ")
            print ("{:<15} {:<10} {:<10} {:<10}".format('Capital Type','Volume','Val/Unit*','Value in £*'))
            print("--------------------------------------------------")
            for asset in portfolio:
                count += 1
                if count == 1:
                    continue
                if count == 2:
                    value += portfolio.get(asset)
                    print ("{:<15} {:<10} {:<10} {:<10}".format(asset.capitalize(),1,"{: .2f}".format(portfolio.get(asset)),"{: .2f}".format(portfolio.get(asset))))
                    continue
                if count >= 3:
                    value += portfolio.get(asset) * L(asset,date)
                    print ("{:<15} {:<10} {:<10} {:<10}".format("Shares of " + asset, "{: .2f}".format(portfolio.get(asset)),"{: .2f}".format(L(asset,date)), "{: .2f}".format(L(asset,date) * portfolio.get(asset))))
                    continue
            print("--------------------------------------------------")
            print("{:<37} {:<10}".format("Total Value ", "{: .2f}".format(value)))
    except TypeError:
        raise DateError( date + " is not a trading day")
        
    return float("{: .2f}".format(value))


def addTransaction(trans, verbose = False):
    """
    Takes as input a dictionary trans corresponding to a buy/sell transaction 
    on our portfolio and an optional Boolean variable verbose, which is False
    by default.
    
    The dictionary trans has three items as follows:
        
        -The key date whose value is any string accepted by the function 
        normaliseDate()
        -The key symbol whose value is a string corresponding to the symbol
        of a stock
        -The key volume whose value is an integer corresponding to the number 
        of shares to buy or sell.
        
        Example { 'date' : '2013-08-12', 'symbol' : 'SKY', 'volume' : -5 }
        
    A call to the addTransaction(trans):
        
        -Updates the portfolio value for cash.
        -Inserts, updates, or deletes the number of shares.
        -Updates the date of portfolio to the date of the transaction.
        -Appends trans to the list transactions.
        
    It buys on the highest price of the day and sells for the lowest price for
    the stock on the specified date.
    
    If verbose = True, the function will print to the console an informative 
    statement about the performed transaction.
    
    
    """
    
    if DateCheck(portfolio.get('date'), trans.get('date')) == False:
        raise DateError("Your transaction is earlier than the portfolio date")
        
    try:
        v = portfolio[trans.get('symbol')]
        lv = trans.get('volume')*L(trans.get("symbol"),trans.get('date'))
        hv = trans.get('volume')*H(trans.get("symbol"),trans.get('date'))
        if trans.get('volume') >= 0:
            n = portfolio.get('cash')// H(trans.get("symbol"),trans.get('date'))
            if trans.get('volume') > n:
                raise TransactionError("You havent got enough cash for this transaction")
            portfolio['cash'] += -hv
        if trans.get('volume') < 0:
            n = portfolio[trans.get('symbol')]
            if trans.get('volume') + n < 0:
                raise TransactionError("You cant sell more shares than you have.")
            portfolio['cash'] += -lv
        
        portfolio['date']= trans.get('date')
        portfolio[trans.get('symbol')] += trans.get('volume')
        if  portfolio.get(trans['symbol']) == 0:
            portfolio.pop(trans['symbol'])
    except KeyError:
        try:
            lv = trans.get('volume')*L(trans.get("symbol"),trans.get('date'))
            hv = trans.get('volume')*H(trans.get("symbol"),trans.get('date'))
            if trans.get('volume') >= 0:
                n = portfolio.get('cash')// H(trans.get("symbol"),trans.get('date'))
                if trans.get('volume') > n:
                    raise TransactionError("You havent got enough cash for this transaction")
                portfolio['cash'] += -hv
            if trans.get('volume') < 0:
                raise TransactionError("You cant sell more shares than you have.")
            portfolio['date']= trans.get('date')
            portfolio[trans.get('symbol')] = trans.get('volume')
        except AttributeError:
            raise ValueError("Please load the stock to the stocks dictionary")

    transactions.append(trans)
    
    if verbose == True:
        if trans.get('volume') >= 0:
            print('> ' +  portfolio.get('date') + ': Bought ' + str(trans.get('volume')) +' shares of ' + trans.get('symbol') + ' for a total of £' + "{: .2f}".format(hv))
        if trans.get('volume') < 0:
            print('> ' +  portfolio.get('date') + ': Sold ' + str(-trans.get('volume')) +' shares of ' + trans.get('symbol') + ' for a total of £' + "{: .2f}".format(-lv))
        print('Available cash £' + "{: .2f}".format(portfolio.get('cash')))
        
def savePortfolio(fname = "portfolio"):
    """
    That saves the current dictionary portfolio to a CSV file with name fname.
    The file will be saved in the same directory as the stocktrader.py module.
    If no filename is provided, the name portfolio.csv should be assumed.
    
    The function does not return anything.
    """
    f = open(fname + ".csv", mode="wt", encoding="utf8")
    count = 0
    for key in portfolio:
        count += 1
        if count <= 2:
            f.write(str(portfolio.get(key))+ "\n")
        if count > 2:
            f.write(key + "," + str(portfolio.get(key)) + "\n")
    f.close()

def sellAll(date = None, verbose = False):
    """
    Sells all shares in the portfolio on a particular date.
    Date is an optional string of any format accepted by the function 
    normaliseDate() and verbose is an optional Boolean variable which is False
    by default. If date is not provided, the date of the portfolio is assumed 
    for the sell out.
    
    If verbose=True all selling transactions are printed to the console. 
    """
    if date == None:
        date = portfolio.get('date')
    
    l = list(portfolio.keys()) # Saw this in www.geeksforgeeks.org
    while len(l) > 2:  
        trans = {'date':date, 'symbol':l[2], 'volume': -portfolio.get(l[2])}
        l.pop(2)
        if verbose == False:
            addTransaction(trans, False)
        if verbose == True:
            addTransaction(trans, True)

def loadAllStocks():
    """
    Loads all stocks into the dictionary stocks.The corresponding stock CSV 
    files should be in the same folder as stocktrader.py, and they should
    be of the form XYZ.csv where XYZ is a string containing only capital 
    letters.
    
    If the loading of one of the files fails, this file is ignored.
    """
    L = os.listdir((os.getcwd()))
    csv_files = []
    for file in L:  # Learnt this functions when attempting task3 in minitest 2
        if file[-4:] == ".csv" and file[:-4].isupper() and file[:-4].isalpha():
            csv_files.append(file)
    for file in csv_files:
        file = file.rstrip(".csv")
        try:
            loadStock(file)
        except ValueError:
            pass

def Q_buy(s,j):
    """
    Criteria to buy a stock, takes as inputs stock s from stocks and index j
    from the list of trading days. It returns a floating point number.
    """
    x = list_of_trading_days[j]
    Q1 = 10*H(s,x)
    Q2 = 0
    for i in range(0,10):
        Q2 += H(s,list_of_trading_days[j-i])
        
    Q = Q1/Q2
    return Q

state = "buy"
def tradeStrategy1(verbose):
    """
    Goes through all trading days in the dictionary stocks and buys and sells 
    shares automatically.
    
    The strategy is as follows:
       
       -The earliest buying decision is either on the date of the portfolio or 
       the tenth available trading day in stock whichever is later
       -At any time, we buy the highest possible volume of a stock given the 
       available cash.
       -When shares have been bought, no other shares will be bought until all
       shares from the previous buying transaction are sold again.
       -All shares from a previous buying transaction are sold at once.
       -If shares are being sold on trading day j it will only consider buying 
       new shares on the following trading day, j+1.
       
       After buying shares it will sell them when either profit of 30% or loss
       of 30%.
       It will buy by calculating 
       Q_buy(s,j) = 10*H(s,l[j]) / (H(s,l[j]) + H(s,l[j-1]) + H(s,l[j-2]) + ... + H(s,l[j-9]))
       where H(s,l[j]) is the high price of stock s at the j-th trading day.
       It will buy the stock with the maximal quotient.
       
       It takes as inputs either Boolean True or False.
       If verbose True it will print information about the transactions.
       If verbose False it wont print anything
       It will modify the portfolio until the date of data available.
       

    """
    global state, list_of_trading_days
    loadAllStocks()
    list_of_trading_days = []
    l = list(stocks.keys())
    for key in stocks.get(l[0]).keys():
        list_of_trading_days.append(key)
    try:
        starting_point = list_of_trading_days.index(portfolio.get('date'))
    except ValueError:
        i = 0
        while DateCheck(portfolio.get('date'), list_of_trading_days[i]) == False:
            i +=1
        starting_point = i
    if DateCheck(portfolio.get('date'), list_of_trading_days[9]) == True:
        starting_point = 9
    
    for j in range(starting_point,len(list_of_trading_days)):
        global Q_win
        if state=="buy":
            Q_win = (0,0)
            Q_1 = 0
            for stock in stocks:
                Q_2 = Q_buy(stock,j)
                if Q_2 > Q_1:
                    Q_win = (stock, list_of_trading_days[j])
                    Q_1 = Q_2
            v = float(portfolio.get('cash')) // H(Q_win[0],Q_win[1])
            trans1 = { 'date':list_of_trading_days[j] , 'symbol': Q_win[0] , 'volume': v }
            state = "sell"
            if verbose == True:
                addTransaction(trans1, verbose = True)
            if verbose == False:
                addTransaction(trans1, verbose = False)
        else:
            Q_sell = L(Q_win[0],list_of_trading_days[j])/H(Q_win[0],Q_win[1])
            if Q_sell >= 1.3 or Q_sell <= 0.7:
                if verbose == True:
                    sellAll(list_of_trading_days[j],True)
                if verbose == False:
                    sellAll(list_of_trading_days[j],False)
                state = "buy"

def main():
    # 
    return

# the following allows your module to be run as a program
if __name__ == '__main__' or __name__ == 'builtins':
    main()