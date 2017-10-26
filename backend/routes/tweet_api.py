from routes.Route import Route
from controllers.tweets_controller import TweetController
from server_utils import create_get_response, get_body_content, create_not_found_response
from flask import request

PATH = "/tweet"
NAME = "tweet_api"


class TweetApi(Route):
    def __init__(self):
        Route.__init__(self, NAME, PATH)
        controller = TweetController()
        bp = self._bp

        @bp.route('', methods=["GET"])
        def _get_tweets():
            tweet = controller._generate_random_tweet()
            return create_get_response(tweet)

        @bp.route('', methods=["POST"])
        def _post_new_tweet():
            tweet = controller._post_tweet()
            return create_get_response({'tweet': tweet._json.get('text')})
