from flask import Flask, request
import subprocess

app = Flask(__name__)

@app.route("/email_scrape", methods=["GET"])
def email_scrape():
    user_input = request.args.get("user_input")
    if not user_input:
        return "Error: Input not provided"
    
    processed_result = subprocess.check_output(['python3', 'email_scrapper.py', user_input])
    processed_result = processed_result.decode('utf-8')
    return processed_result

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=6004)
