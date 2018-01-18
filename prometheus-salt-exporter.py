#!/usr/bin/python
from prometheus_client import start_http_server, Metric, REGISTRY
import time
import salt.client

class ServiceCollector(object):
  def collect(self):
    local = salt.client.LocalClient()
    returns = local.cmd('front*','service.status', ['consul-template'], timeout=1)
    metric = Metric('consul-template up', 'Status', 'gauge')
    for k, v in returns.items():
        metric.add_sample('service_up', value=v, labels={'instance': k, 'service': 'consul-template'})
    yield metric
    
if __name__ == '__main__':
  
  start_http_server(8000)
  REGISTRY.register(ServiceCollector())

  while True: 
     time.sleep(1)
