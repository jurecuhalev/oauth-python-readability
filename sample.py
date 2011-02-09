from oauthreadability import OAuthApi

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


# access_token = {'oauth_token': '',
#                 'oauth_token_secret': ''}

# # Do a test API call using our new credentials

readability = OAuthApi(consumer_key, consumer_secret, access_token['oauth_token'], access_token['oauth_token_secret'])

print readability.getBookmarks()
print readability.addBookmark(url='http://blog.arc90.com/2010/11/30/silence-is-golden/')
