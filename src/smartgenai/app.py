from flask import Flask, jsonify, request
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from smartgenai.ragWrapper import ragWrapper

app = Flask(__name__)

# Route pour récupérer tous les livres
@app.route('/v1/prompt', methods=['POST'])
def send_prompt():
    try:
        postParameters = request.get_json()
        if not postParameters:
            return jsonify({"error": "No configuration provided"}), 400
        myRag = ragWrapper()
        response, outs = myRag.prompt("Do you know pytorch ?", postParameters)
        return jsonify({"response": response,
                        "trace": myRag.trace.getFullJSON(),
                        "output": outs}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Exécuter l'application
if __name__ == '__main__':
    app.run(debug=True)