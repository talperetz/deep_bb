# -*- coding: utf-8 -*-
import config as config
import server_utils as utils
import pprint

# logger = basic_load(__file__, os.environ.get('ENV_OBJECT'))
from flask import Flask, request, abort
from flask_cors import CORS, cross_origin


def load_blueprints(app):
    from routes.tweet_api import TweetApi
    from routes.speech_api import SpeechApi
    tweet_api = TweetApi()
    speech_api = SpeechApi()
    app.register_blueprint(tweet_api._bp)
    app.register_blueprint(speech_api._bp)


def init_server(app):
    printer = pprint.PrettyPrinter(indent=4)

    @app.before_request
    def before():
        if not utils.is_request_authorized(request):
            abort(501)
            utils.init_incoming_request(request)

    @app.after_request
    def after(response):
        after_request = dict()
        after_request['status'] = response.status
        after_request['headers'] = response.headers
        if not response.direct_passthrough:
            after_request['data'] = response.get_data()
        request_data = utils.get_request_details(request)
        after_request.update(request_data)
        # logger.info(printer.pformat(after_request))
        return response


if __name__ == '__main__':
    app = Flask(__name__)
    CORS(app)
    load_blueprints(app)
    init_server(app)
    app.run(host=config.SERVER_IP,
            port=config.SERVER_PORT)
