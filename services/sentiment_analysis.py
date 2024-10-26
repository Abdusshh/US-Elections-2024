import os
from qstash import QStash
from qstash.chat import openai
from dotenv import load_dotenv

load_dotenv()

qstash_token = os.getenv("QSTASH_TOKEN")
openai_api_key = os.getenv("OPENAI_API_KEY")
api_base_url = os.getenv("API_BASE_URL")

qstash_client = QStash(qstash_token)

def analyze_sentiment(text: str, candidate: str, title: str):
    qstash_client.message.publish_json(
        api={"name": "llm", "provider": openai(openai_api_key)},
        body={
            "model": "gpt-3.5-turbo",
            "messages": [
                {
                    "role": "user",
                    "content": f"""
Please assess the sentiment of the following text on a scale from 0 to 100, where 0 represents strong negativity (hate) and 100 represents strong positivity (love):

‘{text}’

The text mentions {candidate}, a 2024 presidential candidate. Rate the sentiment based on the tone toward {candidate}.

Provide a single number between 0 and 100 to reflect the overall sentiment in the text.
                    """,
                }
            ],
        },
        callback=f"{api_base_url}/sentiment-callback?candidate={candidate}&title={title}",
        headers={"Upstash-Callback-Retries": "1"},
        retries=1,
    )