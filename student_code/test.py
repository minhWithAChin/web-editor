name=""
symbol=""
purchase_price=0.0
capital=0.0
purchased_volume=0
alphaNumSet=['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z','A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z','1','2','3','4','5','6','7','8','9','0']

def set_stock(stockName, stockSymbol) -> bool:
    if(isinstance(stockName,str) and isinstance(stockSymbol,str)):
        global name 
        name=stockName
        global symbol 
        symbol=stockSymbol
        return True
    return False

def change_available_capital(deltaCapital: float) -> bool:
    global capital
    if(capital + deltaCapital >= 0):
        capital=capital + deltaCapital
        return True
    return False

def profit_or_loss(newPrice:float) -> float:
    return (newPrice - purchase_price)*purchased_volume

def total_capital(newPrice:float) -> float:
    return capital + (newPrice*purchased_volume)

# wie viel gekauft wird, negativ für verkaufen
def purchase_sell(newPrice:float, deltaVolume: int) -> bool:
    #Checks for invalid stuff
    global purchase_price, purchased_volume
    if(symbol == ''):
        print("needs Symbol")
        return False
    if(not checkStringValidChars(symbol, alphaNumSet)):
        print("invalid Symbol: "+symbol)
        return False
    if(newPrice*deltaVolume > capital):
        print(f"you only have {capital:.2f}€, but the purchase costs {newPrice*deltaVolume:.2f}€")
        return False
    if(purchased_volume+deltaVolume < 0):
        print(f"you only have {purchased_volume} Stocks")
        return False
    change_available_capital(-newPrice*deltaVolume)
    purchase_price = float(newPrice)
    purchased_volume += deltaVolume
    return True

def pretty_str(newPrice:float)-> str:
    if(not checkStringValidChars(symbol,alphaNumSet)):
        return ""
    return f"${symbol}\ngekauftes Volumen: {purchased_volume}\nBeim Verkauf: {profit_or_loss(newPrice)}\nGesamtkapital: {total_capital(newPrice)}\nverfügbares Kapital: {capital}"

def infodump():
    print("//")
    print(name)
    print(symbol)
    print(capital)
    print(purchase_price)
    print(purchased_volume)
    print("//")


def checkStringValidChars(string:str, allowedChars:list)->bool:
    for char in string:
        charInStringValid=False
        for validChar in allowedChars:
            if char == validChar:
                charInStringValid=True
                break
        if not charInStringValid:
            return False
    return True



print(set_stock("abc","少女A"))
print(set_stock("abc","123"))
print(set_stock(0,"$YOLO"))
print(change_available_capital(+100))
purchase_sell(1,99)
purchase_sell(1,-9)
print(profit_or_loss(1.5))
print(total_capital(1.5))
infodump()
print(pretty_str(1.5))