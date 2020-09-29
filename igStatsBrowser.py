import os.path
import time
import pickle
import re
import urllib.parse
from configparser import ConfigParser 

from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

import igWebFunctions as igWeb


def main():    
    conf = ConfigParser() 
    conf.read('igStats.ini')
    try:        
        pname = conf["settings"]["Instagram profile"]
        ffp = conf["settings"]["Firefox Profile"]
        dump = conf["settings"]["Dump followers"]        
    except Exception:
        print("Check your configuration file.")
        quit()
    ffoptions = Options()
    ffoptions.add_argument("--headless")
    ffprofile = webdriver.FirefoxProfile(ffp)
    print(f"Account: {pname}")
    print(f"Firefox profile path: {ffp}")   
    driver = webdriver.Firefox(firefox_profile=ffprofile, options=ffoptions)
 
    driver.implicitly_wait(10) 
    profile_url = "https://www.instagram.com/" + pname
    print(f"Fetching: {profile_url}")
    driver.get(profile_url)
    
    if(igWeb.is_logged_in(driver) == False):
        print("Warning. User not logged in")
        driver.quit() #we need a visible browser to perform login        
        cookies = igWeb.login(pname) 
        if cookies == None:
            return
            
        #new headless driver, so I can inject cookies
        #Firefox 78.02 still don't save cookies in the profile,but maybe the will implement it in the future
        driver = webdriver.Firefox(firefox_profile=ffprofile, options=ffoptions)            
        for cookie in cookies: 
            driver.add_cookie(cookie)
        driver.get(profile_url)

    #retrieving followers number    
    ft = driver.find_element_by_xpath(f"//a[@href='/{pname}/followers/']").text
    ft = re.sub("[,.']", "", ft) #remove digit separator
    followersN = int (ft.split()[0])

    #retrieving following number    
    ft = driver.find_element_by_xpath(f"//a[@href='/{pname}/following/']").text
    ft = re.sub("[,.']", "", ft) #remove digit separator
    followingN = int (ft.split()[0])

    print(f"You are following {followingN} profiles.")
    print(f"You have {followersN} followers.")

    #downloading list of followers
    l = driver.find_element_by_xpath(f"//a[@href='/{pname}/followers/']")
    l.click()    
    print('Downloading "followers" list:')
    code = ""
    code = igWeb.getHtmlList(driver, followersN)
    print("Not able to download all list, but never back down ahaha")
    fwers = igWeb.parse_html_list(code)
    fwersSet = set(fwers)

    #downloading list of who I am following
    driver.get(profile_url)
    l = driver.find_element_by_xpath(f"//a[@href='/{pname}/following/']")
    l.click()
    print('Downloading "following" list:')
    code = ""
    code = igWeb.getHtmlList(driver, followingN)
    fwing = igWeb.parse_html_list(code)
    fwingSet = set(fwing)

    #dumping followers to file:
    if dump.lower() == "yes":
        t = time.time()
        filename =  f"followers_{str(t)}.pkl" 
        with open(filename, "wb") as f:
            pickle.dump((t, fwersSet), f)
        print(f"Followers's list saved as {filename}")

    f0 = fwingSet - fwersSet
    f1 = fwersSet - fwingSet

    f0htmlList = ""
    for p in f0:
        f0htmlList += fwing.get(p, "<li> ERROR :( </li>")

    f1htmlList = ""
    for p in f1:
        f1htmlList += fwers.get(p, "<li> ERROR :( </li>")

    source = driver.page_source
    f0html = igWeb.createHtmlPage(f0htmlList, source, "Following - Followers:")  
    f1html = igWeb.createHtmlPage(f1htmlList, source, "Followers - Following:")  

    with open("fwing-fwers.html", "w") as f:
        f.write(f0html)
    print('saved "fwing-fwers.html" to disk.')

    with open("fwers-fwing.html", "w") as f:
        f.write(f1html)
    print('saved "fwers-fwing.html" to disk')

    
    if (driver):
        driver.quit()
 

if __name__ == '__main__':
    main()