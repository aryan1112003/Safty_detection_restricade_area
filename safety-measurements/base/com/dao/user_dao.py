from werkzeug.security import check_password_hash
from flask_login import current_user
from base import app, db
from base.com.vo.user_vo import UserVO
from base.com.vo.detection_vo import DetectionVO


class UserDAO():
    def view_one_user(self, user_vo):
        user = UserVO.query.filter_by(
            login_username=user_vo.login_username).first()

        if not user:
            return None

        password = user_vo.login_password
        status = check_password_hash(user.login_password, password)
        if status:
            return user
        return None

    def save(self, user_vo):
        db.session.add(user_vo)
        db.session.commit()
