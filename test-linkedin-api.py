"""
Brad account
API_KEY = 'ko0u7ep77k3k'
API_SECRET = 'R6ZxOytLHoVNovC4'
OAUTH_TOKEN = '40e92a9b-454b-489b-8ff3-9e0a1e059c73'
OAUTH_TOKEN_SECRET = 'ebcf877e-6767-48ef-a90c-2d4d676f6912'
"""

# Praful Account
API_KEY = 'ghxn2rzq9hdi'
API_SECRET = 'TaYCyB20AXb0t5o0'
OAUTH_TOKEN = '1fe3c246-9ddd-4ee2-8b55-3f77bee60a4e'
OAUTH_TOKEN_SECRET = '62d59740-8aec-420f-8068-a31c904c63f8'

from linkedin import LinkedinAPI
from pprint import pprint as pp
import sys

l = LinkedinAPI(api_key = API_KEY,
              api_secret = API_SECRET,
              oauth_token= OAUTH_TOKEN,
              oauth_token_secret=OAUTH_TOKEN_SECRET,)


# Get search results
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
