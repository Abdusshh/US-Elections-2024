from qstash import QStash
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

qstash_token = os.getenv("QSTASH_TOKEN")
qstash_client = QStash(token=qstash_token)

def schedule_reddit_fetch():
    response = qstash_client.schedule.create(
        destination="https://your-app-domain.com/fetch-posts",
        cron="0 * * * *",  # Every hour
    )
    print(f"Scheduled job ID: {response['schedule_id']}")