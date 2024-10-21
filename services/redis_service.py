from upstash_redis import Redis
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
redis_client = Redis.from_env()

def store_post(candidate: str, title: str, url: str, score: float):
    key = f"{candidate}:{title}"
    data = {"title": title, "url": url, "score": score}
    redis_client.hset(key, values=data)
    # store all post keys in a list without duplicates
    redis_client.lpush(f"{candidate}:posts", key)

def store_score(candidate: str, title: str, score: float):
    key = f"{candidate}:{title}"
    redis_client.hset(key, "score", score)

def get_all_posts(candidate: str):
    keys = redis_client.lrange(f"{candidate}:posts", 0, -1)
    posts = []
    for key in keys:
        post = redis_client.hgetall(key)
        posts.append(post)
    return posts

def get_recent_posts(candidate: str, limit: int):
    keys = redis_client.lrange(f"{candidate}:posts", 0, limit - 1)
    posts = []
    for key in keys:
        post = redis_client.hgetall(key)
        posts.append(post)
    return posts

