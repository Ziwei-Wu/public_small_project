# coding: utf-8
# this code can be used to predict the scintillation time-scale using scattering time and proper motion.
# The first step is to find the brightest pulsar using psrcat.
# then, using psrcat to get the distcane, proper motion, scattering decay time and assuming a scattering screen at a distance xD (x=0.5),
# then, based on function 11.15 and 11.16 at 1988_Book_GalacticAndExtragalacticRadioAstronomy,
# then, we can get what we want.

import subprocess
import codecs
import argparse
import numpy as np
import matplotlib.pyplot as plt
import warnings

def ignorewarning():
    warnings.simplefilter('ignore', RuntimeWarning)
    warnings.simplefilter('ignore', UserWarning)
    warnings.simplefilter('ignore', FutureWarning)

def calwavelength(frequency):
    """This converts a given frequency of light to an 
    approximate wavelength.
    """
    sol = 299792458.00 #this is the speed of light in m/s
    #sol = 300000000.00 #this is the speed of light in m/s
    frequency = (1.0*10**6) * frequency
    frequency = float(frequency)
    answerlamda = sol / frequency
    """
    print "the wavelength is %s meters" % answerlamda
    if answerlamda >=1000:
        print "Theoretically long Radio wave"
    if answerlamda <= 1000 and answerlamda >= 0.01:
        print "Radio Wave"
    elif answerlamda <= 0.01 and answerlamda >= 0.00001:
        print "Microwave"
    elif answerlamda <= 0.00001 and answerlamda >= 0.0000005:
        print "Infra Red"
    elif answerlamda <= 0.0000005 and answerlamda >= 0.00000001:
        print "Visible Light"
    elif answerlamda <= 0.00000001 and answerlamda >= 0.0000000001:
        print "Ultra Violet"
    elif answerlamda <= 0.0000000001 and answerlamda >= 0.000000000001:
        print "X-Rays"
    elif answerlamda <= 0.000000000001:
        print "Gamma Rays"
    else:
        print "Not within a range generally observed"
    """
    return answerlamda

def runpsrchive(outputname):
    """Using psrcat to get pulsar parameters.
    """
    #print ('Getting pulsar parameters from Psrcat......')
    subprocess.call('psrcat -nohead -nocand -nonumber -o long_error -s s400 -l "s400>20 && decj > -30.0 && Tau_sc!=0" -c "jname p0 s400 Tau_sc VTrans Dist" > %s.txt' % (outputname), shell=True)

def getdata(outputname):
    f = codecs.open(('%s.txt' % outputname), mode='r', encoding='utf-8')
    lines = f.readlines()
    length = len(lines)
    i = 0
    pulsar_name = []
    distance = []
    scattering_decay = []
    proper_motion = []
    
    while i< length:
        if '*' in lines[i]:
            i += 1
        else:
            line = lines[i].split()
            pulsar_name.append(line[0])
            distance.append(float(line[8]))
            scattering_decay.append(float(line[5]))
            proper_motion.append(float(line[7]))
            i += 1

    return pulsar_name, distance, scattering_decay, proper_motion

def cal_time_scale(pulsar_name, distance, scattering_decay, proper_motion, wavelength, x, freq):
    time_scale = []
    c = 299792458.00
    unit = 30856775812799586000
    i = 0
    
    while i < len(pulsar_name):
        distance_meter = distance[i] * unit
        pm = proper_motion[i] * 1000.0
        scattering_sec = scattering_decay[i]* ((freq/1000.0)**(-4.4))
        scintillation_time_scale =  wavelength * (distance_meter**0.5) * ((x*(1-x))**0.5) * (scattering_sec ** (-0.5)) / (pm * c**0.5)
        print ('The prediction scintillation time-scale of %s is %s mins.' % (pulsar_name[i], scintillation_time_scale/60))
        i += 1
 
        
    
def main():
    parser = argparse.ArgumentParser(description='Select the archive.')
    parser.add_argument('outputname', help='the output name')
    parser.add_argument('-f', '--frequency', type=float, default=150.0, help='the observation frequency in the unit of MHz')
    parser.add_argument('-x', '--distancefactor', type=float, default=0.5, help='a scattering screen at a distance xD, where D is the distcane of pulsar')
    args = parser.parse_args()
    
    outputname = args.outputname
    freq = args.frequency
    x = args.distancefactor

    wavelength = calwavelength(freq)
    
    runpsrchive(outputname)
    
    pulsar_name, pulsardistance, scattering_decay, proper_motion = getdata(outputname)
    
    cal_time_scale(pulsar_name, pulsardistance, scattering_decay, proper_motion, wavelength, x, freq)
    
if  __name__=="__main__":
    ignorewarning()
    main()
