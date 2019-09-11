from astropy import units as u
from astropy.coordinates import SkyCoord
import matplotlib.pyplot as plt
import numpy as np
from astropy.coordinates import ICRS, Galactic, FK4, FK5 
from astropy.coordinates import Angle, Latitude, Longitude
import warnings
import argparse
import codecs
import subprocess

def ignorewarning():
    warnings.simplefilter('ignore', RuntimeWarning)
    warnings.simplefilter('ignore', UserWarning)
    warnings.simplefilter('ignore', FutureWarning)

def runpsrchive(inputname):
    """Using psrcat to get pulsar parameters.
    """
    #print ('Getting pulsar parameters from Psrcat......')
    subprocess.call('psrcat -nohead -nocand -nonumber -o long_error -c "jname RAJD DecjD" > %s.txt' % (inputname), shell=True)

def getdata(inputname):
    f = codecs.open(('%s.txt' % inputname), mode='r', encoding='utf-8')
    lines = f.readlines()
    length = len(lines)
    i = 0
    pulsar_name = []
    raj = []
    decj = []
    
    while i< length:
        if '*' in lines[i]:
            i += 1
        else:
            line = lines[i].split()
            #print line
            pulsar_name.append(line[0])
            raj.append(line[1])
            decj.append(line[2])
            i += 1

    return pulsar_name, raj, decj

def get_position(ra,dec):
    coords_radec = SkyCoord(ra, dec, unit='deg')
    coords_galactic = coords_radec.transform_to(Galactic)
    coords_l = coords_galactic.l.wrap_at(180 * u.deg).radian
    coords_b = coords_galactic.b.radian
    return coords_l, coords_b

def main():
    parser = argparse.ArgumentParser(description='PLot the sky distribution of known pulsar')
    parser.add_argument('inputname', help='the input name, you can just input any name')
    args = parser.parse_args()
    
    inputname = args.inputname

    runpsrchive(inputname)

    pulsar_name, raj, decj = getdata(inputname)

    #print pulsar_name, raj, decj

    ra_rad_list, dec_rad_list = [], []

    i = 0
    while i < len(pulsar_name):
        ra_rad, dec_rad = get_position(raj[i],decj[i])
        ra_rad_list.append(ra_rad)
        dec_rad_list.append(dec_rad)
        i += 1

    #show figure
    plt.figure(dpi=100, facecolor='w',edgecolor='w')
    plt.subplot(111, projection="aitoff")
    plt.title("Sky Distribution of Known Pulsar", y=1.08)
    plt.xlabel(" Galactic longitude")
    plt.ylabel("Galactic latitude")
    plt.grid(True)
    plt.plot(ra_rad_list, dec_rad_list, 'ro', markersize=2, alpha=0.3, ls='none')
    plt.subplots_adjust(top=0.95,bottom=0.0)
    plt.show()


if  __name__=="__main__":
    ignorewarning()
    main()
