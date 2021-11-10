import requests
import urllib3
import time
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

s = requests.session()
s.auth = ('sdbox', 'sdbox')
s.verify = False

sws = s.get('https://192.168.11.232/api/openflow/switch/').json()
for sw in sws:
    resp = s.delete(
        f'https://192.168.11.232/api/openflow/switch/{sw["id"]}/')
    print(f"delete sw {sw['name']}: {resp.text}")
time.sleep(5)
resp = s.get(f'https://192.168.11.232/api/serve/rewrite_config')
print(f"rewrite_config:")
print(resp.text)

sws = s.get('https://192.168.11.232/api/openflow/link/').json()
for sw in sws:
    resp = s.delete(
        f'https://192.168.11.232/api/openflow/link/{sw["id"]}/')
    print(f"delete link {sw['id']}: {resp.text}")
time.sleep(5)
resp = s.get(f'https://192.168.11.232/api/serve/rewrite_config')
print(f"rewrite_config:")
print(resp.text)
