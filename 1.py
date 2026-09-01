#post flask 

from flask import Flask , request 

app = Flask(__name__)

@app.route("/item" , methods=["POST"])
