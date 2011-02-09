#!/usr/bin/env python
# 
# Copyright under  the latest Apache License 2.0

'''

Based on code that Konpaku Kogasa used to create code.google.com/p/oauth-python-twitter2/

Requires:
  simplejson
  oauth2
'''

__author__ = "Jure Cuhalev, Konpaku Kogasa, Hameedullah Khan"
__version__ = "0.1"

# Library modules
import urllib
import urllib2
import urlparse
import time

# Non library modules
import simplejson
import oauth2

# Taken from oauth implementation at: http://github.com/harperreed/twitteroauth-python/tree/master
REQUEST_TOKEN_URL = 'https://www.readability.com/api/rest/v1/oauth/request_token/'
ACCESS_TOKEN_URL = 'https://www.readability.com/api/rest/v1/oauth/access_token/'
AUTHORIZATION_URL = 'https://www.readability.com/api/rest/v1/oauth/authorize/'

class OAuthApi():
    def __init__(self, consumer_key, consumer_secret, token=None, token_secret=None):
      if token and token_secret:
        token = oauth2.Token(token, token_secret)
      else:
        token = None

      self._Consumer = oauth2.Consumer(consumer_key, consumer_secret)
      #self._signature_method = oauth2.SignatureMethod_PLAINTEXT()
      self._access_token = token 

    def _FetchUrl(self,url, http_method=None,parameters=None):
        client = oauth2.Client(self._Consumer, self._access_token)

        if http_method == 'POST':
            body = urllib.urlencode(parameters)
            return client.request(url, method=http_method, body=body)
        else:
            return client.request(url, method=http_method)    

    def getAuthorizationURL(self, token, url=AUTHORIZATION_URL):
        '''Create a signed authorization URL
        
        Returns:
          A signed OAuthRequest authorization URL 
        '''
        return "%s?oauth_token=%s" % (url, token['oauth_token'])

    def getRequestToken(self, url=REQUEST_TOKEN_URL):
        '''Get a Request Token from Twitter
        
        Returns:
          A OAuthToken object containing a request token
        '''
        resp, content = oauth2.Client(self._Consumer).request(url, "GET")

        if resp['status'] != '200':
            raise Exception("Invalid response %s." % resp['status'])

        return dict(urlparse.parse_qsl(content))
    
    def getAccessToken(self, token, verifier, url=ACCESS_TOKEN_URL):
        '''Get a Request Token from Twitter
        
        Returns:
          A OAuthToken object containing a request token
        '''
        token = oauth2.Token(token['oauth_token'], token['oauth_token_secret'])
        token.set_verifier(verifier)
        client = oauth2.Client(self._Consumer, token)
        
        resp, content = client.request(url, "POST")
        return dict(urlparse.parse_qsl(content))
    


    def addBookmark(self, url, favorite=0, archive=0, options={}):
        '''Add a bookmark. Returns 202 Accepted, meaning that the bookmark has been added 
        but no guarantees are made as to whether the article proper has yet been parsed.
        '''
        options['url'] = url

        resp, content = self.ApiCall('bookmarks', 'POST', options)

        if resp.get('status') == '409':
          raise Exception("409 Conflict/Duplicate - %s" % url)
        elif resp.get('status') == '202':
          return {'x-article-location': resp.get('x-article-location'),
                  'location': resp.get('location')}

    def getBookmarks(self, options={}):
        return simplejson.loads(self.ApiCall('bookmarks', 'GET', options)[1])

    def getSubresources(self, options={}):
        return self.ApiCall('', 'GET', options)

    
    def ApiCall(self, call, type="GET", parameters={}):
        '''Calls the twitter API
        
       Args:
          call: The name of the api call (ie. account/rate_limit_status)
          type: One of "GET" or "POST"
          parameters: Parameters to pass to the Readability API call
        Returns:
          Returns the twitter.User object
        '''
        response = self._FetchUrl("https://www.readability.com/api/rest/v1/%s/" % call, type, parameters)
        return response
        
