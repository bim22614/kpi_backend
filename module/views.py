from . import app
from flask import jsonify
import datetime


@app.route('/healthcheck', methods=['GET'])
def healthcheck():
  date = datetime.datetime.now()
  status = "OK"

  return jsonify({
    "date": date,
    "status": status
  })
