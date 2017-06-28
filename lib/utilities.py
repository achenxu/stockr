import os
import datetime
import sys
import traceback
import time
import requests
import re

def get_domain(url):
    return re.search(r'//(.*?)/', url + '/').group(1)

def get_relative_path(path):
    script_dir = os.path.dirname(__file__)
    return os.path.join(script_dir, path)

def get_proxies_from_file(proxy_file_name):
    proxies = []
    proxy_file_path = get_relative_path('../proxies/{}'.format(proxy_file_name))
    with open(proxy_file_path) as proxy_file:
        for line in proxy_file.readlines():
            split_line = line.strip('\n').split(':')
            proxy_ip = ':'.join(split_line[0:2])
            if len(split_line) == 4: # Then it's a username/password auth'd proxy
                proxy_ip = '{}:{}@{}'.format(split_line[2], split_line[3], proxy_ip)
            proxy = { # Need to specify both protocols
                'http': 'http://{}'.format(proxy_ip),
                'https': 'https://{}'.format(proxy_ip)
            }
            proxies.append(proxy)
    if not proxies:
        proxies = [{}]
    return proxies

def log(event, log_file_name=None):
    log_time = datetime.datetime.now().strftime('%H:%M:%S:%f')
    log_string = '{} ::: {}'.format(log_time, event)
    sys.stdout.write(log_string + '\n')
    sys.stdout.flush()
    if log_file_name:
        log_file_path = 'logs/{}'.format(log_file_name)
        with open(log_file_path) as log_file:
            log_file.write(log_string + '\n')

def run_until_complete(target=None, args=()):
    result = None
    while not result or (isinstance(result, tuple) and not all(result)):
        try:
            result = target(*args)
        except KeyboardInterrupt:
            log('ERROR ::: SHUT DOWN BY KEYBOARD INTERRUPT')
            sys.exit(1)
        except requests.packages.urllib3.exceptions.NewConnectionError:
            log('ERROR ::: FAILED TO ESTABLISH A NEW CONNECTION')
        except requests.packages.urllib3.exceptions.MaxRetryError:
            log('ERROR ::: MAX RETRIES EXCEEDED')
        except requests.exceptions.ProxyError:
            log('ERROR ::: CANNOT CONNECT TO PROXY')
        except requests.exceptions.ConnectionError:
            log('ERROR ::: CANNOT CONNECT TO PROXY')
        except BrokenPipeError:
            log('ERROR ::: BROKEN PIPE')
        except ConnectionResetError:
            log('ERROR ::: CONNECTION RESET BY PEER')
        except ConnectionRefusedError:
            log('ERROR ::: CONNECTION REFUSED')
        except TimeoutError:
            log('ERROR ::: TIMEOUT ERROR')
        except Exception:
            log('ERROR ::: \n{}'.format(traceback.format_exc()))
        time.sleep(0.01)
    return result
