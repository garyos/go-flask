from werkzeug.security import safe_str_cmp  #is safe string compare function for py2.7
from user import User

#{ This was an example user
#    'id': 1,
#    'username': 'bob',
#    'password': 'asdf'
#}

users = [
    User(1,'bob', 'asdf')
]

username_mapping = {u.username: u for u in users}
#{
#    'bob': {
#        'id' = 1,
#        'username' = 'bob',
#        'password' = 'asdf'
#    }
#}

userid_mapping = {u.id: u for u in users}
#{
#    1: {
#        'id': 1,
#        'username': 'bob',
#        'password': 'asdf'
#    }
#}

def authenticate(username, password):
    user = username_mapping.get(username, None)
    if user and safe_str_cmp(user.password,password):
        return user

def identity(payload):
    user_id = payload['identity']
    return userid_mapping.get(user_id, None)
