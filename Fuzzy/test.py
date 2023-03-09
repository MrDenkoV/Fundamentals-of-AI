
# https://github.com/carmelgafa/ml_from_scratch/tree/master/fuzzy_inference
 
import matplotlib.pyplot as plt; plt.rcdefaults()
import numpy as np
 
from fuzzy_system.fuzzy_variable_output import FuzzyOutputVariable
from fuzzy_system.fuzzy_variable_input import FuzzyInputVariable
from fuzzy_system.fuzzy_system import FuzzySystem
 
# DEFINE VARIABLES ####################################################
 
stock = FuzzyInputVariable('Stock', 0, 100, 100)
stock.add_triangular('Low', 0, 0, 50)
stock.add_triangular('Medium', 25, 50, 75)
stock.add_triangular('High', 50, 100, 100)
 
weekend = FuzzyInputVariable('Weekday', 1, 6, 6)# niedziela wolna
weekend.add_triangular('No', 1, 1, 5)
weekend.add_triangular('Yes', 4, 6, 6)
 
temp = FuzzyInputVariable('Temperature', -20, 40, 120)
temp.add_triangular('Low', -20, -20, 15)
temp.add_triangular('Medium', 10, 18, 25)
temp.add_triangular('Hot', 20, 28, 35) # 30
temp.add_triangular('VeryHot', 30, 40, 40) # 25
 
buy = FuzzyOutputVariable('Buy', 0, 100, 100)
buy.add_triangular('SmallLot', 0, 0, 50)
buy.add_triangular('MediumLot', 25, 50, 75)
buy.add_triangular('BigLot', 50, 100, 100)
 
system = FuzzySystem()
system.add_input_variable(stock)
system.add_input_variable(weekend)
system.add_input_variable(temp)
system.add_output_variable(buy)
 
# DEFINE RULES ##############################################################################
 
 
# TEMP LOW ############################################################## stock 10 v 50 v 90 / przy 0
 
system.add_rule({'Temperature':'Low',
   	  'Stock':'High'
   	   },
   	 { 'Buy':'SmallLot'})
 
system.add_rule({'Temperature':'Low',
   	  'Stock':'Low'
   	   },
   	 { 'Buy':'MediumLot'})
 
system.add_rule({'Temperature':'Low',
   	  'Stock':'Medium',
   	  'Weekday':'No'
   	   },
   	 { 'Buy':'SmallLot'})
 
system.add_rule({'Temperature':'Low',
   	  'Stock':'Medium',
   	  'Weekday':'Yes'
   	   },
   	 { 'Buy':'MediumLot'})
 
# TEMP MEDIUM ##############################################################
 
system.add_rule({'Temperature':'Medium',
   	  'Stock':'Medium',
   	  'Weekday':'Yes'
   	   },
   	 { 'Buy':'BigLot'})
 
system.add_rule({'Temperature':'Medium',
   	  'Stock':'Medium',
   	  'Weekday':'No'
   	   },
   	 { 'Buy':'MediumLot'})
 
system.add_rule({'Temperature':'Medium',
   	  'Stock':'Low',
   	  'Weekday':'Yes'
   	   },
   	 { 'Buy':'BigLot'})
 
system.add_rule({'Temperature':'Medium',
   	  'Stock':'Low',
   	  'Weekday':'No'
   	   },
   	 { 'Buy':'MediumLot'})
 
 
system.add_rule({'Temperature':'Medium',
   	  'Stock':'High',
   	  'Weekday':'Yes'
   	   },
   	 { 'Buy':'MediumLot'})
 
system.add_rule({'Temperature':'Medium',
   	  'Stock':'High',
   	  'Weekday':'No'
   	   },
   	 { 'Buy':'SmallLot'})
 
# TEMPERATURE HOT ######################################################## 50 W 21
 
system.add_rule({'Temperature':'Hot',
   	   'Weekday':'No'
   	   },
   	 { 'Buy':'MediumLot'})
 
system.add_rule({'Temperature':'Hot',
   	   'Weekday':'Yes'
   	   },
   	 { 'Buy':'BigLot'})
 
# TEMPERATURE VERY HOT #################################################### 50 W 35
 
system.add_rule({'Temperature':'VeryHot'
   	   },
   	 { 'Buy':'BigLot'})
 
# SIMULATIONS #############################################################
 
objects = ['Mon','Tue','Wed','Thu','Fri','Sat'] # np.arange (1,7,1)
fig, ax = plt.subplots()
x_pos   = np.arange(len(objects))
bar_w   = 0.25
 
buy_val = [[] for i in range (3)]
 
def calc_buy_val(stock, temp):
    val = []
    for W in range (1, 7, 1):
   	 #for T in range (0, 40, 5):
   	 output = system.evaluate_output({
   		 'Stock':stock,
   		 'Weekday':W,
   		 'Temperature':temp
   	 })
   	 val.append(output['Buy'])
   	 print("WD " + str(W) + " Temp " + " = " + str (output['Buy']))
    return val
 
buy_val[0] = calc_buy_val (50, 12) # stock 10..50..90 # temp 10 21 38
buy_val[1] = calc_buy_val (50, 18) # stock 28 40 # temp 12 18 24
buy_val[2] = calc_buy_val (50, 24)
 
##############################################################################
 
plt.bar(x_pos, buy_val[0], bar_w, color='r', label='Temp 10', alpha=0.5)
plt.bar(x_pos+bar_w, buy_val[1],  bar_w, color='b', label='Temp 21', alpha=0.5)
plt.bar(x_pos+2*bar_w, buy_val[2],  bar_w, color='g', label='Temp 28', alpha=0.5)
 
plt.xticks(x_pos+bar_w, objects)     # na osy X (szerokość, etykiety?)
 
plt.ylabel('Buy Qty')
plt.title('Buy Qty per Weekday')
plt.legend()
plt.show()
 
# PRINT FUZZY SETS ##########################################################
 
system.plot_system()
    
# THE END ###################################################################

