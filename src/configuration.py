import os

ENV_PORT="TRANSCAT_PORT"
ENV_HOST="TRANSCAT_HOST"
ENV_ASSETS_DIR = "TRANSCAT_ASSETS"

class Configuration():
  def __init__(self,config: dict):
    self.serverAddress = os.getenv(ENV_HOST) or config.get('server_address','127.0.0.1')
    self.serverPort = os.getenv(ENV_PORT) or config.get('server_port',8010)
    self.assetsDir = os.getenv(ENV_ASSETS_DIR) or config.get('assets_dir')
    self.appKey = config.get('app_key')
    assert self.appKey, 'app_key must not be empty'
    self.datasource = config.get('datasource')
    self.mode = config.get('mode')
    assert self.mode in ['select','load-balance'], 'mode must be select or load-balance'
    self.loadbalanceRule = config.get('load-balance-rule')
    self.services = config.get('services')
    assert len(self.services) > 0, 'services must not be empty'