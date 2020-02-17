import numpy as np
import matplotlib.pyplot as plt
import random

def load_from_txt(text):
    """
    Loading data from input .txt file
    """
    with open(text, 'r') as myfile:
        lines = myfile.readlines()
    meta_data = lines[-1]
    _, _, name, site, minFreq, maxFreq, mjd_start, mjd_end, ra, dec = meta_data.split(' ')
    mjd_start = float(mjd_start)
    mjd_end = float(mjd_end)
    length = (mjd_end - mjd_start)*24.0*3600.0
    minFreq = float(minFreq)
    maxFreq = float(maxFreq)
    diff = maxFreq - minFreq
    full_arr = np.genfromtxt('%s' % text)
    print ("\n\t OBSERVATION PROPERTIES\n")
    print ("Pulsar Name:\t\t\t{0}".format(name))
    print ("Observation Station:\t\t{0}".format(site))
    print ("Centre MJD:\t\t\t{0}".format((mjd_end + mjd_start)/2.0))
    print("Centre Frequency (MHz):\t\t{0}".format((maxFreq + minFreq)/2.0))
    print("Bandwidth (MHz):\t\t{0}".format(diff))
    print("Channel Bandwidth (MHz):\t{0}".format(diff/(full_arr.T.shape[0]-1)))
    print("Integration Time (s):\t\t{0}".format(length))
    print("Subintegration Time (s):\t{0}\n".format(length/(full_arr.T.shape[1]-1)))
    
    return full_arr, diff, length, minFreq, maxFreq, mjd_start, mjd_end, name

def fack():
    x = np.linspace(1, 350, 350, endpoint = True)
    y = []
    for x0 in x:
        y0 = -0.001*(x0-175)**2 + random.randint(98, 102)
        y.append(y0)
    x_new = np.linspace(1, 700, 700, endpoint = True)
    x_new = np.array(x_new)
    y_new = np.array(y)
    y_new = np.concatenate((y_new, y_new), axis=0)
    plt.scatter(x_new,y_new, s=10)
    plt.show()

    return x_new, y_new

def clean(mjd, flux):
    #remove "0"
    mjd = list(mjd)
    flux = list(flux)
    bad = []
    for i in range(len(flux)):
        if flux[i] == 0.0:
            bad.append(i)

    for i in sorted(bad, reverse=True):
        del flux[i]
        del mjd[i]


    # remove "masked"
    mjd = list(mjd)
    flux = list(flux)
    bad = []
    for i in range(len(flux)):
        if str(flux[i]) == "--":
            bad.append(i)

    for i in sorted(bad, reverse=True):
        del flux[i]
        del mjd[i]

    return mjd, flux

def timeseries(dynspec):
    time_series = dynspec.mean(0)
    time_series /= np.mean(time_series)
    mjd = np.linspace(1, len(time_series), len(time_series), endpoint = True)
    mjd, time_series = clean(mjd, time_series)
    #plt.scatter(mjd, time_series)
    #plt.show()
    #mjd, time_series = fack()
    structure_function_new(mjd, time_series)
    #fit_structure(mjd, time_series)

def structure_function(time, para):
    para_mean = (np.mean(para))**2

    n = 1
    structure_time = []
    structure = []
    while n < np.max(time):
        structure_time.append(n)
        sum_list = []

        for i in range(np.max(time)-n):
            value = (para[i] - para[i+n])**2
            sum_list.append(value)
            
        structure.append(np.sum(sum_list)/(para_mean*len(sum_list)))
        n *= 2

    fig, ax = plt.subplots()
    ax.set_xscale('log')
    ax.set_yscale('log')
    plt.ylabel('Structure function of Flux')
    plt.xlabel('Time Lag (mins)')
    plt.scatter(structure_time, structure, s=10)
    plt.show()

def x_coor(threshold, number):
    #get max threshold
    i = 0
    while 10**i < threshold:
        i += 1

    #get initial x coordiate
    x = 10.0**np.linspace(0.0, i, number)
    #get in initial x coordiate
    x = [int(ele) for ele in x]
    #remove repeate element in x coordiate
    x = list(set(x))
    #sort x coordiate
    x.sort(cmp=None, key=None, reverse=False)
    #get those values that are smaller than threshold
    x_new_list = []
    for x_ele in x:
        if x_ele < threshold:
            x_new_list.append(x_ele)
    
    return x_new_list

def structure_function_new(time, para):
    """
    This part code is writen by Ziwei to get the structure function of time series
    """
    time = list(time)
    para_mean = (np.mean(para))**2

    n = 1
    structure_time = []
    structure = []
    x_coordiate = x_coor(0.75*np.max(time), 20)
    for n in x_coordiate:
        structure_time.append(n)
        sum_list = []

        for i in range(len(time)):
            a = time[i] + n
            if a in time:
                value = (para[i] - para[time.index(a)])**2
                sum_list.append(value)

        print ("The structure function at time lag %.0f is %f with %.0f points." % (n, np.sum(sum_list)/(para_mean*len(sum_list)), int(len(sum_list))))
        #structure.append(np.sum(sum_list)/(para_mean*len(sum_list)))
        structure.append(np.sum(sum_list)/len(sum_list))
        #n *= 2

    fig = plt.figure(figsize=(10,10))
    plt.xscale('log')
    plt.yscale('log')
    plt.ylabel('Structure function of Flux')
    plt.xlabel('Time Lag (mins)')
    #plt.ylim(np.min(structure/np.mean(structure)), 1.3*np.max(structure/np.mean(structure)))
    #plt.scatter(structure_time, structure/np.mean(structure), s=10)
    plt.scatter(structure_time, structure, s=10)
    plt.show()

def fit_structure(mjd, flux):
    """
    This part code is writen by Yulan to get the structure function of time series
    """
    D_k=[]
    klag =[]
    mjd_list= list(mjd)
    
    F=np.mean(flux)
    k=1
    days = np.max(mjd)-np.min(mjd)
    while k <= np.max(mjd):
        i=0
        stru=0
        Nk=0
        while mjd[i]+k <= np.max(mjd):
            if mjd[i]+k in mjd:
                stru=stru+(flux[i]-flux[mjd_list.index(mjd[i]+k)])**2
                Nk += 1
            else:
                pass
            i += 1
        if Nk >=1:
            klag.append(k)
            D_k.append(stru/(F**2)/Nk)
        else:
            pass
        print('the lag of %.0f days have %.0f points:%f' % (k,Nk,stru/(F**2)/Nk))
        
        k *= 2
    
    fig, ax = plt.subplots()
    ax.set_xscale('log')
    ax.set_yscale('log')
    plt.scatter(klag,D_k)
    plt.show()


def main():
    #mjd, time_series = fack()
    structure_function_new(mjd, time_series)
    #fit_structure(mjd, time_series)

if __name__ == "__main__":
    main()
    
