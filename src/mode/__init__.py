from src.mode.loadbalancer import LoadBalancer
from src.mode.select import Select

MODE_DICT = {
  'select': Select,
  'load-balance': LoadBalancer
}