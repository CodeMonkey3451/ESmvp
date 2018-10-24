import numpy as np
import time
from scipy.optimize import minimize
import random
import matplotlib.pyplot as plt


#set up all the relevant values
beeRadius   = 200    # m
beeEff      = 3      # peak of the gaussian distribution
satVal      = 3.5    # saturation of the pollination

lengthX     = 1000   # fieldsize in meter
lengthY     = 1000   # fieldsize in meter
elementSize = 20     # the size of one element in the simulation

tol         = 1e-3   # tolerance for the minimization
nShowCount  = 50

#get the meshgrid for the pollinisation functions
nu = int((lengthX + elementSize) / elementSize)
nv = int((lengthY + elementSize) / elementSize)
u, v = np.meshgrid(np.linspace(0, lengthX, nu), np.linspace(0, lengthY, nv))



def showPollinisation(img, title="title", vmax=None):
    #shows the pollinisation to the user
    fig, ax = plt.subplots()
    cax = ax.imshow(img, cmap='inferno', interpolation='none', vmax=vmax, vmin=0)
    ax.set_title(title)
    cbar = fig.colorbar(cax)
    plt.show()



def makeRndHives(nHives):
    hives = []
    for pos in range(nHives * 2):
        if pos %2 == 0:
            hives.append(random.random() * lengthY)
        else:
            hives.append(random.random() * lengthX)
    return np.asarray(hives)


#a 2D gaussian
def gaussian(peak, fwhm, x, y, x0, y0):
    return peak * np.exp(-(np.power(x - x0, 2) + np.power(y - y0, 2)) / np.power(fwhm, 2) * 4 * np.log(2))


#exponential saturation
def saturation(val, amplitude, alpha):
    return amplitude * (1 - np.exp(-alpha * val))



def calcPollinisation(positions, **args):
    #init empty field
    pol = np.zeros(u.shape)

    #minimization only takes arguments as a one dimensional List. If we want to have arguments in a more readable
    #2D array we need to convert the input first
    val = 0
    pos = []
    for i in range(int(len(positions)/2)):
        pos.append([positions[val], positions[val+1]])
        val += 2

    #calculate the pollinization of each hive in the field
    for p in pos:
        pol += gaussian(beeEff, beeRadius, v, u, p[0] ,p[1])

    #a certain saturation of the pollinization
    pol = saturation(pol, 1, satVal)

    #return different data according to the requirements of the function call
    if 'mode' in args:
        if args['mode'] == 'sum':
            return -np.sum(pol)
        if args['mode'] == 'polMap':
            return pol
    else:
        #track the minimization steps
        c.count()
        c.showProg(nShowCount)
        #return the pollinization value of the field
        return -np.sum(pol)



class Counter():
    #a class to track the number of minimization steps and the required time
    def __init__(self, time):
        self.t = time
        self.i = 0

    def count(self):
        self.i += 1

    def showProg(self, n=10):
        #show count each nth step
        if self.i%n == 0:
            print("Round: " ,self.i, " Mean Time: ", (time.time() - self.t) / n)
            self.t = time.time()



if __name__ == "__main__":
    initPos = makeRndHives(nHives=9)

    #show inital random hive positions
    showPollinisation(calcPollinisation(initPos, mode='polMap'), title='startValue')

    #initalize counter for tracking of the progress in minimize
    c = Counter(time.time())

    tStart = time.time()
    #run the minimization
    res = minimize(calcPollinisation, initPos, method='Powell', tol=tol)
    tEnd = time.time()
    print("Time to run minimization: " + str((tEnd-tStart)) +" s")

    #show results of minimization
    print(res)

    #show the final result as an image
    showPollinisation(calcPollinisation(res.x, mode='polMap'), title='Optimized')
