"""
Author: Luciano Garbarino
Description: This script collects the top posts of the day from the selected subreddit and their respective comments,
             saving them into Excel files. It handles rate limiting and ensures the results directory is cleaned up before each run.
"""

import pandas as pd
import os
import praw
from functions import get_todays_posts, get_comments
from prawcore.exceptions import TooManyRequests
from time import sleep
from settings import CLIENT_ID, CLIENT_SECRET, USER_AGENT, RATE_LIMIT, TARGET_SUBREDDIT

# Define the directory paths
module_dir = os.path.dirname(__file__)
results_dir = os.path.join(module_dir, 'results')

# Create the results directory if it does not exist
if not os.path.exists(results_dir):
    os.makedirs(results_dir)

# Define the path to the Excel file that will store the top posts of the day
posts_excel_path = os.path.join(results_dir, 'posts.xlsx')
if os.path.exists(posts_excel_path):
    posts_df = pd.read_excel(posts_excel_path)
else:
    posts_df = None

# Define the path to the Excel file that will store the comments
comments_excel_path = os.path.join(results_dir, 'comments.xlsx')
if os.path.exists(comments_excel_path):
    comments_df = pd.read_excel(comments_excel_path)
else:
    comments_df = None

# Initialize the Reddit instance with the provided credentials and rate limit settings
reddit = praw.Reddit(
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    user_agent=USER_AGENT,
    ratelimit_seconds=RATE_LIMIT
)

def main():
    """
    Main function to collect the top posts of the day and their comments.
    """
    global posts_df
    global comments_df

    # Get the subreddit instance
    subreddit = reddit.subreddit(TARGET_SUBREDDIT)

    # Get today's top posts
    todays_posts_df = get_todays_posts(subreddit)

    if posts_df is None:
        posts_df = todays_posts_df
    else:
        # Append the new posts to the existing posts DataFrame
        posts_df = pd.concat([posts_df, todays_posts_df], ignore_index=True)
        # Drop duplicates based on the 'id' column, keeping the last using "created_utc" as a tiebreaker
        posts_df = posts_df.sort_values(['id', 'created_utc']).drop_duplicates('id', keep='last')

    # Save the updated posts DataFrame to the Excel file
    posts_df.to_excel(posts_excel_path, index=False)
    
    # Iterate through each post and save its comments to the comments DataFrame
    for post_id in todays_posts_df['id']:
        post = reddit.submission(id=post_id)
        todays_comments_df = get_comments(post)
        if comments_df is None:
            comments_df = todays_comments_df
        else:
            # Append the new comments to the existing comments DataFrame
            comments_df = pd.concat([comments_df, todays_comments_df], ignore_index=True)
            # Drop duplicates based on the 'id' column, keeping the last using "created_utc" as a tiebreaker
            comments_df = comments_df.sort_values(['id', 'created_utc']).drop_duplicates('id', keep='last')

    # Save the updated comments DataFrame to the Excel file
    comments_df.to_excel(comments_excel_path, index=False)

# Attempt to run the main function, handling rate limit exceptions gracefully
while True:
    try:
        main()
        break  # Exit the loop if the main function completes successfully
    except TooManyRequests as e:
        # Handle rate limit exceptions by sleeping for the required time before retrying
        print(f"Rate limit exceeded. Please wait {e.retry_after} seconds before re-trying this request.")
        print(f"Sleeping for {int(e.retry_after) * 2} seconds and then re-trying.")
        sleep(int(e.retry_after) * 2)
