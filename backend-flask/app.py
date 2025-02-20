import logging
import os
from time import strftime
from flask import Flask, request, got_request_exception
from flask_cors import CORS, cross_origin

# Honeycomb Tracing
from opentelemetry import trace
from opentelemetry.instrumentation.flask import FlaskInstrumentor
from opentelemetry.instrumentation.requests import RequestsInstrumentor
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor, ConsoleSpanExporter, SimpleSpanProcessor

# AWS X-Ray
from aws_xray_sdk.core import xray_recorder
from aws_xray_sdk.ext.flask.middleware import XRayMiddleware

# CloudWatch Logs
import watchtower

# Rollbar
import rollbar
import rollbar.contrib.flask

# Flask App
app = Flask(__name__)

# Initialize logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger("backend-flask")

# Get Rollbar token with debugging
rollbar_access_token = os.getenv('ROLLBAR_ACCESS_TOKEN')
if not rollbar_access_token:
    logger.error("ROLLBAR_ACCESS_TOKEN is not set!")
else:
    logger.info("Rollbar access token is configured")

# Initialize Rollbar
rollbar.init(
    rollbar_access_token,
    environment='production',
    root=os.path.dirname(os.path.realpath(__file__)),
    allow_logging_basic_config=False
)

# send exceptions from `app` to rollbar, using flask's signal system
got_request_exception.connect(rollbar.contrib.flask.report_exception, app)

# Honeycomb Tracing Setup
provider = TracerProvider()
processor = BatchSpanProcessor(OTLPSpanExporter(
    endpoint="https://api.honeycomb.io/v1/traces",
    headers={"x-honeycomb-team": os.getenv('HONEYCOMB_API_KEY')}
))
provider.add_span_processor(processor)

# Console Logging for Debugging
simple_processor = SimpleSpanProcessor(ConsoleSpanExporter())
provider.add_span_processor(simple_processor)

# Set OpenTelemetry Tracer Provider
trace.set_tracer_provider(provider)

# AWS X-Ray Setup
try:
    xray_url = os.getenv("AWS_XRAY_URL")
    xray_daemon_address = os.getenv("AWS_XRAY_DAEMON_ADDRESS", "xray-daemon:2000")

    if xray_url:
        xray_recorder.configure(
            service="backend-flask",
            dynamic_naming=xray_url,
            daemon_address=xray_daemon_address,
            context_missing="LOG_ERROR",
            sampling=False
        )
        XRayMiddleware(app, xray_recorder)
        logger.info(f"AWS X-Ray initialized with daemon address: {xray_daemon_address}")
    else:
        logger.warning("AWS X-Ray is disabled (AWS_XRAY_URL not set)")
except Exception as e:
    logger.error(f"Failed to initialize AWS X-Ray: {str(e)}")

# Initialize Flask Instrumentation
FlaskInstrumentor().instrument_app(app)
RequestsInstrumentor().instrument()

# Import Services
from services.home_activities import *
from services.notifications_activities import *
from services.user_activities import *
from services.create_activity import *
from services.create_reply import *
from services.search_activities import *
from services.message_groups import *
from services.messages import *
from services.create_message import *
from services.show_activity import *

# CORS Setup
frontend = os.getenv('FRONTEND_URL')
backend = os.getenv('BACKEND_URL')
CORS(app, resources={r"/api/*": {"origins": [frontend, backend]}})

@app.route("/api/message_groups", methods=['GET'])
def data_message_groups():
    user_handle = "andrewbrown"
    model = MessageGroups.run(user_handle=user_handle)
    if model['errors']:
        return model['errors'], 422
    return model['data'], 200

@app.route("/api/messages/@<string:handle>", methods=['GET'])
def data_messages(handle):
    user_sender_handle = "andrewbrown"
    user_receiver_handle = request.args.get('user_receiver_handle')
    model = Messages.run(
        user_sender_handle=user_sender_handle,
        user_receiver_handle=user_receiver_handle
    )
    if model['errors']:
        return model['errors'], 422
    return model['data'], 200

@app.route("/api/messages", methods=['POST', 'OPTIONS'])
@cross_origin()
def data_create_message():
    user_sender_handle = "andrewbrown"
    user_receiver_handle = request.json.get('user_receiver_handle')
    message = request.json.get('message')
    model = CreateMessage.run(
        message=message,
        user_sender_handle=user_sender_handle,
        user_receiver_handle=user_receiver_handle
    )
    if model['errors']:
        return model['errors'], 422
    return model['data'], 200

@app.route("/api/activities/home", methods=['GET'])
def data_home():
    data = HomeActivities.run()
    return data, 200

@app.route("/api/activities/notifications", methods=['GET'])
def data_notifications():
    data = NotificationsActivities.run()
    return data, 200

@app.route("/api/activities/@<string:handle>", methods=['GET'])
def data_handle(handle):
    model = UserActivities.run(handle)
    if model['errors']:
        return model['errors'], 422
    return model['data'], 200

@app.route("/api/activities/search", methods=['GET'])
def data_search():
    term = request.args.get('term')
    model = SearchActivities.run(term)
    if model['errors']:
        return model['errors'], 422
    return model['data'], 200

@app.route("/api/activities", methods=['POST', 'OPTIONS'])
@cross_origin()
def data_activities():
    user_handle = "andrewbrown"
    message = request.json.get('message')
    ttl = request.json.get('ttl')
    model = CreateActivity.run(message, user_handle, ttl)
    if model['errors']:
        return model['errors'], 422
    return model['data'], 200

@app.route("/api/activities/<string:activity_uuid>", methods=['GET'])
def data_show_activity(activity_uuid):
    data = ShowActivity.run(activity_uuid=activity_uuid)
    return data, 200

@app.route("/api/activities/<string:activity_uuid>/reply", methods=['POST', 'OPTIONS'])
@cross_origin()
def data_activities_reply(activity_uuid):
    user_handle = "andrewbrown"
    message = request.json.get('message')
    model = CreateReply.run(message, user_handle, activity_uuid)
    if model['errors']:
        return model['errors'], 422
    return model['data'], 200

@app.route("/api/health-check")
def health_check():
    return {"success": True}, 200

@app.route("/api/env-check")
def check_env():
    return {
        "ROLLBAR_ACCESS_TOKEN": bool(os.getenv('ROLLBAR_ACCESS_TOKEN')),
        "token_length": len(os.getenv('ROLLBAR_ACCESS_TOKEN', '')),
        "frontend_url": frontend,
        "backend_url": backend
    }

@app.route('/api/rollbar/test')
def test_rollbar():
    try:
        # Intentionally raise an exception to test Rollbar
        rollbar.report_message('Hello World!', 'warning')
        raise Exception('This is an intentional test exception')
    except Exception as e:
        rollbar.report_exc_info()
        return "Exception reported to Rollbar", 200

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=4567)