import yfinance as yf
from yahoo_fin import stock_info as si
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.backends.backend_agg as agg
import matplotlib.pyplot as plt
import pygame
import pylab
import numpy as np
import tkinter as tk
from tkinter import *
from tkinter import messagebox


black = (0, 0, 0)
white = (255, 255, 255)
green = (0, 128, 0)
brown = (139,69,19)
red = (255, 0, 0)
grey = (128,128,128)

lightGrey = (211,211,211)

FlexyPath = os.path.dirname(os.path.abspath(__file__))
d=open(FlexyPath + "/balance.txt", "r")
bankBalance = d.read()
bankBalance = int(bankBalance)
d.close()
f=open(FlexyPath + "/data.txt", "r")
contents = eval(f.read())
f.close()

root = tk.Tk()
root.title("Trading Game")
embed = tk.Frame(root, width=700, height=550)
embed.grid(columnspan=500, rowspan=500)
embed.pack(side=LEFT)
os.environ['SDL_WINDOWID'] = str(embed.winfo_id())
os.environ['SDL_VIDEODRIVER'] = 'windib'
window = pygame.display.set_mode((700 , 550))
window.fill(pygame.Color(255, 255, 255))

pygame.display.init()
pygame.display.update()

listbox = Listbox(root)
listbox.pack(side = LEFT, fill = BOTH)
scrollbar = Scrollbar(root)
scrollbar.pack(side = RIGHT, fill = BOTH)
listbox.config(yscrollcommand = scrollbar.set)

root.update()
pygame.init()
base_font = pygame.font.Font(None, 32)

Found = False
class plotClass(object):
    def __init__(self, tickerText):
        self.tickerText = tickerText
        if tickerText == "Type Here":
            print("runnning")
            self.tickerText = "tsla"
        self.stock = yf.Ticker(self.tickerText)
        print(self.stock)
        self.stock_historical = self.stock.history(start="2020-01-1", interval="1d")
        print(self.stock_historical)
        self.stock_historical = self.stock_historical.drop(['Stock Splits', 'Dividends', 'Volume', 'Open', 'Low', 'High'], axis = 1)
        self.window = pygame.display.get_surface()

        self.figure2 = plt.Figure(figsize=(5,4), dpi=100)
        self.ax2 = self.figure2.add_subplot(111)   
        self.stock_historical.plot(kind='line', legend=True, ax=self.ax2, color='r', fontsize=10)
        self.livePrice = si.get_live_price(self.tickerText)     
        print(self.livePrice)
        self.ax2.set_title(self.tickerText.upper() + " Curr Price: "+ str(self.livePrice))


    def draw(self):
        self.canvas = agg.FigureCanvasAgg(self.figure2)
        self.canvas.draw()
        self.renderer = self.canvas.get_renderer()
        self.raw_data = self.renderer.tostring_rgb()


        self.size = self.canvas.get_width_height()

        self.surf = pygame.image.fromstring(self.raw_data, self.size, "RGB")
        window.blit(self.surf, (0,0))

def textRender(text, font , colour):
    textSurface = font.render(text, True, colour)
    return textSurface, textSurface.get_rect()

def showText(text, fontSize, textloc, colour):
    Font = pygame.font.Font(FlexyPath+'/Quicksand/Quicksand-VariableFont_wght.ttf', fontSize)
    finalText, textLoc = textRender(text, Font , colour)
    window.blit(finalText, textloc)

class textInput(object):
    def __init__(self, user_text, x, y):
        self.user_text = user_text
        self.hovering = False
        self.active = False
        self.colour = lightGrey
        self.x = x
        self.y = y
        self.input_rect = pygame.Rect(self.x,self.y,140,32)

    def draw(self, text):
        showText(text, 20, (self.x, self.y - 25), black)
        self.text_surface = base_font.render(self.user_text, True, (self.colour))
        pygame.draw.rect(window, self.colour, self.input_rect, 2)
        window.blit(self.text_surface, (self.input_rect.x +5, self.input_rect.y+5))
        self.input_rect.w = max(100, self.text_surface.get_width() + 10)

class button(object):
    def __init__(self, x, y, text):
        self.x = x
        self.y = y
        self.text = text
        self.rectangle = pygame.Rect(self.x,self.y,100,32)
        self.msel = "Shares"
    def draw(self, market):
        global marketSelected
        global Found
        self.colour = lightGrey
        self.market = market

        if self.rectangle.collidepoint(pygame.mouse.get_pos()):
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.msel = ""
                self.colour = black
                if self.market == "Cripto AU":
                    self.msel = "Cripto AU"

                elif self.market == "Shares":
                    self.msel = "Shares"

                elif self.market == "Currency":
                    self.msel = "Currency"

                elif self.market == "Indices":
                    self.msel = "Indices"

                elif self.market == "Futures":
                    self.msel = "Futures"

                if self.msel != "" and Found == False:
                    Found = True
                    marketSelected = self.msel
                    print(marketSelected+"after")

            else:
                self.colour = grey



        pygame.draw.rect(window, self.colour, self.rectangle)
        showText(self.text, 20, (self.x + 5, self.y + 5), black)

