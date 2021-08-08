from  subprocess import check_output
from time import sleep
import  pyautogui as py
from time import time
from random import gauss, random, randrange, shuffle

py.PAUSE = randrange(380, 500) / 1000



def highAlch():
	x = 0
	while(True):
		check_output(["xdotool", "click", "1"])
		sleep(max(0.1, gauss(0.49123, .74321)))
		if x < 8:
				sleep(max(0.15, gauss(0.2123, .923)))
				check_output(["xdotool", "click", "1"])
				sleep(max(0.25, gauss(0.5123, 1.14321)))

		check_output(["xdotool", "click", "1"])

		# short or long sleep?
		x = int(random() * 100)
		print(x)
		if x < 5:
			sleep(max(7, gauss(8.002, 4.7123)))
		elif x < 20:
			sleep(max(2.9, gauss(3.002, 1.5123)))
		else:
			sleep(max(1.4, gauss(1.4002, 1.29123)))

		# sleep(max(8, gauss(8.4002, 1.29123)))

def rr(a, b):
	return randrange(a,b)


## Global vars used for running
cur_run = 100  # Starting run energy when the script is started.
is_running = True  # Assume the character is running when script is started
stopped_running = 0   # once we run out of energy, save the time to check when we have restored back to 100%
RESTORE_RATE = 4.286
FULL_RESTORE_TIME = RESTORE_RATE * 100 # https://oldschool.runescape.wiki/w/Energy#Recovering_energy
DRAIN_RATE = 4.0  # Net loss run energy after ea loop
TRIPS = 0
#################################


# helpy guy
def click_run():
	print("Click run icon")
	py.moveTo(rr(1723, 1761), rr(185, 191), duration=max(0.175, gauss(0.3002, .4123)))
	py.click()

# Check at beginning of ea run, starting at the furnace
# Toggles on / off run.
def check_run():
	global is_running
	global cur_run
	global stopped_running
	global FULL_RESTORE_TIME


	print(f'is running: {is_running}')
	print(f'Cur energy: {cur_run}')
	print(f'Time since last stop: {time() - stopped_running}')

	if(is_running):
		if(cur_run - DRAIN_RATE <= 6):
			is_running = False
			click_run()
			stopped_running = time()
		cur_run -= DRAIN_RATE
		return
	else:
		# Check if run should be on
		if(time() - stopped_running >= FULL_RESTORE_TIME):
			click_run()
			is_running = True
			cur_run = 100

def random_sleep(n, thresh):
	""" n is the range of random numbers, n = 100, 0,99"""
	global cur_run
	x = int(random() * n)
	# Ex: x = 40 n = 100, thresh = .5
	#			40 < 50
	if(x < thresh * n):
		slept = time()
		sleep(max(6, gauss(6.6, 0.39123)))
		slept = time() - slept
		recovered = slept / RESTORE_RATE
		if(cur_run + recovered <= 100.0):
			cur_run += recovered
		else:
			# cur run will be full, so set to 100.
			cur_run = 100

