import requests
import praw
import os
import secrets as s
import logging

# Set up logging for debugging HTTP requests to the Reddit API
if s.IS_DEBUG:
        handler = logging.StreamHandler()
        handler.setLevel(logging.DEBUG)
        for logger_name in ("praw", "prawcore"):
                logger = logging.getLogger(logger_name)
                logger.setLevel(logging.DEBUG)
                logger.addHandler(handler)



BASE_URL = 'https://www.reddit.com'

reddit = praw.Reddit(
        user_agent=s.USER_AGENT,
        client_id=s.CLIENT_ID,
        client_secret=s.CLIENT_SECRET,
        username=s.USERNAME,
        password=s.PASSWORD
)


endpoint = "/user/moneymay195/comments"
url = BASE_URL + endpoint
submission = reddit.submission(url=url)

print("SUCCESS")

# note that CLIENT_ID refers to 'personal use script' and SECRET_TOKEN to 'token'
# auth = requests.auth.HTTPBasicAuth(s.CLIENT_ID, s.CLIENT_SECRET)

# # here we pass our login method (password), username, and password
# data = {'grant_type': 'password',
#         'user_agent': s.USER_AGENT,
#         'username': s.USERNAME,
#         'password': s.PASSWORD, 
#         'client_id': s.CLIENT_ID,
#         'client_secret': s.CLIENT_SECRET}

# # setup our header info, which gives reddit a brief description of our app
# headers = {'User-Agent': s.USER_AGENT}

# # send our request for an OAuth token
# res = requests.post(base_url + 'api/v1/access_token',
#                     auth=auth, data=data, headers=headers)

# # convert response to JSON and pull access_token value
# TOKEN = res.json()['access_token']

# # add authorization to our headers dictionary
# headers = {**headers, **{'Authorization': f"bearer {TOKEN}"}}

# base_url = 'https://oauth.reddit.com'

# response = requests.get(base_url + '/api/v1/me', headers=headers)

# if response.status_code == 200:
#     print(response.json()['name'], response.json()['comment_karma'])

