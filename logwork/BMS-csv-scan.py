import os
import glob
import re

def main():
    dpath='C:/Users/new/Documents/PlanetaryLT/DeepSea'
    fname = input("CSV filename: ")
    #dpath='C:\\Users\\new\\Downloads\\SFTP'
    #pat='*bms*'
    os.chdir(dpath)
    print(os.getcwd())
    #bms_files = glob.glob(pat)
    #print(len(bms_files))

    #for fname in glob.iglob(pat):
        #print(fname)
     #   if fname.split('.')[1]=='csv':
     #       check_file(fname,',R,')

    # read the CSV file line by line
    fd=open(fname,mode='r')
    mline={}
    for n,line in enumerate(fd):
        #print(n,line)
        elements = line.split(',')
        for i,ele in enumerate(elements):
            if ele:
                #print(i,ele)
                mline[str(i)]=ele
        m=[]
        for j in range(len(mline)):
            if str(j) in mline.keys():
                m.append(mline[str(j)])
        print(','.join(m))

    print("%i lines read"%n);
if __name__ == '__main__':
    main()
