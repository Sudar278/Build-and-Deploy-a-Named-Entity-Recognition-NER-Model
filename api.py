import os
import logging
from flask import Flask, request, jsonify
from transformers import AutoTokenizer, AutoModelForTokenClassification, pipeline
from dotenv import load_dotenv
import numpy as np

# Load environment variables from .env file
load_dotenv()

# Initialize Flask app
app = Flask(__name__)

# Configure logging
logging.basicConfig(
    filename="app.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
console_handler.setFormatter(formatter)
app.logger.addHandler(console_handler)

# Load trained NER model
MODEL_DIR = "./bert-ner-trained"  # Update with your trained model path
try:
    tokenizer = AutoTokenizer.from_pretrained(MODEL_DIR)
    model = AutoModelForTokenClassification.from_pretrained(MODEL_DIR)
    ner_pipeline = pipeline("ner", model=model, tokenizer=tokenizer, aggregation_strategy="simple")
    app.logger.info("Model loaded successfully.")
except Exception as e:
    app.logger.error(f"Error loading model: {str(e)}")
    raise RuntimeError("Failed to load NER model.")

# Load API Key from .env file
API_KEY = os.getenv("API_KEY")

# Verify API Key Function
def verify_api_key(request):
    api_key = request.headers.get("X-API-Key")  # Read API key from headers
    if not api_key:
        app.logger.warning("Missing API key.")
        return jsonify({"detail": "Missing API key"}), 401
    if api_key != API_KEY:
        app.logger.warning(f"Invalid API key received: {api_key}")
        return jsonify({"detail": "Invalid API key"}), 401
    return None  # Return None if API key is valid

# Prediction Route
@app.route("/predict", methods=["POST"])
def predict():
    app.logger.info("Received request: %s", request.json)

    auth_error = verify_api_key(request)
    if auth_error:
        return auth_error  # Return auth error if API key is invalid

    data = request.get_json()
    if not data or "text" not in data:
        app.logger.error("Bad request: Missing text field.")
        return jsonify({"detail": "Text field is required"}), 400

    text = data["text"]
    
    try:
        entities = ner_pipeline(text)

        # Convert np.float32 to native float for JSON serialization
        for entity in entities:
            entity["score"] = float(entity["score"])

        app.logger.info("Response sent successfully.")
        return jsonify({"entities": entities})

    except Exception as e:
        app.logger.error(f"Error during prediction: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500

# Run Flask app
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
