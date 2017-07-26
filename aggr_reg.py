__author__ = 'Valerio'

'''
Created on 25/lug/2017

@author: Valerio
'''

import sys
import csv

if len(sys.argv) <> 2:
    print("Usage: aggr_reg.py filname")
    sys.exit(1)

filename = sys.argv[1]
print(filename)

csvfile = open(filename+'.csv', 'r')
reader = csv.reader(csvfile, delimiter=';')
headers = reader.next()

###READ AND AGGREGATE VALUES###
aggr = {}
for row in reader:
    region = row[0]
    check = 0
    try:
        data = map(lambda x: float(x), row[3:])
        for d in data:
            if math.isnan(d):
                check = 1
        if check==1:
            continue
        if region in aggr:
            aggr[region] = [x + y for x, y in zip(aggr[region], data)]
        else:
            aggr[region] = data
    except ValueError:
        continue
csvfile.close()

###COMPUTE NEW COLUMNS AND WRITE TO FILE###
for region in aggr:
    values = aggr[region]
    maschi = int(values[1])
    totali = int(values[0])
    femmine = totali - maschi
    votanti = values[2]
    percvotanti = 100*votanti/totali
    votantisi = 100*values[4]/votanti
    votantino = 100*values[5]/votanti
    altri = 100*sum(values[6:8])/votanti
    aggr[region] = [region, maschi, femmine, totali, percvotanti, votantisi, votantino, altri]
#print(aggr)

###WRITE TO FILE###
out = open(filename+'-aggregated.csv','wb')
writer = csv.writer(out, delimiter = ';')
newheaders = ['Regione',
              'Elettori Maschi',
              'Elettori Femmine',
              'Elettori Totali',
              'Percentuali votanti',
              'Percentuale voti si',
              'Percentuale voti no',
              'Percentuale schede bianche, non valide o contestate']
writer.writerow(newheaders)
for region in aggr:
    writer.writerow(aggr[region])
out.close()