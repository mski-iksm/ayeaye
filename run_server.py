from logging import getLogger

import fire
import flask

from ayeaye.set_server import setup_app

logger = getLogger(__name__)


def run_server(port_number: int = 7888):
    app = flask.Flask(__name__)
    app.config['JSON_AS_ASCII'] = False  # JSONでの日本語文字化け対策

    setup_app(app)

    logger.info('**** Flask starting server ****')
    app.run(port=port_number, ssl_context='adhoc', debug=False, host='0.0.0.0')


if __name__ == '__main__':
    fire.Fire(run_server)
