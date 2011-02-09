from oauth import oauth
from oauthreadability import OAuthApi
import pprint

consumer_key = ""
consumer_secret = ""
 
readability = OAuthApi(consumer_key, consumer_secret)

# Get the temporary credentials for our next few calls
temp_credentials = readability.getRequestToken()

# User pastes this into their browser to bring back a pin number
print(readability.getAuthorizationURL(temp_credentials))

# Get the pin # from the user and get our permanent credentials
oauth_verifier = raw_input('What is the PIN? ')
access_token = readability.getAccessToken(temp_credentials, oauth_verifier)

print("oauth_token: " + access_token['oauth_token'])
print("oauth_token_secret: " + access_token['oauth_token_secret'])

# access_token = {'oauth_token': 'sjKcmqbm4N5jShge83',
#                 'oauth_token_secret': 'W8s4vhT25LBZh5y5yvbxRH96CrRZ69b6'}

# # Do a test API call using our new credentials

readability = OAuthApi(consumer_key, consumer_secret, access_token['oauth_token'], access_token['oauth_token_secret'])


#print readability.getSubresources()
print readability.getBookmarks()

#print readability.addBookmark('http://tech.slashdot.org/story/11/02/09/1820253/MPAA-Threatens-To-Disconnect-Google-From-Internet')