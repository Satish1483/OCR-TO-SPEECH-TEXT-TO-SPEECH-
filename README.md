# OCR & Text-to-Speech Engine

A lightweight and efficient web application that extracts text from **images and PDF files** using Optical Character Recognition (OCR) and converts the extracted text into **natural-sounding speech**.

## 🚀 Features

* 🔍 **Advanced OCR Engine** – Extracts text from images with different fonts, layouts, and orientations.
* 📄 **PDF Support** – Supports both text-based and scanned PDF files.
* 🤖 **Hybrid OCR** – Uses **Tesseract OCR** and **EasyOCR** for improved text recognition.
* 🔊 **Text-to-Speech** – Converts extracted text into speech.
* 🎙️ **Multiple Voice Options** – Supports different voices, accents, speed, and volume settings.
* 🖱️ **User-Friendly Interface** – Easy file upload, OCR processing, and audio playback.
* 🔐 **User Authentication** – Secure user registration and login system.
* ⚡ **Fast Processing** – Optimized for efficient OCR and speech generation.

---

## 🛠️ Technologies Used

| Technology    | Purpose                   |
| ------------- | ------------------------- |
| Python        | Backend Development       |
| Flask         | Web Framework             |
| Tesseract OCR | Text Extraction           |
| EasyOCR       | Advanced OCR              |
| OpenCV        | Image Processing          |
| Pillow        | Image Handling            |
| PyPDF2        | PDF Text Extraction       |
| pdfplumber    | PDF Processing            |
| pdf2image     | Scanned PDF Processing    |
| pyttsx3       | Offline Text-to-Speech    |
| gTTS          | Google Text-to-Speech     |
| SQLite        | User Database             |
| HTML          | Frontend Structure        |
| CSS           | Styling                   |
| JavaScript    | Client-Side Functionality |

---

## 📁 Project Structure

```text
OCR-To-Speech/
│
├── app.py
├── requirements.txt
├── ocr_tts.db
│
├── templates/
│   ├── index.html
│   ├── login.html
│   ├── register.html
│   ├── dashboard.html
│   ├── home.html
│   ├── about.html
│   └── contact.html
│
├── static/
│   ├── css/
│   ├── js/
│   └── images/
│
├── uploads/
│
├── audio/
│
└── .venv/
```

---

# ⚙️ Installation

## 1. Clone the Repository

```bash
git clone https://github.com/Satish1483/OCR-TO-SPEECH.git
```

Navigate to the project folder:

```bash
cd OCR-TO-SPEECH
```

---

## 2. Install Tesseract OCR

### Windows

Install Tesseract OCR and ensure the executable path is configured correctly:

```text
C:\Program Files\Tesseract-OCR\tesseract.exe
```

In `app.py`, configure the path if required:

```python
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
```

### macOS

```bash
brew install tesseract
```

### Linux

```bash
sudo apt install tesseract-ocr
```

---

## 3. Install Poppler (Optional)

Poppler is recommended for processing scanned PDF files.

### Windows

Download and install Poppler, then add it to your system PATH.

### macOS

```bash
brew install poppler
```

### Linux

```bash
sudo apt install poppler-utils
```

---

## 4. Create a Virtual Environment

### Windows

```bash
python -m venv .venv
```

### macOS/Linux

```bash
python3 -m venv .venv
```

---

## 5. Activate the Virtual Environment

### Windows PowerShell

```powershell
.\.venv\Scripts\Activate.ps1
```

### Windows Command Prompt

```cmd
.\.venv\Scripts\activate.bat
```

### macOS/Linux

```bash
source .venv/bin/activate
```

---

## 6. Install Dependencies

```bash
pip install -r requirements.txt
```

Install Google Text-to-Speech:

```bash
pip install gtts
```

---

# ▶️ How to Run

Navigate to the project directory:

```powershell
cd "C:\Users\YourUsername\OneDrive\Documents\OCR-To-Speech\Aa18"
```

Activate the virtual environment:

```powershell
..\ .venv\Scripts\Activate.ps1
```

Then run the Flask application:

```bash
python app.py
```

Alternatively, run it directly:

```powershell
cd "C:\Users\YourUsername\OneDrive\Documents\OCR-To-Speech"
& ".\.venv\Scripts\python.exe" ".\Aa18\app.py"
```

After starting the application, open your browser and visit:

```text
http://127.0.0.1:5000
```

---

# 💻 Usage

## 1. Register or Login

Create a new account or log in using an existing account.

## 2. Upload a File

The application supports:

* PNG
* JPG
* JPEG
* PDF

## 3. Extract Text

For images, the system uses OCR to extract text.

For PDFs:

* Text-based PDFs are processed directly.
* Scanned PDFs are converted into images and processed using OCR.

## 4. Convert Text to Speech

After extracting the text:

* Select a voice.
* Adjust speech speed.
* Adjust volume.
* Click **Convert to Speech**.

The generated audio can then be played using the built-in audio player.

---

# 🎙️ Voice Options

The application supports:

* Default Voice
* Male Voice
* Female Voice
* Different accents and language options through Google Text-to-Speech.

Voice availability may depend on the operating system and installed speech engines.

---

# 🔧 Troubleshooting

## Tesseract Not Found

Make sure Tesseract OCR is installed and the path is correctly configured:

```python
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
```

---

## Module Not Found Error

Activate your virtual environment and reinstall dependencies:

```bash
pip install -r requirements.txt
```

You can verify installed packages using:

```bash
pip list
```

---

## PDF Processing Issues

For scanned PDFs, make sure **Poppler** is installed correctly.

Text-based PDFs can usually be processed without Poppler.

---

## Port Already in Use

Change the port in `app.py`:

```python
app.run(debug=True, port=5001)
```

Then open:

```text
http://127.0.0.1:5001
```

---

# 📌 Future Improvements

* Support for more languages.
* Improved voice customization.
* Cloud-based OCR integration.
* Download generated audio files.
* OCR accuracy improvements.
* Dark mode support.
* Deployment using Docker or cloud platforms.

---

# 👨‍💻 Author

**Satish Hanji**

GitHub: `https://github.com/Satish1483`

---

## ⭐ Support

If you like this project, please consider giving the repository a **star ⭐**.
