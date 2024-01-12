from flask import Flask
import os

app = Flask(__name__)

@app.route('/')
def hello():
    app_key = os.environ.get('APP_KEY')
    if not app_key:
        return "APP_KEY not set!", 500
    return f"Hello, World! APP_KEY is {app_key}", 200

if __name__ == "__main__":
    app.run()
