from flask import Blueprint, request, current_app, jsonify
import os
import uuid
from api.img_recog.model_three import model_three_func
from api.img_recog.model_one import model_one_func
from api.img_recog.model_two import model_two_func
from api.key import AUTHENTICATION_KEY


rg_bp = Blueprint('rg_bp', __name__)


ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@rg_bp.route('/rg-process', methods=['POST'])
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
                path = os.path.join(current_app.config['upload'], f_name + extension)
                file.save(path)
                result_1 = None
                result_2 = None
                new_result = None
                try:
                    result_1 = model_one_func(path)
                    result_2 = model_two_func(path)
                    result_2 = list(result_2[0][0])
                    result_2 = [str(i) for i in result_2]

                    result_3 = model_three_func(path)
                    result_3 = result_3[0]
                    # result_3 = [list(i) for i in result_3]
                    new_result = []
                    for i in result_3:
                        # print(i)
                        lst = [str(x) for x in i]
                        new_result.append(lst)

                except Exception:
                    pass

                if result_1 and result_2 and new_result:
                    if os.path.exists(os.path.join(current_app.config['upload'], f_name + extension)):
                        os.remove(os.path.join(current_app.config['upload'], f_name + extension))

                    return jsonify(response={"success": {
                                                        'result_one': list(result_1),
                                                        'result_two': result_2,
                                                        'result_three': new_result
                                                        }
                                            }
                                )
                else:
                    return jsonify(error={"Message": "Something went wrong, please try again."}), 500
            else:
                return jsonify(error={"Message": "Allowed image types are -> png, jpg, jpeg"}), 404
        else:
            return jsonify(error={"Message": "Unauthorized"}), 401