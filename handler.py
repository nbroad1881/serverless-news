from datetime import datetime, timedelta, timezone

from news import get_recent_articles


def main(event, context):

    try:
        params = event['queryStringParameters']
        start_date = datetime.fromisoformat(params['start_date'])
        end_date = datetime.fromisoformat(params['end_date'])
        num_steps = params['num_steps']

        start_date = start_date.replace(tzinfo=timezone.utc)
        end_date = end_date.replace(tzinfo=timezone.utc)

    except KeyError as e:
        print("No parameters detected. Doing default 1-hour check")
        end_date = datetime.now()
        start_date = end_date - timedelta(hours=1)
        num_steps = 10

    try:
        key_num = event['queryStringParameters']['key_num']
    except KeyError as e:
        print("No key specified. Using default of 1")
        key_num = 1

    get_recent_articles(start_date=start_date, end_date=end_date, num_steps=num_steps, key_num=1)

    response = {
        "statusCode": 200,
        "body": "Function complete"
    }

    return response
