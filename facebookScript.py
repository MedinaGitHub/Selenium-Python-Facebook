from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
import geckodriver_autoinstaller
import time
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import asyncio

async def login(driver, email, password):
    wait = WebDriverWait(driver, 10)
    driver.get('https://m.facebook.com/')
    email_input = driver.find_element_by_xpath('//*[@id="m_login_email"]')
    email_input.send_keys(email)
    password_input = driver.find_element_by_xpath(
        '//*[@id="m_login_password"]')
    password_input.send_keys(password)
    login_btn = driver.find_element_by_xpath(
        '/html/body/div[1]/div/div[2]/div[1]/div/div/div[2]/div/div[3]/form/div[5]/div[1]/button')
    login_btn.click()
    wait.until(EC.url_changes('https://m.facebook.com/'))
    return driver


async def navigateTargetPage(driver, facebookTargetPage):
    driver.get(facebookTargetPage)
    time.sleep(3)


async def insertText(driver, txt):
    driver.find_element_by_xpath(
        '//div[@aria-label="Escribe un comentario"]').send_keys(txt)


async def insertMention(driver, mention):
    driver.find_element_by_xpath(
        '//div[@aria-label="Escribe un comentario"]').send_keys(mention)
    time.sleep(3)
    actions = ActionChains(driver)  # Action Chains)
    actions.send_keys(Keys.ENTER)  # Press ENTER
    actions.perform()  # To perfrom all the operations in the action chains
    time.sleep(3)


async def insertImage(driver, img):
    imgArea = driver.find_element_by_xpath(
        '//input[@accept="video/*,  video/x-m4v, video/webm, video/x-ms-wmv, video/x-msvideo, video/3gpp, video/flv, video/x-flv, video/mp4, video/quicktime, video/mpeg, video/ogv, .ts, .mkv, image/*, image/heic, image/heif"]')
    imgArea.send_keys(img)
    time.sleep(5)


async def submit(driver):
    driver.find_element_by_xpath(
        '//div[@aria-label="Escribe un comentario"]').send_keys(' ')
    actionSubmit = ActionChains(driver)  # Action Chains)
    # Press ENTER to post the content on facebook
    actionSubmit.send_keys(Keys.ENTER)
    actionSubmit.perform()  # To perfrom all the operations in the action chains
    time.sleep(4)


async def scriptFacebook(email, password, txt, mention, img, facebookTargetPage):

    geckodriver_autoinstaller.install()
    driver = webdriver.Firefox()

    await login(driver, email, password)
    await navigateTargetPage(driver, facebookTargetPage)
    await insertText(driver, txt)
    if mention : await insertMention(driver, mention)
    if img: await insertImage(driver, img)
    await submit(driver)

    driver.quit()
    return 'success'


async def main():
    email = 'some@gmail.com'
    password = 'somePass'
    txt = 'Hola amigo '
    mention = '@Sebastian'
    img = '/home/sebastian/Escritorio/image.png'
    facebookTargetPage = 'https://www.facebook.com/profile.php?id={someID}'
    await scriptFacebook(email, password, txt, mention, img, facebookTargetPage)

asyncio.run(main())