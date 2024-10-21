from upstash_redis import Redis
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
redis_client = Redis.from_env()

def store_post(candidate: str, title: str, url: str, score: float):
    key = f"{candidate}:{title}"
    data = {"title": title, "url": url, "score": score}
    redis_client.hset(key, values=data)
    redis_client.lpush(f"{candidate}:posts", key)
    # Keep only the latest 1000 posts
    redis_client.ltrim(f"{candidate}:posts", 0, 999)

def get_posts(candidate: str):
    # Get 10 latest posts
    keys = redis_client.lrange(f"{candidate}:posts", 0, 9)
    posts = []
    for key in keys:
        post = redis_client.hgetall(key)
        posts.append(post)
    return posts

def get_post(candidate: str, title: str):
    key = f"{candidate}:{title}"
    post = redis_client.hgetall(key)
    return post

def store_score(candidate: str, title: str, score: float):
    key = f"{candidate}:{title}"
    redis_client.hset(key, "score", score)
