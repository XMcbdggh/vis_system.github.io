from flask import Flask

#app = Flask(__name__)

from APP import create_app

app=create_app()

if __name__ == '__main__':
    app.run(debug=True,port=8081)
