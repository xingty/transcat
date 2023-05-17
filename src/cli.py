import argparse,os,json
from src.context import initApplicationContext

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
  from src.web.api.translate import translation
  app.register_blueprint(translation.bp)

  address = config.get('server_address') or '127.0.0.1'
  port = config.get('server_port') or 8010
  app.run(address,port,debug=False,threaded=True)

def main():
  options = getOptions()
  config = loadConfig(options)

  app = initApplicationContext(config)

  startWebServer(app,config)

if __name__ == '__main__':
  main()