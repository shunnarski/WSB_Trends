import requests
import praw

reddit = praw.Reddit(
    client_id='DfqePo7ZMhlddA',
    client_secret='mXKFSAo-SgdAPj7mg2QsPl1SeDRQiA',
    user_agent='MyBot/0.0.1'
)

for submission in reddit.subreddit("wallstreetbets").hot(limit=10):
    print(submission.title)

base_url = 'https://www.reddit.com/'

# note that CLIENT_ID refers to 'personal use script' and SECRET_TOKEN to 'token'
auth = requests.auth.HTTPBasicAuth('DfqePo7ZMhlddA', 'mXKFSAo-SgdAPj7mg2QsPl1SeDRQiA')

# here we pass our login method (password), username, and password
data = {'grant_type': 'password',
        'username': 'checkTheLeaderboard',
        'password': 'MMl678CK1u$V'}

# setup our header info, which gives reddit a brief description of our app
headers = {'User-Agent': 'MyBot/0.0.1'}

# send our request for an OAuth token
res = requests.post(base_url + 'api/v1/access_token',
                    auth=auth, data=data, headers=headers)

# convert response to JSON and pull access_token value
TOKEN = res.json()['access_token']

# add authorization to our headers dictionary
headers = {**headers, **{'Authorization': f"bearer {TOKEN}"}}

base_url = 'https://oauth.reddit.com'

response = requests.get(base_url + '/r/wallstreetbets/about/rules', headers=headers)

#if response.status_code == 200:
    #print(response.json())

