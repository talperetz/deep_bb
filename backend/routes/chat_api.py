from controllers.chat_controller import ChatController
from routes.Route import Route
from server_utils import create_get_response

PATH = "/chat"
NAME = "chat_api"


class ChatApi(Route):
    def __init__(self):
        Route.__init__(self, NAME, PATH)
        controller = ChatController()
        bp = self._bp

        @bp.route('', methods=["POST"])
        def _chat():
            response = controller._generate_speech()
            return create_get_response({"response": response})