def reDraw():
    global marketSelected
    global Found
    window.fill(white)
    graph.draw()
    criptoAu.draw("Cripto AU")
    Shares.draw("Shares")
    Currency.draw("Currency")
    Indices.draw("Indices")
    Futures.draw("Futures")
    Found = False

    showText("Balance: $" + str(bankBalance), 25, (20,450), black)
    showText("Current Market: " + marketSelected, 25, (20,500), black)
    tickerStock.draw("Ticker (e.g. TSLA)")
    buySellBox.draw("Buy$/Sell$")
    pygame.display.flip()
    root.update()

def save():
    f = open(FlexyPath + '/data.txt','w')
    f.write(str(FolioStocks))
    f.close()
    d = open(FlexyPath + '/balance.txt','w')
    d.write(str(bankBalance))
    d.close()
    
def textboxD(boxSelect):
    
    if event.type == pygame.MOUSEBUTTONDOWN:
        if boxSelect.input_rect.collidepoint(event.pos):
            boxSelect.user_text = ""
            boxSelect.active = True
        else:
            boxSelect.active = False

    elif boxSelect.active == False and boxSelect.input_rect.collidepoint(pygame.mouse.get_pos()):
            boxSelect.hovering = True
            boxSelect.colour = grey
    else:
        boxSelect.hovering = False
        boxSelect.colour = lightGrey

    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_ESCAPE:
            running = False
        if boxSelect.active == True:
            if event.key == pygame.K_BACKSPACE:
                boxSelect.user_text = boxSelect.user_text[0:-1]
            else:
                if event.key != pygame.K_RETURN:
                    boxSelect.user_text += event.unicode



    if boxSelect.active is True:
        boxSelect.colour = black
    elif boxSelect.hovering is False:
        boxSelect.colour = lightGrey

clock = pygame.time.Clock()
running = True
tickerStock = textInput("Type Here", 500, 40)
graph = plotClass(tickerStock.user_text)
text = "Price: "
buySellBox = textInput("Type Here", 500, 100)
buttonYs = 500
criptoAu = button(buttonYs, 200, "Cripto AU")
Shares = button(buttonYs, 250, "Shares")
Currency = button(buttonYs, 300, "Currency")
Indices = button(buttonYs, 350, "Indices")
Futures = button(buttonYs, 400, "Futures")
FolioStocks = {}
marketSelected = "Shares"
print(contents)
if str(contents) != str(FolioStocks):
    FolioStocks = contents
    for key, val in FolioStocks.items():
        listbox.insert(END, str(key) + " => "+ str(val))


while running:
    clock.tick(144)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        pygame.draw.rect(window,black,(600,200,170,50))

        
        textboxD(tickerStock)
        textboxD(buySellBox)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                print(marketSelected)
                print(tickerStock.user_text.isalpha())
                if marketSelected == "Cripto AU" and "-AUD" in tickerStock.user_text.upper() or marketSelected == "Shares" and tickerStock.user_text.isalpha() or marketSelected == "Currency" and "=X" in tickerStock.user_text.upper() or marketSelected == "Indices" and "^" in tickerStock.user_text.upper() or marketSelected == "Futures" and "=F" in tickerStock.user_text.upper():
                    if tickerStock.active is True:
                        try:
                            graph = plotClass(tickerStock.user_text)
                        except:
                            messagebox.showerror("Error", "Please enter a valid ticker for the selected market")

                    elif buySellBox.active is True:

                        # try:
                        if tickerStock.user_text == "Type Here":
                            tickerStock.user_text = "tsla"

                        bankBalance -= int(buySellBox.user_text)

                        if tickerStock.user_text.upper() in FolioStocks:
                            print(graph.livePrice)
                            FolioStocks[tickerStock.user_text.upper()] += float(buySellBox.user_text) / float(graph.livePrice)
                        else:
                            FolioStocks[tickerStock.user_text.upper()] = float(buySellBox.user_text) / float(graph.livePrice)
                        print(FolioStocks)

                        save()
                        listbox.delete(0, tk.END)
                        for key, val in FolioStocks.items():
                            listbox.insert(END, str(key) + " => "+ str(val))
                else:
                    messagebox.showerror("Error", "Please enter a valid ticker for the selected market")
            if event.key == pygame.K_ESCAPE:
                running = False
                

    reDraw()



pygame.quit()