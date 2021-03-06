import flask
from flask import Flask
from sklearn.linear_model import LogisticRegression
import numpy as np
import pandas as pd

#--------- MODEL IN MEMORY --------------#
# Read the scientific data on breast cancer survival, 
# Build a LogisticRegression predictor on it

patients = pd.read_csv("haberman.data", header=None)
patients.columns = ['age', 'year', 'nodes', 'survived']
patients = patients.replace(2, 0) # the value 2 means death in 5 years

X = patients[['age', 'year', 'nodes']]
Y = patients['survived']
PREDICTOR = LogisticRegression().fit(X,Y)




#--------- URLs and WEB PAGES -----------#
app = Flask(__name__)

# this is a decorator
@app.route("/")

def viz_page():
    """
    Homepage:  server our visualization page, awesome.html
    """
    with open("awesome.html", 'r') as viz_file:
         return viz_file.read()


# Get an example and return its score from the predictor model
@app.route("/score", methods=["POST"])
def score():
    """
    When a POST request with JSON data is made to this url,
    read the example from the JSON, predict probability and
    send it with a response
    """
    # Get decision score for our example that came with the request
    data = flask.request.json
    x = np.matrix(data["example"])
    score = PREDICTOR.predict_proba(x)
    
    # Put the result in a nice dict so we can send it as a json
    results = {"score": score[0,1]}
    return flask.jsonify(results)


if __name__ == "__main__":
    app.run(debug = True, host='0.0.0.0')



