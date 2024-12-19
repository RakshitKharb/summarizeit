# app.py

from flask import Flask, request, render_template, redirect, url_for
import os
from utils.extract_text import extract_text_from_pdf, extract_text_from_txt
from utils.preprocess import preprocess_text
from utils.summarize import initialize_summarizer, summarize_text

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads/'

# Ensure the upload folder exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Initialize the summarizer once to reuse across requests
summarizer = initialize_summarizer()

# Set maximum file size (e.g., 10MB)
app.config['MAX_CONTENT_LENGTH'] = 10 * 1024 * 1024  # 10 MB

ALLOWED_EXTENSIONS = {'pdf', 'txt'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # Check if file is in request
        if 'file' not in request.files:
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(filepath)
            
            # Extract text
            if filepath.endswith('.pdf'):
                text = extract_text_from_pdf(filepath)
            elif filepath.endswith('.txt'):
                text = extract_text_from_txt(filepath)
            else:
                return "Unsupported file format.", 400
            
            # Preprocess text
            cleaned_text = preprocess_text(text)
            
            # Summarize text
            summary = summarize_text(cleaned_text, summarizer)
            
            # Optionally, remove the uploaded file after processing
            os.remove(filepath)
            
            return render_template('result.html', summary=summary)
        else:
            return "Unsupported file format.", 400
    return render_template('upload.html')

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
