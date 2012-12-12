# Imports
import requests
import traceback
#import sys

from bs4 import BeautifulSoup
from linkedin import LinkedinAPI
from urlparse import urlparse
from datetime import datetime

# LinkedIn Constants
"""
# Praful Mathur
API_KEY = 'ghxn2rzq9hdi'
API_SECRET = 'TaYCyB20AXb0t5o0'
OAUTH_TOKEN = '1fe3c246-9ddd-4ee2-8b55-3f77bee60a4e'
OAUTH_TOKEN_SECRET = '62d59740-8aec-420f-8068-a31c904c63f8'
"""

# Joe Startup
"""
API_KEY = '29bsmtimu742'
API_SECRET = 'VHAKjMM3HpXHCgsm'
OAUTH_TOKEN = '5aa7807e-ad2e-4360-99ec-f3bf3ed5cf56'
OAUTH_TOKEN_SECRET = '317facaf-374f-4c87-a984-4a0c3ea95fbc'
"""

API_KEY = 'yx5n43kkh749'
API_SECRET = 'kT8leTdqx2QUMsAW'
OAUTH_TOKEN = '973e6614-28ec-49a8-ab76-98d4078d0392'
OAUTH_TOKEN_SECRET = '647afa78-ae06-4ce7-ab55-3d7d38fb6568'

li = LinkedinAPI(api_key = API_KEY,
        api_secret = API_SECRET,
        oauth_token= OAUTH_TOKEN,
        oauth_token_secret=OAUTH_TOKEN_SECRET,)

seen_domains = []

def xpath_get(mydict, path):
    elem = mydict

    try:
        for x in path.strip("/").split("/"):
            elem = elem.get(x)
    except:
        pass

    return elem


def get_co_industry(company_id):
    company_profile = li.get("companies/%d" %(company_id), fields='industries')
    company_industries = xpath_get(company_profile, '/industries/values')
    company_industry = xpath_get(company_industries[0], '/code')

    return company_industry

EXCHANGE = 'NASDAQ'
print 'Reading all %s companies' %(EXCHANGE)
f = open('%s_company_list.txt' %(EXCHANGE.lower()), 'r')
for sq in f.readlines():
    print "Requesting link for stock quote -- %s" %(sq)
    r = requests.get("http://finance.google.com?q=%s" %(sq))

    print "Got Data!"
    data = r.content

    print "Converting to soup"
    soup = BeautifulSoup(data)

    print "Find me company domain!"
    try:
        link = soup.find(id="fs-chome").getText().strip('\n').lower()
        link = urlparse(link).hostname
        company_domain = link.replace('www.','')
        if(company_domain in seen_domains):
            print 'Seen domain before...'
            continue
        seen_domains.append(company_domain)
        print 'Found company domain: %s' %(company_domain)
    except:
        print "ERROR on stock quote: %s" %(sq)
        continue

    try:
        print 'Does this exist on LinkedIn?'
        companies_search = li.get('companies', params={'email-domain' : company_domain })
        print 'Exists on LinkedIn!'

        for company_search in companies_search['values']:
            company_id = company_search['id']

            try:
                company_person_updates = li.get('companies/%d/updates' %(company_id),
                    # fields='update-content:(company-person-update:(person:(id)))',
                    params={'event-type': 'position-change',
                            'event-type': 'new-hire',
                            'start': 0,
                            'count': 500})
            except:
                print traceback.format_exc()
                f = open('nasdaq_links.err', 'a')
                f.write('Company Domain: %s\n' %(company_domain))
                f.write('Company Search: %s\n' %(company_search))
                f.write('Error:\n%s\n' %(traceback.format_exc()))
                f.write('-------------\n')
                f.close()

            if not company_person_updates.has_key('values'):
                continue

            values = company_person_updates['values']
            for update in values:
                company_person_update = xpath_get(update, '/updateContent/companyPersonUpdate')
                new_position = xpath_get(company_person_update, '/newPosition')
                old_position = xpath_get(company_person_update, '/oldPosition')

                db_profile_id = xpath_get(company_person_update, '/person/id')

                db_to_company_id = xpath_get(new_position, '/company/id')
                db_to_company_name = xpath_get(new_position, '/company/name')
                db_to_company_position = xpath_get(new_position, '/title')
                db_to_company_industry = get_co_industry(db_to_company_id)

                db_from_company_id = xpath_get(old_position, '/company/id') or 'NULL'
                db_from_company_name = 'NULL'
                db_from_company_position = 'NULL'
                db_from_company_industry = 'NULL'
                db_joined_date = 'NULL'

                if(not db_from_company_id == 'NULL'):
                    db_from_company_name = xpath_get(old_position, '/company/name')
                    db_from_company_position = xpath_get(old_position, '/title')
                    db_from_company_industry = get_co_industry(db_from_company_id)

                    try:
                        profile = li.get("people/%s" %(db_profile_id), fields='positions')
                        positions = xpath_get(profile, '/positions/values/')[0]
                        start_date = xpath_get(positions, '/startDate')
                        db_joined_date = datetime(start_date['year'], start_date['month'], 1)
                        db_joined_date = db_joined_date.strftime('%Y-%m-%d')
                    except:
                        print traceback.format_exc()
                        f = open('nasdaq_links.err', 'a')
                        f.write('Company Domain: %s\n' %(company_domain))
                        f.write('Company Search: %s\n' %(company_search))
                        f.write('Person ID: %s\n' %(db_profile_id))
                        f.write('Error:\n%s\n' %(traceback.format_exc()))
                        f.write('-------------\n')
                        f.close()

                # Assume first of month - LinkedIn only provides month/year
                sql_value = (db_profile_id,
                        db_to_company_id, db_to_company_name, db_to_company_position, db_to_company_industry,
                        db_from_company_id, db_from_company_name, db_from_company_position, db_from_company_industry,
                        db_joined_date)

                print 'Writing SQL'
                o = open('nasdaq_linkedin_data.sql', 'a')
                o.write(str(sql_value))
                o.write('\n')
                o.close()
                print 'Finished'

                print '-----------------'
                print

    except:
        print traceback.format_exc()
        f = open('nasdaq_links.err', 'a')
        f.write('Company Domain: %s\n' %(company_domain))
        f.write('Company Search: %s\n' %(company_search))
        f.write('Error:\n%s\n' %(traceback.format_exc()))
        f.write('-------------\n')
        f.close()
        #sys.stdin.read(1)

f.close()
