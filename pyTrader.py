import sys

sys.path.insert(0, './app')

from termcolor import colored



from binance.client import Client


api_key = MARSHALL, ADD YOUR KEY
api_secret = MARSHALL, ADD YOUR SECRET

class Strategy:

    def trades(self):
        client = Client(api_key, api_secret)
        #Change ths to change the asset you're buying witg
        asset = "BNB"
        #Change pair you're trading
        symbol ='BNBBTC'
        balance= (client.get_asset_balance(asset))
        balance = float(balance['free'])
        startBalance=(client.get_asset_balance(asset))
        startBalance= float(startBalance['free'])
        #lastPrice = float(Orders.get_ticker(symbol)['lastPrice'])
        currentPrice = client.get_ticker(symbol =symbol)
        currentPrice=float(currentPrice['lastPrice'])
        #MANUALLY CHANGE LINE 31 TO WHAT YOU WANT
        firstBuyPrice = 11074.01

        numberOfBuys = 0
        balances = client.get_account()
       

        lowCertainty = firstBuyPrice * .02
        highCertainty = firstBuyPrice * .03
        sellCertainty = firstBuyPrice * .7

        buylowCertainty= float(round((balance * 0.05)/currentPrice))
        buyhighCertainty= float(round((balance * 0.10)/currentPrice))
        sellhighCertainty= float(round(balance * 0.95))

        lowCounter= 0
        highCounter= 0
        sellcounter = 0

        cycle = 0
        actions = []

        

        print colored('Auto Trading with binance', "cyan")
        print colored('Waiting to sell at', "blue")
        print  sellCertainty
  

        
        while balance>= (startBalance/2):
            #Line 61 is not getting triggered all other statements seem fine
            if currentPrice >= sellCertainty:
                #it never prints this. WHY? Code has forsaken me!
                print colored('TEST', "blue")
                order = client.create_order(
                    symbol='BTCUSDT',
                    side= Client.SIDE_SELL,
                    type=Client.ORDER_TYPE_MARKET,
                    quantity=sellhighCertainty
                )
                print colored('sold at high certainty', "blue")
                #increase count
                sellcounter= sellcounter + 1
                #recheck balance
                balance= (client.get_asset_balance('BTC'))
                balance = float(balance['free'])

            #Checks to see if it should buy at low settings
            elif lowCounter <= 1 and currentPrice< highCertainty:
                if currentPrice >= lowCertainty and currentPrice< highCertainty:
                    order = client.create_order(
                    symbol='BTCUSDT',
                    side= Client.SIDE_BUY,
                    type=Client.ORDER_TYPE_MARKET,
                    quantity=buylowCertainty
                )
                    firstBuyPrice = currentPrice
                    print colored('bought at low certainty', "blue")
                    #recheck the balance
                    balance= (client.get_asset_balance('USDT'))
                    balance = float(balance['free'])
                    #increase count
                    lowCounter= lowCounter +1
                    print colored('Bought at', "green")
                    print  firstBuyPrice
                    print colored('Waiting to sell at', "blue")
                    print  sellCertainty

             #Checks to see if it should buy at high settings
            elif currentPrice>= highCertainty and currentPrice < sellCertainty and highCounter < 1:
                order = client.create_order(
                symbol='BTCUSDT',
                side= Client.SIDE_BUY,
                type=Client.ORDER_TYPE_MARKET,
                quantity=buyhighCertainty
            )
                firstBuyPrice = currentPrice
                print colored('bought at high certainty', "blue")
                #increase counter
                highCounter = highCounter + 1
                #recheck balance
                balance= (client.get_asset_balance('BTC'))
                balance = float(balance['free'])
                print colored('Bought at', "green")
                print  firstBuyPrice
                print colored('Waiting to sell at', "blue")
                print  sellCertainty

            #Also tried selling here. Damn thing not working. 
            elif currentPrice >= sellCertainty:
                order =client.order_limit_sell(
                   symbol='BTCUSDT',
                   quantity=20
                )
                print colored('sold at high certainty', "blue")
                #increase counter
                sellcounter= sellcounter + 1
                #reset balance
                balance= (client.get_asset_balance('BTC'))
                balance = float(balance['free'])
                
strat = Strategy()
strat.trades()
