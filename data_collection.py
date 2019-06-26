"""

Author: Sourav Ghosh

"""

import requests
from bs4 import BeautifulSoup
import json
from lxml import html
import time


NOT_FOUND = 404

states = ['U0' + str(u) for u in range(1, 8)] + ['S0' + str(s) if s < 10 else 'S' + str(s) for s in range(1, 30)]

base_url = 'http://results.eci.gov.in/pc/en/constituencywise/Constituencywise'

results = list()

for state in states:
    for constituency_code in range(1, 99):
        url = base_url + state + str(constituency_code) + '.htm?ac=' + str(constituency_code)
        response = requests.get(url)

        if NOT_FOUND == response.status_code:
            break

        response_text = response.text
        soup = BeautifulSoup(response_text, 'lxml')
        tbodies = list(soup.find_all('tbody'))
        tbody = tbodies[10]
        trs = list(tbody.find_all('tr'))

        seat = dict()
        seat['candidates'] = list()
        for tr_index, tr in enumerate(trs):
            if tr_index == 0:
                state_and_constituency = tr.find('th').text.strip().split('-')
                seat['state'] = state_and_constituency[0].strip().lower()
                seat['constituency'] = state_and_constituency[1].strip().lower()
                continue

            if tr_index in [1, 2]:
                continue

            tds = list(tr.find_all('td'))

            candidate = dict()

            if tds[1].text.strip().lower() == 'total':
                seat['evm_total'] = int(tds[3].text.strip())
                if seat['state'] == 'jammu & kashmir':
                    seat['migrant_total'] = int(tds[4].text.strip())
                    seat['post_total'] = int(tds[5].text.strip())
                    seat['total'] = int(tds[6].text.strip())
                else:
                    seat['post_total'] = int(tds[4].text.strip())
                    seat['total'] = int(tds[5].text.strip())
                continue
            else:
                candidate['candidate_name'] = tds[1].text.strip().lower()
                candidate['paty_name'] = tds[2].text.strip().lower()
                candidate['evm_votes'] = int(tds[3].text.strip().lower())
                if seat['state'] == 'jammu & kashmir':
                    candidate['migrant_votes'] = int(tds[4].text.strip().lower())
                    candidate['post_votes'] = int(tds[5].text.strip().lower())
                    candidate['total_votes'] = int(tds[6].text.strip().lower())
                    candidate['share'] = float(tds[7].text.strip().lower())
                else:
                    candidate['post_votes'] = int(tds[4].text.strip().lower())
                    candidate['total_votes'] = int(tds[5].text.strip().lower())
                    candidate['share'] = float(tds[6].text.strip().lower())

            seat['candidates'].append(candidate)

    # print(json.dumps(seat, indent=2))
    results.append(seat)
    print("Collected data for", seat['state'], state, seat['constituency'], constituency_code, len(results))
    time.sleep(0.5)

with open("election_data.json", "a+") as f:
    f.write(json.dumps(results, indent=2))
