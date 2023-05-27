import argparse,os,json
from src.context import initApplicationContext
from waitress import serve

ENV_PORT="TRANSCAT_PORT"
ENV_HOST="TRANSCAT_HOST"

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

def startWebServer(app,config):
  from src.web.api import translation
  app.register_blueprint(translation.bp)

  address = os.getenv(ENV_HOST) or config.get('server_address','127.0.0.1')
  port = os.getenv(ENV_PORT) or config.get('server_port',8010)
  print(f'transcat is running on {address}:{port}')
  serve(app,host=address,port=port)
  # app.run(host=address,port=port,debug=True,threaded=True)

def main():
  options = getOptions()
  config = loadConfig(options)

  app = initApplicationContext(config)

  startWebServer(app,config)

if __name__ == '__main__':
  main()