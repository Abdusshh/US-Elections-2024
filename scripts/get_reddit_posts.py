# A script to fetch posts from Reddit and fill our Redis store
from services.reddit_client import fetch_posts
from services.qstash_service import publish_message_to_qstash

CANDIDATES = ["Donald Trump", "Kamala Harris"]

for candidate in CANDIDATES:
    relevant_posts = fetch_posts(candidate, limit=10, sort="relevant", time_filter="day")
    print("Relevant posts fetched")

    hot_posts = fetch_posts(candidate, limit=10, sort="hot")
    print("Hot posts fetched")

    publish_message_to_qstash(
        body={
            "posts": relevant_posts,
            "candidate": candidate
        },
        url="store-post"
    )

    publish_message_to_qstash(
        body={
            "posts": hot_posts,
            "candidate": candidate
        },
        url="store-post"
    )
