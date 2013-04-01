from linkedin import LinkedinAPI
#from pprint import pprint as pp
#import json

class LinkedIn:
        def __init__(self, api_key, api_secret,
                     oauth_token=None, oauth_token_secret=None):
        if not oauth_token or not oauth_token_secret:
            tokens = self.get_oauth2_tokens(api_key,
    									    api_secret)
            oauth_token = tokens['oauth_token']
            oauth_token_secret = tokens['oauth_token_secret']

        self.liAPI = LinkedinAPI(api_key,
                                 api_secret,
                                 oauth_token,
                                 oauth_token_secret)

    def my_network_updates(self):
        return self.liAPI.get('people/~/network/network-stats')
    
    def get_oauth2_tokens(self, api_key, api_secret):
        lo = LinkedinAPI(api_key,
                         api_secret,
                         callback_url=None)

        return lo.get_authentication_tokens()

if __name__ == '__main__':
    # Praful Account
    api_key = 'za1xifvosj7p'
    api_secret = 'HhaxCgXUsyrehODw'
    oauth_token = '1dddc1d6-6585-4314-9195-dda3edea33c4'
    oauth_token_secret = '11156d45-6555-4d64-9f78-3921fbdb9ffa'
    
    liObj = LinkedIn(api_key, api_secret, oauth_token, oauth_token_secret)
    print liObj.my_network_updates()

# Get search results
"""
while(True):
  try:
    company_domain = raw_input("Company domain (stop to quit): ")
    if company_domain == "stop":
      break
    companies_search = l.get('companies', params={'email-domain' : company_domain })
    print companies_search

##    for company_search in companies_search['values']:
##      print company_search['name']
##      company_id = company_search['id']
##
##      company_person_updates = l.get('companies/%d/updates' %(company_id),
##           #fields='update-content:(company-person-update:(person:(id)))',
##           params={'event-type': 'position-change',
##                   #'event-type': 'new-hire',
##                   'start': 0,
##                   'count': 500}
##          )
##
##      print "Company Updates: ", len(company_person_updates)
##      sys.stdin.read(1)
##
##      if company_person_updates.has_key('values'):
##        values = company_person_updates['values']
##        for update in values:
##          pp(update)
##          print '--------------------'
##          sys.stdin.read(1)
  except:
    pass
"""
