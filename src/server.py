from flask import Flask, render_template
from threading import Thread
from datetime import datetime, timedelta
import os
import logging

app = Flask(__name__, template_folder='./templates')

# Store the server start time
start_time = datetime.now()

# Set up a custom logger to suppress Werkzeug logs
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)  # Set the logging level to ERROR

@app.route('/')
def main():
    # Calculate uptime and downtime in seconds
    uptime_seconds = (datetime.now() - start_time).total_seconds()
    downtime_seconds = 0  # Assuming downtime is not implemented in your code yet

    # Format the uptime and downtime
    uptime_formatted = format_seconds(uptime_seconds)
    downtime_formatted = format_seconds(downtime_seconds)

    # Format the information for display
    server_info = {
        "Server Start Time": start_time.strftime("%m/%d/%Y, %I:%M:%S %p"),
        "Uptime": uptime_formatted,
        "Downtime": downtime_formatted,
        "Current Date and Time": datetime.now().strftime("%m/%d/%Y, %I:%M:%S %p")
    }

    # Render the template with server_info
    return render_template('index.html', server_info=server_info)

def format_seconds(seconds):
    if seconds < 60:
        return f"{int(seconds)} seconds"
    elif seconds < 3600:
        return f"{int(seconds // 60)} minutes {int(seconds % 60)} seconds"
    elif seconds < 86400:
        return f"{int(seconds // 3600)} hours {int((seconds % 3600) // 60)} minutes {int(seconds % 60)} seconds"
    elif seconds < 2592000:
        return f"{int(seconds // 86400)} days {int((seconds % 86400) // 3600)} hours {int((seconds % 3600) // 60)} minutes {int(seconds % 60)} seconds"
    else:
        return f"{int(seconds // 2592000)} months {int((seconds % 2592000) // 86400)} days {int((seconds % 86400) // 3600)} hours {int((seconds % 3600) // 60)} minutes {int(seconds % 60)} seconds"

def run():
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

def server():
    server = Thread(target=run)
    server.daemon = True  # Set as a daemon thread
    server.start()

if __name__ == '__main__':
    server()