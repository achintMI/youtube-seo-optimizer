import os
import re
import requests
from pytube import extract
import youtube_transcript_api

# from app.pages.services.utils.utils import get_content_from_scraping_bee
# from config import Config
from urllib.parse import urlparse
from configparser import ParsingError
from youtube_transcript_api import YouTubeTranscriptApi

# from app.pages.services.custom_errors import NoContentFound


def get_provider(video_url):
    """
    It takes a video url as an argument and returns the provider of the video

    :param video_url: The url of the video
    :return: The provider of the video
    """

    query = urlparse(video_url)
    if query.hostname in ['vimeo.com', 'vimeo']:
        return "vimeo"
    elif query.hostname in ['youtube.com', 'youtu.be', 'www.youtube.com', 'youtube.com', 'music.youtube.com']:
        return 'youtube'

    return False


def get_video_id(video_url, provider):
    """
    It takes a video url as input and returns the video id

    :param video_url: The URL of the video you want to download
    """
    video_id = None
    try:
        if provider == 'vimeo':
            headers = get_vimeo_headers()
            response = requests.get(f"https://vimeo.com/api/oembed.json?url={video_url}", headers=headers)
            result = response.json()
            video_id = result['video_id']
        elif provider == 'youtube':
            video_id = extract.video_id(video_url)
    except Exception as e:
        return False
    else:
        return video_id


def youtube_extractor(video_id):
    """
    It takes a video id as an argument and returns a dictionary with the captions of the video as a list
    of dictionaries

    :param video_id: The ID of the video you want to get the captions for
    """
    try:
        # os.environ['HTTPS_PROXY'] = "http://user-default:CrmnTTX6Xva1@resi.proxiware.com:8080"
        transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)

        transcript_list = ['en'] + [tr.language_code for tr in transcript_list]
        response_text = YouTubeTranscriptApi.get_transcript(video_id, languages=transcript_list)
        text_list = [d['text'] for d in response_text]
        captions = ' '.join(text_list)
    except (youtube_transcript_api._errors.NoTranscriptFound):
        os.environ.pop('HTTPS_PROXY', None)
        raise Exception(f"No transcript found for {video_id}")
    except Exception as e:
        os.environ.pop('HTTPS_PROXY', None)
        raise e
    else:
        os.environ.pop('HTTPS_PROXY', None)
        return captions


def get_vimeo_headers():
    return {
        # "Authorization": f"Bearer {Config.VIMEO_ACCESS_TOKEN}",
        # "Content-Type": "application/json",
        # "Accept": "application/vnd.vimeo.*+json;version=3.4",
    }


def vimeo_extractor(video_id):
    captions = ''
    headers = get_vimeo_headers()

    try:
        response = requests.get(f"https://api.vimeo.com/videos/{video_id}/texttracks", headers=headers)
        if response.status_code == 200:
            text_tracks = response.json().get('data')

            if not text_tracks:
                raise Exception(f"No transcript found for {video_id}")

            for text_track in text_tracks:
                link = text_track.get('link')
                captions_response = requests.get(link, headers=headers)
                if captions_response.status_code == 200:
                    captions += captions_response.text
    except Exception as e:
        raise Exception(f"No transcript found for {video_id}")
    else:
        pattern = re.compile(r"\d+:\d+\.\d+\s--> \d+:\d+\.\d+")
        clean_text = re.sub(pattern, "", captions).replace('\n\n\n', ' ').replace('\n', ' ').lstrip(
            'WEBVTT').strip().lstrip('-').strip()
        return clean_text


# def get_video_title(video_url):
#     response = get_content_from_scraping_bee(video_url, {'render_js': False})
#     content = response.content.decode('utf-8')
#     match = re.search('<title>(.*)</title>', content)
#     if match:
#         return match.group(1)
#     else:
#         return None


def extract_captions(provider, video_url):
    video_id = get_video_id(video_url, provider=provider)
    if not video_id:
        raise ParsingError("Unable to extract video_id from URL")
    if provider == "youtube":
        return youtube_extractor(video_id=video_id)
    elif provider == "vimeo":
        return vimeo_extractor(video_id=video_id)


def get_captions_from_video(url):
    provider = get_provider(url)
    captions = extract_captions(provider, url)
    return captions