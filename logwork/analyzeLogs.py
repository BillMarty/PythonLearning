# Read and process a directory of log files generated by HyGen CMS.
#   Thanks to Herb Hainey for some source code contributions.

import os
import glob

verbose = True  # Switch dev print statements on and off
log_path = '/Users/billmarty/CMSlogs'
# We're going to create a sub_directory for our output files.
sub_dir = 'dayFiles'

def main():

    # Go to the log directory and get a list of the 'run' log files.
    os.chdir(log_path)
    if verbose: print('Working dir: ' + str(os.getcwd()))
    run_files = glob.glob("*run*.csv")
    if verbose: print('There are ' + str(len(run_files)) + ' run log files.')
    run_files.sort()

    # Does our output file sub_directory already exist?
    dirs = os.listdir(log_path)
    if not sub_dir in dirs:
        if verbose: print('mkdir ' + sub_dir)
        try:
            os.mkdir(sub_dir, mode=0o777)
        except:
            print('!!mkdir exception!!')


    # File name template: year-month-day_hour_run#.csv
    # Get a list of the dates.
    date_list = []
    for file in run_files:
        if '_' in file:
            underscore = file.find('_')
            file_date = file[:underscore]
            if not file_date in date_list:
                date_list.append(file_date)
    if verbose:
        print(str(len(date_list)) + ' unique dates')
        print(date_list)
        print('Most recent date is: ' + str(date_list[-1]))

    # Let's start with the run files for the most recent date.
    # In theory, run_files is already a sorted by date.
    recent_date_files = []
    while date_list[-1] in run_files[-1]:
        recent_date_files.append(run_files.pop())
    recent_date_files.reverse()
    if verbose:
        print(str(len(recent_date_files)) + ' recent date files')
        print(recent_date_files)

    # Let's concatenate the recent_date_files into a single file.
    # While concatenating, let's build a table that highlights gaps in the log.
    is_first_header = True  # Only copy the header line once.
    line_count = 0
    recent_date_file_name = date_list[-1] +'_day_run.csv'
    sub_dir_file_name = './' + sub_dir + '/' + recent_date_file_name
    if verbose:
        print(recent_date_file_name)
        print(sub_dir_file_name)
    with open(sub_dir_file_name, 'w') as outfile:
        for file in recent_date_files:
            with open(file, 'r') as infile:
                lines = infile.readlines()
                header = lines.pop(0)
                if is_first_header:
                    outfile.write(header)
                    line_count += 1
                    is_first_header = False
                for line in lines:
                    outfile.write(line)
                    line_count += 1

    if verbose: print('Line count: ' + str(line_count))







if __name__ == '__main__':
    main()
