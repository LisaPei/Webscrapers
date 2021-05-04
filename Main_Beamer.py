
from multiprocessing import Pool
from Beamer import scrape 
import csv

# 
if __name__ == '__main__':
    with open('/Users/lisapei/Documents/Beamer_Data.csv','rt') as infile:
        data = csv.reader(infile)
        lines = []
        for line in data:
            lines += line[0].split(';')
        lines = [x for x in lines if x != ""]
        # for rows with multiple websites
    with Pool(100) as p:
        results = p.map(scrape, lines)
    with open('/Users/lisapei/Documents/Beamer_OutputData.csv', mode='w+') as output:
        writer = csv.writer(output, delimiter=',')
        writer.writerows(results)
        #method (writerow) is part of the class (writer)
    print('done')