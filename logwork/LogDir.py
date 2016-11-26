# Read and process a directory of log files generated by HyGen CMS.

import os
import glob

verbose = True  # Switch dev print statements on and off
#log_path = '/Users/billmarty/CMSlogs'
log_path = '/Users/billmarty/CMSlogsShort'
#log_path = '/Users/billmarty/V2logs/logs'
# We're going to create a sub_directory for our output files.
sub_dir = 'dayFiles'

class LogDir():
    """The LogDir class manages the directory in which CMS log files are
    located. The CMS generates new log files each hour.  We want to concatenate
    hourly files into daily logs, and locate those in a subdirectory.  Then
    the hourly log files will be discarded."""

    def __init__(self, log_path):
        # Go to the log directory and get a list of the 'run' log files.
        # Also list 'bms' files and 'fast' files (if any).
        os.chdir(log_path)
        if verbose: print('Working dir: {}'.format(os.getcwd()))
        self.run_files = glob.glob("*run*.csv")
        self.bms_files = glob.glob("*bms*.csv")
        self.fast_files = glob.glob("*fast*.csv")
        if verbose:
            print('There are {} run files, {} bms files, and {} fast files.'
                  .format(len(self.run_files), len(self.bms_files),
                          len(self.fast_files)))
        self.run_files.sort()
        self.bms_files.sort()
        # Don't bother sorting fast files, as we're just going to discard 'em.

        # Does our output file sub_directory already exist?
        dir_contents = os.listdir(log_path)
        if sub_dir not in dir_contents:
            if verbose: print('mkdir ' + sub_dir)
            try:
                os.mkdir(sub_dir, mode=0o777)
            except:
                print('!!mkdir exception!!')
        dir_contents = None

        # File name template: year-month-day_hour_run#.csv
        # Get a list of the dates.
        self.date_list = []
        surprise_files = []
        for file in self.run_files:
            if '_' in file:
                underscore = file.find('_')
                file_date = file[:underscore]
                if file_date not in self.date_list:
                    self.date_list.append(file_date)
            else:
                surprise_files.append(file)
        if verbose:
            if surprise_files:
                print('Surprise files: {}'.format(surprise_files))
            print("{} unique dates: {}".format(len(self.date_list), self.date_list))

    @staticmethod
    def parse_csv_fields(header, data):
        """Our run log files are stored in csv format, with the first line
        in the file a header that defines the fields.  This function creates
        a dictionary from a header line and a data line by matching up
        fields."""
        info = {}
        header_fields = str.split(header.rstrip(), ',')
        data_fields = str.split(data.rstrip(), ',')

        # Our header may contain extra fields of information.
        # If so, truncate it.
        if len(header_fields) != len(data_fields):
            header_fields = header_fields[:len(data_fields)]

        # Match up the lists to create a dictionary.
        # Include only fields with non-empty data
        for index in range(len(data_fields)):
            if data_fields[index]:
                info[header_fields[index]] = data_fields[index]

        return info

    def add_table_entry(self, table, file, first_line, last_line):
        """When analyzing a batch of run log files, I want answers
        to a couple of questions:
            Are there gaps in the log?
            Does the engine start or stop in this file?
            Any other obvious anomalies?
        This function fills in a table for at-a-glance analysis
        of a day's log files."""

        # Define the table header for use later when writing the file.
        self.table_header = ['file', 'startTime', 'endTime', 'gap', 'starts']

        # Gaps shorter than this are not flagged.
        gap_tolerance = 10.0

        entry = {'file': file}
        if first_line and last_line:
            try: entry['startTime'] = first_line['linuxtime']
            except KeyError: entry['startTime'] = ''
            try: entry['endTime'] = last_line['linuxtime']
            except KeyError: entry['endTime'] = ''
            if table:
                try:
                    gap = float(entry['startTime']) - float(table[-1]['endTime'])
                except (KeyError, ValueError):
                    entry['gap'] = ''
                else:
                    if gap > gap_tolerance:
                        entry['gap'] = str(int(gap))

            try:
                entry['starts'] = str(float(last_line['Engine Starts'])
                                    - float(first_line['Engine Starts']))
            except KeyError:
                entry['starts'] = ''
        else:
            entry['startTime'] = 'Zero byte file'
            entry['endTime'] = '0'

        table.append(entry)

    def write_table_file(self, table, sub_dir_table_name):
        """Assuming a completed analysis table, will write it out
        as a csv file."""

        lines = 0
        with open(sub_dir_table_name, 'w') as outfile:
            # Write the header line.
            line = self.table_header[0]
            for field in self.table_header[1:]:
                line += ',' + field
            outfile.write(line + '\n')
            lines += 1

            # Write the table lines.
            for entry in table:
                line = entry[self.table_header[0]]
                for field in self.table_header[1:]:
                    try:
                        line += ','+ entry[field]
                    except KeyError:
                        line += ','
                outfile.write(line + '\n')
                lines += 1

        if verbose:
            print('{} table lines written to {}'.format(lines, sub_dir_table_name))

    def recent_date_logs(self):
        """Look at the list of log files in the target directory, and RETURN
        a list of all the files from the most recent date.  Then, pop that
        date from the list"""

        # In theory, run_files are already sorted by date.
        self.recent_date_files = []
        while self.date_list[-1] in self.run_files[-1]:
            self.recent_date_files.append(self.run_files.pop())
            # Avoid the IndexError when we pop the last run_file.
            if not self.run_files: break
        self.recent_date_files.reverse()
        # Pop this date from the list.
        self.active_date = self.date_list.pop()
        if verbose:
            print('\nMost recent date is {}'.format(self.active_date))
            print('{} recent date files: {}'.format(len(self.recent_date_files),
                                                    self.recent_date_files))

        return self.recent_date_files

    def concatenate_recent_logs(self):
        """Let's concatenate the recent_date_files into a single file.
        While concatenating, let's build a table that highlights gaps
        in the log."""
        is_first_header = True  # Only copy the header line once.
        line_count = 0
        table = []
        recent_date_file_name = self.active_date + '_day_run.csv'
        recent_date_table_name = self.active_date + '_analysis.csv'
        sub_dir_file_name = './{}/{}'.format(sub_dir, recent_date_file_name)
        sub_dir_table_name = './{}/{}'.format(sub_dir, recent_date_table_name)
        if verbose:
            print(sub_dir_file_name)
        with open(sub_dir_file_name, 'w') as outfile:
            for file in self.recent_date_files:
                with open(file, 'r') as infile:
                    lines = infile.readlines()
                    # Check for empty files.  We got some in development.
                    # Also have seen files with only a header line.
                    if len(lines) > 1:
                        header = lines.pop(0)
                        if is_first_header:
                            outfile.write(header)
                            line_count += 1
                            is_first_header = False
                        # I've seen at least one run log file where
                        # the last line is corrupt or invalid.
                        # So, check the last line, and dump if necessary.
                        keep = True
                        commas = header.count(',') - 5  # Header has extra fields.
                        if lines[-1].count(',') < commas: keep = False
                        # Any more tests?
                        if not keep:
                            line_invalid = lines.pop()
                        for n, line in enumerate(lines):
                            outfile.write(line)
                            line_count += 1
                        # Grab the first and last line info I want for my table.
                        first_line = self.parse_csv_fields(header, lines[0])
                        last_line = self.parse_csv_fields(header, lines[-1])
                    else:
                        first_line = None
                        last_line = None
                    self.add_table_entry(table, file, first_line, last_line)
                # We're done with lines here.  Can we encourage garbage
                # collection to free the memory?
                del lines[:]
        if verbose:
            print('Line count: {}'.format(line_count))
            print('Table entries: {}'.format(len(table)))
        self.write_table_file(table, sub_dir_table_name)

    def process_all_dates(self):
        """If logging has been running for a while, the directory will have
        log files for multiple dates.  Process them all :-)"""

        while self.date_list:
            self.recent_date_logs()
            self.concatenate_recent_logs()



def main():
    """Read and process a directory of log files generated by HyGen CMS.
    In main, we'll handle things like detecting the OS, and determining
    the path to the directory of log files."""

    # TODO - locate OS detection code here.
    my_logdir = LogDir(log_path)
    my_logdir.process_all_dates()


if __name__ == '__main__':
    main()
