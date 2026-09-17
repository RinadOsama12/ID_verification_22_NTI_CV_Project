# 🪪 AI-Based ID Verification System

An AI-powered identity verification system that verifies a user's identity by analyzing an uploaded ID document and a selfie.

The system combines **YOLOv8**, **DeepFace with FaceNet512**, and **EasyOCR**, with **FastAPI** providing the backend API and **ngrok** enabling public access to the local API.

---
## 🚀 Live Demo

Try the deployed application here:

👉 **[Open ID Verification System](https://idverification22nticvproject-4sqvhhr4mqr2un6y8qvuak.streamlit.app/)**

The system allows you to:

* 🪪 Upload your ID
* 🤳 Take a selfie
* 🔍 Detect ID information using YOLOv8
* 👤 Verify your identity using DeepFace + FaceNet512
* 📝 Extract your name, address, and ID number using EasyOCR

> **Note:** Camera access may require allowing camera permissions in your browser.



## 🚀 System Overview

The user provides:

1. 🪪 **An ID document image**
2. 🤳 **A selfie**

The system then:

* Detects relevant information and the face on the ID using **YOLOv8**
* Extracts the ID face
* Compares the ID face with the selfie using **DeepFace / FaceNet512**
* Uses a **cosine-distance threshold of 0.39** for the face verification decision
* Extracts information such as **name, address, and ID number** using **EasyOCR**
* Provides the results through a **Streamlit interface**
* Uses **FastAPI** as the backend API
* Uses **ngrok** to expose the local FastAPI server through a public URL

---

## 🏗️ System Architecture

```text
                 👤 User
                   │
          ┌────────┴────────┐
          │                 │
      🪪 ID Image        🤳 Selfie
          │                 │
          ▼                 │
       YOLOv8               │
          │                 │
     ┌────┴─────┐           │
     │          │           │
 Face Detection │           │
     │      ID Information │
     │          │           │
     ▼          ▼           │
 Face Crop   Text Crops     │
     │          │           │
     │          ▼           │
     │       EasyOCR        │
     │          │           │
     │     Name / Address   │
     │      / ID Number     │
     │                       │
     ▼                       ▼
 DeepFace / FaceNet512
          │
          │ Face Comparison
          │
          ▼
   Cosine Distance
      Threshold: 0.39
          │
          ▼
   ┌───────────────┐
   │ Verification  │
   │    Result     │
   └───────────────┘
          │
          ▼
      Streamlit UI
```

---

## 🧠 Technologies Used

| Technology     | Purpose                                   |
| -------------- | ----------------------------------------- |
| **YOLOv8**     | Detects the face and relevant ID fields   |
| **DeepFace**   | Face verification framework               |
| **FaceNet512** | Face recognition/embedding model          |
| **EasyOCR**    | Extracts text from ID fields              |
| **FastAPI**    | Backend REST API                          |
| **Streamlit**  | User interface                            |
| **ngrok**      | Exposes the local FastAPI server publicly |
| **OpenCV**     | Image processing                          |
| **Python**     | Main programming language                 |

---

## 🔍 How It Works

### 1. Upload ID

The user uploads a picture of their ID document.

YOLOv8 processes the image and detects the relevant regions, including:

* Face
* Name
* Address
* ID number

The detected regions are cropped from the original image.

---

### 2. Take a Selfie

The user takes a selfie using the application's camera interface.

The selfie is sent to the FastAPI backend together with the uploaded ID.

---

### 3. Face Detection with YOLOv8

YOLOv8 is used to detect the face region on the ID.

The detected face is cropped and passed to the face verification stage.

The YOLO model also detects the regions containing the user's information.

---

### 4. Face Verification

The ID face and selfie are compared using:

**DeepFace + FaceNet512**

The system uses the **cosine distance** between the generated face embeddings.

The current verification threshold is:

```text
Threshold = 0.39
```

The decision is based on the configured threshold:

```text
distance ≤ 0.39
        ↓
    Verified

distance > 0.39
        ↓
 Not Verified
```

> **Note:** The threshold of 0.39 is a project-specific configuration and should ideally be calibrated and validated using genuine and impostor face pairs for a production system.

---

### 5. OCR Information Extraction

After YOLO detects the relevant text regions, the cropped regions are passed to **EasyOCR**.

The OCR system supports:

* 🇬🇧 English
* 🇪🇬 Arabic

The system extracts:

```text
Name
Address
ID Number
```

---

## 🔌 Backend API

The backend is implemented using **FastAPI**.

Main endpoint:

```text
POST /verify-face
```

The endpoint receives:

```text
id_image
selfie
```

and returns information such as:

```json
{
    "verified": true,
    "id_detected": true,
    "face_distance": 0.28,
    "threshold": 0.39,
    "yolo_confidence": 0.87,
    "name": "...",
    "address": "...",
    "id_number": "..."
}
```

---

## 🌐 Public Access with ngrok

During development, FastAPI runs locally:

```text
http://localhost:8000
```

ngrok is used to expose the FastAPI server through a public URL:

```text
Local FastAPI
      ↓
   ngrok
      ↓
Public HTTPS URL
```

This allows the Streamlit application and other users to communicate with the locally running FastAPI backend.

---

## 🖥️ User Interface

The Streamlit interface provides two main sections:

### 🔐 Identity Verification

The user can:

* Upload an ID
* Take a selfie
* Start verification
* View the verification result
* View face distance and threshold

### 📄 Extracted ID Information

After processing, the application displays:

* Name
* Address
* ID Number

---

## 📁 Project Structure

```text
ID_verification_22_NTI_CV_Project/
│
├── app/
│   ├── app.py
│   ├── model.py
│   ├── face_verification.py
│   ├── ocr.py
│   └── streamlit_app.py
│
├── models/
│   └── best.pt
│
├── test_ocr.py
├── requirements.txt
└── README.md
```

---

## ⚙️ Installation

Clone the repository:

```bash
git clone <YOUR_GITHUB_REPOSITORY_URL>
cd ID_verification_22_NTI_CV_Project
```

Create a virtual environment:

```bash
python -m venv .venv
```

Activate it on Windows:

```powershell
.venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## ▶️ Running the Project

### Start FastAPI

```bash
python -m uvicorn app.app:app --reload
```

FastAPI will run on:

```text
http://localhost:8000
```

### Start Streamlit

In another terminal:

```bash
streamlit run app/streamlit_app.py
```

The Streamlit application will normally run on:

```text
http://localhost:8501
```

### Start ngrok

To expose FastAPI:

```bash
ngrok http 8000
```

Copy the generated public HTTPS URL and use it as the API URL in the Streamlit application.

---

## 🔄 Complete Processing Pipeline

```text
User
 │
 ├── Upload ID
 │
 └── Take Selfie
       │
       ▼
   Streamlit
       │
       ▼
    FastAPI
       │
       ▼
     YOLOv8
       │
       ├───────────────┐
       │               │
       ▼               ▼
   ID Face         ID Fields
       │               │
       │               ▼
       │            EasyOCR
       │               │
       │        Name / Address /
       │          ID Number
       │
       ▼
 DeepFace
 FaceNet512
       │
       ▼
 Face Embeddings
       │
       ▼
 Cosine Distance
       │
       ▼
 Threshold = 0.39
       │
       ▼
 Verification Result
       │
       ▼
    Streamlit
       │
       ▼
   Final Result
```

---

## 🔒 Security Considerations

This project is intended for educational and demonstration purposes.

For production deployment, additional security measures would be required, including:

* Secure handling of uploaded identity documents
* Encryption of sensitive data
* Authentication and authorization
* Secure API communication
* Input validation
* Rate limiting
* Protection against spoofing and presentation attacks
* Liveness detection
* Proper biometric threshold calibration
* Avoiding unnecessary storage of ID images and selfies

---

## 🎯 Project Goal

The goal of this project is to demonstrate how multiple AI technologies can be combined into an end-to-end identity verification pipeline:

**Object Detection → Face Verification → OCR → API → Web Application**

The project demonstrates the integration of computer vision, deep learning, OCR, backend development, and web deployment into a single practical application.


## 🚀 System Overview

The user provides:

1. 🪪 **An ID document image**
2. 🤳 **A selfie**

The system then:

* Detects relevant information and the face on the ID using **YOLOv8**
* Extracts the ID face
* Compares the ID face with the selfie using **DeepFace / FaceNet512**
* Uses a **cosine-distance threshold of 0.39** for the face verification decision
* Extracts information such as **name, address, and ID number** using **EasyOCR**
* Provides the results through a **Streamlit interface**
* Uses **FastAPI** as the backend API
* Uses **ngrok** to expose the local FastAPI server through a public URL

---

## 🏗️ System Architecture

```text
                 👤 User
                   │
          ┌────────┴────────┐
          │                 │
      🪪 ID Image        🤳 Selfie
          │                 │
          ▼                 │
       YOLOv8               │
          │                 │
     ┌────┴─────┐           │
     │          │           │
 Face Detection │           │
     │      ID Information │
     │          │           │
     ▼          ▼           │
 Face Crop   Text Crops     │
     │          │           │
     │          ▼           │
     │       EasyOCR        │
     │          │           │
     │     Name / Address   │
     │      / ID Number     │
     │                       │
     ▼                       ▼
 DeepFace / FaceNet512
          │
          │ Face Comparison
          │
          ▼
   Cosine Distance
      Threshold: 0.39
          │
          ▼
   ┌───────────────┐
   │ Verification  │
   │    Result     │
   └───────────────┘
          │
          ▼
      Streamlit UI
```

---

## 🧠 Technologies Used

| Technology     | Purpose                                   |
| -------------- | ----------------------------------------- |
| **YOLOv8**     | Detects the face and relevant ID fields   |
| **DeepFace**   | Face verification framework               |
| **FaceNet512** | Face recognition/embedding model          |
| **EasyOCR**    | Extracts text from ID fields              |
| **FastAPI**    | Backend REST API                          |
| **Streamlit**  | User interface                            |
| **ngrok**      | Exposes the local FastAPI server publicly |
| **OpenCV**     | Image processing                          |
| **Python**     | Main programming language                 |

---

## 🔍 How It Works

### 1. Upload ID

The user uploads a picture of their ID document.

YOLOv8 processes the image and detects the relevant regions, including:

* Face
* Name
* Address
* ID number

The detected regions are cropped from the original image.

---

### 2. Take a Selfie

The user takes a selfie using the application's camera interface.

The selfie is sent to the FastAPI backend together with the uploaded ID.

---

### 3. Face Detection with YOLOv8

YOLOv8 is used to detect the face region on the ID.

The detected face is cropped and passed to the face verification stage.

The YOLO model also detects the regions containing the user's information.

---

### 4. Face Verification

The ID face and selfie are compared using:

**DeepFace + FaceNet512**

The system uses the **cosine distance** between the generated face embeddings.

The current verification threshold is:

```text
Threshold = 0.39
```

The decision is based on the configured threshold:

```text
distance ≤ 0.39
        ↓
    Verified

distance > 0.39
        ↓
 Not Verified
```

> **Note:** The threshold of 0.39 is a project-specific configuration and should ideally be calibrated and validated using genuine and impostor face pairs for a production system.

---

### 5. OCR Information Extraction

After YOLO detects the relevant text regions, the cropped regions are passed to **EasyOCR**.

The OCR system supports:

* 🇬🇧 English
* 🇪🇬 Arabic

The system extracts:

```text
Name
Address
ID Number
```

---

## 🔌 Backend API

The backend is implemented using **FastAPI**.

Main endpoint:

```text
POST /verify-face
```

The endpoint receives:

```text
id_image
selfie
```

and returns information such as:

```json
{
    "verified": true,
    "id_detected": true,
    "face_distance": 0.28,
    "threshold": 0.39,
    "yolo_confidence": 0.87,
    "name": "...",
    "address": "...",
    "id_number": "..."
}
```

---

## 🌐 Public Access with ngrok

During development, FastAPI runs locally:

```text
http://localhost:8000
```

ngrok is used to expose the FastAPI server through a public URL:

```text
Local FastAPI
      ↓
   ngrok
      ↓
Public HTTPS URL
```

This allows the Streamlit application and other users to communicate with the locally running FastAPI backend.

---

## 🖥️ User Interface

The Streamlit interface provides two main sections:

### 🔐 Identity Verification

The user can:

* Upload an ID
* Take a selfie
* Start verification
* View the verification result
* View face distance and threshold

### 📄 Extracted ID Information

After processing, the application displays:

* Name
* Address
* ID Number

---

## 📁 Project Structure

```text
ID_verification_22_NTI_CV_Project/
│
├── app/
│   ├── app.py
│   ├── model.py
│   ├── face_verification.py
│   ├── ocr.py
│   └── streamlit_app.py
│
├── models/
│   └── best.pt
│
├── test_ocr.py
├── requirements.txt
└── README.md
```

---

## ⚙️ Installation

Clone the repository:

```bash
git clone <YOUR_GITHUB_REPOSITORY_URL>
cd ID_verification_22_NTI_CV_Project
```

Create a virtual environment:

```bash
python -m venv .venv
```

Activate it on Windows:

```powershell
.venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## ▶️ Running the Project

### Start FastAPI

```bash
python -m uvicorn app.app:app --reload
```

FastAPI will run on:

```text
http://localhost:8000
```

### Start Streamlit

In another terminal:

```bash
streamlit run app/streamlit_app.py
```

The Streamlit application will normally run on:

```text
http://localhost:8501
```

### Start ngrok

To expose FastAPI:

```bash
ngrok http 8000
```

Copy the generated public HTTPS URL and use it as the API URL in the Streamlit application.

---

## 🔄 Complete Processing Pipeline

```text
User
 │
 ├── Upload ID
 │
 └── Take Selfie
       │
       ▼
   Streamlit
       │
       ▼
    FastAPI
       │
       ▼
     YOLOv8
       │
       ├───────────────┐
       │               │
       ▼               ▼
   ID Face         ID Fields
       │               │
       │               ▼
       │            EasyOCR
       │               │
       │        Name / Address /
       │          ID Number
       │
       ▼
 DeepFace
 FaceNet512
       │
       ▼
 Face Embeddings
       │
       ▼
 Cosine Distance
       │
       ▼
 Threshold = 0.39
       │
       ▼
 Verification Result
       │
       ▼
    Streamlit
       │
       ▼
   Final Result
```

---

## 🔒 Security Considerations

This project is intended for educational and demonstration purposes.

For production deployment, additional security measures would be required, including:

* Secure handling of uploaded identity documents
* Encryption of sensitive data
* Authentication and authorization
* Secure API communication
* Input validation
* Rate limiting
* Protection against spoofing and presentation attacks
* Liveness detection
* Proper biometric threshold calibration
* Avoiding unnecessary storage of ID images and selfies

---

## 🎯 Project Goal

The goal of this project is to demonstrate how multiple AI technologies can be combined into an end-to-end identity verification pipeline:

**Object Detection → Face Verification → OCR → API → Web Application**

The project demonstrates the integration of computer vision, deep learning, OCR, backend development, and web deployment into a single practical application.

