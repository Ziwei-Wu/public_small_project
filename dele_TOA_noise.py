import argparse
import warnings
import matplotlib.pyplot as plt
import subprocess

def ignorewarnings():   
    warnings.simplefilter('ignore', RuntimeWarning)
    warnings.simplefilter('ignore', UserWarning)
    warnings.simplefilter('ignore', FutureWarning)

def getbadchan(parfile, timfile):
    """use tempo2 to get all TOAs,
    and then, remove tempo2 information, only keep TOAs."""

    toafile = timfile.split('.',1)[0]
    subprocess.call('tempo2 -output general2 -f %s %s -s "{bat} {freq} {post} \n" > %s_toa.txt' % (parfile, timfile, toafile), shell=True)

    alltoas = open('%s_toa.txt' % toafile,'r')
    contexts = alltoas.readlines()
    
    i, start, end = 0, 0, 0
    while i < len(contexts):        
        if contexts[i].split(' ')[0] == "Starting":
            start = i
        if contexts[i].split(' ')[0] == "Finishing": 
            end = i
        i += 1 
    
    i = start + 1
    bad_freq = []
    while start < i < end-1:
        if float(contexts[i].split(' ')[2]) > 0.01 or float(contexts[i].split(' ')[2]) < -0.01:
            chan = round(float(contexts[i].split(' ')[1]), 6)
            bad_freq.append(chan)
        i += 1

    return bad_freq

def removebadchan(badchan, timfile):
    with open(timfile, "r+") as f:
        d = f.readlines()
        data0 = d[0]
        d = d[1:]
        f.seek(0)
        for i in d:
            chan = float(i.split(' ')[1])
            if chan in badchan:
                print chan
            else:
                f.write(i)
        f.truncate()
    return data0

def addinfo(data0, timfile):
    f = open(timfile)
    text = f.read()
    f.close()
    f = open(timfile, 'w')
    f.write('%s' % data0)
    f.write(text)
    f.close

                
        

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Select the archive.')
    parser.add_argument('-p', '--parfile', help='The chosen par file')
    parser.add_argument('-t', '--timfile', help='The chosen tim file that needs to remove noise toas')
    args = parser.parse_args()
    parfile = args.parfile
    timfile = args.timfile

    ignorewarnings()
    badchan = getbadchan(parfile, timfile)
    print ('we have %s bad channels' % len(badchan))
    data0 = removebadchan(badchan, timfile)
    addinfo(data0, timfile)
