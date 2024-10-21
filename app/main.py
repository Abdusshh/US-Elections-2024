from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.templating import Jinja2Templates
from services.reddit_client import fetch_posts
from services.sentiment_analysis import analyze_sentiment
from services.redis_service import store_post, get_all_posts, store_score, get_recent_posts
import base64
import json

app = FastAPI()

templates = Jinja2Templates(directory="templates")

NUMBER_OF_POSTS = 2
CANDIDATES = ["Donald Trump", "Kamala Harris"]
NUMBER_OF_POSTS_TO_DISPLAY = 5

# This endpoint will display the sentiment scores for each candidate
@app.get("/")
def read_root(request: Request):
    candidates = CANDIDATES
    scores = {}
    for candidate in candidates:
        posts = get_all_posts(candidate)
        if posts:
            average_score = sum(float(post['score']) for post in posts) / len(posts)
            scores[candidate] = round(average_score, 2)
        else:
            scores[candidate] = "No data"
    return templates.TemplateResponse("index.html", {"request": request, "scores": scores})

# This endpoint will display the posts for a specific candidate
@app.get("/candidate/{candidate_name}")
def read_candidate(request: Request, candidate_name: str):
    posts = get_recent_posts(candidate_name, limit=NUMBER_OF_POSTS_TO_DISPLAY)
    return templates.TemplateResponse("candidate.html", {"request": request, "candidate": candidate_name, "posts": posts})

# This endpoint will be called by the scheduler to fetch the latest posts
@app.post("/fetch-posts")
def fetch_posts_endpoint():
    candidates = CANDIDATES
    for candidate in candidates:
        posts = fetch_posts(candidate, limit=NUMBER_OF_POSTS)
        for post in posts:
            store_post(candidate, post.title, post.url, 50) # Default score of 50
            analyze_sentiment(f"Candidate: {candidate}, Title: {post.title}, Text: {post.selftext}", candidate, post.title)
    return {"status": "Fetching started"}

# This endpoint will be used as the callback URL for the sentiment analysis
# It will parse the response and store the sentiment score to redis
@app.post("/sentiment-callback")
def sentiment_callback(candidate: str, title: str, request: Request):

    # Parse the request body to JSON format
    data = await request.json()
    print(data)

    # Decode the base64-encoded 'body' field from the callback
    encoded_body = data.get('body', '')
    decoded_body = base64.b64decode(encoded_body).decode('utf-8')

    # Parse the decoded body to JSON format
    decoded_data = json.loads(decoded_body)

    # Extract the summary from the decoded response
    response = decoded_data['choices'][0]['message']['content']

    # Parse the response to extract the sentiment score
    score = parse_response(response)

    # Store the sentiment score to redis
    store_score(candidate, title, score)

    return JSONResponse(content={"status": "Sentiment score stored"})

# Function to parse the response and extract the sentiment score
def parse_response(response):
    score = float(''.join(filter(str.isdigit, response)))
    return score