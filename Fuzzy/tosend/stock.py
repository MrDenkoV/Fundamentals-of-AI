import numpy as np
import skfuzzy as fz
from skfuzzy import control as ctrl
import matplotlib.pyplot as plt
import pandas as pd
import sys


############ Antecedent/Consequent objects

temp = ctrl.Antecedent(np.arange(0,46,1), 'Temperature')
stock = ctrl.Antecedent(np.arange(0,101,1), 'Stock')
weekend = ctrl.Antecedent(np.arange(0,6,1), 'Weekend')

buy = ctrl.Consequent(np.arange(0,101,1), 'Buy')


# stock.automf(3)
# buy.automf(3)

stock['Low'] = fz.trimf(stock.universe, [0,0,50])
stock['Medium'] = fz.trimf(stock.universe, [25,50,75])
stock['High'] = fz.trimf(stock.universe, [50,100,100])

buy['Low'] = fz.trimf(buy.universe, [0,0,50])
buy['Medium'] = fz.trimf(buy.universe, [25,50,75])
buy['High'] = fz.trimf(buy.universe, [50,100,100])

temp['Low'] = fz.trimf(temp.universe, [0,0,17])
temp['Medium'] = fz.trimf(temp.universe, [10,15,25])
temp['Hot'] = fz.trimf(temp.universe, [13,25,35])
temp['SuperHot'] = fz.trimf(temp.universe, [30,45,45])

weekend['Yes'] = fz.trimf(weekend.universe, [3,5,5])
weekend['No'] = fz.trapmf(weekend.universe, [0,0,3,5])
# weekend['No'] = fz.trimf(weekend.universe, [0,0,4])

########### RULES
rules = [None]*11

# Temp low

rules[0] = ctrl.Rule(temp['Low'] & stock['High'], buy['Low'])
rules[1] = ctrl.Rule(temp['Low'] & stock['Low'], buy['Medium'])
rules[2] = ctrl.Rule(temp['Low'] & stock['Medium'] & weekend['No'], buy['Low'])
rules[3] = ctrl.Rule(temp['Low'] & stock['Medium'] & weekend['Yes'], buy['Medium'])

# Temp medium

rules[4] = ctrl.Rule(temp['Medium'] & (stock['Medium'] | stock['Low']) & weekend['Yes'], buy['High'])
rules[5] = ctrl.Rule(temp['Medium'] & (stock['Medium'] | stock['Low']) & weekend['No'], buy['Medium'])
# rule[6] = ctrl.Rule(temp['Medium'] & stock['Low'] & weekend['Yes'], buy['High'])
# rule[6] = ctrl.Rule(temp['Medium'] & stock['Low'] & weekend['No'], buy['Medium'])
rules[6] = ctrl.Rule(temp['Medium'] & stock['High'] & weekend['Yes'], buy['Medium'])
rules[7] = ctrl.Rule(temp['Medium'] & stock['High'] & weekend['No'], buy['Low'])

# Temp Hot

rules[8] = ctrl.Rule(temp['Hot'] & weekend['No'], buy['Medium'])
rules[9] = ctrl.Rule(temp['Hot'] & weekend['Yes'], buy['High'])

# Temp Super Hot

rules[10] = ctrl.Rule(temp['SuperHot'], buy['High'])

######### Rules end

beer_manager = ctrl.ControlSystem(rules)
beer = ctrl.ControlSystemSimulation(beer_manager)


def beerOrder(beer, stock, temp, weekday, graph=None):
	beer.input['Stock'] = stock
	beer.input['Temperature'] = temp
	beer.input['Weekend'] = weekday
	beer.compute()
	if graph:
		graph.view(sim=beer)
		# plt.show()
	return beer.output['Buy']

# print(beerOrder(beer, 70, 33, 4))
# print(beerOrder(beer, 30, 13, 4))
weekdays = {}
for it,day in enumerate(["MD", "TU", "WE", "TH", "FR", "SA"]):
	weekdays[day]=it

try:
	if sys.argv[1] not in weekdays.keys():
		raise
	print(f"You should purchase {int(beerOrder(beer, int(sys.argv[2]), int(sys.argv[3]), weekdays[sys.argv[1]]))} units of beer")
    
except:
    print ("BEER ORDERING SYSTEM:")
    print ("Please enter 3 parameters:")
    print ("    weekday current_stock temperature")
    print ("    For weekdays it expects MD for Monday, TU for Tuesday, WE for Wednesday,")
    print ("    TH for Thursday, FR for Friday or SA for Saturday")
    exit (1)

