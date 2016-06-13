from models import User

from models import create_session

from werkzeug.security import check_password_hash, generate_password_hash

session = create_session()

def set_password(password):
    return generate_password_hash(password)

def check_password(password1, password2):
    return check_password_hash(password1, password2)

def addUser(username, password):
    users = session.query(User).all()
    for user in users:
        if user.username == username:
            print('User already in DB')
            return
    pwd = set_password(password)
    user = User(username=username, password=pwd)
    session.begin()
    session.add(user)
    try:
        session.commit()
    except IntegrityError:
        session.rollback()
        print('Unable to add user to DB...')

    print('User successfully added to DB!')

def deleteUsers():
    session.query(User).delete()

