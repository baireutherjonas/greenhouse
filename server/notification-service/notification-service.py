from flask import Flask, request, jsonify
from os import path
import subprocess
import configparser

class SignalNotificationService():
    """Implement the notification service for Join."""

    def __init__(self, sender_nr, recp_nr, signal_conf_path, signal_cli_path):
        """Initialize the service."""
        self.sender_nr = sender_nr
        self.recp_nr = recp_nr
        self.signal_conf_path = signal_conf_path
        self.signal_cli_path = path.join(signal_cli_path, "signal-cli")

    def send_message(self, message=""):
        """Send a message to a user."""
        mainargs = [self.signal_cli_path]

        mainargs.extend(["--config", self.signal_conf_path])
        

        mainargs.extend(["-u", self.sender_nr, "send"])
        mainargs.extend([self.recp_nr])

        mainargs.extend(["-m", message])

        # Raise an Exception if something goes wrong
        p = subprocess.Popen(mainargs, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        # Wait for completion
        p.wait()
        output, err = p.communicate()
        ret = p.returncode

        if ret != 0:
            raise Exception("Signal Error %d: '%s'" % (ret, err))

        return "Message send successfully", 200

config = configparser.ConfigParser()
config.read("config.ini")

api = Flask(__name__)

@api.route('/sendMessage', methods=['PUT'])
def sendMessage():
    #message = request.args.get('message', '')
    content = request.get_json(silent=True)
    message = content["message"]
    return signalSender.send_message(message)

def __initSignal(sender, recp, conf_path, cli_path):
    """Get the Join notification service."""
    sender_nr = sender
    recp_nr = recp
    signal_cli_path = cli_path
    signal_conf_path = conf_path

    if sender_nr is None or signal_cli_path is None:
        return "Please specify sender_nr and signal_cli_path"
    if recp_nr is None:
        return "recp_nr is required"

    return SignalNotificationService(sender_nr, recp_nr, signal_conf_path, signal_cli_path)

signalSender = __initSignal(config.get('Signal','SENDER'),config.get('Signal','RECP'),config.get('Signal','CONF_PATH'),config.get('Signal','CLI_PATH'))

if __name__ == '__main__':
    api.run(host='0.0.0.0')
