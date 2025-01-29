from flask import Flask, request, jsonify
import json
import os  # Added for environment variables

app = Flask(__name__)

# Configuration (use environment variables in production)
CERTIFIED = {
    "OpenAI": os.environ.get("OPENAI_API_KEY", "YOUR_OPENAI_API_KEY"),  # ✅ Use env vars
    "DeepPython": {"PMPY": os.environ.get("DEEPPYTHON_KEY", "DEEPPYTHON_KEY")},
    "Google": {
        "CSE_ID": os.environ.get("GOOGLE_CSE_ID", "YOUR_CSE_ID"),
        "api_key": os.environ.get("GOOGLE_API_KEY", "YOUR_GOOGLE_KEY")
    },
    "Self_Core": {
        "model": "GPT-4",
        "device": "cpu"
    }
}

@app.route('/generate', methods=['POST'])
def generate_response():
    try:
        data = request.get_json()  # Explicitly parse JSON
        if not data:
            return jsonify({"error": "No JSON data provided"}), 400
        
        required_fields = ['group', 'si_node', 'input_process', 'language']
        missing = [f for f in required_fields if f not in data]
        if missing:
            return jsonify({"error": f"Missing fields: {missing}"}), 400

        processed_input = process_input(data['input_process'], data['language'])
        
        if data['si_node'].lower() == 'self-core':  # Case-insensitive check
            response = self_core_generated(processed_input)
        else:
            response = hybrid_command(processed_input)
        
        return jsonify({"response": response})

    except json.JSONDecodeError:
        return jsonify({"error": "Invalid JSON format"}), 400
    except KeyError as ke:
        return jsonify({"error": f"Missing key: {str(ke)}"}), 400
    except Exception as e:
        return jsonify({"error": f"Internal Server Error: {str(e)}"}), 500

def process_input(input_data: str, language: str) -> str:
    """Sanitize input (prevents XSS)"""
    sanitized = input_data.strip().lower()
    sanitized = sanitized.replace("<", "&lt;").replace(">", "&gt;")
    return sanitized

def self_core_generated(input_data: str) -> str:
    """Self-Core response logic"""
    model = CERTIFIED["Self_Core"]["model"]
    return f"[{model}] Response: {input_data}"

def hybrid_command(input_data: str) -> str:
    """Hybrid logic (OpenAI + Google APIs)"""
    openai_key = CERTIFIED["OpenAI"]
    google_cse = CERTIFIED["Google"]["CSE_ID"]
    google_api_key = CERTIFIED["Google"]["api_key"]
    return f"Hybrid({openai_key[:5]}... & {google_cse[:5]}... & {google_api_key[:5]}...) Response: {input_data}"

if __name__ == '_main_':
    app.run(host='0.0.0.0', port=5000, debug=False)