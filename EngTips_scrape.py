from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager 
from icecream import ic
from bs4 import BeautifulSoup
import requests
import re
import math
from datetime import datetime

# get comments
def scrape_EngTips_qpage(qid: int) -> dict:
    print(qid)
    qid_data = {"question"}

    thread_url = f"https://www.eng-tips.com/viewthread.cfm?qid={qid}"
    req = requests.get(thread_url)
    soup = BeautifulSoup(req.content, "html.parser")

    # get forum info
    nav = soup.find('nav', id='breadcrumbs')
    forum = nav.find_all('a')[-1].text

    # find question information
    question = soup.find("article", class_="question")
    # find original poster 
    question_header = question.find("cite", attrs={"itemprop": "author"})
    author_name = question_header.find("a").text
    author_job = question_header.find("span", attrs={"itemprop": "jobTitle"}).text[1:-1]
    question_date = question.find(attrs={"itemprop": "dateCreated"})["datetime"]
    question_div = question.find("div", attrs={"itemprop": "text"})
    p_element = question_div.find("p")
    if p_element:
        p_element.extract() 
    question_text = question_div.text

    qid_data = {
        "question": {
            "qid": str(qid),
            "forum": forum,
            "author_name": author_name,
            "author_job": author_job,
            "post_date": question_date,
            "text": question_text,
            "scrape_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "comments": []
        }
    }

    # find comment information:
    comment_section = soup.find("section", class_="comments")
    articles = comment_section.find_all("article", attrs={"itemprop": "suggestedAnswer"})


    for article in articles or []:
        comment_id = article["id"].split("-")[1]
        comment_header = article.find("cite", attrs={"itemprop": "author"})
        commenter_name = comment_header.find("span", attrs={"itemprop": "name"}).text
        commenter_job = comment_header.find("span", attrs={"itemprop": "jobTitle"}).text[1:-1]
        comment_date = article.find(attrs={"itemprop": "dateCreated"})["datetime"]
        comment_text_div = article.find("div", attrs={"itemprop": "text"})
        # remove sign off 
        p_element = comment_text_div.find("p")
        if p_element:
            p_element.extract() 
        comment_text = comment_text_div.text

        comment_data = {
            "cid": comment_id,
            "commenter_name": commenter_name,
            "commenter_job": commenter_job,
            "post_date": comment_date,
            "text": comment_text,
            "scrape_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

        qid_data["question"]["comments"].append(comment_data)
    return qid_data

def scrape_qid_range(qid_start: int, qid_end: int):
    return [scrape_EngTips_qpage(qid) for qid in range(qid_start,qid_end+1) if check_qid_exists(qid)]
        
    
    
def find_latest_qid_w_bisection_method(qid_start: int) -> int:
    """
    Finds most recent question ID (qid) with an accuracy of +/- 1
    (Does not need to be 100% accurate because newest questions do not have alot of comments)
    """
    qid_start, qid_end = find_bisection_range(qid_start)
    while (qid_end-qid_start)>2:
        qid_mid = math.floor((qid_start+qid_end)/2)
        ic(qid_mid)
        if check_qid_exists(qid_mid):
            qid_start = qid_mid
            ic(qid_start)
        else:
            qid_end = qid_mid
            ic(qid_end)
    return qid_start
    pass

def find_bisection_range(qid_start: int) -> tuple:
    """
    Finds the range to pass to find_latest_qid_w_bisection_method
    The goal is to have a range where the starting qid exists and the end qid does not 
    """
    #esnure start qid exists
    while not check_qid_exists(qid_start):
        qid_start = int(qid_start/2)
    qid_end = qid_start*2
    #esnure end qid does not exist
    while check_qid_exists(qid_end):
        qid_end = int(qid_end*2)
    return qid_start, qid_end
        
def check_qid_exists(qid: int) -> bool:
    thread_url = f"https://www.eng-tips.com/viewthread.cfm?qid={qid}"
    req = requests.get(thread_url)
    soup = BeautifulSoup(req.content, "html.parser")
    error404 = soup.find("h2", string=re.compile("404 - File or directory not found."))
    if error404:
        return False
    else:
        return True

    


if __name__ == "__main__":
    qid = 515863
    # # # find_latest_qid_w_bisection_method(qid)
    # # print(type(find_bisection_range(6562)))
    qid_data = scrape_qid_range(1002,1010)
    print(qid_data["question"]["comments"])











