OCR & Text-to-Speech Engine
A lightweight, efficient application that extracts text from images and PDF files, then converts it to natural-sounding speech.

Features
Advanced OCR Engine: Accurately extracts text from diverse image formats regardless of font, layout, or orientation
PDF Support: Extract text from PDF files (both text-based and scanned PDFs)
Hybrid OCR Approach: Combines Tesseract and EasyOCR for optimal accuracy
Premium TTS System: Natural-sounding speech with customizable voices, speeds, and volume
Multiple Voice Options: Includes premium Google TTS voices (Obama, Bill Gates, Morgan Freeman, Oprah, British, Australian accents)
Intuitive UI: Drag-and-drop file upload, region selection, and audio playback controls
User Authentication: Secure login and registration system
Low Latency: Optimized for fast processing and output
Requirements
Python 3.7+ (Python 3.14 tested)
Tesseract OCR installed on your system (see installation instructions below)
Poppler (optional, for scanned PDF processing)
Installation
Step 1: Install System Dependencies
Tesseract OCR
Windows: Download and install from https://github.com/UB-Mannheim/tesseract/wiki
Default installation path: C:\Program Files\Tesseract-OCR\tesseract.exe
macOS: brew install tesseract
Linux: sudo apt install tesseract-ocr
Poppler (for PDF processing - Optional but Recommended)
Windows: Download from https://github.com/oschwartz10612/poppler-windows/releases/
Extract and add to PATH, or pdf2image will use it automatically if in the same directory
macOS: brew install poppler
Linux: sudo apt install poppler-utils
Step 2: Set Up Python Environment
Navigate to the project directory:

cd Aa18
Create a virtual environment (recommended):

# Windows
python -m venv ..\.venv

# macOS/Linux
python3 -m venv ../venv
Activate the virtual environment:

# Windows PowerShell
..\.venv\Scripts\Activate.ps1

# Windows Command Prompt
..\.venv\Scripts\activate.bat

# macOS/Linux
source ../venv/bin/activate
Install required Python packages:

pip install -r requirements.txt
pip install gtts  # Google Text-to-Speech (for premium voices)
How to Run
Method 1: Using Python Directly
Activate your virtual environment (if using one):

# Windows PowerShell
..\.venv\Scripts\Activate.ps1

# Windows Command Prompt
..\.venv\Scripts\activate.bat

# macOS/Linux
source ../venv/bin/activate
Run the Flask application:

python app.py
Open your browser and navigate to:

http://127.0.0.1:5000
Method 2: Using Virtual Environment Python Directly
Windows:

cd Aa18
..\.venv\Scripts\python.exe app.py
macOS/Linux:

cd Aa18
../venv/bin/python app.py
Usage
Start the application (see "How to Run" above)

Access the web interface: Open http://127.0.0.1:5000 in your browser

Register/Login:

Create a new account or log in with existing credentials
You'll be redirected to the dashboard after login
Upload Files:

Images: Drag and drop or click to upload image files (PNG, JPG, etc.)
PDFs: Upload PDF files - text will be extracted automatically and converted to speech
The system supports both text-based PDFs and scanned PDFs (via OCR)
For Images:

Text is automatically extracted using OCR
Optionally select a specific region for targeted OCR
Adjust voice settings and click "Convert to Speech"
For PDFs:

Text is automatically extracted (direct text extraction or OCR for scanned PDFs)
Audio is automatically generated
Play the audio using the audio player
Voice Options:

Default, Male, Female voices (using pyttsx3)
Premium voices: Obama, Bill Gates, Morgan Freeman, Oprah, British, Australian (using Google TTS)
Project Structure
OCR-To-Speech/
│
├── app.py                      # Main Flask application
├── requirements.txt            # Python dependencies
├── ocr_tts.db                  # SQLite database (auto-created)
│
├── templates/
│   ├── index.html              # Landing page
│   ├── login.html              # Login page
│   ├── register.html           # Registration page
│   ├── dashboard.html          # OCR & Text-to-Speech page
│   ├── home.html               # Home page
│   ├── about.html              # About page
│   └── contact.html            # Contact page
│
├── static/
│   ├── css/
│   ├── js/
│   └── images/
│
├── uploads/                    # Uploaded images & PDFs
│
├── audio/                      # Generated speech files
│
└── .venv/                      # Python virtual environment
Troubleshooting
Tesseract Not Found
Ensure Tesseract is installed and the path in app.py (line 5) matches your installation
Windows default: C:\Program Files\Tesseract-OCR\tesseract.exe
PDF Processing Issues
For scanned PDFs, ensure Poppler is installed
Text-based PDFs work without Poppler
Check console output for specific error messages
Module Not Found Errors
Ensure virtual environment is activated
Run pip install -r requirements.txt again
Verify all packages are installed: pip list
Port Already in Use
Change the port in app.py (last line):
app.run(debug=True, port=5001)  # Use a different port
Technologies Used
OCR: Tesseract OCR, EasyOCR
PDF Processing: PyPDF2, pdf2image, pdfplumber
TTS: pyttsx3, gTTS (Google Text-to-Speech)
Image Processing: OpenCV, PIL (Pillow)
Backend: Flask
Database: SQLite
Frontend: HTML, CSS, JavaScript
Notes
The application runs in debug mode by default (for development)
For production, use a production WSGI server like Gunicorn or uWSGI
EasyOCR will use CPU mode if CUDA/GPU is not available (slower but functional)
Audio files are stored in the audio/ directory
Uploaded files are stored in the uploads/ directory
cd "c:\Users\LATITUDE 5420 I7\OneDrive\Documents\OCR-To-Speech"; & "c:/Users/LATITUDE 5420 I7/OneDrive/Documents/OCR-To-Speech/.venv/Scripts/Activate.ps1"; cd Aa18; python app.py
