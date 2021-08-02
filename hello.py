import json

from flask import Flask

app = Flask(__name__)

test_file = 'new_pages.json'

@app.route("/")
def index():
    print("index() called")

    with open(test_file, 'r') as file:
        label = file.read()

        print(f'file: {label}')

    with open(test_file, 'w') as file:
        json.dump({}, file)


    return label

if __name__ == "__main__":
    app.run(debug=True)