#!/usr/bin/env python3

import os
from dotenv import load_dotenv
import requests
from requests_oauthlib import OAuth1
from quote_fetcher import get_random_verse

load_dotenv()

client_key = os.getenv("CLIENT_KEY")
client_secret = os.getenv("CLIENT_SECRET")
access_token = os.getenv("ACCESS_TOKEN")
access_token_secret = os.getenv("ACCESS_TOKEN_SECRET")

auth = OAuth1(
    client_key,
    client_secret,
    access_token,
    access_token_secret
)

X_BASE_URL = "https://api.twitter.com/2"
TWEET_ENDPOINT = f"{X_BASE_URL}/tweets"

def post_tweet(content):
    print("Posting tweet...")

    data = {"text": content}
    headers = {"Content-Type": "application/json"}
    response = requests.post(TWEET_ENDPOINT, auth=auth, json=data, headers=headers)

    if response.status_code == 201:
        print(f"Tweet posted: {content}")
    else:
        print(f"Error posting tweet: {response.status_code}, {response.text}")

# Runs with cron
def main():
    verse = get_random_verse()
    post_tweet(verse)

if __name__ == "__main__":
    main()
