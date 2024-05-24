import pandas as pd
import pytz

def get_todays_posts(subreddit) -> pd.DataFrame:
    """
    Retrieves the top posts of the day from the given subreddit.

    Args:
        subreddit: A PRAW subreddit instance.

    Returns:
        pd.DataFrame: A DataFrame containing the top posts of the day with columns for post ID, title, selftext, score, author,
                      number of comments, URL, and creation time (converted to datetime).
    """
    posts = []
    # Iterate through the top posts of the day
    for post in subreddit.top("day", limit=None):
        posts.append([
            post.id, post.title, post.subreddit, post.selftext, post.score, post.author,
            post.num_comments, post.url, post.created_utc
        ])
    
    # Create a DataFrame from the collected post data
    df = pd.DataFrame(posts, columns=[
        "id", "title", "subreddit", "selftext", "score", "author",
        "num_comments", "url", "created_utc"
    ])
    
    # Convert the created_utc column to datetime
    df['created_utc'] = pd.to_datetime(df['created_utc'], unit='s')
    
    # Convert the datetime to Central Time
    central = pytz.timezone('US/Central')
    df['created_central'] = df['created_utc'].dt.tz_localize(pytz.utc).dt.tz_convert(central)
    
    print(df.head())
    return df

def get_comments(post) -> pd.DataFrame:
    """
    Retrieves all comments from the given Reddit post.
    Args:
        post: A PRAW submission instance representing a Reddit post.
    Returns:
        pd.DataFrame: A DataFrame containing the comments with columns for comment ID, body, score, author, parent ID,
                      and creation time (converted to datetime).
    """
    comments = []
    # Ensure all comments are loaded
    post.comments.replace_more(limit=None)
    
    # Iterate through all comments in the post
    for comment in post.comments.list():
        comments.append([
            comment.id, comment.subreddit, comment.body, comment.score, comment.author,
            comment.parent_id, comment.created_utc
        ])
    
    # Create a DataFrame from the collected comment data
    df = pd.DataFrame(comments, columns=[
        "id", "subreddit", "body", "score", "author", "parent_id", "created_utc"
    ])
    
    # Convert the created_utc column to datetime
    df['created_utc'] = pd.to_datetime(df['created_utc'], unit='s')
    
    # Convert the datetime to Central Time
    central = pytz.timezone('US/Central')
    df['created_central'] = df['created_utc'].dt.tz_localize(pytz.utc).dt.tz_convert(central)

    return df
