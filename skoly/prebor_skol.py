# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
# @author jmacura 2018
from csv import reader
from pprint import pprint
import sys

# Parse command line params
usage = """Pouziti: prebor_skol.py -f "soubor.csv"
Moznosti:
  -f "Prebor2018vysl.csv"  Cesta k souboru s vysledky
"""

fname = "Prebor2018vysl.csv"
if len(sys.argv) == 3:
     if(str(sys.argv[1]) == '-f'):
         fname = sys.argv[2]
else:
    print(usage)
    quit()

def printRes(category):
    fh.write("{}  {:<20} {:<15} {:>4}\n".format("Pořadí", "Název školy", "Město", "Body"))
    for i,t in enumerate(category):
        fh.write(" {:>3}    {:<20} {:<15} {:>4}\n".format(i+1, t[1], teams[t[1]], t[0]))

# Nacteni vstupnich dat
i = -1
headers = []
data = []
important = ["Příjmení", "Jméno (křest.)", "Klasifikace", "Název oddílu", "Město", "Krátký", "Místo"]
with open(fname) as fh:
    for row in reader(fh, delimiter=";"):
        i += 1
        if i == 0:
            for cell in row:
                headers.append(cell)
        else:
            #print("==={}===".format(i))
            row_dict = {}
            for j,cell in enumerate(row):
                #print(headers[j])
                #print(len(cell.strip()), cell)
                if len(cell.strip()) > 0 and headers[j] in important and headers[j] not in row_dict.keys() :
                    row_dict[headers[j]] = cell
            data.append(row_dict.copy())
            #print(row_list[headers[57]])
        #if i > 5:
            #break
#pprint(data)
no_racers = len(data)
print("Nacteno {} zavodniku".format(no_racers))

# Ulozeni skol do slovniku spolu s jejich mesty
teams = {}
for x in data:
    if x['Název oddílu'] not in teams.keys():
        teams[x['Název oddílu']] = x['Město'] if 'Město' in x.keys() else ""
print("Nalezeno {} škol".format(len(teams.keys())))

# Ulozeni kategorii do seznamu
cats = []
for x in data:
    if x['Krátký'] not in cats:
        cats.append(x['Krátký'])
print("Nalezeno {} kategorii".format(len(cats)))

# Kategorie vcetne jejich obsazeni
team_num = {cat : [] for cat in cats} # vytvoreni prazdneho slovniku
for x in data:
    cat = x['Krátký']
    team = x['Název oddílu']
    if team not in team_num[cat]:
        team_num[cat].append(team)
#pprint(team_num)

# Zjisteni nejobsazenejsi kategorie
team_max = 0
max_cat = None
for x in team_num.keys():
    if len(team_num[x]) > team_max:
        team_max = len(team_num[x])
        max_cat = x
print("Maximum skol je v kategorii {}: {} skol".format(max_cat, team_max))

# Vypocet bodu u zavodniku
data = [x for x in data if x['Klasifikace'] == '0'] # vyhodit DISK zavodniky, uz nejsou potreba
for cat in cats:
    team_score = {t: 0 for t in teams.keys()}
    points = team_max*2
    for x in data:
        if x['Krátký'] == cat:
            if team_score[x['Název oddílu']] < 2:
                x['body'] = points
                team_score[x['Název oddílu']] += 1
                points -= 1
            else:
                x['body'] = 0
#pprint(data)

# Vypocet bodu u druzstev
hd3 = {}
hd5 = {}
hd79 = {}
hds = {}
for x in data:
    if x['Krátký'] == "D3" or x['Krátký'] == "H3":
        if x['Název oddílu'] in hd3.keys():
            hd3[x['Název oddílu']] += x['body']
        else:
            hd3[x['Název oddílu']] = x['body']
    elif x['Krátký'] == "D5" or x['Krátký'] == "H5":
        if x['Název oddílu'] in hd5.keys():
            hd5[x['Název oddílu']] += x['body']
        else:
            hd5[x['Název oddílu']] = x['body']
    elif x['Krátký'] == "D7" or x['Krátký'] == "H7" or x['Krátký'] == "D9" or x['Krátký'] == "H9":
        if x['Název oddílu'] in hd79.keys():
            hd79[x['Název oddílu']] += x['body']
        else:
            hd79[x['Název oddílu']] = x['body']
    elif x['Krátký'] == "DS" or x['Krátký'] == "HS":
        if x['Název oddílu'] in hds.keys():
            hds[x['Název oddílu']] += x['body']
        else:
            hds[x['Název oddílu']] = x['body']
    else:
        print("Neznámá kategorie {} u závodníka/ice {} {}".format(x['Krátký'], x['Jméno (křest.)'], x['Příjmení']))
pprint(hd3)
pprint(hd5)
pprint(hd79)
pprint(hds)

# Serazeni skol podle bodu
hd3i = sorted([(hd3[x], x) for x in hd3], reverse = True)
pprint(hd3i)
hd5i = sorted([(hd5[x], x) for x in hd5], reverse = True)
pprint(hd5i)
hd79i = sorted([(hd79[x], x) for x in hd79], reverse = True)
pprint(hd79i)
hdsi = sorted([(hds[x], x) for x in hds], reverse = True)
pprint(hdsi)

# Vypis vysledku do souboru
with open("vysledky_skoly.txt", 'w', encoding="utf-8") as fh:
    fh.write("{} závodníků\n{} škol\n{} kategorií\n".format(no_racers, len(teams.keys()), len(cats)))
    fh.write("Nejvíce škol v jedné kategorii je {} (kat. {})\n".format(team_max, max_cat))
    fh.write("\n==== D3 + H3 ====\n")
    printRes(hd3i)
    fh.write("\n==== D5 + H5 ====\n")
    printRes(hd5i)
    fh.write("\n==== D7 + H7 + D9 + H9 ====\n")
    printRes(hd79i)
    fh.write("\n==== DS + HS ====\n")
    printRes(hdsi)
print("\nVysledky preboru ulozeny do souboru \"vysledky_skoly.txt\"")
