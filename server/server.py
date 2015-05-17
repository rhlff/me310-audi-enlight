from flask import Flask, render_template
import signal
import sys

from leds import teardown_led_controller
from blueprints.working_light import working_light
from blueprints.beat_detection import beat_detection


app = Flask(__name__)


blueprints = [working_light, beat_detection]
for bp in blueprints:
    app.register_blueprint(bp, url_prefix=bp.url_prefix)


@app.route('/')
def dashboard():
    settings = map(lambda bp: bp.as_json(), blueprints)
    print settings
    return render_template('dashboard.html', settings=settings)


# teardown method
def signal_handler(signal, frame):
        teardown_led_controller()
        sys.exit(0)
signal.signal(signal.SIGINT, signal_handler)
