from flask import Blueprint, jsonify, request, abort

from ..service.captions_extractor import get_captions_from_video
from ..service.seo_optimizer import get_SEO_optiomized_data
from loguru import logger


# define the blueprint
youtube_api = Blueprint(name="youtube_api", import_name=__name__)


@youtube_api.route('', methods=['POST'])
def extract_youtube_metadata():
    data = request.get_json()
    if "url" not in data:
        abort(400, "url missing in request body")

    captions = ""
    try:
        logger.info(f"generating_caption URL: {data['url']}")
        captions = get_captions_from_video(data["url"])
    except Exception as e:
        abort(400, "captions generate from URL error " + str(e))

    try:
        logger.info(f"generating_chatGPT_seo_optimizer")
        return get_SEO_optiomized_data(captions)
    except Exception as e:
        abort(400, "chat gpt response generate error: " + str(e))
