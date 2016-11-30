import os
import re
import glob
import fnmatch

verbose = True
#verbose = False

raw_path = '/Users/billmarty/SN2logs/ThanksgivingWeekend'

# get the bms and run .csv files
# raw_path = input('Enter directory path: ')
if verbose: print(raw_path)
os.chdir(raw_path)
files=glob.glob("*.csv")
bms_files = fnmatch.filter(files,"*bms*")
run_files =fnmatch.filter(files,"*run*")

if verbose:
    print("%i bms, %i run, total = %i"%(len(bms_files),len(run_files),len(files)))

# merge bms files
bms_lines = 0
if bms_files:
    fd_out = open("bms_all.csv","w")
    bms_files.sort()
    for file in bms_files:
        fd_out.write("\n%s\n"%file)
        fd_in = open(file)
        for line in fd_in.readlines():
            fd_out.write(line)
            bms_lines += 1
        fd_in.close()
    fd_out.close()
print("%i lines written to bms_all.csv"%bms_lines)

# merge run files
run_lines = 0
if run_files:
    fd_out = open("run_all.csv","w")
    run_files.sort()
    for file in run_files:
        fd_out.write("\n%s\n"%file)
        fd_in = open(file)
        for line in fd_in.readlines():
            fd_out.write(line)
            run_lines += 1
        fd_in.close()
    fd_out.close()
print("%i lines written to run_all.csv"%run_lines)

