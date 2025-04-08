from flask import Flask, render_template, request, flash, redirect
from flask import abort

from werkzeug.exceptions import RequestEntityTooLarge

app = Flask(__name__)

UPLOAD_FOLDER = 'static/uploads/'

app.secret_key = 'secretkey'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16*1024*1024 #16MB

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

def allowed_file(filename):
   return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS



@app.route('/')
def home():
   return render_template('index.html')

@app.route('/', methods=['POST'])
def upload_image():
   #backend validation fo security and correctness, cannot be bypassed.
   if 'file' not in request.files or request.files['file'].filename == '':
      flash("Please select a file.")
      return redirect(request.url)

   file = request.files.get('file')

   if file:
      content = file.read()
      size_bytes = len(content)

      file_info = {
         'filename': file.filename,
         'content_type': file.content_type,
         'size_kb': round(size_bytes / 1024, 2),
         'size_mb': round(size_bytes / (1024 * 1024), 2)
      }

      file.stream.seek(0)  # Reset stream if needed later
      return file_info
   else:
      return {'error': 'No file uploaded'}

# Custom Error Handler for Large Files
@app.errorhandler(RequestEntityTooLarge)
def handle_file_too_large(e):
    return render_template('413.html', message='File too large (16MB max)!'), 413



   

if __name__ == "__main__":
   app.run()





