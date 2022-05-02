import json
from rich import print
import yfinance as yf
from datetime import date
from datetime import timedelta
from rich.table import Table
import numpy as np
import pandas as pd
import plotly.graph_objs as go

class balance():
    def __init__(self):
        self.dicty = {}
        self.total = 0
        self.openned = 0

    def wallet(self,amount = 0):
        balance.reader(self)
        self.dicty = self.openned
        if "money" not in self.dicty:
            self.dicty["money"] = 0
        else:
            self.dicty["money"] += amount
        j = json.dumps(self.dicty)
        with open("Saved Money.json", "w") as f:
            f.write(j)
        balance.reader(self)

    def reader(self):
        self.openned = json.load(open("Saved Money.json"))

    def readMoney(self):
        print(self.dicty)

class Trade(balance):

    def __init__(self):
        super(balance,self).__init__
        self.portfolio = {}
        self.day = 2
        self.trader_reply = ""
        self.day_viewer = 2
        self.loop = 0
    def Saved(self,stock):
        j = json.dumps(stock)
        with open("Saved Info.json", "w") as f:
            f.write(j)
            f.close()

    def Saved_Reader(self,type = "yes"):
        if type == "no":
            self.portfolio= json.load(open("Saved Info.json"))
        else:
            self.portfolio= json.load(open("Saved Info.json"))
            print("[dark_sea_green2]Your portfolio:[/dark_sea_green2]")
            print(self.portfolio)
            Trade.reader(self)
            print("[dark_sea_green2]Your Total Balance: [/dark_sea_green2]",self.openned)

    def graph_company(self,company):
        data = yf.download(tickers=company, interval="1d",period="1mo")
        fig = go.Figure()

        fig.add_trace(go.Candlestick(x=data.index,
                        open = data["Open"],
                        high = data["High"],
                        low = data["Low"],
                        close = data["Close"], name = "market data"))

        fig.update_layout(
            title = f"{company} share prices",
            yaxis_title = "Stock Price ")

        fig.update_xaxes(
            rangeslider_visible = True,
            rangeselector = dict(
                buttons=list([
                    dict(count=5, label="5days",step="day",stepmode="backward"),
                    dict(count=1, label="months",step="year",stepmode="backward"),
                    dict(step="all")
                ])
            )
        )
        fig.show()

    def infoOptions(self):
        print(
        """
        [dark_slate_gray2]0 : View more days[/dark_slate_gray2]
        
        [chartreuse1]1 : View Graph [chartreuse1]

        [chartreuse4]2 : Look at different stocks[/chartreuse4]

        [chartreuse2]3 : Exit [/chartreuse1]
        """
        )
    def info(self, company = None):
        today = date.today()
        yesterday = today - timedelta(days = self.day_viewer)
        data = yf.download(tickers=company, interval="1d",start=yesterday)

        tickerdata = yf.Ticker(company)
        tickerinfo = tickerdata.info
        current_price = tickerinfo["currentPrice"]

        print(data)
        print(f"[green]The current Price: {current_price}[/green]")

        Trade.infoOptions(self)
        self.trader_reply = input("")
        if self.trader_reply == "0":
            self.day_viewer += 2
            Trade.info(self,company)

        elif self.trader_reply == "1":
            Trade.graph_company(self,company)
            Trade.info(self,company)
            Trade.infoOptions(self)
            self.trader_reply = input("")
        elif self.trader_reply == "2":
            print("[thistle1]What stock would you like to look at?[/thistle1]")
            company = input("")
            Trade.info(self,company)
        elif self.trader_reply == "3":
            Trade.Options(self)
        else:
            print("[red] Invalid Option [/red]")
            Trade.infoOptions(self)
            self.trader_reply = input("")

    def Options(self):
        print(
        """
        [green]1 : Access portfolio[/green]

        [blue]2 : Buy Stocks[/blue]

        [purple]3 : Sell Stocks[/purple]

        [yellow]4 : View Stocks[/yellow]

        [red]5 : Stop Trading[/red]
        """
        )
        answer = input("")
        if answer == "1":
            Trade.Saved_Reader(self)
            Trade.Options(self)
        elif answer == "2":
            Trade.buy(self)
        elif answer == "3":
            Trade.sell(self)
        elif answer == "4":
            print("[thistle1]What stock would you like to look at?[/thistle1]")
            company = input("")
            Trade.info(self,company)
        elif answer == "5":
            exit()
        else:
            print("[red] Invalid Option [/red]")
            Trade.Options(self)

    def buy(self):
        self.portfolio = json.load(open("Saved Info.json"))
        which = input("Name of stock?\n")
        try:
            balance.reader(self)
            tickerdata = yf.Ticker(which)
            tickerinfo = tickerdata.info
            shower = (tickerinfo["currentPrice"])
            print("[blue]How many shares do you want to buy[/blue]")
            amount = input("")
            total = (tickerinfo["currentPrice"]) * int(amount)
            print(total)
            if int(self.openned["money"] > total):
                print("[light_green]Current price right now:[/light_green]",(tickerinfo["currentPrice"]))
                print("[light_green]You have:[/light_green]",self.openned["money"])
                print("\n[cyan1]Are you sure[/cyan1]")
                print("1:[green]YES[/green] 2:[red]NO[/red]")
                answer = input("")
                if answer == "1":
                    balance.wallet(self,-total)
                    if which.upper() not in self.portfolio:
                        self.portfolio[which.upper()] = int(amount)
                        print(which.upper())
                        Trade.Saved(self,self.portfolio)
                        Trade.Options(self)
                        print(f"[red bold]-{shower}[/red bold]")
                        print("[light_green]You now have have:[/light_green]",self.openned["money"])
                    else:
                        self.portfolio[which.upper()] += int(amount)
                        Trade.Saved(self,self.portfolio)
                        print(f"[red bold]-{total}[/red bold]")
                        print("[light_green]You now have have:[/light_green]",self.openned["money"])
                    Trade.Options(self)
                elif answer == "2":
                    Trade.Options(self)
            else:
                print("[red]You dont have enough right now\nYou have[/red]",self.openned["money"],"Dollars[red]\nBuying parts will be coming soon[/red]")
                Trade.Options(self)
        except:
            print("[red bold]That is not a valid share[/red bold]")
            Trade.buy(self)

    def sell(self):
        balance.reader(self)
        print("[green]This is your current portfolio[/green]\n")
        Trade.Saved_Reader(self,"yes")
        print("[bright_magenta]What do you want to sell[/bright_magenta]")
        print("[red]0 : to quit[/red]")
        try:
            answer = input("")
            tickerdata = yf.Ticker(answer)
            tickerinfo = tickerdata.info
            shower = (tickerinfo["currentPrice"])        

            print("Each share is currently:", shower)
            print("[bright_magenta bold]How many shares do you want to sell [/bright_magenta bold]")
            amount = input("")
            if int(amount) < self.portfolio[answer]:
                total = shower * int(amount)
                print("[green bold]You will gain: [/green bold]",total)
            print("1:[green]YES[/green] 2:[red]NO[/red]")
            confirm = input("")
            if confirm == "1":
                self.portfolio[answer] -= int(amount)
                Trade.Saved(self,self.portfolio)
                balance.wallet(self,int(total))
                Trade.Options(self)
            elif confirm == "0":
                Trade.Options(self)
        except:
            print("[red bold]Invalid[/red bold]")
            Trade.Options(self)
Trades = Trade()
Trades.Options()
