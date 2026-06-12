import os
import cv2
import numpy as np
import pytesseract
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
import easyocr
import pyttsx3
import tempfile
import uuid
import json
import sqlite3
import io
from pdf2image import convert_from_path, convert_from_bytes
import PyPDF2
import pkgutil
import importlib.util

# Compatibility shim for Python 3.14+: provide pkgutil.get_loader if missing
if not hasattr(pkgutil, 'get_loader'):
    def _get_loader(name):
        spec = importlib.util.find_spec(name)
        return spec.loader if spec is not None else None
    pkgutil.get_loader = _get_loader

from flask import Flask, render_template, request, jsonify, send_file, redirect, url_for, session
from PIL import Image
from functools import wraps
import hashlib
from gtts import gTTS
import time

# No need to check for PIL version, just handle it in the code where it's used

app = Flask(__name__, static_url_path='/static', static_folder='static')
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['AUDIO_FOLDER'] = 'audio'
app.config['DATABASE'] = 'ocr_tts.db'
app.config['SECRET_KEY'] = 'your-secret-key-here'  # Change this to a secure secret key
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['AUDIO_FOLDER'], exist_ok=True)
os.makedirs('static/images', exist_ok=True)

# Initialize EasyOCR reader
reader = easyocr.Reader(['en'])

# Initialize TTS engine
def get_tts_engine():
    engine = pyttsx3.init()
    return engine

