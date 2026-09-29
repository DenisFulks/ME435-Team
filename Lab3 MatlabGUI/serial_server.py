import flask
import plateloader
import threading

app = flask.Flask(__name__, static_url_path='', static_folder='public')

serial_lock = threading.Lock()
loader = plateloader.PlateLoader() # TODO: Set the port if needed

@app.get('/')
def handle_naked_domain():
    return flask.redirect('/index.html')

@app.get('/api/<command>')
def handle_plateloader_commands(command):
    with serial_lock:
        response = loader.send_command(command)
    return response

loader.connect()
app.run(host='0.0.0.0', port=8080, use_reloader=False)
