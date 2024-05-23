"""
Author: Luciano Garbarino
Description: This script collects the top posts of the day from the "pickleball" subreddit and their respective comments,
             saving them into Excel files. It handles rate limiting and ensures the results directory is cleaned up before each run.
"""

import os
import praw
from functions import get_todays_posts, get_comments
from prawcore.exceptions import TooManyRequests
import shutil
from time import sleep
from settings import CLIENT_ID, CLIENT_SECRET, USER_AGENT, RATE_LIMIT, TARGET_SUBREDDIT

# Define the directory paths
module_dir = os.path.dirname(__file__)
results_dir = os.path.join(module_dir, 'results')

# Delete the results directory if it exists to avoid overlapping data
if os.path.exists(results_dir):
    print("Deleting existing results directory.")
    shutil.rmtree(results_dir)

# Create the results and comments directories
os.makedirs(results_dir)
comments_dir = os.path.join(results_dir, 'comments')
os.makedirs(comments_dir)

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
    # Get the subreddit instance
    subreddit = reddit.subreddit(TARGET_SUBREDDIT)

    # Get today's top posts
    todays_posts_df = get_todays_posts(subreddit)

    # Save the posts to an Excel file
    posts_excel_path = os.path.join(results_dir, 'posts.xlsx')
    todays_posts_df.to_excel(posts_excel_path, index=False)

    # Iterate through each post and save its comments to an individual Excel file
    for post_id in todays_posts_df['id']:
        comments_excel_path = os.path.join(comments_dir, f'{post_id}.xlsx')
        post = reddit.submission(id=post_id)
        comments_df = get_comments(post)
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
