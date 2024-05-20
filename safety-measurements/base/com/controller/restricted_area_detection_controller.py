import os
import json
from datetime import datetime
from werkzeug.utils import secure_filename
from flask import render_template, redirect, request, url_for, jsonify, session
from flask_login import login_required, current_user
from base.com.service.restricted_area_service import get_first_frame, store_uploaded_video, count_persons_entered_restricted_area
from base.com.vo.detection_vo import DetectionVO
from base.com.dao.detection_dao import DetectionDAO
from base import app


@app.route('/restricted-area-detection', methods=['GET', 'POST'])
@login_required
def restricted_area_detection():
    try:
        if request.method == 'GET':
            return render_template('restricted_area_detection/index.html', user=current_user)
        elif request.method == 'POST':
            video = request.files.get('video')

            real_filename = secure_filename(video.filename)
            video_path = store_uploaded_video(video)
            first_frame_path = get_first_frame(video_path)

            session['real_filename'] = real_filename
            session['stored_file_path'] = video_path
            session['first_frame_path'] = first_frame_path

            return redirect('define-area')
        return render_template('error.html', error="Method not available")
    except Exception as e:
        return render_template('error.html', error=e)


@app.route('/define-area', methods=['GET', 'POST'])
@login_required
def define_area():
    try:
        input_filename = session.get('stored_file_path')
        first_frame_path = session.get('first_frame_path')

        if input_filename is None or first_frame_path is None:
            return redirect('restricted-area-detection')

        if request.method == 'GET':
            return render_template(
                'restricted_area_detection/define_area.html',
                first_frame_path=first_frame_path,
                user=current_user
            )

        return render_template('error.html', error="Method not allowed")
    except Exception as e:
        return render_template('error.html', error=e)


@app.route('/process-restricted-area', methods=['GET', "POST"])
@login_required
def process_restricted_area():
    detection_dao_obj = DetectionDAO()
    detection_vo_obj = DetectionVO()
    try:
        if request.method != 'POST':
            return redirect('restricted-area-detection')

        data = request.json
        # Ensure data is a dictionary and has 'coordinates' key
        if isinstance(data, dict) and 'coordinates' in data:
            coordinates = data['coordinates']

            # Convert coordinates to the desired format [(x1, y1), (x2, y2), ...]
            converted_coordinates = [(round(coord['x']), round(
                coord['y'])) for coord in coordinates if 'x' in coord and 'y' in coord]

            detection_vo_obj.detection_datetime = int(
                datetime.now().timestamp())
            result = count_persons_entered_restricted_area(
                session.get('stored_file_path'),
                converted_coordinates
            )
            input_video_path, output_video_path, result_percentage = result

            session['output_video_path'] = output_video_path
            detection_vo_obj.created_by = current_user.login_id
            detection_vo_obj.modified_by = current_user.login_id
            detection_vo_obj.input_file_path = input_video_path
            detection_vo_obj.output_file_path = output_video_path
            detection_vo_obj.detection_type = 'restricted'
            detection_vo_obj.is_deleted = False
            detection_vo_obj.created_on = int(
                datetime.now().timestamp())
            detection_vo_obj.modified_on = int(
                datetime.now().timestamp())
            detection_vo_obj.detection_stats = json.dumps(
                result_percentage)
            detection_vo_obj.detection_source = 'video'

            detection_dao_obj.save(detection_vo_obj)

            # Store person_count in the session
            session['person_count'] = result_percentage.get('count')

            # Redirect to the restricted_area_result route with the person count as a parameter
            return jsonify({'success': True, 'person_count': result_percentage.get('count')})
        else:
            raise ValueError('Invalid or missing coordinates in the request')
    except Exception as e:
        return render_template('error.html', error=e)


@app.route('/restricted-area-result', methods=["GET"])
@login_required
def restricted_area_result():
    try:
        person_count = session.get('person_count', default=0)

        return render_template(
            'restricted_area_detection/result.html',
            person_count=person_count,
            video_name=session.get('real_filename').upper(),
            video=session.get('output_video_path')[4:],
            user=current_user
        )
    except Exception as e:
        return redirect('restricted-area-detection')
