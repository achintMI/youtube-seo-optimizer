from flask import Blueprint, jsonify, request, Response
import flask

from ..service.captions_extractor import get_captions_from_video
from ..service.seo_optimizer import get_SEO_optiomized_data
from loguru import logger

# define the blueprint
youtube_api = Blueprint(name="youtube_api", import_name=__name__)


@youtube_api.route('', methods=['POST'])
def extract_youtube_metadata():
    data = request.get_json()
    if not data["url"]:
        return jsonify(exception="url is missing in request body", code=400)

    try:
        logger.info(f"generating_caption URL: {data['url']}")
        captions = get_captions_from_video(data["url"])

        logger.info(f"generating_chatGPT_seo_optimizer")
        return get_SEO_optiomized_data(captions)
    except Exception as e:
        raise jsonify(exception="Please try after sometime")
