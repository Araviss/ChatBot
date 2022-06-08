from flask import Flask, render_template, request, jsonify, render_template
import json
import chatbot

intents = json.loads(open('intents.json').read())

app = Flask(__name__)
@app.route("/")
def index_get():
    return render_template("index.html")

#Sending Javascript Data to Python
@app.route('/postmethod', methods=['POST', 'GET'])
def login():
    user_info = request.get_json()
    ints = chatbot.predict_class(user_info)
    res = chatbot.get_response(ints,intents)
    print(res)
    return jsonify(res)

if __name__== '__main__':
    app.run(debug=True)
