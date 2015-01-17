##########################################################
## This file is used exlusively by the gravity game to  ##
## determine the gravitational forces in each direction ##
##########################################################

def getDirectionTowards(x0,y0,x1,y1): # returns the unit vector that points from (x0,y0) --> (x1,y1)
    d = (x0 - x1, y0 - y1)
    magnitude = (d[0] ** 2 + d[1] ** 2) ** .5
    u = (d[0] / magnitude, d[1] / magnitude)
    return u

# getDirectionTowards(0,0,-1,2)