import argparse,os,json
from src import context
from waitress import serve
from flask import Flask

def loadConfig(options):
  path = options.config
  if not os.path.exists(path):
    raise FileNotFoundError(f"Config file not found: {path}")

  with open(path) as f:
    return json.load(f)


def getOptions():
  parser = argparse.ArgumentParser()
  parser.add_argument(
    '--config',
    type=str,
    dest='config',
    help="path to config file",
  )

  return parser.parse_args()

def startWebServer(app: Flask,config):
  from src.web.api import translation,server
  app.register_blueprint(translation.bp)
  app.register_blueprint(server.bp)

  address = config.serverAddress
  port = config.serverPort
  print(f'transcat is running on {address}:{port}')
  serve(app,host=address,port=port)
  # app.run(host=address,port=port,debug=True,threaded=True)

def main():
  options = getOptions()
  config = loadConfig(options)

  configuration = context.initConfiguration(config)
  app = context.initApplicationContext(configuration)
  startWebServer(app,configuration)

if __name__ == '__main__':
  main()