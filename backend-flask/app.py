# app.py
import logging
from flask import Flask
from flask import request
from flask_cors import CORS, cross_origin
import os

# HoneyComb ----------- 
from opentelemetry import trace
from opentelemetry.instrumentation.flask import FlaskInstrumentor
from opentelemetry.instrumentation.requests import RequestsInstrumentor
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.sdk.trace.export import ConsoleSpanExporter, SimpleSpanProcessor

# AWS X-Ray ----------- 
from aws_xray_sdk.core import xray_recorder
from aws_xray_sdk.ext.flask.middleware import XRayMiddleware

#CLOUDWATCH Logs ---------
import watchtower
import logging
from time import strftime

# Configuring Logger to Use CloudWatch
# LOGGER = logging.getLogger(__name__)
# LOGGER.setLevel(logging.DEBUG)
# console_handler = logging.StreamHandler()
# cw_handler = watchtower.CloudWatchLogHandler(log_group='cruddur')
# LOGGER.addHandler(console_handler)
# LOGGER.addHandler(cw_handler)
# LOGGER.info("TEST LOG")

# Initialize logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger('opentelemetry')
logger.setLevel(logging.DEBUG)

# Initialize tracing and an exporter that can send data to Honeycomb
provider = TracerProvider()
processor = BatchSpanProcessor(OTLPSpanExporter(
    endpoint="https://api.honeycomb.io/v1/traces",
    headers={
        "x-honeycomb-team": os.getenv('HONEYCOMB_API_KEY')
    }
))
provider.add_span_processor(processor)

# Show this in the logs within the backend-flask app (STDOUT)
simple_processor = SimpleSpanProcessor(ConsoleSpanExporter())
provider.add_span_processor(simple_processor)

# Set the tracer provider
trace.set_tracer_provider(provider)

# Create Flask app
app = Flask(__name__)

# X-RAY Middleware ---------------
# xray_url = os.getenv("AWS_XRAY_URL", None)
# xray_daemon_address = os.getenv("AWS_XRAY_DAEMON_ADDRESS", None)

# if xray_url and xray_daemon_address:
#    try:
        # Configure X-Ray recorder with local sampling rules
#        xray_recorder.configure(
#            service='backend-flask',
#           dynamic_naming=xray_url,
#            daemon_address=xray_daemon_address,
#            context_missing='LOG_ERROR',
#            sampling=False  # Disable sampling in development
#        )
        # Initialize X-Ray middleware
#        XRayMiddleware(app, xray_recorder)
#        logger.info("AWS X-Ray initialized with daemon address: %s", xray_daemon_address)
#    except Exception as e:
#       logger.warning("Failed to initialize X-Ray: %s", str(e))
       # Configure X-Ray for local development
#        xray_recorder.configure(
#            service='backend-flask',
#            sampling=False,
#            context_missing='LOG_ERROR',
#            daemon_address='xray-daemon:2000',
#            local_mode=True
#        )
#        XRayMiddleware(app, xray_recorder)
#         logger.info("AWS X-Ray initialized in local mode")
# else:
#    logger.info("X-Ray is disabled because AWS_XRAY_URL or AWS_XRAY_DAEMON_ADDRESS is not set")

# Initialize automatic instrumentation with Flask
FlaskInstrumentor().instrument_app(app)
RequestsInstrumentor().instrument()

# Your service imports
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

frontend = os.getenv('FRONTEND_URL')
backend = os.getenv('BACKEND_URL')
origins = [frontend, backend]
cors = CORS(
    app, 
    resources={r"/api/*": {"origins": origins}}, 
    expose_headers="location,link", 
    allow_headers="content-type,if-modified-since", 
    methods="OPTIONS,GET,HEAD,POST"
)

# @app.after_request
# def after_request(response):
 #   timestamp = strftime('[%Y-%b-%d %H:%M]')
 #   LOGGER.error('%s %s %s %s %s %s', timestamp, request.remote_addr, request.method, request.scheme, request.full_path, response.status)
 #   return response


@app.route("/api/message_groups", methods=['GET'])
def data_message_groups():
    user_handle  = 'andrewbrown'
    model = MessageGroups.run(user_handle=user_handle)
    if model['errors'] is not None:
        return model['errors'], 422
    else:
        return model['data'], 200

@app.route("/api/messages/@<string:handle>", methods=['GET'])
def data_messages(handle):
    user_sender_handle = 'andrewbrown'
    user_receiver_handle = request.args.get('user_receiver_handle')

    model = Messages.run(user_sender_handle=user_sender_handle, user_receiver_handle=user_receiver_handle)
    if model['errors'] is not None:
        return model['errors'], 422
    else:
        return model['data'], 200

@app.route("/api/messages", methods=['POST','OPTIONS'])
@cross_origin()
def data_create_message():
    user_sender_handle = 'andrewbrown'
    user_receiver_handle = request.json['user_receiver_handle']
    message = request.json['message']

    model = CreateMessage.run(message=message, user_sender_handle=user_sender_handle, user_receiver_handle=user_receiver_handle)
    if model['errors'] is not None:
        return model['errors'], 422
    else:
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
    if model['errors'] is not None:
        return model['errors'], 422
    else:
        return model['data'], 200

@app.route("/api/activities/search", methods=['GET'])
def data_search():
    term = request.args.get('term')
    model = SearchActivities.run(term)
    if model['errors'] is not None:
        return model['errors'], 422
    else:
        return model['data'], 200

@app.route("/api/activities", methods=['POST','OPTIONS'])
@cross_origin()
def data_activities():
    user_handle  = 'andrewbrown'
    message = request.json['message']
    ttl = request.json['ttl']
    model = CreateActivity.run(message, user_handle, ttl)
    if model['errors'] is not None:
        return model['errors'], 422
    else:
        return model['data'], 200

@app.route("/api/activities/<string:activity_uuid>", methods=['GET'])
def data_show_activity(activity_uuid):
    data = ShowActivity.run(activity_uuid=activity_uuid)
    return data, 200

@app.route("/api/activities/<string:activity_uuid>/reply", methods=['POST','OPTIONS'])
@cross_origin()
def data_activities_reply(activity_uuid):
    user_handle  = 'andrewbrown'
    message = request.json['message']
    model = CreateReply.run(message, user_handle, activity_uuid)
    if model['errors'] is not None:
        return model['errors'], 422
    else:
        return model['data'], 200

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=4567)