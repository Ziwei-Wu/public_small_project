import matplotlib.pyplot as plt
import numpy as np
import argparse
import warnings

def ignorewarning():
    warnings.simplefilter('ignore', RuntimeWarning)
    warnings.simplefilter('ignore', UserWarning)

###step-0, fake data
def fakedata():
    #10 years and 500 observations
    mjd = np.linspace(1, 3650, 2500)
    para = 0.1*np.sin(mjd/50) + 0.1*np.cos(mjd/50) + 0.1

    #int observation time
    int_mjd = []
    for x in mjd:
        int_mjd.append(int(x))

    return int_mjd, para

def cal_structure(mjd,para):
    #Based on the equation(3) from Stinebring et al.2000 (539,300-316, ApJ)

    #fake the lag of K.
    obser_len = int(np.max(mjd) - np.min(mjd)) 
    k = 2
    k_list = []
    power = 0
    a = 0
    while a < obser_len/2:
        a = k**power
        k_list.append(a)
        power += 1

    print k_list

    #calcuate structure function
    M = len(mjd)

    stru_list = []

    weight = np.mean(para)**2
    for lag in k_list:
        sum = 0
        number = 0
        i = 0
        while i < M:
            target = mjd[i] + lag
            if target in mjd:
                location = mjd.index(target)
                sum += (para[i] - para[location])**2
                number += 1
                
            i += 1
        print number
        stru_value = sum/(number*weight)
        print ('the value of the structure function at %f is %f' % (lag, stru_value))
        stru_list.append(stru_value)

    return k_list, stru_list  


if __name__ == '__main__':
    ignorewarning()
    x, y =fakedata()
    k_list, stru_list = cal_structure(x,y)
    plt.subplot(121)
    plt.plot(x,y)

    plt.subplot(122)
    plt.plot(k_list, stru_list)
    plt.yscale('log')
    plt.xscale('log')
    plt.show()
