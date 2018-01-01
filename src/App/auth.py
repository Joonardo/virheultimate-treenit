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
    def verify(*args, **kwargs):
        u = DB.User.verify_auth_token(request.headers['Authorization'])
        if not u:
            return 'Unauthorized', 403
        g.user = u
        return fn(*args, **kwargs)
    return verify


@app.route('/api/login/test', methods=['GET'])
@required
def test():
    print(g.user.username)
    return "Hello, {:s}".format(g.user.username)
