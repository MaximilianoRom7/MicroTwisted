from MicroTwisted.services import Flask
from MicroTwisted.utils import create_test_routes

app = Flask(__name__)

create_test_routes(app, "service2", 5, True)

if __name__ == '__main__':
    app.run(debug=True)
