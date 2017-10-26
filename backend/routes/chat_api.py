from controllers.chat_controller import ChatController
from routes.Route import Route
from server_utils import create_get_response, get_body_content, create_not_found_response
from flask import response

PATH = "/chat"
NAME = "chat_api"


class ChatApi(Route):
    def __init__(self):
        Route.__init__(self, NAME, PATH)
        controller = ChatController()
        bp = self._bp

        @bp.route('', methods=["POST"])
        def _chat():
            body = get_body_content(response)
            if 'msg' in body:
                response = controller._answer(body.get('msg'))
                return create_get_response({"response": response})
            else:
                return create_not_found_response()
