import re
import time
import argparse
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException


def open_login(mail, passwd):
    browser = webdriver.Chrome()
    browser.get("https://foxford.ru/user/login")
    email = browser.find_element_by_name("email")
    password = browser.find_element_by_name("password")
    email.send_keys(mail)
    password.send_keys(passwd)
    password.send_keys(Keys.ENTER)
    return browser

def replace_all(text, dct):
    for i, j in dct.items():
        text = text.replace(i, j)
    return text
 
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--email", '-m', help="email for you foxford account")
    parser.add_argument("--password", "-p", help="password for you foxford account")
    parser.add_argument("--url", "-u", help="foxford test url")
    parser.add_argument("--type", "-t", help="type")
    args = parser.parse_args()

    browser = open_login(args.email, args.password)

    confirm = input('Enter Y if you are logged in [y/n]: ')

    if confirm.lower() == 'y':
        if browser.current_url == 'https://foxford.ru/dashboard':
            browser.get(args.url)
            time.sleep(3)

            if args.type == '1':
                fail_element_class_name = browser.find_element_by_xpath("/html/body/div[2]/div[2]/div[2]/div/div/div/div[1]/a[1]").get_attribute("class").split()[3]
                max_score_html = browser.find_element_by_xpath("/html/body/div[2]/div[2]/div[2]/div/div/div/div[2]/div[3]/div/span[3]").get_attribute("innerHTML").split()[1]
                final_text = browser.find_element_by_xpath("/html/body/div[2]/div[2]/div[2]/div/div/div/div[2]/div[1]/div[2]").get_attribute("class").split()[4]
                score_class_name = browser.find_element_by_xpath("/html/body/div[2]/div[2]/div[2]/div/div/div/div[2]/div[3]/div/span[2]").get_attribute("class")

                browser.execute_script("var qwe = document.getElementsByClassName('{0}'); for (var i = 0; i < qwe.length; i++) {{ qwe[i].style.backgroundColor = '#7fc92e'; }}".format(fail_element_class_name))
                browser.execute_script("document.getElementsByClassName('{0}')[1].innerHTML = '<p>Блестяще! Ни одной ошибки. Так держать!</p>'".format(final_text))
                browser.execute_script("document.getElementsByClassName('{0}')[0].style.color = '#7fc92e'; document.getElementsByClassName('{1}')[0].innerHTML = '{2}'".format(score_class_name.split()[4], score_class_name, max_score_html))


            elif args.type == '2':
                try:                                              
                    num_of_questions = browser.find_element_by_xpath("/html/body/div[2]/div[2]/div[2]/div/div/div/div/div[3]/span[2]").get_attribute("innerHTML").split()[0]
                    num_of_max_score = browser.find_element_by_xpath("/html/body/div[2]/div[2]/div[2]/div/div/div/div/div[3]/div[3]/span[2]").get_attribute("innerHTML").split()[0]
                    paper_root_class_name  = browser.find_element_by_xpath("/html/body/div[2]/div[2]/div[2]/div/div/div").get_attribute("class")
                    paper_root_html = browser.find_element_by_xpath("/html/body/div[2]/div[2]/div[2]/div/div/div").get_attribute("innerHTML")
                    final_text = browser.find_element_by_xpath("/html/body/div[2]/div[2]/div[2]/div/div/div/div/div[1]/div[2]/span").get_attribute("class")
                    button_class_name = browser.find_element_by_xpath("/html/body/div[2]/div[2]/div[2]/div/div/div/div/div[4]/button/span").get_attribute("class")

                except NoSuchElementException: 
                    num_of_questions = browser.find_element_by_xpath("/html/body/div[2]/div[2]/div[2]/div/div/div/div/div[2]/span[2]").get_attribute("innerHTML").split()[0]
                    num_of_max_score = browser.find_element_by_xpath("/html/body/div[2]/div[2]/div[2]/div/div/div/div/div[2]/div[3]/span[2]").get_attribute("innerHTML").split()[0]
                    paper_root_class_name  = browser.find_element_by_xpath("/html/body/div[2]/div[2]/div[2]/div/div/div").get_attribute("class")
                    paper_root_html = browser.find_element_by_xpath("/html/body/div[2]/div[2]/div[2]/div/div/div").get_attribute("innerHTML")
                    final_text = browser.find_element_by_xpath("/html/body/div[2]/div[2]/div[2]/div/div/div/div/div[1]/div[2]/span").get_attribute("class")
                    button_class_name = browser.find_element_by_xpath("/html/body/div[2]/div[2]/div[2]/div/div/div/div/div[3]/button/span").get_attribute("class")

                points_score_text = "<div class='EarnedPoints_root__3VROm'><span class='Text_root__3j40U Text_weight-normal__2T_yh Text_lineHeight-m__2YyYN Text_fontStyle-normal__264_c FontSize_fontSize-20__1rxeY Color_color-mineShaft__2PSyK'>Получено баллов</span><div class='PadMarg_margin-left-28__1Bl6g Display_display-inline__306hu'></div><span class='Text_root__3j40U Text_weight-normal__2T_yh Text_lineHeight-m__2YyYN Text_fontStyle-normal__264_c FontSize_fontSize-20__1rxeY Color_color-atlantis__ZZEzG'>{0}</span>&nbsp;<span class='Text_root__3j40U Text_weight-normal__2T_yh Text_lineHeight-m__2YyYN Text_fontStyle-normal__264_c FontSize_fontSize-20__1rxeY Color_color-silver__EB-_4'>| {0}</span></div>".format(num_of_max_score)
                points_class_name = browser.find_element_by_xpath("/html/body/div[2]/div[2]/div[2]/div/div/div/div/div[3]").get_attribute("class")

                quetion_numbers = "".join(
                    "<a href='/trainings/2183/tasks/31901' class='e2e-pick-training-item indicator_indicator__2jzTG indicator_clickable__3K0rP indicator_success__mLwxF indicator_preventUserSelect__1icnx'><span>{0}</span></a>".format(
                        i
                    )
                    for i in range(1, int(num_of_questions) + 1)
                )

                new_root_html = "<div class='indicator_root__xvUCE'>" + quetion_numbers + "</div>" + paper_root_html
                replace_dict = {'\"':'\''}
                html = replace_all(new_root_html, replace_dict)

                browser.execute_script(re.sub("^\s+|\n|\r|\s+$", '', "document.getElementsByClassName('{0}')[0].innerHTML = \"{1}\"; document.getElementsByClassName('{2}')[1].innerHTML = '<p>Блестяще! Ни одной ошибки. Так держать!</p>'; document.getElementsByClassName('{3}')[0].innerHTML = \"{4}\"; document.getElementsByClassName('{5}')[0].innerText = 'Посмотреть задачи'".format(paper_root_class_name, html, final_text, points_class_name, points_score_text, button_class_name)))
            print("ok! Take a screenshot for your teacher!")
            browser.get_screenshot_as_file('results_screen.png')
            while True:
                    continue
    else:
        print('Sorry, but I can’t help.')


if __name__ == "__main__":
    main()