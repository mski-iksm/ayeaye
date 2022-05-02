from logging import getLogger

import flask

from ayeaye.remote_controller import RemoteController

logger = getLogger(__name__)


def setup_app(app):
    remote_controller = RemoteController.build()

    @app.route('/hello', methods=['get'])
    def hello():
        response = {'message': 'server running', 'Content-Type': 'application/json'}
        return flask.jsonify(response)

    @app.route('/incoming', methods=['post'])
    def incoming():
        response = {
            'message': 'not valid key',
            'text': 'NA',
            'Content-Type': 'application/json',
        }
        posted_data = flask.request.get_json()

        response = remote_controller.posted(posted_data)
        return response
