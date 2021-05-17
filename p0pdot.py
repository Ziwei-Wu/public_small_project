#python2.7
#program to show p-p dot plot

import numpy as np
import matplotlib.pyplot as plt
import subprocess

#load pulsar's information from psrcat
proc=subprocess.Popen("psrcat -nohead -nocand -o long_error -c 'jname p0 p1'",stdout=subprocess.PIPE, shell=True)
stdout = proc.stdout.read()
data_cub = stdout.split('\n')
pulsar_name, p0, p1 = [], [], []

for i in range(0, len(data_cub)):
    information = []
    for infor in data_cub[i].split(' '):
        if infor != "":
            information.append(infor)

    try:
        p1.append(float(information[6]))
        p0.append(float(information[3]))
        pulsar_name.append(information[1])
    except:
        pass

fig = plt.subplots(nrows=1, ncols=1, figsize=(10,10))
plt.subplots_adjust(left=0.1, bottom=0.06, right=0.99, top=0.99, wspace=None, hspace=None)
plt.plot(p0, p1, 'bs', color='gray')

p0 = np.linspace(1E-3, 20, 1000)

characteristic_age = [1E+3, 1E+6, 1E+9]
n = 3
angle=20
for age in characteristic_age:
    p1_show = np.array(p0) / (age * 365.25 * 86400 * (n-1))
    plt.plot(p0, p1_show, linestyle='--', color='black')
    time = int(float(str(age).count('0')))-1
    plt.text(np.min(p0), np.min(p1_show), r'$\tau = 10^{%.0f} yr$' % time, fontsize=16, rotation=angle, rotation_mode='anchor')

magnetic = [1E+14, 1E+12, 1E+10]
angle=-20
for magnetic_plot in magnetic:
    p2_show = np.power(magnetic_plot/(3.2E+19 * np.sqrt(p0)), 2.0)
    plt.plot(p0, p2_show, linestyle='-.', color='black')
    time = int(float(str(magnetic_plot/10000).count('0'))) + 3
    plt.text(np.max(p0)-15, np.min(p2_show)*4.2, r'$B = 10^{%.0f} G$' % time, fontsize=16, rotation=angle, rotation_mode='anchor')

plt.yscale('log')
plt.xscale('log')
plt.xlim(1E-3, 20)
plt.ylim(1E-22, 1E-9)
plt.xlabel("Period (s)", fontsize=20)
plt.ylabel("dp/dt (s/s)", fontsize=20)
plt.show()
    
