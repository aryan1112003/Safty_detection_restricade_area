import os
import json
from datetime import datetime
from werkzeug.utils import secure_filename
from flask import render_template, request, session
from flask_login import login_required, current_user
from base.com.service.safety_service import apply_safety_detection
from base.com.vo.detection_vo import DetectionVO
from base.com.dao.detection_dao import DetectionDAO
from base import app


@app.route('/safety-detection', methods=['GET', 'POST'])
@login_required
def safety_detection():
    detection_vo_obj = DetectionVO()
    detection_dao_obj = DetectionDAO()
    try:
        if request.method == 'GET':
            return render_template('safety_detection/index.html', user=current_user)
        elif request.method == 'POST':
            video = request.files.get('video')

            if video:
                real_filename = secure_filename(video.filename)
                filename = real_filename.split('.')
                filename = f"{filename[0]} ({int(datetime.now().timestamp())}).{filename[1]}"
                input_video_path = os.path.join(
                    app.config['SAFETY_UPLOAD_FOLDER'], filename)
                video.save(input_video_path)
                # try:
                detection_vo_obj.detection_datetime = int(
                    datetime.now().timestamp())

                result = apply_safety_detection(
                    input_video_path)
                output_video_name, result_percentage = result
                
                detection_vo_obj.created_by = current_user.login_id
                detection_vo_obj.modified_by = current_user.login_id
                detection_vo_obj.input_file_path = input_video_path
                detection_vo_obj.output_file_path = output_video_name
                detection_vo_obj.detection_type = 'safety'
                detection_vo_obj.is_deleted = False
                detection_vo_obj.created_on = int(
                    datetime.now().timestamp())
                detection_vo_obj.modified_on = int(
                    datetime.now().timestamp())
                detection_vo_obj.detection_stats = json.dumps(
                    result_percentage)
                detection_vo_obj.detection_source = 'video'

                detection_dao_obj.save(
                    detection_vo_obj)
                return render_template('safety_detection/result.html',
                                        user=current_user,
                                        video=output_video_name[4:],
                                        video_name=real_filename.upper(),
                                        result_percentage=result_percentage
                                        )
                # finally:
                    # os.remove(input_video_path)
                    # session.clear()

            return render_template('error.html', error="Video not available")
    except Exception as e:
        return render_template('error.html', error=e)
