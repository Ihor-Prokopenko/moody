from django.conf import settings
from urllib.parse import urlparse, parse_qs

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

YOUTUBE_API_KEY = settings.YOUTUBE_API_KEY


def get_video_id(url):
    """
    Examples:
    - http://youtu.be/SA2iWivDJiE
    - http://www.youtube.com/watch?v=_oPAwA_Udwc&feature=feedu
    - http://www.youtube.com/embed/SA2iWivDJiE
    - http://www.youtube.com/v/SA2iWivDJiE?version=3&amp;hl=en_US
    """
    query = urlparse(url)
    if query.hostname == 'youtu.be':
        return query.path[1:]
    if query.hostname in ('www.youtube.com', 'youtube.com'):
        if query.path == '/watch':
            p = parse_qs(query.query)
            return p['v'][0]
        if query.path[:7] == '/embed/':
            return query.path.split('/')[2]
        if query.path[:3] == '/v/':
            return query.path.split('/')[2]
    return None


def get_comments_from_youtube(link: str = None):
    dummy_link = "https://www.youtube.com/watch?v=ZDTJDZNUfwA"

    video_id = get_video_id(dummy_link)

    youtube = build('youtube', 'v3', developerKey=YOUTUBE_API_KEY)

    try:
        results = youtube.commentThreads().list(
            part='snippet',
            videoId=video_id,
            textFormat='plainText'
        ).execute()

    except HttpError as e:
        return None

    res = []

    for item in results['items']:
        comment = item['snippet']['topLevelComment']['snippet']['textDisplay']
        res.append(comment)

    # print(results)
    return res


