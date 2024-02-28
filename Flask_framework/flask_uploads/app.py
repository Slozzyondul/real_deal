from flask import Flask, render_template, request
from flask_uploads import UploadSet, configure_uploads, IMAGES, UploadNotAllowed, TEXT

app = Flask(__name__)

photos =UploadSet('photos', IMAGES)

app.config['UPLOADED_PHOTOS_DEST'] = '/home/solo/Pictures'
app.config['UPLOADED_PHOTOS_ALLOW'] = ['txt', 'py']
app.config['UPLOADED_PHOTOS_DENY'] = ['pdf']
app.config['UPLOADES_DEFAULT_DEST'] ='other'

configure_uploads(app, (photos, docs))

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST' and 'thefile' in request.files:
        try:
            image_filename = photos.save(request.files['thefile'])
            #return '<h1>+photos.path(image_filename)+</h1>'
            return '<h1>+photos.url(image_filename)+</h1>'
        except UploadNotAllowed:
            return '<h1>File is not allowed</h1>'
    return render_template('upload.html')

if __name__ == '__main__':
    app.run(debug=True)   