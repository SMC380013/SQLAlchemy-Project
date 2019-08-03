from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/')
def index():
    return (
        f"Available Routes:<br />"
        f"/api/v1.0/precipitation<br />"
        f"/api/v1.0/stations<br />"
        f"/api/v1.0/tobs<br />"
        f"/api/v1.0/<start><br />"
        f"/api/v1.0/<start>/<end><br />"
    )

@app.route('/api/v1.0/precipitation')
def prcp_api():
    return jsonify(     )

if __name__ == "__main__":
    app.run(debug=True)
