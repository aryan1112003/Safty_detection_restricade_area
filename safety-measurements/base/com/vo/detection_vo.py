from base import db, app
from base.com.vo.user_vo import UserVO


class DetectionVO(db.Model):
    __tablename__ = 'detection_table'

    detection_id = db.Column(db.Integer, primary_key=True)
    created_by = db.Column(db.Integer, db.ForeignKey(UserVO.login_id))
    modified_by = db.Column(db.Integer, db.ForeignKey(UserVO.login_id))
    input_file_path = db.Column(db.String(255), nullable=False)
    output_file_path = db.Column(db.String(255), nullable=False)
    detection_type = db.Column(db.String(255), nullable=False)
    detection_source = db.Column(db.String(255), nullable=False)
    is_deleted = db.Column(db.Boolean, nullable=False)
    detection_datetime = db.Column(db.Integer, nullable=False)
    created_on = db.Column(db.Integer, nullable=False)
    modified_on = db.Column(db.Integer, nullable=False)
    detection_stats = db.Column(db.Text, nullable=False)

    def as_dict(self):
        return {
            'login_id': self.login_id,
            'created_by': self.created_by,
            'modified_by': self.modified_by,
            'input_file_path': self.input_file_path,
            'output_file_path': self.output_file_path,
            'detection_type': self.detection_type,
            'detection_source': self.detection_source,
            'is_deleted': self.is_deleted,
            'detection_datetime': self.detection_datetime,
            'created_on': self.created_on,
            'modified_on': self.modified_on,
            'detection_stats': self.detection_stats,
        }


with app.app_context():
    db.create_all()
