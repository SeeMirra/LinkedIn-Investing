from linkedin import LinkedinAPI
from pprint import pprint as pp

l = LinkedinAPI(api_key = 'ghxn2rzq9hdi',
              api_secret = 'TaYCyB20AXb0t5o0',
              oauth_token='1fe3c246-9ddd-4ee2-8b55-3f77bee60a4e',
              oauth_token_secret='62d59740-8aec-420f-8068-a31c904c63f8')


# Get search results
search = l.get('people-search', 
     fields='people:(id,first-name,last-name),num-results', 
     params={'company-name':'Amp Idea Corp',
       'current-companty': False, 
       'scope': 'r_fullprofile'})
pp(search)
