import base64
import logging

from bunch import bunchify
from flask import request, session, jsonify
from flask.helpers import make_response
from flask_classful import FlaskView, route
from flask_login import login_user, logout_user
from requests.status_codes import codes as status_codes

from utils.shared_state import SharedState
from utils.trace import trace


class LoginApi(FlaskView):
    decorators = [trace]

    @route('/login', methods=['POST'])
    def login(self):
        data = None
        try:
            request_data = request.get_json()
            if not request_data:
                message='Login credentials not provided'
                logging.getLogger(__name__).info(message)
                return make_response(jsonify(message=message), status_codes.bad_request)

            data = bunchify(request_data)

            user_manager = SharedState.getInstance().user_mgr
            data.username = data.username
            data.password = base64.b64decode(data.password)
            user = user_manager.find_user_by_username(data.username)
            logging.getLogger(__name__).info("Logging in as {}".format(data.username))
            if not user:
                message='User: {} does not exist'.format(data.username)
                logging.getLogger(__name__).info(message)
                return make_response(jsonify(message=message), status_codes.bad_request)

            # Successful authentication
            if not user_manager.verify_password(data.password, user):
                message='Invalid password for User: {}'.format(data.username)
                logging.getLogger(__name__).info(message)
                return make_response(jsonify(message=message), status_codes.bad_request)

            # Use Flask-Login to sign in user: fails if user is inactive
            if not login_user(user):
                message='User: {} Account Disabled'.format(data.username)
                logging.getLogger(__name__).info(message)
                return make_response(jsonify(message=message), status_codes.bad_request)

            session['library_name'] = user.library.name
            session['username'] = data.username
            session['password'] = data.password
            login_utils.set_fake_login(bn=session['library_name'], u=session['username'], pw=session['password'], is_loggedin=True)

            status_info, role = login_utils.get_role(from_login=True)
            if not status_info.status:
                raise Exception('Invalid role')

            session['role'] = role.value
            login_utils.set_fake_login(r=session['role'])
            message='User: {} Logged in successfully'.format(data.username)
            logging.getLogger(__name__).info(message)
            return make_response(jsonify(message=message), status_codes.ok)
        except Exception as e:
            logging.getLogger(__name__).exception(e)
            if data:
                logging.getLogger(__name__).info('username:{}, exception message:{}'.format(data.username, e.message))
            else:
                logging.getLogger(__name__).info('exception message:{}'.format(e.message))
            return make_response(jsonify(message=e.message), status_codes.bad_request)

    @route('/logout', methods=['GET'])
    def logout(self):
        try:
            if logout_user():
                session.pop('username',None)
                session.pop('password',None)
                message='Logged out successfully.'
                logging.getLogger(__name__).info(message)
                return make_response(jsonify(message=message), status_codes.ok)
            else:
                message='Logout failed.'
                logging.getLogger(__name__).info(message)
                return make_response(jsonify(message=message), status_codes.bad_request)
        except Exception as e:
            logging.getLogger(__name__).info('{}{}'.format(e.message, e))
            return make_response(jsonify(message=e.message), status_codes.bad_request)

LoginApi.register(SharedState().getInstance().app, route_base='/api/user')
