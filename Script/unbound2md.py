import re
import fileinput
import os
import csv
import markdownify



lsg = Bible("Louis Segond","french_lsg","LSG",False,True)
pes = Bible("Peshitta","peshitta","PST",False,True)
vul = Bible("Vulgata Clementina","latin_vulgata_clementina","VG",True,False)
novVul = Bible("Nova Vulgata","latin_nova_vulgata","NVG",True,True)
hebrew = Bible("Hebrew BHS accents","hebrew_bhs_vowels","BHS",True,True)
lxx = Bible("Septante accentuée","lxx_a_accents","LXX",True,False)
wlc = Bible("Hebrew WLC","wlc","WLC",True,True)
#web = Bible("English WEB","web","WEB",True,True)

