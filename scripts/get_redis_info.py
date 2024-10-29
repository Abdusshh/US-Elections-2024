from upstash_redis import Redis
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
redis_client = Redis.from_env()

CANDIDATES = ["Kamala Harris", "Donald Trump"]

# We have a set, sorted set and a list for posts for each candidate
# Set is called candidate:posts, sorted set is called candidate:post_order and list is called candidate:scores
# We will get the number of posts, scores and posts in order for each candidate

def get_redis_info():
    for candidate in CANDIDATES:
        post_count = redis_client.scard(f"{candidate}:posts")
        post_order_count = redis_client.zcard(f"{candidate}:post_order")
        score_count = redis_client.llen(f"{candidate}:scores")
        print(f"Number of posts for {candidate}: {post_count}")
        print(f"Number of scores for {candidate}: {score_count}")
        print(f"Number of posts in order for {candidate}: {post_order_count}")

if __name__ == "__main__":
    get_redis_info()