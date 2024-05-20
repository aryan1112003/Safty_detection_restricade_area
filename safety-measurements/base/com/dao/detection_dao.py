from flask_login import current_user
from base import app, db
from base.com.vo.detection_vo import DetectionVO


class DetectionDAO():
    def save(self, detection_vo_obj):
        db.session.add(detection_vo_obj)
        db.session.commit()

    def get_user_records(self):
        return DetectionVO.query.filter_by(is_deleted=False).filter_by(created_by=current_user.login_id).all()

    def update_record(self, detection_vo_obj):
        db.session.merge(detection_vo_obj)
        db.session.commit()
