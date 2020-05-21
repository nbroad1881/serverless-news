import os
import csv
from datetime import datetime

import boto3
from botocore.exceptions import ClientError
from newsapi import NewsApiClient
from newsapi.newsapi_exception import NewsAPIException

from schema import Article


PAGE_SIZE = 100
QUERY = '(Trump) OR (Biden) OR (Bernie) OR (Sanders) OR ' \
        '(Klobuchar) OR (Warren) OR (Harris) OR ' \
        '(Buttigieg) OR (Bloomberg) OR (Yang) OR (Steyer) '
SORT_BY = 'relevancy'
LANG = 'en'

local_filename = f'/tmp/{datetime.now().strftime("%Y-%m-%d-%H-%M")}.csv'  # 2020-04-04-12-23.csv
s3_filename = f'{datetime.now().strftime("%Y-%m-%d-%H-%M")}.csv'

COUNTER = [0]


def get_recent_articles(start_date, end_date, num_steps: int, key_num: int) -> None:
    """
    Breaks the time period from start_date to end_date up in num_steps chunks. Uses the NewsApiClient to
    get everything from those time chunks and upload to s3

    """
    try:
        news_client = NewsApiClient(api_key=os.environ[f'NEWS_API_KEY_{key_num}'])
    except KeyError as e:
        print(f"Invalid key given: {key_num}. Function ending.")
        return

    increment = (end_date - start_date) / num_steps

    from_date = start_date
    with open(local_filename, 'w') as csv_file:
        writer = csv.writer(csv_file)
        for i in range(num_steps):
            to_date = from_date + increment

            try:
                results = news_client.get_everything(from_param=from_date,
                                                 to=to_date,
                                                 page_size=PAGE_SIZE,
                                                 qintitle=QUERY,
                                                 language=LANG,
                                                 sort_by=SORT_BY)
            except NewsAPIException as e:
                print(f"NewsAPI Exception: {e}")
                return None

            print(f"Calling get_everything with parameters:",
                  f"from_param={from_date}",
                  f"to_date={to_date}",
                  f"page_size={PAGE_SIZE}",
                  f"qintitle={QUERY}",
                  f"language={LANG}",
                  f"sort_by={SORT_BY}",
                  sep='\n')

            if results['status'] == 'ok':
                parse_results(results['articles'], writer)
            else:
                print(f"Status not ok: {results['status']}")
            #todo: something to handle rate limit

            from_date += increment

    upload_file(local_filename, os.environ['BUCKET_NAME'], s3_filename)

    print(f"The number of articles logged was {COUNTER[0]}.")


def parse_results(results: dict, writer: csv.writer) -> None:
    """
    Given a dict of results from the news-api client. Parse through each article and
    use the writer to write a row to the csv.
    """
    for article in results:

        try:
            source = article['source']
        except KeyError as e:
            print("KeyError: source not in results")
            source_id, source_name = '', ''
        else:
            source_id = article['source'].get('id', '')
            source_name = article['source'].get('name', '')

        author = article.get('author', '')
        title = article.get('title', '')
        content = article.get('content', '')
        url = article.get('url', '')
        published_at = article.get('publishedAt', '')

        writer.writerow([source_id, source_name, author, title, content, url, published_at])
        COUNTER[0] += 1


def upload_file(file_name, bucket, object_name=None):
    """Upload a file to an S3 bucket

    :param file_name: File to upload
    :param bucket: Bucket to upload to
    :param object_name: S3 object name. If not specified then file_name is used
    :return: True if file was uploaded, else False
    """

    # If S3 object_name was not specified, use file_name
    if object_name is None:
        object_name = file_name

    # Upload the file
    s3_client = boto3.client('s3')
    try:
        response = s3_client.upload_file(file_name, bucket, object_name)
    except ClientError as e:
        print("Error: ", e)
        return False
    return True


