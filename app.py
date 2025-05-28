from flask import Flask
from flask_smorest import Api, Blueprint
from flask.views import MethodView
from marshmallow import fields, Schema
import uuid
import enum
from datetime import datetime, timezone


app = Flask(__name__)


class APIConfig:
    API_TITLE = "TODO API"
    API_VERSION = "v1"
    OPENAPI_VERSION = "3.1.1"
    OPENAPI_URL_PREFIX = "/"
    OPENAPI_SWAGGER_UI_PATH = "/docs"
    OPENAPI_SWAGGER_UI_URL = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
app.config.from_object(APIConfig)
api = Api(app)

bp = Blueprint("todo", "todo", url_prefix="/todo", description="TODO")

tasks = [
    {
        "id": uuid.UUID("f1b1c14b-db39-4816-a498-4cc76c081d5c"),
        "created": datetime.now(timezone.utc),
        "completed": False,
        "task": "Sandbox"
    }
]

class createTask(Schema):
    task = fields.String()
    
class updateTask(createTask):
    completed = fields.Bool()
    
class task(updateTask):
    id = fields.UUID()
    created = fields.DateTime()
    
    
class listTasks(Schema):
    tasks = fields.List(fields.Nested(task))
    
class sortByEnum(enum.Enum):
    task = "task"
    created = "created"
    
class sortDirectionEnum(enum.Enum):
    asc = "asc"
    desc = "desc"
    
class listTasksParameters(Schema):
    order_by = fields.Enum(sortByEnum, load_default=sortByEnum.created)
    order = fields.Enum(sortDirectionEnum, load_default=sortDirectionEnum.asc)

# collections are a collection of items
@bp.route("/bp")
class collection(MethodView):
    
    @bp.arguments(listTasksParameters, location="query")
    @bp.response(status_code=200, schema=listTasks)
    def get(self, parameters):
        return {"tasks": tasks}
    @bp.arguments(createTask)
    @bp.response(status_code=201, schema=task)
    def post(self, task):
        task["id"] = uuid.uuid4()
        task["created"] = datetime.now(timezone.utc)
        task["completed"] = False
        tasks.append(task)
        return task
    
# singleton is a single item
    

api.register_blueprint(bp)