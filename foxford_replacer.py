import argparse
import time

from selenium import webdriver
from selenium.webdriver.common.keys import Keys


def start_browser():
    driver = webdriver.Chrome()
    return driver

def open_login(mail, passwd):
    browser = start_browser()
    browser.get("https://foxford.ru/user/login")

    email = browser.find_element_by_name("email")
    password = browser.find_element_by_name("password")

    email.send_keys(mail)
    password.send_keys(passwd)
    password.send_keys(Keys.ENTER)

    return browser

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--email", '-m', help="email for you foxford account")
    parser.add_argument("--password", "-p", help="password for you foxford account")
    parser.add_argument("--url", "-u", help="foxford test url")
    
    args = parser.parse_args()
        
    browser = open_login(args.email, args.password)
    
    confirm = input('Enter Y if you are logged in [y/n]:')
    if confirm.lower() == 'y':
        if browser.current_url == 'https://foxford.ru/dashboard':
            browser.get(args.url)
            fail_element = browser.find_element_by_xpath("/html/body/div[2]/div[2]/div[2]/div/div/div/div[1]/a[1]").get_attribute("class").split()[3]
            time.sleep(3)
            max_count = browser.find_element_by_xpath("/html/body/div[2]/div[2]/div[2]/div/div/div/div[2]/div[3]/div/span[3]").get_attribute("innerHTML").split()[1]
            final_text = browser.find_element_by_xpath("/html/body/div[2]/div[2]/div[2]/div/div/div/div[2]/div[1]/div[2]").get_attribute("class").split()[4]
            browser.execute_script("var qwe = document.getElementsByClassName('{0}'); for (var i = 0; i < qwe.length; i++) {{ qwe[i].style.backgroundColor = '#7fc92e'; }}".format(fail_element))
            browser.execute_script("var text_f = document.getElementsByClassName('{0}')[1].innerHTML = 'Блестяще! Ни одной ошибки. Так держать!'".format(final_text))

            count_html = browser.find_element_by_xpath("/html/body/div[2]/div[2]/div[2]/div/div/div/div[2]/div[3]/div/span[2]").get_attribute("class")

            browser.execute_script("document.getElementsByClassName('{0}')[0].style.color = '#7fc92e'; document.getElementsByClassName('{1}')[0].innerHTML = '{2}'".format(count_html.split()[4], count_html, max_count))
            print("ok! Take a screenshot for your teacher!")
            while True:
                continue
    else:

        print('Sorry, but I can’t help.')


if __name__ == "__main__":
    main()