# sentiment_analysis.py
import os
from qstash import QStash
from qstash.chat import openai
from dotenv import load_dotenv

load_dotenv()

qstash_token = os.getenv("QSTASH_TOKEN")
openai_api_key = os.getenv("OPENAI_API_KEY")
api_base_url = os.getenv("API_BASE_URL")

qstash_client = QStash(qstash_token)

async def analyze_sentiment(text: str) -> float:
    response = qstash_client.message.publish_json(
        api={"name": "llm", "provider": openai(openai_api_key)},
        body={
            "model": "gpt-3.5-turbo",
            "messages": [
                {
                    "role": "user",
                    "content": f"Rate the sentiment of the following text between 0 (hate) and 100 (love) for the president candidate mentioned: '{text}'",
                }
            ],
        },
        callback=f"{api_base_url}/sentiment-callback",
    )
    # response is message_id
    return response

# def parse_response(response):
#     # Implement the logic to parse the response and extract the score
#     # For example, assume the assistant returns: "The sentiment score is 75."
#     content = response.get('choices')[0]['message']['content']
#     score = float(''.join(filter(str.isdigit, content)))
    return score