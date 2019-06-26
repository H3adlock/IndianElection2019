"""

Author: Sourav Ghosh

"""

import requests
from bs4 import BeautifulSoup
import json
from lxml import html
import time


NOT_FOUND = 404

states = ['U0' + str(u) for u in range(1,8)] + ['S0' + str(s) if s<10 else 'S' + str(s) for s in range (1,30)]

base_url = 'http://results.eci.gov.in/pc/en/constituencywise/Constituencywise'

results = list()

for state in  states:
    for constituency_code in range(1,99):
    url = base_url +  state + str(constituency_code) + '.htm?ac=' + str(constituency_code)
