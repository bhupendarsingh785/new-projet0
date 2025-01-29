# Line 1-2: Correct Flask import and initialization
from flask import Flask, request, jsonify

app = Flask(__name__)  # ✅ Double underscores __name_

# Line 5-13: Configuration fixes
CERTIFIED = {
    "OpenAI": "YOUR_OPENAI_API_KEY",
    "DeepPython": {"PMPY": "DEEPTNINK_KEY"},  # ✅ Fixed structure
    "Google": {
        "CSE_ID": "YOUR_CSE_ID",  # ✅ Correct key name
        "api_key": "YOUR_GOOGLE_KEY"
    },
    "Self_Core": {
        "model": "Microsoft-SQL-2",
        "device": "cpu"
    }
}

# Line 16-33: Route handler with validation
@app.route('/generate', methods=['POST'])
def generate_response():
    try:
        data = request.json
        
        # Check required fields
        required_fields = ['group', 'si_node', 'input_process', 'language']
        if not all(field in data for field in required_fields):
            return jsonify({"error": "Missing required fields"}), 400

        # Process input
        processed_input = process_input(
            input_data=data['input_process'],
            language=data['language']
        )

        # Generate response
        if data['si_node'] == 'self-core':
            response = self_core_generated(processed_input)
        else:
            response = hybrid_command(processed_input)

        return jsonify({"response": response})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Line 36-49: Helper functions
def process_input(input_data: str, language: str) -> str:
    """Sanitize input"""
    return input_data.strip().lower()  # Add custom logic here

def self_core_generated(input_data: str) -> str:
    """Self-Core response"""
    model = CERTIFIED["Self_Core"]["model"]
    return f"{model} Response: {input_data}"

def hybrid_command(input_data: str) -> str:
    """Hybrid logic"""
    openai_key = CERTIFIED["OpenAI"]
    google_cse = CERTIFIED["Google"]["CSE_ID"]  # ✅ Correct key
    return f"Hybrid({openai_key[:5]}... & {google_cse}) Response: {input_data}"

# Line 51-52: Production settings
if __name__ == '__main__':  # ✅ Correct syntax
    app.run(host='0.0.0.0', port=5000, debug=False)