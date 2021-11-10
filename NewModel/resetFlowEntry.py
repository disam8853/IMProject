import requests
import urllib3
import time
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

s = requests.session()
s.auth = ('sdbox', 'sdbox')
s.verify = False

sws = s.get('https://192.168.11.232/api/openflow/flowentry/').json()
for sw in sws:
    if sw["priority"] >= 700 and sw["priority"] <= 900:
        resp = s.delete(
            f'https://192.168.11.232/api/openflow/flowentry/{sw["id"]}/')
        print(f"delete flowentry {sw['id']}: {resp.text}")
time.sleep(5)
resp = s.get(f'https://192.168.11.232/api/serve/rewrite_config')
print(f"rewrite_config:")
print(resp.text)
