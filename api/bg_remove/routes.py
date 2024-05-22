from flask import request, jsonify, Blueprint, current_app
import os
import uuid
from rembg.bg import remove
import io
from PIL import Image, ImageFile
from api.key import AUTHENTICATION_KEY

bg_bp = Blueprint('bg_bp', __name__)

ImageFile.LOAD_TRUNCATED_IMAGES = True

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@bg_bp.route('/bg-process', methods=['POST'])
def upload_image():
    if request.method == 'POST':
        key = request.args.get('key',None)
        if key and key == AUTHENTICATION_KEY:
            if 'photo' not in request.files:
                return jsonify(error={"Message": "No photo key in the body"}), 404

            file = request.files['photo']

            if file.filename == '':
                return jsonify(error={"Message": "No image selected for uploading"}), 404

            if file and allowed_file(file.filename):
                extension = os.path.splitext(file.filename)[1]
                f_name = str(uuid.uuid4())
                file.save(os.path.join(current_app.config['upload'], f_name + extension))

                input = Image.open(os.path.join(current_app.config['upload'], f_name + extension))
                output = remove(input)
                output.save(os.path.join(current_app.config['images'], f_name + '.png'))


                if os.path.exists(os.path.join(current_app.config['upload'], f_name + extension)):
                    os.remove(os.path.join(current_app.config['upload'], f_name + extension))
                return jsonify(response={"success": request.host_url + "images/" + f_name + '.png'})
            else:
                return jsonify(error={"Message": "Allowed image types are -> png, jpg, jpeg"}), 404
        else:
            return jsonify(error={"Message": "Unauthorized"}), 401


@bg_bp.route('/images/<filename>', methods=['GET'])
def view_image(filename=''):
    from flask import send_file
    file_path = os.path.join(current_app.config['images'], filename)

    return_data = io.BytesIO()
    with open(file_path, 'rb') as fo:
        return_data.write(fo.read())
    # (after writing, cursor will be at last byte, so move it to start)
    return_data.seek(0)

    os.remove(file_path)

    return send_file(return_data, mimetype='image/png', download_name='image.png')
