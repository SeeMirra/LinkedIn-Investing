# Praful Account
API_KEY = 'ghxn2rzq9hdi'
API_SECRET = 'TaYCyB20AXb0t5o0'
OAUTH_TOKEN = '488161fe-28c7-4bd7-8be0-41163a4a77fe'
OAUTH_TOKEN_SECRET = '4b347a52-a4b2-4298-8dd8-5f4875d414fa'

from linkedin import LinkedinAPI
from pprint import pprint as pp
import json


l = LinkedinAPI(api_key=API_KEY,
        api_secret=API_SECRET,
        oauth_token=OAUTH_TOKEN,
        oauth_token_secret=OAUTH_TOKEN_SECRET,)


# Get network updates
my_network_updates = l.get('people/~/network/network-stats')
print json.dumps(my_network_updates, indent=4)

lo = LinkedinAPI(api_key=API_KEY,
        api_secret=API_SECRET,
        callback_url=None)

oauth_tokens = lo.get_authentication_tokens()
pp(oauth_tokens)


# Get search results
"""
while(True):
  try:
    company_domain = raw_input("Company domain: ")
    companies_search = l.get('companies', params={'email-domain' : company_domain })
    print companies_search

    for company_search in companies_search['values']:
      print company_search['name']
      company_id = company_search['id']

      company_person_updates = l.get('companies/%d/updates' %(company_id),
           #fields='update-content:(company-person-update:(person:(id)))',
           params={'event-type': 'position-change',
                   #'event-type': 'new-hire',
                   'start': 0,
                   'count': 500}
          )

      print "Company Updates: ", len(company_person_updates)
      sys.stdin.read(1)

      if company_person_updates.has_key('values'):
        values = company_person_updates['values']
        for update in values:
          pp(update)
          print '--------------------'
          sys.stdin.read(1)
  except:
    pass
"""
