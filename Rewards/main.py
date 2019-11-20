from flask import Flask
import config
import routes

app = Flask(__name__)
app.config.from_object(config)
routes.add_app(app)

if __name__ == '__main__':
    app.run(debug=True)

