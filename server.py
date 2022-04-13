from flask import Flask, jsonify, request, make_response
from dotenv import load_dotenv
import subprocess
import os

load_dotenv()
app = Flask(__name__)
port = os.environ["PORT"]
host = os.environ["HOST"]
host_mac = os.environ["HOST_MAC"]
xAccessToken = os.environ["X_ACCESS_TOKEN"]

powerOnCommand = ["sudo", "/usr/sbin/etherwake",
                  "-i", "wlan0", "-b", host_mac]
powerOffCommand = ["curl", "--interface", "wlan0",
                   "-X", "POST", host + "/poweroff"]


@app.route('/pc', methods=['POST'])
def index():
    command = ""
    message = ""
    try:
        token = request.headers["x-access-token"]
    except:
        message = "Missing x-access-token header."
        return make_response(buildErrorResponse(message), 400)

    if token != xAccessToken:
        message = "Invalid access token header: " + token
        return make_response(buildErrorResponse(message), 401)

    try:
        power = request.json["power"]
        if power == 1:
            command = powerOnCommand
            message = "start the computer"
        elif power == 0:
            command = powerOffCommand
            message = "shutdown the computer"
        else:
            message = "Power value invalid. Must me an integer 1/0 or boolean true/false"
            return make_response(buildErrorResponse(message), 400)

        subprocess.Popen(command, stdout=subprocess.PIPE).communicate()
    except Exception as e:
        message = "Something here didn't go as planned. " + str(e)
        return make_response(buildErrorResponse(message), 500)

    return make_response(buildResponse(message), 200)


def buildResponse(message):
    return jsonify(
        success=1,
        message="Initiated command: " + message
    )


def buildErrorResponse(message):
    return jsonify(
        success=0,
        message=message
    )


app.run(host="localhost", port=port)