# Database functions
def get_db_connection():
    conn = sqlite3.connect(app.config['DATABASE'])
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    with get_db_connection() as conn:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                email TEXT NOT NULL,
                password TEXT NOT NULL
            )
        ''')
        conn.commit()

# Create tables when the application starts
init_db()

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Authentication decorator
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

# Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        data = request.json
        username = data.get('username')
        password = data.get('password')
        
        if not username or not password:
            return jsonify({'success': False, 'message': 'Username and password are required'})
            
        with get_db_connection() as conn:
            user = conn.execute('SELECT * FROM users WHERE username = ?', (username,)).fetchone()
            
        if user and user['password'] == hash_password(password):
            session['user_id'] = user['id']
            session['username'] = user['username']
            return jsonify({'success': True})
            
        return jsonify({'success': False, 'message': 'Invalid credentials'})
    
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        data = request.json
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')
        
        if not username or not email or not password:
            return jsonify({'success': False, 'message': 'All fields are required'})
            
        hashed_password = hash_password(password)
        
        try:
            with get_db_connection() as conn:
                conn.execute('INSERT INTO users (username, email, password) VALUES (?, ?, ?)',
                            (username, email, hashed_password))
                conn.commit()
            return jsonify({'success': True})
        except sqlite3.IntegrityError:
            return jsonify({'success': False, 'message': 'Username already exists'})
    
    return render_template('register.html')

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    session.pop('username', None)
    return redirect(url_for('index'))

@app.route('/check-auth')
def check_auth():
    return jsonify({'authenticated': 'user_id' in session})

@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')

@app.route('/home')
@login_required
def home():
    return render_template('home.html')

@app.route('/about')
@login_required
def about():
    return render_template('about.html')

@app.route('/contact', methods=['GET', 'POST'])
@login_required
def contact():
    if request.method == 'POST':
        data = request.json
        # TODO: Implement contact form handling
        return jsonify({'success': True})
    
    return render_template('contact.html')

@app.route('/ocr')
@login_required
def ocr():
    return render_template('dashboard.html')

# Existing OCR and TTS routes
@app.route('/upload', methods=['POST'])
@login_required
def upload_file():
    # Ensure upload folder exists
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    # Save the uploaded file
    ext = os.path.splitext(file.filename)[1].lower()
    filename = f"{uuid.uuid4()}{ext}"
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(filepath)

    # If PDF, extract text (try direct text extraction first, then OCR pages)
    if ext == '.pdf':
        text = process_pdf(filepath)

        # Check if text extraction was successful
        if not text or not text.strip():
            return jsonify({
                'error': 'Could not extract text from PDF. The PDF might be corrupted, password-protected, or contain only images without text.',
                'text': '',
                'file_path': filename
            }), 400

        # Generate audio from PDF text
        audio_filename = None
        try:
            audio_filename = text_to_speech(text, {})
        except Exception as e:
            print(f"Error generating audio from PDF text: {e}")
            # Continue even if audio generation fails - text extraction was successful

        return jsonify({
            'text': text,
            'file_path': filename,
            'audio_path': audio_filename,
            'file_type': 'pdf'
        })

    # Otherwise assume an image and process with OCR
    text = process_image(filepath)

    return jsonify({
        'text': text,
        'image_path': filename  # Return just the filename, not the full path
    })

@app.route('/uploads/<path:filename>')
@login_required
def uploaded_file(filename):
    # Remove any 'uploads/' prefix in the filename to avoid duplication
    clean_filename = filename.replace('uploads/', '')
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], clean_filename)
    if os.path.exists(filepath):
        return send_file(filepath)
    else:
        return "File not found", 404

@app.route('/process_region', methods=['POST'])
@login_required
def process_region():
    data = request.json
    image_path = data.get('image_path')
    region = data.get('region')  # [x, y, width, height]
    
    if not image_path or not region:
        return jsonify({'error': 'Missing image path or region'}), 400
    
    # Extract text from the specified region
    text = process_image_region(image_path, region)
    
    return jsonify({'text': text})

@app.route('/speak', methods=['POST'])
@login_required
def speak_text():
    data = request.json
    text = data.get('text')
    voice_settings = data.get('voice_settings', {})
    
    if not text:
        return jsonify({'error': 'No text provided'}), 400
    
    # Generate speech from text
    audio_path = text_to_speech(text, voice_settings)
    
    return jsonify({'audio_path': audio_path})

@app.route('/audio/<filename>')
@login_required
def get_audio(filename):
    return send_file(os.path.join(app.config['AUDIO_FOLDER'], filename))

# Helper functions
def process_image(image_path):
    """Process image with OCR using both Tesseract and EasyOCR for better accuracy"""
    try:
        # Try with Tesseract first
        image = Image.open(image_path)
        # Process image without using ANTIALIAS
        tesseract_text = pytesseract.image_to_string(image)
        
        # If Tesseract result is poor, use EasyOCR
        if len(tesseract_text.strip()) < 10:  # Arbitrary threshold
            # Use EasyOCR
            result = reader.readtext(image_path)
            easyocr_text = ' '.join([entry[1] for entry in result])
            
            # Use the better result
            text = easyocr_text if len(easyocr_text) > len(tesseract_text) else tesseract_text
        else:
            text = tesseract_text
            
        return text.strip()
    except Exception as e:
        print(f"Error processing image: {e}")
        return ""

def process_image_region(image_path, region):
    """Process specific region of an image with OCR"""
    try:
        # Load image and crop to region
        full_image_path = os.path.join(app.config['UPLOAD_FOLDER'], image_path)
        image = cv2.imread(full_image_path)
        if image is None:
            print(f"Error: Could not read image from {full_image_path}")
            return "Image could not be processed"
        
        x, y, width, height = region
        cropped = image[y:y+height, x:x+width]
        
        # Save cropped image temporarily
        temp_path = os.path.join(tempfile.gettempdir(), f"region_{uuid.uuid4()}.png")
        cv2.imwrite(temp_path, cropped)
        
        # Process with OCR
        text = process_image(temp_path)
        
        # Clean up
        os.remove(temp_path)
        
        return text
    except Exception as e:
        print(f"Error processing image region: {e}")
        return ""

def process_pdf(pdf_path):
    """Extract text from a PDF. Try direct text extraction first, then fall back to
    converting pages to images and running OCR on each page."""
    try:
        text = ""

        # Try extracting text with PyPDF2 (works for text-based PDFs)
        try:
            with open(pdf_path, 'rb') as f:
                reader = PyPDF2.PdfReader(f)
                num_pages = len(reader.pages)
                print(f"Processing PDF with {num_pages} page(s)...")
                
                for i, page in enumerate(reader.pages):
                    try:
                        page_text = page.extract_text() or ""
                        if page_text:
                            text += page_text + "\n"
                            print(f"Extracted text from page {i+1}/{num_pages}")
                    except Exception as e:
                        print(f"Error extracting text from page {i+1}: {e}")
                        continue
        except Exception as e:
            print(f"PyPDF2 extraction error: {e}")

        if text.strip():
            print(f"Successfully extracted {len(text)} characters from PDF using direct text extraction")
            return text.strip()

        # If no text found, convert pages to images and OCR each page
        print("No text found in PDF, attempting OCR on pages...")
        try:
            images = convert_from_path(pdf_path)
            print(f"Converted PDF to {len(images)} image(s) for OCR processing")
            page_texts = []
            for i, img in enumerate(images):
                temp_img_path = os.path.join(tempfile.gettempdir(), f"pdf_page_{uuid.uuid4()}.png")
                img.save(temp_img_path, 'PNG')
                page_text = process_image(temp_img_path)
                page_texts.append(page_text)
                print(f"OCR completed for page {i+1}/{len(images)}")
                try:
                    os.remove(temp_img_path)
                except Exception:
                    pass

            combined_text = "\n".join([p for p in page_texts if p])
            if combined_text.strip():
                print(f"Successfully extracted {len(combined_text)} characters from PDF using OCR")
            return combined_text
        except Exception as e:
            error_msg = str(e)
            if "poppler" in error_msg.lower() or "pdftoppm" in error_msg.lower():
                print(f"PDF to image conversion error: {e}")
                print("Note: Poppler may need to be installed for scanned PDF processing")
            else:
                print(f"PDF to image OCR error: {e}")
            return ""

    except Exception as e:
        print(f"Error processing PDF: {e}")
        return ""

def text_to_speech(text, voice_settings):
    """Convert text to speech using pyttsx3 or gTTS based on voice selection"""
    try:
        voice_type = voice_settings.get('voice', 'default')
        
        # Use gTTS for premium voices
        if voice_type in ['obama', 'billgates', 'morgan', 'oprah', 'british', 'australian']:
            return text_to_speech_gtts(text, voice_type)
        
        # Fallback to pyttsx3 for basic voices
        engine = get_tts_engine()
        rate = voice_settings.get('rate', 1.0)
        volume = voice_settings.get('volume', 1.0)
        
        # Get available voices
        voices = engine.getProperty('voices')
        base_rate = engine.getProperty('rate')
        
        # Configure voice parameters based on selection
        if voice_type == 'male' and len(voices) > 0:
            engine.setProperty('voice', voices[0].id)
            engine.setProperty('rate', int(base_rate * rate))
        elif voice_type == 'female' and len(voices) > 1:
            engine.setProperty('voice', voices[1].id)
            engine.setProperty('rate', int(base_rate * rate))
        else:
            # Default voice
            if len(voices) > 0:
                engine.setProperty('voice', voices[0].id)
            engine.setProperty('rate', int(base_rate * rate))
        
        # Set volume
        engine.setProperty('volume', volume)
        
        # Generate audio file
        audio_filename = f"{uuid.uuid4()}.mp3"
        audio_path = os.path.join(app.config['AUDIO_FOLDER'], audio_filename)
        
        engine.save_to_file(text, audio_path)
        engine.runAndWait()
        
        return audio_filename
    except Exception as e:
        print(f"Error converting text to speech: {e}")
        return ""

def text_to_speech_gtts(text, voice_type):
    """Use Google Text-to-Speech for better quality voices"""
    try:
        # Set language and accent based on voice type
        if voice_type == 'british':
            tts = gTTS(text=text, lang='en', tld='co.uk', slow=False)
        elif voice_type == 'australian':
            tts = gTTS(text=text, lang='en', tld='com.au', slow=False)
        elif voice_type == 'obama':
            # Use US accent with slower speed for Obama-like cadence
            tts = gTTS(text=text, lang='en', tld='us', slow=True)
        elif voice_type == 'morgan':
            # Use deep US voice (will sound better than pyttsx3)
            tts = gTTS(text=text, lang='en', tld='us', slow=True)
        elif voice_type == 'oprah':
            # Use US female voice
            tts = gTTS(text=text, lang='en', tld='us', slow=False)
        elif voice_type == 'billgates':
            # Use standard US voice
            tts = gTTS(text=text, lang='en', tld='us', slow=False)
        else:
            # Default to US accent
            tts = gTTS(text=text, lang='en', tld='us', slow=False)
        
        # Generate audio file
        audio_filename = f"{uuid.uuid4()}.mp3"
        audio_path = os.path.join(app.config['AUDIO_FOLDER'], audio_filename)
        
        # Save the file
        tts.save(audio_path)
        
        # Add a small delay to ensure file is properly saved
        time.sleep(0.5)
        
        return audio_filename
    except Exception as e:
        print(f"Error using gTTS: {e}")
        # Fallback to basic TTS if gTTS fails
        engine = get_tts_engine()
        audio_filename = f"{uuid.uuid4()}.mp3"
        audio_path = os.path.join(app.config['AUDIO_FOLDER'], audio_filename)
        engine.save_to_file(text, audio_path)
        engine.runAndWait()
        return audio_filename

if __name__ == '__main__':
    app.run(debug=True) 