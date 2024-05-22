from flask import Blueprint, request, current_app, jsonify
import os
import cv2
import numpy as np
import uuid
import io
import imutils
from sklearn.cluster import KMeans
from api.key import AUTHENTICATION_KEY

dominant_bp = Blueprint('dominant_bp', __name__)

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@dominant_bp.route('/dm-process', methods=['POST'])
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

                clusters = 5

                img = cv2.imread(os.path.join(current_app.config['upload'], f_name + extension))

                org_img = img.copy()
                print('Org image shape --> ', img.shape)
                img = imutils.resize(img, height=200)
                print('After resizing shape --> ', img.shape)
                flat_img = np.reshape(img, (-1, 3))
                print('After Flattening shape --> ', flat_img.shape)
                kmeans = KMeans(n_clusters=clusters, random_state=0)
                kmeans.fit(flat_img)
                dominant_colors = np.array(kmeans.cluster_centers_, dtype='uint')
                dominant_colors_lst = dominant_colors.tolist()
                print(dominant_colors_lst)
                percentages = (np.unique(kmeans.labels_, return_counts=True)[1]) / flat_img.shape[0]
                percentages_lst = percentages.tolist()
                print(percentages_lst)
                p_and_c = zip(percentages, dominant_colors)
                p_and_c_list = zip(percentages_lst, dominant_colors_lst)
                p_and_c_list = sorted(p_and_c_list, reverse=True)
                print(p_and_c_list)
                p_and_c = sorted(p_and_c, reverse=True)
                print(type(p_and_c))

                block = np.ones((50, 50, 3), dtype='uint')

                for i in range(clusters):
                    block[:] = p_and_c[i][1][::-1]
                bar = np.ones((50, 500, 3), dtype='uint')
                start = 0
                i = 1
                for p, c in p_and_c:
                    end = start + int(p * bar.shape[1])
                    if i == clusters:
                        bar[:, start:] = c[::-1]
                    else:
                        bar[:, start:end] = c[::-1]
                    start = end
                    i += 1
                rows = 1000
                cols = int((org_img.shape[0] / org_img.shape[1]) * rows)
                img = cv2.resize(org_img, dsize=(rows, cols), interpolation=cv2.INTER_LINEAR)
                copy = img.copy()
                cv2.rectangle(copy, (rows // 2 - 250, cols // 2 - 90), (rows // 2 + 250, cols // 2 + 110), (255, 255, 255),
                            -1)
                final = cv2.addWeighted(img, 0.1, copy, 0.9, 0)
                cv2.putText(final, 'Most Dominant Colors in the Image', (rows // 2 - 230, cols // 2 - 40),
                            cv2.FONT_HERSHEY_DUPLEX, 0.8, (0, 0, 0), 1, cv2.LINE_AA)
                start = rows // 2 - 220
                for i in range(5):
                    end = start + 70
                    final[cols // 2:cols // 2 + 70, start:end] = p_and_c[i][1]
                    cv2.putText(final, str(i + 1), (start + 25, cols // 2 + 45), cv2.FONT_HERSHEY_DUPLEX, 1,
                                (255, 255, 255), 1, cv2.LINE_AA)
                    start = end + 20
                cv2.imwrite(os.path.join(current_app.config['images'], f_name + '.png'), final)

                if os.path.exists(os.path.join(current_app.config['upload'], f_name + extension)):
                    os.remove(os.path.join(current_app.config['upload'], f_name + extension))
                return jsonify(response={"success": {'output_image': request.host_url + "images/" + f_name + '.png',
                                                    'dominant_colors': p_and_c_list}})
            else:
                return jsonify(error={"Message": "Allowed image types are -> png, jpg, jpeg"}), 404
        else:
            return jsonify(error={"Message": "Unauthorized"}), 401


@dominant_bp.route('/images/<filename>', methods=['GET'])
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
