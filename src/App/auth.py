from App import app
import DB

from flask import request, jsonify, g

@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    if not ('email' in data and 'password' in data):
        return jsonify({'error': 'missing required information'})

    user = DB.User.query.filter_by(email=data['email']).first()
    if not user:
        return jsonify({'error': 'user was not found'})

    if not user.authorize(data['password']):
        return jsonify({'error': 'wrong password'})

    return jsonify({'Authorization': user.generate_auth_token()})


def required(fn):
    def wrapper(*args, **kwargs):
        u = DB.User.verify_auth_token(request.headers['Authorization'])
        if not u:
            return "Unauthorized", 403
        g.user = u
        return fn(*args, **kwargs)
    return wrapper

def requires_role(role):
    def decorator(fn):
        @required
        def wrapper(*args, **kwargs):
            if not role.upper() in g.user.roles:
                return "Unauthorized", 403
            return fn(*args, **kwargs)
        return wrapper
    return decorator


@app.route('/api/login/test', methods=['GET'])
@required
def test_user():
    return "Hello, {:s}".format(g.user.username)

@app.route('/api/login/test/user', methods=['GET'])
@requires_role('user')
def test_user():
    return "Hello, user {:s}".format(g.user.username)

@app.route('/api/login/test/admin', methods=['GET'])
@requires_role('admin')
def test_admin():
    return "Hello, admin {:s}".format(g.user.username)
