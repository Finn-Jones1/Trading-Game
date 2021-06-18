# Trading Game
 Python stocks trading game using yahoo finance api

# Disclamer
This program will only run on windows

# Game Justification
### Problem Definition
The problem that I am aiming to solve with this game is to allow people that are interested in trading on the stock market but either don't have the money or don't want to take the risk.
With a trading simulation you can learn how to trade stocks without the worry of loosing real money. Once learning the ropes on a simulator the user can then progress onto trading real 
stocks with real money and hopefully make a profit after learning about what works in the simulator.
### Needs/Objectives
This simulator will need to retrieve real time stock information to allow the simulator to be as realistic as possible so that the transition from the simulator to real life can be easier.
The software will need to be able to save the state when the program is closed so that the simulator can be used over a longer period of time.
This software will need to be able to be more basic than actual stock trading so that it is easier to learn how stocks work and you don't have to spend much time on learning how the software works


# How To Play
To play the game it might help to look at yfinance markets page: https://au.finance.yahoo.com/ this will have a list of tickers which can be used to find stocks
once you have a stock that you want to track you type it into the ticker feild and then enter the ammount of money that you want to put into that stock in the second feild and press enter.
Once a stock is purchased it will be added to the bought list on the right of the screen and can be sold at any time by entering a negative number into the buy/sell feild.
Any progress on the game will be saved to a text file in the same directory as the python file to reset the game set the data.txt file to "{}" and the balance.txt file to the desired starting amount of money.

# Dependancies
- pip3 install yfinance
- pip3 install yahoo_fin
- pip3 install matplotlib
- pip3 install pygame==1.9.6
- pip3 install tkinter



