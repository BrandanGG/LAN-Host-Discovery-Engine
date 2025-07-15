from flask import Flask, request, jsonify
from flask_smorest import Api, Blueprint
from flask.views import MethodView
from marshmallow import fields, Schema, ValidationError
import uuid
import enum
from datetime import datetime, timezone
import json
import os
from db import init_app

app = Flask(__name__)

class Config:
    API_TITLE = "Agent API"
    API_VERSION = "v1"
    OPENAPI_VERSION = "3.1.1"
    OPENAPI_URL_PREFIX = "/"
    OPENAPI_SWAGGER_UI_PATH = "/docs"
    OPENAPI_SWAGGER_UI_URL = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
    DATABASE = "lan_host_discovery.db"

# app and DB setup
app.config.from_object(Config)
api_app = Api(app)
init_app(app)

# In-memory storage (replace with database in production)
agent_data = []

# Schemas
class AgentDataSchema(Schema):
    id = fields.UUID(dump_only=True)
    agent_id = fields.String(required=True)
    data = fields.Dict(required=True)
    timestamp = fields.DateTime(dump_only=True)
    file_name = fields.String()

class AgentDataListSchema(Schema):
    data = fields.List(fields.Nested(AgentDataSchema))

# Agent Blueprint
agent_bp = Blueprint("agent", "agent", url_prefix="/agent/v1", description="Agent API endpoints")
bp = Blueprint("bp", "bp", url_prefix="/display", description="data display")

@agent_bp.route("/upload")
class AgentFileUpload(MethodView):
    #TODO add validation for the JSON file
    #TODO add authentication for the API
    def post(self):
        """Upload JSON file from agent"""
        try:
            # Get JSON data from request
            if request.is_json:
                json_data = request.get_json()
            else:
                return {"error": "Content-Type must be application/json"}, 400
            
            # Validate required fields
            if not json_data.get("agent_id"):
                return {"error": "agent_id is required"}, 400
            
            if not json_data.get("data"):
                return {"error": "data is required"}, 400
            
            # Store the data
            agent_record = {
                "id": str(uuid.uuid4()),
                "agent_id": json_data["agent_id"],
                "data": json_data["data"],
                "timestamp": datetime.now(timezone.utc),
                "file_name": json_data.get("file_name", "uploaded_file.json")
            }
            agent_data.append(agent_record)
            
            return {
                "message": "File uploaded successfully",
                "id": agent_record["id"],
                "timestamp": agent_record["timestamp"]
            }, 201
            
        except Exception as e:
            return {"error": f"Failed to process upload: {str(e)}"}, 500

@bp.route("/")
def index():
    return f"<p>{agent_data}</p>"

# Register blueprints
api_app.register_blueprint(agent_bp)
api_app.register_blueprint(bp)

# Health check endpoint
@app.route('/health')
def health_check():
    return {"status": "healthy", "timestamp": datetime.now(timezone.utc)}

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)