import flask
import predict_status
import importlib
from flask import render_template
app = flask.Flask(__name__)

@app.route("/")
def root():
    return render_template('index.html')


@app.route("/loadModels/")
def load_model():
    importlib.reload(predict_status)
    return 'True'


@app.route('/predictStatus/', methods=['POST'])
def get_status_predictions():

    data = flask.request.get_json(silent=True)

    prediction = predict_status.predict_status(json_data=data)
    prediction = str(prediction)
    return flask.jsonify({"predicted_status":prediction})

if __name__ == "__main__":
    app.run(threaded=True)
