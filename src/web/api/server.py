import json
from flask import Blueprint,render_template
from src.web.server_state import getServerState

bp = Blueprint('server', __name__)

@bp.route('/api/server/status',methods=['GET'])
def serverState():
  return getServerState()

@bp.route('/',methods=['GET'])
def index():
  data = getServerState()
  return render_template('index.html',data=json.dumps(data))