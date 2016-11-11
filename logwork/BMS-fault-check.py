import os
import glob
import re

nfaults=0

def check_file(fname,pat):
    ## check file for a given pattern
    #pat = re.compile(r'001,[SIORDCF]{1},122')
    pat = re.compile(r'001,S,122,')
    new_stat = ''
    old_stat = ''
    global nfaults
    print("Checking file %s"%(fname))
    print("fSize = %i"%os.lstat(fname).st_size)
    f=open(fname)

    for n,line in enumerate(f.readlines()):
        # see if this is a STRING status message
        mat = pat.search(line)  #get a MATCH obj

        if mat:   # if not None
            new_stat = line[mat.start()+17]  #locate STATE char
            if new_stat != old_stat:
                if new_stat == 'F':         # flag any fault states
                    print('*** *** *** '*5)
                    nfaults += 1
                print('%8i %c %s'%(n,new_stat,line))
                old_stat = new_stat

def main():
    #dpath='C:/Users/new/Documents/PlanetaryLT/LogArchive/Jack10-4-16/logs'
    dpath='C:\\Users\\new\\Documents\\PlanetaryLT\\LogArchive\\Jack10-11-16\\logs'
    pat='*bms*'
    os.chdir(dpath)
    print(os.getcwd())
    bms_files = glob.glob(pat)
    print(len(bms_files))

    for fname in glob.iglob(pat):
        #print(fname)
        if fname.split('.')[1]=='csv':
            check_file(fname,',R,')

    print('Number of Faults = %i'%nfaults)

if __name__ == '__main__':
    main()
