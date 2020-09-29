import argparse
import os 
import time
import pickle
import re
import random
import sys
import urllib.parse

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys


def login (pname):
    print("Performing login")    
    # geckodriver won't save login informations to Firefox profile, so it's useless to specify profile
    driver = webdriver.Firefox()
    driver.get("https://www.instagram.com/accounts/login/?next=%2F"+pname)

    try:
        element = WebDriverWait(driver, 300).until(
            EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/section/nav/div[2]/div/div/div[3]"))
        )
    except:
        print("Driver error. Unable to perform login in.\nTerminating the program!") 
        quit()
    else:        
        if element.text != "":
            print("Unable to perform login in. Are your credentials correct?\nTerminating the program!")
            driver.quit()
            quit()            
        else:
            print("Successfully logged in.")        
            cookies = driver.get_cookies()             
            driver.quit()
            return cookies

def is_logged_in(driver): #TODO INFOhow to use type hints here? it's a class!
    """
        Checking if logged in. 
        locate the upper right element, if the browser is already logged in
        there won't be a text string ("as Log in"), just links with images.
    """
    e = driver.find_element_by_xpath("/html/body/div[1]/section/nav/div[2]/div/div/div[3]")        
    if e.text == "" or e.text.isnumeric():
        return True
    else:
        return False

def getHtmlList(driver, list_lenght):
    """
        expand list of followers/following and return its HTML code
    """
    attempts = 0
    n1 = n = -1

    elems = [] #elements found
    list_area = driver.find_element_by_xpath("//div[contains(@class, 'isgrP')]") 
    totatt = -1 #total attempts
    failatt = 0 #failed attempts
    while(n1 < list_lenght):  #first iteration will always be ran (ranned? correct english term?)
        totatt += 1

        list_area.send_keys(Keys.PAGE_DOWN)       
        list_area.send_keys(Keys.PAGE_DOWN)    #random rnumber of key presses?
        list_area.send_keys(Keys.PAGE_DOWN)         
        #time.sleep (random.randint(0,2)) #time.sleep(0.5)  
        time.sleep(0.5)  
        elems = driver.find_elements_by_xpath("//div[contains(@class, 'isgrP')]//li")
        n1 = len(elems)                

        p = (100/list_lenght) * n1
        nb = (p*50)/100 #num bars; 50 is the progess bar lenght
        bars = int(round(nb)) * '#'
        # T=total, D=downloads, F=Fails
        print(f"\r[{bars:50}] {p:.0f}%  -  T: {list_lenght} | D: {n1} | F: {failatt}", end="")

        if (n1 == list_lenght):
            print()
            break
        #if (n1 < list_lenght and attempts >= 10): #time to give up
        elif (attempts > 8): #time to give up
            raise Exception("Unable to download entire list.")            
        elif (n1 < list_lenght and n1 == n): #no improvements since last iteration.
            failatt += 1
            attempts += 1       
            time.sleep(attempts)
        else:
            attempts = 0
        n = n1         
    print()
    return list_area.get_attribute('innerHTML')

def parse_html_list(html):
    """ Parses an html code containing a list of instagram profiles, which are described between <li> ... </li> tags.
        For every element of the list, it extracts profilename and html code (<li> ... </li>), stripping off the "Follow/Unfollow" button.
        
        Returns:
          a dictionary in the form  {key: "profilename", value = "<li> ..... </li>}
    """
    print("Parsing list... ", end="")
    profiles = dict()

    bs = BeautifulSoup(html, 'html.parser')#'python-lxml') #'html.parser'
    lst = bs.findAll('li')
    for l in lst:
        #picking up first element of generator. 
        #it's ok, since the list has only 1 direct son
        l1 = next(l.children) 
        l2 = list(l1.children)
        #l2 has 2 sons: the iage and text section, and the button section.
        #deleting the button element
        l2[1].extract()
        l3 = list(l2[0].children)
        # l3[0] contains profile's image
        # l3[1] contains "profile name" and "link" to open it
        #l3[1].a.get('href') #this gets me the profile's link, in the form '/goga_asana_london/'
        profilename = l3[1].a.text #profile       
        #str(l): object's html code         
        profiles[profilename] = str (l) #profiles.add(profilename) #if the return value were  a Set()

    print("ok")
    return profiles

def extract_cssLinks(code):
    """ extract all css links from code, and return them as a set().
    """
    #p = re.compile(r"<link href=\"([.\w\/]*\.css)\"") # <link href="/static/bundles/es6/ProfilePageContainer.css/57d0d16bc368.css"
    #ss","151":"/static/bundles/es6/DirectSearchUserContainer.css/ad12791c2bf9.css","152":"/stati
    allcss = re.compile(r"\"([.\w\/]*\.css)\"")
    
    cssLinks = set()
    for link in allcss.findall(code):
        cssLinks.add(urllib.parse.urljoin("http://www.instagram.com/", link))
    return cssLinks

def extract_ul(code):
    """ ectract <ul> tag from code and returns it.
    """
#'<div class="isgrP focus-visible" data-focus-visible-added=""><ul class="jSC57 _6xe7A"><div class="PZuss"><li class="wo9IH"><div class="uu6c_"><div class="t2ksc"><div class="Jv7Aj pZp3x"><div aria-disabled="true" class="RR-M- SAvC5" role="button" tabindex="-1"><canvas class="CfWVH" height="40" style="position: absolute; top: -5px; left: -5px; width: 40px; height: 40px;" width="40"></canvas><a class="_2dbep qNELH kIKUG" href="/taen04/" style="width: 30px; height: 30px;" tabindex="0"><img alt="taen04\'s profile picture" class="_6q-tv" data-testid="user-avatar" draggable="false" src="https://scontent-mrs2-2.cdninstagram.com/v/t51.2885-19/s150x150/117880693_350158106144683_8550162994140597522_n.jpg?_nc_ht=scontent-mrs2-2.cdninstagram.com&amp;_nc_ohc=_qcLxOF9HCIAX_dhuD3&amp;oh=68bf277b1ae826b50501494716189e91&amp;oe=5F8EEC92"/></a></div></div><div class="enpQJ"><div class="d7ByH"><span class="Jv7Aj MqpiF"><a class="FPmhX notranslate _0imsa" href="/taen04/" tabindex="0" title="taen04">taen04</'
    p = re.compile(r"(\<div class=\"isgrP.+?\>)<li")
    
    ul = p.findall(code)
    if(ul == []):
        return ""
    else:
        return ul[0]

def createHtmlPage(listHtml, source, msg):
    """ Creates a html page with listHtml. msg will be placed as title and inside <h1> tags. 
        source will be parsed in order to found CSS classes, so they can me injected on the new page too.
    
        Returns the complete html source code of a web page so the a browser will be able to render listHTML with the relative CSS.
    """

    cssLinks = extract_cssLinks(source)
    div_ul = extract_ul(source)

    html = f""" <!DOCTYPE html>
                <html>
                <head>
                <meta charset="utf-8">
                    <title>{msg}</title>
            """
    for link in cssLinks:
        html +=  f""" <link rel="stylesheet" type = "text/css" href="{link}" ">\n"""
    html += "</head><body>\n"
    html += f"<h1>{msg}</h1>"
    html += div_ul
    html += listHtml
    html += "</body></html>"
    
    return html