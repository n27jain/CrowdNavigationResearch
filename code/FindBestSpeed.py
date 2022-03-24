



# given a map

# give a route

# we must minimize travel time by adjusting out speed


# Delay = time at traffic light + expect start up delay 

#Let’s assume that there is an additional penalty for stopping at a red light. There usually is a 2 second delay reaction before cars can reach the expected average speed of the coming road.


from time import time
from mapGenerator import *

def doYouMakeIt(c, timeArrival, t_stop, t_go , onStartGreen):
    # 0 - stuck on light
    # 1 - green free to go
    if onStartGreen:
        if timeArrival < t_go:
            return 1
        else:
            A = timeArrival/c
            B = A * c
            if timeArrival <= B + t_go and timeArrival > B:
                return 1
            else:
                return 0

def test():
    x,y,n = seeData()
    print(x,y,n)


test()

