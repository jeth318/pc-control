from flask import Flask, jsonify
from flask import request
from flask import make_response
from dotenv import load_dotenv
import subprocess
import os

load_dotenv()
app = Flask(__name__)
port = os.environ["PORT"]
host = os.environ["HOST"]
host_mac = os.environ["HOST_MAC"]
powerOnCommand = ["sudo", "/usr/sbin/etherwake",
                  "-i", "wlan0", "-b", host_mac]
powerOffCommand = ["curl", "--interface", "wlan0",
                   "-X", "POST", host + "/poweroff"]


@app.route('/pc', methods=['POST'])
def index():
    power = request.json["power"]
    if power == 1:
        command = powerOnCommand
        infoMessage = "start the computer"
    elif power == 0:
        command = powerOffCommand
        infoMessage = "shutdown the computer"

    print(infoMessage)
    subprocess.Popen(command, stdout=subprocess.PIPE).communicate()

    return make_response(buildResponse(infoMessage))


def buildResponse(message):
    return jsonify(
        success=1,
        message="Initiated command: " + message
    )


app.run(host="localhost", port=port)
