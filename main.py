import csv  # This is needed for reading and writing CSV files
from multiprocessing import Pool  # This is needed to make requests in parallel
from beamer import scrape

input_path = '/Users/lisapei/Documents/Beamer_Data.csv'
output_path = '/Users/lisapei/Documents/Beamer_OutputData.csv'
processes = 100

if __name__ == '__main__':
    with open(input_path, 'rt') as input_file:  # open the input file
        lines = []  # this list will contain urls to scrape
        for line in csv.reader(input_file):  # for each row in the CSV
            lines += line[0].split(';')   # split the contents of the 0th column on ';', and add those to the list
        lines = [x for x in lines if x != '']  # filter out empty strings, if there are any

    with Pool(processes) as p:   # create a pool of processes
        results = p.map(scrape, lines)   # make a list of results by mapping [url] -> [csv row]

    with open(output_path, mode='w+', newline='') as output_file:  # open the output file
        print(results)
        csv.writer(output_file, delimiter=',').writerows(results)  # write the results to the file, formatted as a CSV

    print('done!')  # let the user know it's finished
