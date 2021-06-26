# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
# @author jmacura 2021
import sys

# Parse command line params
usage = """Pouziti: prebor_oblasti.py -f "soubor.txt [-c seznam_oddilu.txt] [-o soubor_s_vysledky.txt]"
Moznosti:
  -f "export_csos_6281.txt"  Cesta k souboru s vysledky (format CSOS)
  -c "clubs_include.txt"  Cesta k souboru se seznamem klubu oblasti. Kazdy radek = jedna zkratka klubu
  -o "vysledky_preboru.txt"  Nazev souboru s vypoctenymi vysledky preboru
"""

# Global vars
clubsFileName = './clubs_include.txt'
resultsFileName = ''
outFileName = './vysledky_preboru.txt'
clubs = []
isHeadRead = False

# Read cmd input
if len(sys.argv) == 3 and str(sys.argv[1]) == '-f':
	resultsFileName = sys.argv[2]
elif len(sys.argv) == 5 and str(sys.argv[1]) == '-f' and str(sys.argv[3]) == '-c':
	resultsFileName = sys.argv[2]
	clubsFileName = sys.argv[4]
elif len(sys.argv) == 5 and str(sys.argv[1]) == '-f' and str(sys.argv[3]) == '-o':
	resultsFileName = sys.argv[2]
	outFileName = sys.argv[4]
elif len(sys.argv) == 7 and str(sys.argv[1]) == '-f' and str(sys.argv[3]) == '-c' and str(sys.argv[5]) == '-o':
	resultsFileName = sys.argv[2]
	clubsFileName = sys.argv[4]
	outFileName = sys.argv[6]
elif len(sys.argv) == 7 and str(sys.argv[1]) == '-f' and str(sys.argv[3]) == '-o' and str(sys.argv[5]) == '-c':
	resultsFileName = sys.argv[2]
	outFileName = sys.argv[4]
	clubsFileName = sys.argv[6]
else:
	print(usage)
	quit()

# Read club_list_input
with open(clubsFileName) as fh:
	for row in fh:
		clubs.append(row.strip())

out = open(outFileName, "w", encoding="utf-8")

# Parse results and do the job
with open(resultsFileName) as fh:
	for row in fh:
		if not isHeadRead:
			out.write(row)
			if row.startswith('-----'):
				isHeadRead = True
		elif any(club in row for club in clubs):
			out.write(row)
		else: pass

print('Done!')
print('Vysledky ulozeny do souboru {}'.format(outFileName))
