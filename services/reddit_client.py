import os
import praw
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

reddit_client_id = os.getenv("REDDIT_CLIENT_ID")
reddit_client_secret = os.getenv("REDDIT_CLIENT_SECRET")
reddit_user_agent = os.getenv("REDDIT_USER_AGENT")

# Create a Reddit instance
reddit = praw.Reddit(
    client_id=reddit_client_id,
    client_secret=reddit_client_secret,
    user_agent=reddit_user_agent
)

# Function to fetch posts from Reddit
def fetch_posts(candidate: str, limit: int = 10):
    query = candidate
    subreddit = reddit.subreddit("all")
    posts = subreddit.search(query, limit=limit, sort='new')
    return posts