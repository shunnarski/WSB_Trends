import requests
import praw
import os
import secrets as s
import logging
import pandas as pd
import re
import ystockquote as ysq



def getTopWSBStocks():
    # Set up logging for debugging HTTP requests to the Reddit API
    if s.IS_DEBUG:
        handler = logging.StreamHandler()
        handler.setLevel(logging.DEBUG)
        for logger_name in ("praw", "prawcore"):
                logger = logging.getLogger(logger_name)
                logger.setLevel(logging.DEBUG)
                logger.addHandler(handler)

    try: 
        BASE_URL = 'https://www.reddit.com'
        SUBREDDIT = "wallstreetbets"

        reddit = praw.Reddit(
                user_agent=s.USER_AGENT,
                client_id=s.CLIENT_ID,
                client_secret=s.CLIENT_SECRET,
                username=s.USERNAME,
                password=s.PASSWORD
        )

        # Potential strategy:
        #
        #     Read the top 50 titles of wallstreetbets, parse those for tickers
        #
        #     Read the 10,000 most recent comments on wallstreetbets, scan for tickers and group them
        #
        #     Either take the top 10,000 comments or the comments from the top 50 posts

        subreddit = reddit.subreddit(SUBREDDIT).hot(limit=10)

        # Getting the top 200 comments
        comments = reddit.subreddit(SUBREDDIT).comments(limit=1000)


    except Exception as e:
        print("There was an issue connecting to the Reddit API...")
        raise e

    # extract the comments from the array and send to pandas dataframe
    comment_arr = [com.body.upper() for com in comments]

    # put all the individual words from the comments into an arr
    word_arr = []
    for com in comment_arr:
        words = com.split(" ")
        word_arr.extend(words)

    x = list(filter(lambda word: len(word) != 0 and word[0] == '$', word_arr))

    print(len(x))

    # only get words where length is 1-5 characters long
    pot_tickers = list(filter(lambda word: len(word) < 6, word_arr))

    # only get words with actual characters in them
    regex_pattern = "[A-Z]"
    pattern = re.compile(regex_pattern)
    pot_tickers = list(filter(lambda word: pattern.match(word), pot_tickers))

    # for each word, strip everything out except for letters
    pot_tickers = list(map(lambda word: re.sub(r'[^A-Z]', '', word), pot_tickers))

    print(len(pot_tickers))

    # create a dataframe with the stickers and count the number of times the word appears
    data = {"pot_tickers": pot_tickers}
    df = pd.DataFrame(data=data)

    # get the csv with the list of stock tickers that currently exist
    tickers_file = "nyse_ticks.csv"
    nyse_df = pd.read_csv(tickers_file)
    tickers_file = "nasdaq_ticks.csv"
    nasdaq_df = pd.read_csv(tickers_file)

    # concatenate the nyse and nasdaq stock tickers
    st_df = pd.concat([nyse_df, nasdaq_df])

    # Filter out stocks that don't have any sales
    st_df = st_df[st_df['Last Sale'].notnull()]

    # do an inner join on the ticker names so we are only left with legit stock tickers
    stock_tickers_wsb = pd.merge(left=df, right=st_df, left_on="pot_tickers", right_on="Symbol")['pot_tickers']

    # count up all the times the ticker appears in the dataframe
    vc_df = stock_tickers_wsb.value_counts(sort=True)

    return vc_df.to_json()

    
