import sys
import json
import csv

#read file
with open('timeseries.json', 'r') as jsonfile:
    data = jsonfile.read()


#parse file
dataobj = json.loads(data)


f = csv.writer(open("sample_data_countries.csv", "w"))

initialrow = ["date", "country", "confirmed", "deaths", "recovered"]
f.writerow(initialrow)

'''
this is the csv format
date, country, confirmed, deaths, recovered
'''
for all in dataobj:
    for each in dataobj[all]:
        key = []
        key.append(each['date'])
        key.append(each['confirmed'])
        key.append(each['deaths'])
        key.append(each['recovered'])
        key.insert(1, all)
        f.writerow(key)
    # for all in each:
    #     f.writerow(all['confirmed'])
    #     f.writerow(all['deaths'])
    #     f.writerow(all['recovered'])
    # for node in point:
    #     for element in node:
            

        


