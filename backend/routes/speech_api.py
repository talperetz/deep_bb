from controllers.speech_controller import SpeechController
from routes.Route import Route
from server_utils import create_get_response

PATH = "/speech"
NAME = "speech_api"


class SpeechApi(Route):
    def __init__(self):
        Route.__init__(self, NAME, PATH)
        controller = SpeechController()
        bp = self._bp

        @bp.route('', methods=["GET"])
        def _get_speech():
            speech = controller._generate_speech()
            return create_get_response(speech)
