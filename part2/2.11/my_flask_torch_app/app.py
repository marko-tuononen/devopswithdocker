import io
import os
import json
import uuid

import numpy as np
import torch as torch
import torchvision.models as models
import torchvision.transforms as transforms
from flask import Flask, jsonify, request
from werkzeug.utils import secure_filename
from PIL import Image

import const as c

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = c.UPLOAD_FOLDER

model  = None
labels = None
loader = None

def load_model():
    global model, loader, labels
    model  = models.densenet161(pretrained=True).eval()
    loader = transforms.Compose([
                transforms.Resize(c.IMG_SIZE),
                transforms.CenterCrop(c.IMG_SHAPE),
                transforms.ToTensor(),
                transforms.Normalize(mean=c.IMG_MEAN,std=c.IMG_STD),
             ])
    labels = json.load(io.open("labels.json"))

def get_image_from_request(request, key):
    if not request.files.get(key): 
        return None
    
    # read the image in PIL format
    image = request.files[key].read()
    try:
        return Image.open(io.BytesIO(image))
    except IOError:
        return None     

def prepare_image(image):
    # ensure that format is RGB
    if image.mode != "RGB":
        image = image.convert("RGB")

    # resize and preprocess 
    return loader(image)

@app.route("/persist/<string:label>", methods=["POST"])
def persist(label=None):
    image = get_image_from_request(request, "image")
    if image is None:        
        return jsonify({"error": c.ERROR_IMAGE}), 400

    # separate directory for each label
    label = secure_filename(label)
    path = os.path.join(app.config['UPLOAD_FOLDER'], label)
    if not os.path.exists(path):
        os.makedirs(path)

    # save image with random filename
    filename = str(uuid.uuid4())+c.UPLOAD_SAVE_EXT
    image.save(os.path.join(path,filename))

    return jsonify({ "label": label, "filename": filename })

@app.route("/predict", methods=["POST"])
def predict():
    image = get_image_from_request(request, "image")
    if image is None:
        return jsonify({"error": c.ERROR_IMAGE}), 400

    # preprocess the image and prepare it for classification
    image = prepare_image(image)

    # classify the input image and find top predictions
    with torch.no_grad():
        input = image.unsqueeze(0)
        output = model(input)
        scores, indices = output.topk(c.NUMBER_OF_PREDICTIONS)

    scores = scores.flatten().tolist()
    indices = indices.flatten().tolist()

    # construct and return the classification results
    data = {}
    data["predictions"] = []
    for score, index in zip(scores, indices):
        prediction = { "label": labels[str(index)], "score": score }
        data["predictions"].append(prediction)

    return jsonify(data)

if __name__ == "__main__":
    load_model()
    app.run(debug=c.APP_DEBUG, host=c.APP_HOST)