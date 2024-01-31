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

# get comments
def scrape_EngTips_qpage(qid: int):
    thread_url = f"https://www.eng-tips.com/viewthread.cfm?qid={qid}"
    req = requests.get(thread_url)
    soup = BeautifulSoup(req.content, "html.parser")

    # get forum info
    nav = soup.find('nav', id='breadcrumbs')
    forum_link = nav.find_all('a')[-1].text
    print(forum_link)

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

    print("___QUESTION INFO___")
    print(author_name, author_job, question_date)
    print(question_text)

    # find comment information:
    comment_section = soup.find("section", class_="comments")
    articles = comment_section.find_all("article", attrs={"itemprop": "suggestedAnswer"})

    for article in articles:
        comment_header = article.find("cite", attrs={"itemprop": "author"})
        commenter_name = comment_header.find("a").text
        commenter_job = comment_header.find("span", attrs={"itemprop": "jobTitle"}).text[1:-1]
        comment_date = article.find(attrs={"itemprop": "dateCreated"})["datetime"]
        comment_text_div = article.find("div", attrs={"itemprop": "text"})
        # remove sign off 
        p_element = comment_text_div.find("p")
        if p_element:
            p_element.extract() 
        comment_text = comment_text_div.text
        print("___COMMENT INFO___")
        print(commenter_name, commenter_job, comment_date)
        print(comment_text)

def scrape_qid_range(qid_start: int, qid_end: int):
    for i in range(qid_start,qid_end+1):
        scrape_EngTips_qpage(i)
    
    
def find_latest_qid_w_bisection_method(qid_start):
    qid_start, qid_end = find_bisection_range(qid_start)
    while qid_mid:
        qid_mid = math.floor((qid_start+qid_end)/2)
        print(qid_mid)
        if check_qid_exists(qid_mid):
            qid_start = qid_mid
            print(qid_start)
        else:
            qid_end = qid_mid
            print(qid_end)
    pass

def find_bisection_range(qid_start: int):
    """
    Finds the range to pass to find_latest_qid_w_bisection_method
    The goal is to have a range where the starting qid exists and the end qid does not 
    """
    print(qid_start)
    while not check_qid_exists(qid_start):
        qid_start = int(qid_start/2)
        print(qid_start)
    qid_end = qid_start*2
    while check_qid_exists(qid_end):
        qid_end = int(qid_end*2)
        print(qid_end)
    return qid_start, qid_end
        
def check_qid_exists(qid):
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
    find_bisection_range(6562)
    # scrape_EngTips_qpage(qid)
    # scrape_qid_range(0,5)
    









