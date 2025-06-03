import os
import random
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import torch
import torch.nn as nn
import torchvision.transforms as transforms
from torchvision.datasets import ImageFolder
from torch.utils.data import DataLoader
from timm import create_model
from PIL import Image

# === Settings ===
DATA_DIR = 'eyepac-light-v2-512-jpg'
BATCH_SIZE = 32
NUM_EPOCHS = 10
NUM_CLASSES = 2
IMAGE_SIZE = 224
MODEL_PATH = 'glaucoma_model.pth'
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

# === Transformations ===
transform = transforms.Compose([
    transforms.Resize((IMAGE_SIZE, IMAGE_SIZE)),
    transforms.ToTensor(),
    transforms.Normalize([0.5, 0.5, 0.5], [0.5, 0.5, 0.5])
])

# === Load Datasets ===
def get_loaders():
    train_dataset = ImageFolder(os.path.join(DATA_DIR, 'train'), transform=transform)
    val_dataset = ImageFolder(os.path.join(DATA_DIR, 'validation'), transform=transform)
    test_dataset = ImageFolder(os.path.join(DATA_DIR, 'test'), transform=transform)

    train_loader = DataLoader(train_dataset, batch_size=BATCH_SIZE, shuffle=True, num_workers=2)
    val_loader = DataLoader(val_dataset, batch_size=BATCH_SIZE, num_workers=2)
    test_loader = DataLoader(test_dataset, batch_size=BATCH_SIZE, num_workers=2)
    return train_loader, val_loader, test_loader

# === Model Setup ===
def setup_model():
    model = create_model('efficientnet_b0', pretrained=True, num_classes=NUM_CLASSES)
    return model

# === Training ===
def train_model():
    train_loader, _, _ = get_loaders()
    model = setup_model().to(device)
    criterion = nn.CrossEntropyLoss()
    optimizer = torch.optim.Adam(model.parameters(), lr=0.001)

    print("Training started...")
    for epoch in range(NUM_EPOCHS):
        model.train()
        running_loss = 0.0
        for images, labels in train_loader:
            images, labels = images.to(device), labels.to(device)
            optimizer.zero_grad()
            outputs = model(images)
            loss = criterion(outputs, labels)
            loss.backward()
            optimizer.step()
            running_loss += loss.item()
        print(f"Epoch [{epoch+1}/{NUM_EPOCHS}], Loss: {running_loss:.4f}")
    
    torch.save(model.state_dict(), MODEL_PATH)
    print("Training complete. Model saved.")

# === Prediction ===
def predict_image(image_path):
    model = setup_model().to(device)
    model.load_state_dict(torch.load(MODEL_PATH, map_location=device))
    model.eval()

    img = Image.open(image_path).convert('RGB')
    img = transform(img).unsqueeze(0).to(device)

    with torch.no_grad():
        output = model(img)
        pred = torch.argmax(output, dim=1).item()

    return "Glaucoma" if pred == 1 else "Normal"

# === Simulate CDR + Treatment Info Based on Prediction ===
def simulate_cdr(prediction):
    if prediction.lower() == "normal":
        # Safe value for normal
        cdr = round(random.uniform(0.2, 0.29), 2)
        severity = "Low (Normal)"
        medicine = "No medication needed"
        doctor_name = ""
        doctor_contact = ""
    else:
        cdr = round(random.uniform(0.3, 0.9), 2)
        if cdr <= 0.6:
            severity = "Moderate (Suspicious)"
            medicine = "Timolol eye drops (0.5%)"
            doctor_name = "Dr. Riya Sen"
            doctor_contact = "9876543210"
        else:
            severity = "High (Glaucoma likely)"
            medicine = "Latanoprost (0.005%) + Brimonidine"
            doctor_name = "Dr. Riya Sen"
            doctor_contact = "9876543210"
    
    return cdr, severity, medicine, doctor_name, doctor_contact

# === Flask App ===
app = Flask(__name__, static_folder='.', static_url_path='')
CORS(app)

@app.route('/')
def serve_index():
    return send_from_directory('.', 'index.html')

@app.route('/favicon.ico')
def favicon():
    return '', 204

@app.route('/predict', methods=['POST'])
def predict():
    if 'image' not in request.files:
        return jsonify({'error': 'No image uploaded'}), 400

    image_file = request.files['image']
    if image_file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    try:
        temp_dir = 'temp'
        os.makedirs(temp_dir, exist_ok=True)
        image_path = os.path.join(temp_dir, 'temp_input.jpg')
        image_file.save(image_path)

        result = predict_image(image_path)
        cdr, severity, medicine, doctor_name, doctor_contact = simulate_cdr(result)

        return jsonify({
            'result': result,
            'cdr': cdr,
            'cdr_severity': severity,
            'medicine': medicine,
            'doctor_name': doctor_name,
            'doctor_contact': doctor_contact
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        try:
            if os.path.exists(image_path):
                os.remove(image_path)
        except:
            pass

if __name__ == '__main__':
    if not os.path.exists(MODEL_PATH):
        print("Model not found. Training now...")
        train_model()
    app.run(host='0.0.0.0', port=5000, debug=True)
