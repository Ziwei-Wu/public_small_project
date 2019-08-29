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


def get_txt(archives):
        print ('Creating the Profile of %s' % archives)
        subprocess.call('pdv -t -FTp %s > %s.txt' % (archives, archives), shell=True)
        
def get_values(archive):
    f = codecs.open(('%s.txt' % archive), mode='r', encoding='utf-8') 
    lines = f.readlines()
    lines = lines[1:]
    lent = len(lines)

    i=0
    profile = []
    while i < lent:
        a = lines[i].split()
        value = float(a[3])
        profile.append(value)
        i = i+1

    return profile


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Select the archive.')
    parser.add_argument('archive', help='The chosen archives')
    args = parser.parse_args()
    archives = args.archive

    ignorewarning()

    get_txt(archives)

    profile = get_values(archives)

    plt.plot(profile)
    plt.show()
    
