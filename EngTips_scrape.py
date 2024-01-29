from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager


driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))


# options = Options()
# options.add_argument('--incognito')
# drtiver_path = "/Applications/Drivers/chromedriver.exe"
qid = "515863"
thread_url = f"https://www.eng-tips.com/viewthread.cfm?qid={qid}"
# driver = webdriver.Chrome(executable_path=drtiver_path)
driver.get(thread_url)

# get forum info
top_nav_bar = driver.find_element(By.ID, "breadcrumbs")
anchors = top_nav_bar.find_elements(By.TAG_NAME, "a")
print(anchors[-1].text)

# get question name
q_name = driver.find_element(By.CLASS_NAME, "threadlink")
print(q_name.text)


# get initial post:
question = driver.find_element(By.CLASS_NAME, "question")
print(question.text)

# get comments







# thread_1_anchor = threads_r0[0].find_element(By.TAG_NAME, "a")
# thread_1_anchor.click()
# for section in sections:
#     print(section.text)


time.sleep(1000)