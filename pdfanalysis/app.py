from flask import Flask, request
import subprocess

app = Flask(__name__)

@app.route("/pdfanalysis", methods=["GET"])
def pdfanalysis():
    user_input = request.args.get("user_input")
    if not user_input:
        return "Error: Input not provided"
    
    pdf_path = '/app/pdf_files/temp.pdf'
    processed_result = subprocess.check_output(['python3', 'pdfanalysis.py', pdf_path])
    processed_result = processed_result.decode('utf-8')
    return processed_result

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=6003)
