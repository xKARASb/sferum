from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService # Similar thing for firefox also!
from subprocess import CREATE_NO_WINDOW


import time, json, ast, requests
import os, websockets, asyncio
from dotenv import load_dotenv

load_dotenv()

auth_cookie = os.getenv("COOKIE")

caps = DesiredCapabilities.CHROME
caps['goog:loggingPrefs'] = {'performance': 'ALL'}
options = webdriver.ChromeOptions()

options.add_argument('--log-level=3')
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36 OPR/97.0.0.0")
options.add_argument("--headless")
options.add_argument('remote-debugging-port=9222')

chrome_service = ChromeService()
chrome_service.creationflags = CREATE_NO_WINDOW

driver = webdriver.Chrome(executable_path="D:\\works\\coding\\python\\sferum\\driver\\chromedriver.exe", options=options, desired_capabilities=caps, service=chrome_service)


print(driver.capabilities) 


def send_msg(text):
  params = {
     "chat_id": "-1001917922644",
     "text": text,
  }
  requests.get("https://api.telegram.org/bot6203980861:AAGs41AffVm4Kib88x5m85kqBnVz8OJCcxI/sendMessage", params=params)

#async with websockets.connect("") as ws:
#  pass

def process_browser_log_entry(entry):
    response = json.loads(entry['message'])['message']
    return response

#def logging(entity: list):
#    for el in entity:
#        print(el)
#        print()
#        print(type(el))
#        if el["url"] == "https://api.vk.me/ruim791593813?version=19&mode=682":
#            pass
          #print(type(el))

          #print(el)
          #print()
#          resp = driver.execute_cdp_cmd('Network.responseReceived', {'requestId': el["params"]["requestId"]})
#          write = f"{el}\n{resp}"
#          with open("log.json", "w") as f:
#              json.dump(write, f)
          


driver.get("https://web.vk.me")

#аунтификация
driver.add_cookie({"name": "remixdsid", "value": auth_cookie, "domain":"web.vk.me", "path":"/", "secure": True})
driver.refresh()

browser_log = driver.get_log('performance')
#events = [process_browser_log_entry(entry) for entry in browser_log]

#for el in events:
#  if el["method"] == "Network.Request":
#    if el['params']["response"]["url"] == "https://api.vk.me/method/account.setOnline?v=5.204":
#        print(el)
#        


while True:
  time.sleep(10)
  browser_log = driver.get_log('performance')
  events = [process_browser_log_entry(entry) for entry in browser_log]
  for el in events:
    if el["method"] == "Network.responseReceived":
      if el['params']["response"]["url"] == "https://api.vk.me/ruim791593813?version=19&mode=682":
        if el["params"].get("requestId", False):
          resp = driver.execute_cdp_cmd('Network.getResponseBody', {'requestId': el["params"]["requestId"]})
          resp["body"] = ast.literal_eval(resp["body"])
          if resp["body"].get("updates", None):
            if len(resp["body"]["updates"][0]) > 5:
              date = requests.get(f'https://helloacm.com/api/unix-timestamp-converter/?cached&s={resp["body"]["updates"][0][5]}').json()
              text = f'{resp["body"]["updates"][0][6]}\n{date}'
              print(text)
              send_msg(text)

