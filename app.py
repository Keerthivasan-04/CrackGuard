from flask import Flask, render_template, request, send_file
import tensorflow as tf
import numpy as np
import cv2
import os
import json
from datetime import datetime
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import A4

app = Flask(__name__)

MODEL_PATH = "crack_classifier_model.h5"
model = tf.keras.models.load_model(
    MODEL_PATH,
    compile=False,
    safe_mode=False
)

IMG_SIZE = 256
HISTORY_FILE = "history.json"

if not os.path.exists(HISTORY_FILE):
    with open(HISTORY_FILE, "w") as f:
        json.dump([], f)

def generate_heatmap(img):
    edges = cv2.Canny((img*255).astype(np.uint8), 50, 150)
    heatmap = cv2.applyColorMap(edges, cv2.COLORMAP_JET)
    return heatmap

@app.route("/")
def home():
    with open(HISTORY_FILE, "r") as f:
        history = json.load(f)
    return render_template("index.html", history=history)

@app.route("/predict", methods=["POST"])
def predict():
    file = request.files["image"]
    filepath = os.path.join("static", "uploaded.jpg")
    file.save(filepath)

    img = cv2.imread(filepath, cv2.IMREAD_GRAYSCALE)
    img = cv2.resize(img, (IMG_SIZE, IMG_SIZE))
    img = img / 255.0

    input_img = np.expand_dims(img, axis=-1)
    input_img = np.expand_dims(input_img, axis=0)

    prediction = model.predict(input_img)[0][0]
    confidence = round(float(prediction) * 100, 2)

    if confidence > 70:
        result = "CRITICAL CRACK DETECTED"
    elif confidence > 40:
        result = "MODERATE STRUCTURAL DAMAGE"
    else:
        result = "STRUCTURE SAFE"

    heatmap = generate_heatmap(img)
    heatmap_path = os.path.join("static", "heatmap.jpg")
    cv2.imwrite(heatmap_path, heatmap)

    entry = {
        "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "result": result,
        "confidence": confidence
    }

    with open(HISTORY_FILE, "r") as f:
        history = json.load(f)

    history.insert(0, entry)

    with open(HISTORY_FILE, "w") as f:
        json.dump(history, f)

    return render_template("index.html",
                           result=result,
                           confidence=confidence,
                           image_path="static/uploaded.jpg",
                           heatmap_path="static/heatmap.jpg",
                           history=history)

@app.route("/download")
def download():
    pdf_path = "report.pdf"
    doc = SimpleDocTemplate(pdf_path, pagesize=A4)
    elements = []

    # PDF title
    style_title = ParagraphStyle(name='Title', fontSize=20, textColor=colors.darkblue, alignment=1, spaceAfter=20)
    elements.append(Paragraph("AI Structural Health Monitoring Report", style_title))

    # Add images
    elements.append(Image("static/uploaded.jpg", width=4*inch, height=3*inch))
    elements.append(Spacer(1, 0.3 * inch))
    elements.append(Image("static/heatmap.jpg", width=4*inch, height=3*inch))
    elements.append(Spacer(1, 0.3 * inch))

    # Add analysis/recommendation
    style_text = ParagraphStyle(name='Normal', fontSize=12, leading=16, spaceAfter=12)
    with open(HISTORY_FILE, "r") as f:
        history = json.load(f)
    latest = history[0]

    if latest["result"] in ["CRITICAL CRACK DETECTED", "MODERATE STRUCTURAL DAMAGE"]:
        analysis_text = (
            "Based on the analysis of the inspection image, significant cracks were detected "
            "on the structure. Immediate attention is required to assess the structural integrity. "
            "Recommended actions include consulting a structural engineer, performing a detailed "
            "stress analysis, and reinforcing the damaged sections to prevent further deterioration. "
            "Regular monitoring is advised to ensure safety and longevity of the structure. "
            "Preventive maintenance and timely repair can help reduce the risk of structural failure "
            "and ensure the safety of the occupants."
        )
    else:
        analysis_text = "The wall is intact and shows no cracks.\nThis indicates a strong and stable structure, ensuring long-term safety."

    elements.append(Paragraph(analysis_text, style_text))
    doc.build(elements)

    return send_file(pdf_path, as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)