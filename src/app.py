"""Flask Application"""

from flask import Flask, jsonify

# load modules
from src.routes.api import youtube_api
from src.routes.swagger import swagger_ui_blueprint, SWAGGER_URL

# init Flask app
app = Flask(__name__)

# register blueprints. ensure that all paths are versioned!
app.register_blueprint(youtube_api, url_prefix="/youtube-seo-optimize")

from src.api_spec import spec


@app.route("/api/swagger.json")
def create_swagger_spec():
    """
    Swagger API definition.
    """
    return jsonify(spec.to_dict())


@app.errorhandler(404)
def page_not_found(e):
    return jsonify(error=404, text=str(e)), 404


@app.errorhandler(500)
def internal_server_error(e):
    return jsonify(error=500, text=str(e)), 500


app.register_blueprint(swagger_ui_blueprint, url_prefix=SWAGGER_URL)

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
