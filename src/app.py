from flask import Flask, jsonify, json

# load modules
from src.routes.api import youtube_api
from werkzeug.exceptions import HTTPException

# init Flask app
app = Flask(__name__)

# register blueprints. ensure that all paths are versioned!
app.register_blueprint(youtube_api, url_prefix="/youtube-seo-optimize")

@app.errorhandler(HTTPException)
def handle_exception(e):
    response = e.get_response()
    response.data = json.dumps({
        "error": {
            "code": e.code,
            "name": e.name,
            "description": e.description,
        }
    })
    response.content_type = "application/json"
    return response


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)