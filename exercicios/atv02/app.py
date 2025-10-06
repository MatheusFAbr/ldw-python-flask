from flask import Flask
from controllers.routes import init_app

app = Flask(__name__, template_folder="views")
app.secret_key = "supersecretkey" 
init_app(app)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=4000, debug=True)
