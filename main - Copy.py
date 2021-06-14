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

black = (0, 0, 0)
white = (255, 255, 255)
green = (0, 128, 0)
brown = (139,69,19)
red = (255, 0, 0)
grey = (128,128,128)

lightGrey = (211,211,211)

FlexyPath = os.path.dirname(os.path.abspath(__file__))


# pygame.display.set_caption("Stock Trading Game")

root = tk.Tk()
embed = tk.Frame(root, width=1000, height=550)
embed.grid(columnspan=500, rowspan=500)
embed.pack(side=LEFT)
# buttonwin = tk.Frame(root, width=75, height=500)
# buttonwin.pack(side=LEFT)
os.environ['SDL_WINDOWID'] = str(embed.winfo_id())
os.environ['SDL_VIDEODRIVER'] = 'windib'
window = pygame.display.set_mode((1000 , 550))
window.fill(pygame.Color(255, 255, 255))
pygame.display.init()
pygame.display.update()



listbox = Listbox(root)
# Adding Listbox to the left
# side of root window
listbox.pack(side = LEFT, fill = BOTH)

# Creating a Scrollbar and 
# attaching it to root window
scrollbar = Scrollbar(root)

# Adding Scrollbar to the right
# side of root window
scrollbar.pack(side = RIGHT, fill = BOTH)

# Insert elements into the listbox

    
# Attaching Listbox to Scrollbar
# Since we need to have a vertical 
# scroll we use yscrollcommand
listbox.config(yscrollcommand = scrollbar.set)

root.update()
pygame.init()
base_font = pygame.font.Font(None, 32)
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
        # print("rendering")
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

                
def reDraw():
    window.fill(white)
    graph.draw()
    showText("Balance: $" + str(bankBalance), 25, (400,450), black)
    # showText("Balance: $" + str(bankBalance), 25, (400,450), black)
    # pygame.draw.rect(window, colour, input_rect, 2)
    # window.blit(text_surface, (input_rect.x +5, input_rect.y+5))
    # try:
    #     plotGraph()

    # except:
    #     print("error")
    tickerStock.draw("Stock Ticker")
    buySellBox.draw("Buy/Sell")

    pygame.display.flip()
    root.update()
    
def textboxD(boxSelect):
    
    if event.type == pygame.MOUSEBUTTONDOWN:
        if boxSelect.input_rect.collidepoint(event.pos):
            boxSelect.user_text = ""
            boxSelect.active = True
        else:
            # boxSelect.user_text = "Type Here"
            # if boxSelect == tickerStock:
            # graph = plotClass(tickerStock.user_text)
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
FolioStocks = {}
bankBalance = 200000

while running:
    clock.tick(144)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False


        textboxD(tickerStock)
        textboxD(buySellBox)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                if tickerStock.active is True:
                    graph = plotClass(tickerStock.user_text)
                elif buySellBox.active is True:
                    try:
                        if tickerStock.user_text == "Type Here":
                            tickerStock.user_text = "tsla"

                        bankBalance -= int(buySellBox.user_text)
 
                        if tickerStock.user_text in FolioStocks:
                            FolioStocks[tickerStock.user_text] += int(buySellBox.user_text) / int(graph.livePrice)
                        else:
                            FolioStocks[tickerStock.user_text] = int(buySellBox.user_text) / int(graph.livePrice)
                        print(FolioStocks)

                    except:
                        print("not a real number")
                    for key, val in FolioStocks.items():
                        listbox.insert(END, str(key) + " => "+ str(val))
                
            if event.key == pygame.K_ESCAPE:
                running = False


    



    


    reDraw()



pygame.quit()