import matplotlib.pyplot as plt
import numpy as np
import os
import sys
import csv

clearsky = []
globalradiation = []

if len(sys.argv) == 1:
    directory = '.'
    pathnames = os.listdir('.')
else:
    if sys.argv[1] == '-d':
        directory = './' + sys.argv[2]
        pathnames = os.listdir(directory)
    else:
        directory = '.'
        pathnames = sys.argv[1:]


for path in pathnames:
    if path[7:] == 'CS.csv':
        filename = directory + '/' + path
        try:
            with open(os.path.abspath(filename), 'r') as csvfile:
                readCSV = csv.reader(csvfile, delimiter=';')
                for row in readCSV:
                    globalradiation.append(float(row[6]))
                    if row[5] == 'N/A':
                        clearsky.append(float(0))
                    else:
                        clearsky.append(float(row[5]))
                fig = plt.figure()
                plt.plot(clearsky, label='Clearsky data')
                plt.plot(globalradiation, label='Global data')
                plt.legend(loc='upper right')
                plt.title(path[:-4])
                plt.show()
                fig.savefig(path[:-4])
        except IOError:
            raise IOError
#