def craftGoldJewelery(test):
	global is_running
	global TRIPS
	while(True):
			antiban1 = randrange(0,1000)
			print(f'Anitban: {antiban1}')

		# Check if we need to toggle run
			check_run()

		  # 1. Click bank
			if antiban1 < 300:
				py.moveTo(rr(501, 513), rr(411, 430), max(0.256, gauss(0.5002, .4123)), py.easeOutQuad)
			elif antiban1 <= 1000:
				py.moveTo(rr(501, 513), rr(411, 430), max(0.256, gauss(0.5002, .4123)), py.easeOutBounce)
			py.click()
			sleep(max(10, gauss(10.6, 0.59123))) if not is_running else sleep(max(4.75, gauss(4.8, 0.39123)))

			# 2a.Deposit
			py.moveTo(rr(1785, 1800), rr(265, 289), duration=max(0.256, gauss(0.3002, .1123)))
			py.click()
			sleep(max(.250, gauss(.3, .29123)))

			# # 2b.Deposit
			# py.moveTo(rr(1785, 1800), rr(375, 395), duration=max(0.256, gauss(0.3002, .4123)))
			# py.click()
			# sleep(max(.250, gauss(.3, .29123)))

			# # 2c.Deposit
			# py.moveTo(rr(1825, 1848), rr(485, 500), duration=max(0.256, gauss(0.2002, .4123)))
			# py.click()
			# sleep(max(.250, gauss(.3, .29123)))

			# 3. Withdraw Ruby
			py.moveTo(rr(1036, 1055), rr(175, 195), duration=max(0.156, gauss(0.2002, .1123)))
			py.click()

			# 4. Gold
			py.moveTo(rr(1038, 1054), rr(210, 230), duration=max(0.1, gauss(0.1002, .2123)))
			py.click()

			# 5. Click furnance
			py.moveTo(rr(1232, 1240), rr(232, 243), duration=max(0.256, gauss(0.3002, .1123)))
			py.click()
			sleep(max(10, gauss(10.4002, .59123))) if not is_running else sleep(max(4.75, gauss(4.8, 0.39123)))

			# 6. Click bracelet
			# click ammy mould spot
			py.moveTo(rr(880, 895), rr(330, 345), duration=max(0.256, gauss(0.5002, .2123)))
			py.click()
			# 6. Click ammy
			# click ammy mould spot
			# py.moveTo(rr(875, 895), rr(265, 290), duration=max(0.256, gauss(0.5002, .2123)))
			# py.click()
			# 6. Click Necklace mould spot
			# py.moveTo(rr(877, 893), rr(265, 289), duration=max(0.256, gauss(0.4002, .3123)))
			# py.click()
			TRIPS +=1
			print(f"Trips: {TRIPS}")
			sleep(max(24.5, gauss(25.4002, 2.29123)))
			random_sleep(1000, 0.08)  # Sleeps 8% of the time, adds recovered energy rate uring sleep



def test():
	while(True):
		print(py.position())

# sets of valid y vals for each row
INV_ROWS = [
	[270, 290],
	[300, 325],
	[341, 362],
	[375, 395],
	[413, 433],
	[452, 472],
	[482, 500],
]
# Sets of valid x vals for each column
INV_COLS =[
	[1735, 1761],
	[1783, 1800],
	[1824, 1845],
	[1865, 1886],
]

def getBoxRandomCoords(pos):
	pos -=1
	r = pos//4
	c = pos%4
	print(f'rigPos {pos+1}, pos:{pos}, r:{r}, c:{c}')
	return [INV_COLS[c], INV_ROWS[r]]

def fletchInInv():
	while(True):
		# returns [cols[x1,x2], rows[y1,y2]]
		boxes = [
				getBoxRandomCoords(5),
				getBoxRandomCoords(6)
			]
		shuffle(boxes)
		[boxA, boxB] = boxes

		'''1. Click  arrows or shafts'''
		py.moveTo(rr(boxA[0][0], boxA[0][1]), rr(boxA[1][0], boxA[1][1]),
		 duration=max(0.05, gauss(0.05002, .0123)))
		py.click()
		'''1a. Click  arrows or shafts'''
		py.moveTo(rr(boxB[0][0], boxB[0][1]), rr(boxB[1][0], boxB[1][1]),
			duration=max(0.05, gauss(0.05002, .0123)))
		py.click()

		'''1. Press space, either 3-5 imes or hold for roughly half a second'''
		x = randrange(0,101)
		if x < 20:
			for i in range(0, randrange(3,5)):
				py.press('space')
				sleep(max(.156, gauss(.256, 0.59123)))
		else:
			py.keyDown('space')
			sleep(max(.256, gauss(.456, 0.59123)))
			py.keyUp('space')

		sleep(max(13.75, gauss(14.33, 2.19123)))



if( __name__ == "__main__"):
	print("Running....")
	# test()
	# highAlch()
	craftGoldJewelery(False)
	# fletchInInv()
