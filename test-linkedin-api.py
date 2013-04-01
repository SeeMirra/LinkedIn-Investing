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
    api_key = ''
    api_secret = ''
    oauth_token = ''
    oauth_token_secret = ''

    liObj = LinkedIn(api_key, api_secret, oauth_token, oauth_token_secret)
    print liObj.my_network_updates()
