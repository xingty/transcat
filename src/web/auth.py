from src.context import applicationContext as app
from src.context import configuration as config
from flask import request,Response
import json

@app.before_request
def doAuth():
  if not request.path.startswith('/api'):
    return

  appKey = getTokenFromHeader(request.headers)
  if appKey is None:
    if request.path == '/api/translate/deeplx/adapter':
       appKey = request.args.get('app_key')
  
  if appKey == config.appKey:
    return

  response = {
    'code': 403,
    'message': 'Unauthorized: invalid app key'
  }
  headers = {'Content-Type': 'application/json'}
  return Response(json.dumps(response), status=403, headers=headers)


def getTokenFromHeader(headers):
  token = None
  if 'Authorization' in headers:
    token = headers['Authorization'].split(' ')[1]
  return token