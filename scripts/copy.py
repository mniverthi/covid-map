import csv

oldcsv = csv.reader(open("./results-20200415-asian-discrimination-coronavirus.csv"))
newcsv = open("./results-20200415-asian-discrimination-coronavirus.csv", 'w')
for row in oldcsv:
    current = row[1]
    print(current)
    newcsv.write(current + "\n")