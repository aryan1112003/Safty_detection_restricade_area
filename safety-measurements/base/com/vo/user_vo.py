from base import db, app
from flask_login import UserMixin


class UserVO(db.Model, UserMixin):
    __tablename__ = 'login_table'
    login_id = db.Column(db.Integer, primary_key=True)
    login_username = db.Column(db.String(255), unique=True, nullable=False)
    login_password = db.Column(db.String(255), nullable=False)
    login_role = db.Column(db.String(255), nullable=False)
    is_deleted = db.Column(db.Boolean, nullable=False)
    created_on = db.Column(db.Integer, nullable=False)
    modified_on = db.Column(db.Integer, nullable=False)

    def as_dict(self):
        return {
            'login_id': self.login_id,
            'login_username': self.login_username,
            'login_password': self.login_password,
            'login_role': self.login_role,
            'is_deleted': self.is_deleted,
            'created_on': self.created_on,
            'modified_on': self.modified_on
        }
        
    @staticmethod
    def get(login_id):
        return UserVO(login_id)

    def get_id(self):
        return str(self.login_id)


with app.app_context():
    db.create_all()
