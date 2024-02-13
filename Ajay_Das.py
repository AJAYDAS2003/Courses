import requests
import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
import undetected_chromedriver as uc
import time
from selenium.webdriver.common.by import By

title=[]
timing=[]
duration=[]
start_date=[]
description=[]
course_link=[]
what_will_learn=[]
skills=[]
target_students=[]
content_list=[]
fac1_name=[]
fac2_name=[]
fac1_des=[]
fac2_des=[]
fac1_desc=[]
fac2_desc=[]
institute=[]
usd_fees=[]
inr_fees=[]

headers={'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5)AppleWebKit/605.1.15 (KHTML, like Gecko)Version/12.1.1 Safari/605.1.15'}

driver=uc.Chrome()
driver.get('https://talentedge.com/browse-courses')
time.sleep(7)
try:
    driver.find_element(by=By.XPATH,value='//*[@id="app"]/section/div/div/div/div/div[1]/div/div[2]/div[2]/form/div[3]/div/div[13]/label').click()
except:
    pass
driver.find_element(by=By.XPATH,value='//*[@id="app"]/section/div/div/div/div/div[1]/div/div[2]/div[2]/form/div[3]/div/div[13]/label').click()
time.sleep(5)
web=driver.page_source
driver.close()
page=BeautifulSoup(web)


courses=page.find_all('div',class_='col-md-6')
for course in courses:
    try:
        url = course.find('a', class_='view-all').get('href')
        web2 = requests.get(url,headers=headers).text
        page2 = BeautifulSoup(web2,'lxml')
    except:
        continue

    try:
        title.append(course.find('input').get('data-coursename'))
        timing.append(course.find_all('li')[1].text)
        duration.append(course.find_all('li')[2].text)
        start_date.append(course.find_all('li')[3].text.strip())
    except:
        pass

    try:
        course_link.append(url)
    except:
        course_link.append(np.nan)

    try:
        description.append(page2.find('div', class_='desc_less').find_all('p')[1].text.split('    ')[0][:-1])
    except:
        try:
            description.append(page2.find('div', class_='desc').find_all('p')[0].text.split('    ')[0][:-1])
        except:
            description.append(page2.find('div', class_='desc_less').find_all('p')[1].text.split('    ')[0][:-1])

    try:
        lis1 = page2.find('div', class_='pl-deeper-undstnd to_flex_ul').find_all('li')
        learning_things = ''
        for content in lis1:
            learning_things = learning_things + content.text + ' | '
        what_will_learn.append(learning_things[:-2])
    except:
        what_will_learn.append(np.nan)

    try:
        lis2 = page2.find('div', class_='key-skills-sec').find_all('li')
        learning_skills = ''
        for content in lis2:
            learning_skills = learning_skills + content.text + ' | '
        skills.append(learning_skills[:-2])
    except:
        skills.append(np.nan)

    try:
        target_students.append(page2.find('div', class_='cs-content').find('h4').text.strip())
        contents = page2.find('div', class_='sylab-tab-ul').find_all('li')
        res = ''
        for i in range(1, len(contents) + 1):
            res = res + str(i) + '.' + contents[i - 1].find('a').text.strip() + '\n'
        content_list.append(res)
    except:
        content_list.append('no result')

    faculties = page2.find_all('div', class_='facutly-card')
    if (len(faculties) > 1):
        try:
            fac1_name.append(faculties[0].find('h4').text.strip())
        except:
            fac1_name.append(np.nan)
        try:
            fac1_des.append(faculties[0].find('p').text.strip())
        except:
            fac1_des.append(np.nan)
        try:
            fac1_desc.append(faculties[0].find('a').get('data-description'))
        except:
            fac1_desc.append(np.nan)
        try:
            fac2_name.append(faculties[1].find('h4').text.strip())
        except:
            fac2_name.append(np.nan)
        try:
            fac2_des.append(faculties[1].find('p').text.strip())
        except:
            fac2_des.append(np.nan)
        try:
            fac2_desc.append(faculties[1].find('a').get('data-description'))
        except:
            fac2_desc.append(np.nan)
    else:
        try:
            fac1_name.append(faculties[0].find('h4').text.strip())
            fac2_name.append(np.nan)
        except:
            fac1_name.append(np.nan)
            fac2_name.append(np.nan)
        try:
            fac1_des.append(faculties[0].find('p').text.strip())
            fac2_des.append(np.nan)
        except:
            fac1_des.append(np.nan)
            fac2_des.append(np.nan)
        try:
            fac1_desc.append(faculties[0].find('a').get('data-description'))
            fac2_desc.append(np.nan)
        except:
            fac1_desc.append(np.nan)
            fac2_desc.append(np.nan)

    try:
        institute.append(page2.find('div', class_='plc-institute').find('h4').text.strip())
    except:
        institute.append(np.nan)

    try:
        usd_fees_list = page2.find('div',
                                   class_='program-details-total-pay-amt d-flex align-items-center justify-content-between dolor').find(
            'div', class_='program-details-total-pay-amt-right').text.split('\n')
        usd_fees.append(usd_fees_list[0] + ' ' + usd_fees_list[1].strip() + ' ' + usd_fees_list[2].strip())
    except:
        usd_fees.append(np.nan)

    try:
        inr_fees_list = page2.find('div',
                                   class_='program-details-total-pay-amt d-flex align-items-center justify-content-between ruppes').find(
            'div', class_='program-details-total-pay-amt-right').text.split('\n')
        inr_fees.append(inr_fees_list[0] + ' ' + inr_fees_list[1].strip() + ' ' + inr_fees_list[2].strip())
    except:
        inr_fees.append(np.nan)


dic={
    'Course Link': course_link,
    'Title': title,
    'Description': description,
    'Duration': duration,
    'Timing': timing,
    'Course Start Date': start_date,
    'What you will learn': what_will_learn,
    'Skills': skills,
    'Target Students': target_students,
    'Content': content_list,
    'Faculty 1 Name': fac1_name,
    'Faculty 1 Designation': fac1_des,
    'Faculty 1 Description': fac1_desc,
    'Faculty 2 Name': fac2_name,
    'Faculty 2 Designation': fac2_des,
    'Faculty 2 Description': fac2_desc,
    'Institute Name': institute,
    'Fee in INR': inr_fees,
    'Fee in USD': usd_fees
}


df=pd.DataFrame(dic)
with pd.ExcelWriter('Ajay_Das.xlsx') as writer:
    df.to_excel(writer,sheet_name='sheet_1',index=False)