import flask
import numpy as np
from flask_cors import CORS
from flask import  request, send_file , Response
from PIL import Image
import skimage
import cv2
import io
import base64 




app = flask.Flask(__name__, template_folder='src/templates'
                  ,static_folder='src/static', static_url_path='/')
CORS(app)
cors = CORS(app, resources={r"/*": {"origins": ['http://localhost:5000',"http://127.0.0.1:8000"]}})


@app.route('/')
def main():
    return(flask.render_template('index.html'))

@app.route('/home')
def home():
    return flask.render_template('home.html')

@app.route('/contact')
def contact():
    return flask.render_template('signup.html')

@app.route('/signup')
def signup():
    return flask.render_template('signup.html')

@app.route('/forgot')
def forgot_password():
    return flask.render_template('forgot.html')




@app.route('/apple')
def apple():
    return flask.render_template('apple.html')

@app.route('/potato')
def potato():
    return flask.render_template('potato.html')

@app.route('/strawberry')
def strawberry():
    return flask.render_template('strawberry.html')

@app.route('/equalize_image', methods=['POST'])
def equalize_image():
    # Get the uploaded image data
    img_data = request.files['file'].read()
    # Create a PIL image object from the data
    img = Image.open(io.BytesIO(img_data))
    # Convert the image to grayscale
    img = img.convert('L')
    # Apply equalization to the image
    img_equalized = Image.fromarray(np.uint8(skimage.exposure.equalize_hist(np.array(img)) * 255))
    # Create a buffer to hold the image data
    buffer = io.BytesIO()
    # Save the equalized image data to the buffer
    img_equalized.save(buffer, format='PNG')
    # Return the buffer data as a response
    return Response(buffer.getvalue(), mimetype='image/png')

@app.route('/detect_edges', methods=['POST'])
def edge_detection():
    # Get the uploaded image file
    image_file = request.files['file']
    # Read the image file using OpenCV
    image = cv2.imdecode(np.frombuffer(image_file.read(), np.uint8), cv2.IMREAD_UNCHANGED)
    # Perform edge detection
    edges = cv2.Canny(image, 100, 200)
    # Encode the edge detected image as a JPEG file
    _, jpeg = cv2.imencode('.jpg', edges)
    # Return the edge detected image as a file
    return send_file(
        io.BytesIO(jpeg.tobytes()),
        attachment_filename='edge_detected.jpg',
        mimetype='image/jpeg'
    )

@app.route('/histogram_equalization', methods=['GET', 'POST'])
def histogram_equalization():
    if request.method == 'POST':
        # read the uploaded image and create a histogram
        img = cv2.imdecode(np.fromstring(request.files['file'].read(), np.uint8), cv2.IMREAD_UNCHANGED)
        hist = cv2.calcHist([img], [0], None, [256], [0, 256])
        
        # convert the histogram to an image format suitable for web display
        hist = cv2.normalize(hist, hist, 0, 255, cv2.NORM_MINMAX)
        hist = np.uint8(np.around(hist))
        hist_img = np.zeros((256, 256, 3), np.uint8)
        hist_img[:] = (255, 255, 255)
        hist_max = np.max(hist)
        for i in range(256):
            c1 = i, 256
            c2 = i, 256 - int(hist[i] * 256 / hist_max)
            cv2.line(hist_img, (int(c1[0]), int(c1[1])), (int(c2[0]), int(c2[1])), (0, 0, 0), thickness=1)
        
        # encode the histogram image in PNG format
        hist_encode = cv2.imencode('.png', hist_img)[1]
        hist_bytes = io.BytesIO(hist_encode.tobytes())
        
        # return the histogram image as a response to the client's request
        return send_file(hist_bytes, mimetype='image/png')

# @app.route('/equalize', methods=['POST'])
# def equalize():
#     # read the uploaded image
#     img = request.files['file'].read()

#     # convert the image to grayscale
#     gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

#     # apply histogram equalization to the grayscale image
#     equalized = cv2.equalizeHist(gray)

#     # create a histogram of the equalized image
#     hist = cv2.calcHist([equalized], [0], None, [256], [0, 256])
#     cv2.normalize(hist, hist, 0, 255, cv2.NORM_MINMAX)
#     hist_img = np.zeros((256, 256, 3), np.uint8)
#     hist_img[:] = (255, 255, 255)
#     hist_max = np.max(hist)
#     for i in range(256):
#         x1 = i
#         y1 = 256
#         x2 = i
#         y2 = 256 - int(hist[i] * 256 / hist_max)
#         cv2.line(hist_img, (x1, y1), (x2, y2), (0, 0, 0), thickness=1)

#     # encode the images as PNG format for display on the web page
#     _, img_encoded = cv2.imencode('.png', img)
#     _, equalized_encoded = cv2.imencode('.png', equalized)
#     _, hist_encoded = cv2.imencode('.png', hist_img)

#     # convert the encoded images to base64 strings for display on the web page
#     img_base64 = 'data:image/png;base64,' + str(base64.b64encode(img_encoded))[2:-1]
#     equalized_base64 = 'data:image/png;base64,' + str(base64.b64encode(equalized_encoded))[2:-1]
#     hist_base64 = 'data:image/png;base64,' + str(base64.b64encode(hist_encoded))[2:-1]

#     # render the template with the images
#     return send_file(hist_base64, mimetype='image/png')



if __name__ == '__main__':
    app.run(debug=True)





