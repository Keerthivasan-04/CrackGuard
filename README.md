# 🏗️ CrackGuard - AI Structural Health Monitoring

CrackGuard is a web-based application that uses a trained deep learning model to analyze images of walls, bridges, and other structures for cracks and structural damage. It provides instant results, heatmap visualization, inspection history, and downloadable PDF reports.

---

## ✨ Features

- 🔍 **AI-Powered Crack Detection** - Classifies structural images using a trained TensorFlow CNN model
- 🌡️ **Heatmap Visualization** - Edge-detection overlay highlights the cracked regions
- 📊 **Confidence Gauge** - Visual percentage score indicating damage severity
- 🗂️ **Inspection History** - Logs every analysis with timestamp and result
- 📄 **PDF Report Generation** - Download a professional inspection report with images and recommendations

---

## 🧠 Model

The model (`crack_classifier_model.h5`) is a binary image classifier trained to detect cracks in concrete/surface images.

| Property | Value |
|---|---|
| Input size | 256 × 256 grayscale |
| Output | Sigmoid (0.0 – 1.0) |
| Framework | TensorFlow / Keras |

### Severity Thresholds

| Confidence | Verdict |
|---|---|
| > 70% | 🔴 CRITICAL CRACK DETECTED |
| 40% – 70% | 🟡 MODERATE STRUCTURAL DAMAGE |
| < 40% | 🟢 STRUCTURE SAFE |

---

## 🗂️ Project Structure

```
CrackGuard/
│   app.py                      # Flask backend
│   crack_classifier_model.h5   # Trained Keras model
│   history.json                # Inspection log (auto-generated)
│   report.pdf                  # Last generated PDF report
│
├───static/
│       style.css               # App styling
│       script.js               # Frontend JS
│       uploaded.jpg            # Last uploaded image
│       heatmap.jpg             # Generated heatmap
│
└───templates/
        index.html              # Main UI template
```

---

## 🚀 Getting Started

### Prerequisites

- Python 3.8+
- pip

### Installation

```bash
# Clone the repository
git clone https://github.com/Keerthivasan-04/CrackGuard.git
cd crackguard

# Install dependencies
pip install -r requirements.txt

# Run the app
python app.py
```

Visit `http://127.0.0.1:5000` in your browser.

### Requirements

```
flask
tensorflow
opencv-python
numpy
reportlab
gunicorn
```

---

## 🖥️ Usage

1. Click **Upload Inspection Image** and select a crack image (JPG/PNG).
2. Click **Analyze Structure** to run the AI model.
3. View the **confidence score**, **verdict**, and **heatmap**.
4. Click **Download PDF Report** to save the inspection report.
5. Click **View Inspection History** to review past analyses.

---


## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Backend | Python, Flask |
| ML Model | TensorFlow / Keras |
| Image Processing | OpenCV, NumPy |
| PDF Generation | ReportLab |
| Frontend | HTML, CSS, JavaScript |

---

## 📸 Screenshots

### Home / Upload  
![Home Image](https://github.com/Keerthivasan-04/CrackGuard/blob/22c47ac5e6b06b16e4a31ea1e19f8ba6f5228314/assets/Img_1.png)
![Home Image](https://github.com/Keerthivasan-04/CrackGuard/blob/22c47ac5e6b06b16e4a31ea1e19f8ba6f5228314/assets/Img_2.png)

Upload an image and click **Analyze Structure**

### Analysis Result 
![Home Image](https://github.com/Keerthivasan-04/CrackGuard/blob/22c47ac5e6b06b16e4a31ea1e19f8ba6f5228314/assets/Img_3.png)

Confidence score, heatmap overlay, and severity verdict

---

## 📄 License

This project is developed for educational purposes.

---
