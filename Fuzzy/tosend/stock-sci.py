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


def display_Ante_Con(weekend, stock, temp, buy):
	plt.subplot
	weekend.view()
	# plt.show()
	stock.view()
	# plt.show()
	temp.view()
	# plt.show()
	buy.view()
	plt.show()

# display_Ante_Con(weekend, stock, temp, buy)


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


# default stock is const
def getWeekResults(beer, const, d1, d2, d3, pivot=False, graph=None):
	args = []
	cols = []
	title = ''
	if pivot:
		args = [(i, const) for i in [d1, d2, d3]]
		cols = ['Stock {}'.format(i) for i in [d1, d2, d3]]
		title = 'Temperature {}'.format(const)
	else:
		args = [(const, i) for i in [d1, d2, d3]]
		cols = ['Temperature {}'.format(i) for i in [d1, d2, d3]]
		title = 'Stock {}'.format(const)
	res = [None]*6
	# print(*args[0])
	for day in range(6):
		res[day] = [beerOrder(beer, *args[0], day, graph),
			   		beerOrder(beer, *args[1], day, graph),
			   		beerOrder(beer, *args[2], day, graph)]
	# if graph:
	# 	plt.show()
	# print(res)
	data = pd.DataFrame(res, columns=cols)
	data.plot.bar(stacked=False)
	plt.title(title)
	plt.xticks(np.arange(0,6), ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'], rotation=0)
	plt.show()


# stock.view()
# plt.show()
# display_Ante_Con(weekend, stock, temp, buy)
# getWeekResults(beer, 30, 12, 15, 21, False, None)
# getWeekResults(beer, 12, 10, 50, 80, True, None)


try:
    if sys.argv[5] not in ['T','S']:
   		raise
    getWeekResults(beer, int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]), sys.argv[5]=="T", None)
except:
    print ("BEER ORDERING SYSTEM:")
    print ("Please enter 5 parameters:")
    print ("    constant_val series1_val series2_val series3_val constant_val_type")
    print ("    where constant_val_type = T for Temperature")
    print ("    or	constant_val_type = S for Stock")
    print ("Depending on constant_val_type, series should be either Stock or Temperature values")
    print ("while constant_val should represent selected type (opposite to series)")
    exit (1)

