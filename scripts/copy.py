import csv

oldcsv = csv.reader(open("./results.csv"))
newcsv = open("./resultsnew.csv", 'w')
for row in oldcsv:
    current = row[0][1]
    print(current)
    newcsv.write(current + "\n")