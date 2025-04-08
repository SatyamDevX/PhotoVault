from flask import Flask, render_template, request


app = Flask(__name__)


@app.route('/')
def home():
   return render_template('index.html')

@app.route('/', methods=['POST'])
def upload_image():

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





   

if __name__ == "__main__":
   app.run()





