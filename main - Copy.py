import yfinance as yf
from yahoo_fin import stock_info as si
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.backends.backend_agg as agg
import matplotlib.pyplot as plt
import pygame
import pylab

black = (0, 0, 0)
white = (255, 255, 255)
green = (0, 128, 0)
brown = (139,69,19)
red = (255, 0, 0)
grey = (128,128,128)
lightGrey = (211,211,211)
pygame.init()

window = pygame.display.set_mode((1000 , 550))
base_font = pygame.font.Font(None, 32)
pygame.display.set_caption("Stock Trading Game")

input_rect = pygame.Rect(200,200,140,32)

def plotGraph():
    ticker = user_text
    print(user_text)
    stock = yf.Ticker(user_text[0:-1])
    print(stock)
    stock_historical = stock.history(start="2020-01-1", interval="1d")
    print(stock_historical)
    stock_historical = stock_historical.drop(['Stock Splits', 'Dividends', 'Volume', 'Open', 'Low', 'High'], axis = 1)
    window = pygame.display.get_surface()

    figure2 = plt.Figure(figsize=(5,4), dpi=100)
    ax2 = figure2.add_subplot(111)   
    stock_historical.plot(kind='line', legend=True, ax=ax2, color='r', fontsize=10)
    ax2.set_title(ticker.upper())
    canvas = agg.FigureCanvasAgg(figure2)
    canvas.draw()
    renderer = canvas.get_renderer()
    raw_data = renderer.tostring_rgb()


    size = canvas.get_width_height()

    surf = pygame.image.fromstring(raw_data, size, "RGB")
    window.blit(surf, (0,0))
    return surf


def reDraw():
    text_surface = base_font.render(user_text, True, (black))

    window.fill(white)
    pygame.draw.rect(window,colour, input_rect, 2)
    window.blit(text_surface, (input_rect.x +5, input_rect.y+5))
    input_rect.w = max(100, text_surface.get_width() + 10)
    # plotGraph()
    

    pygame.display.flip()
    
clock = pygame.time.Clock()
running = True
user_text = ''

colour = lightGrey
active = False

while running:
    clock.tick(144)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            if input_rect.collidepoint(event.pos):
                active = True
            else:
                active = False
        if event.type == pygame.KEYDOWN:
            if active == True:
                if event.key == pygame.K_BACKSPACE:
                    user_text = user_text[0:-1]
                else:
                    user_text += event.unicode
            if event.key == pygame.K_RETURN:
                surf = plotGraph()
                
            if event.key == pygame.K_ESCAPE:
                running = False
    try:
        window.blit(surf, (0,0))
    except:
        print("nvm")
    if active:
        colour = grey
    else:
        colour = lightGrey

    reDraw()


pygame.quit()