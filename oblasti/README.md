# oblasti
Program pro výpočet výsledků přeboru (mistrovství) oblasti

Automaticky pomocí seznamu klubů v oblasti z výsledků vypustí všechny závodníky mimo soutěžní oblast
Program pracuje s výsledky ve formátu ČSOS (.txt) -- export z ORISu

## Použití
1. Nainstalovat Python verze 3 nebo vyšší (https://www.python.org/), při instalaci zaškrtnout možnost "Add Python 3.x to PATH"
2. Z ORISu exportovat výsledky do formátu ČSOS
3. (Pro jednoduchost stáhnout soubor prebor_oblasti.py do stejné složky s výsledky)
4. Vytvořit soubor **clubs_include.txt** se seznamem klubů v oblasti. Každý klub na nový řádek, nejlépe vypsat jen zkratky.
5. Spustit příkazovou řádku ve složce se souborem **prebor_oblasti.py**
6. Příkazem ```prebor_skol.py -f "cesta/k/souboru/s/vysledky.txt"``` spustit program
7. Pokud je vše ok, vytvoří se ve složce s programem soubor **vysledky_preboru.txt**
