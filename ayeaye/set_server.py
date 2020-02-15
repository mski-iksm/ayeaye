import flask

from ayeaye.remote_controller import RemoteController

# routeとmethodごとにrecieverを設定する
# 受け取ったデータを、処理するオブジェクトに投げ+返信を作成させる
# TODO: 中身の実装はここには書かない


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

        response = remote_controller.run(posted_data)
        return response
