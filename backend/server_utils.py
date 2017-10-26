import time
import json
from flask import Response


def is_request_authorized(request):
    if (request.method == 'POST' or request.method == 'PUT') and (
                    'application/json' not in request.headers['content-type'] and 'multipart/form-data' not in
                request.headers['content-type']):
        return False
    return True


def init_incoming_request(request):
    request.request_start_time = time.time()
    request.request_time = lambda: "%.5fs" % (
        time.time() - request.request_start_time)


def get_request_details(request):
    request_data = dict()
    request_data['ip_address'] = request.headers.environ.get('REMOTE_ADDR')
    request_data['content_type'] = request.headers.environ.get('CONTENT_TYPE')
    request_data['user_agent'] = request.headers.environ.get('HTTP_USER_AGENT')
    return request_data


def create_get_response(data):
    return Response(json.dumps(data),
                    mimetype='application/json', status=200)


def create_not_found_response(desc='not_found'):
    err_dict = dict()
    err_dict['err'] = desc
    return Response(json.dumps(err_dict),
                    mimetype='application/json', status=404)


def get_body_content(args):
    content = {}
    try:
        if args.get_data() == '':
            return content
        params = args.get_json()
        if params:
            for param in params:
                content[param] = params[param]
    except:
        pass
    return content
