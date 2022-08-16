import cv2
import undetected_chromedriver
import time
import easyocr
import requests
from selenium.webdriver.support.select import Select

import api.credential_processor as creds

if __name__ == '__main__':

    user = creds.user_init()
    browser = undetected_chromedriver.Chrome()
    url = 'https://www.vfsglobal.ca/IRCC-AppointmentWave1/Account/RegisteredLogin'
    browser.get(url)
    time.sleep(5)


    def set_credentials() -> None:
        username_input = browser.find_element('id', 'EmailId')
        username_input.clear()
        username_input.send_keys(user.get(creds.EMAIL))
        time.sleep(2)
        password_input = browser.find_element('id', 'Password')
        password_input.clear()
        password_input.send_keys(user.get(creds.PASSWORD))
        time.sleep(2)


    def process_captcha() -> any:
        captcha = browser.find_element('id', 'CaptchaImage')
        captcha_image = captcha.screenshot_as_png

        with open('image.png', 'wb') as f:
            f.write(captcha_image)

        captcha_file = 'image.png'
        img = cv2.imread(captcha_file)
        reader = easyocr.Reader(['en'], gpu=False, verbose=False)

        return reader.readtext(img)


    def set_captcha_to_form(text: str) -> None:
        captcha_input = browser.find_element('id', 'CaptchaInputText')
        captcha_input.send_keys(text)


    def check_validation_error() -> bool:
        try:
            error = browser.find_element('xpath', "//div[@class='validation-summary-errors']")
            if error.is_displayed():
                return False
            return True
        except:
            return True


    def is_captcha_read() -> bool:
        set_credentials()
        result = process_captcha()
        for (bbox, text, prob) in result:
            if prob >= 0.5:
                set_captcha_to_form(text)
                time.sleep(3)
                submit = browser.find_element('xpath', "//input[@type='submit']")
                submit.click()
                return check_validation_error()
            return False


    def schedule_appointment() -> None:
        button = browser.find_element('xpath', "//*[text()='Schedule Appointment']")
        button.click()
        time.sleep(3)
        select_center_lviv()
        set_applicants()
        set_agree_check_box()
        applicant_submit()
        add_applicant()
        add_new_applicant()


    def select_center_lviv() -> None:
        select = browser.find_element('id', 'LocationId')
        drop_down = Select(select)
        drop_down.select_by_visible_text('Canada Visa Application Center - Lviv')
        time.sleep(3)


    def set_applicants() -> None:
        select = browser.find_element('id', 'NoOfApplicantId')
        drop_down = Select(select)
        drop_down.select_by_visible_text('1')
        time.sleep(3)


    def set_agree_check_box() -> None:
        checkbox = browser.find_element('id', 'IAgree')
        checkbox.click()
        time.sleep(3)


    def applicant_submit() -> None:
        submit = browser.find_element('id', 'btnContinue')
        submit.click()
        time.sleep(3)


    def add_applicant() -> None:
        button = browser.find_element('xpath', "//*[text()='Add Applicant']")
        button.click()
        time.sleep(20)


    def add_new_applicant() -> None:
        ircc_input = browser.find_element('id', 'BILNumber')
        ircc_input.clear()
        ircc_input.send_keys(user.get(creds.IRCC))
        time.sleep(3)
        birthday_input = browser.find_element('id', 'DateOfBirth')
        birthday_input.clear()
        birthday_input.send_keys(user.get(creds.BIRTHDAY))
        time.sleep(3)
        submit = browser.find_element('id', 'submitbuttonId')
        submit.click()
        time.sleep(10)
        browser.switch_to.alert.accept()
        time.sleep(15)
        continue_button = browser.find_element('xpath', "//input[@type='submit']")
        continue_button.click()
        time.sleep(15)


    def init() -> None:
        while not is_captcha_read():
            time.sleep(10)
            if not check_validation_error():
                browser.refresh()
                time.sleep(10)

            captcha_reload = browser.find_element('xpath', "//img[@src='/IRCC-AppointmentWave1/Images/refresh.png']")
            captcha_reload.click()
            time.sleep(10)


    def send_to_telegram(
            api_key: str,
            chat_id: str,
            text: str
    ) -> None:
        url = f'https://api.telegram.org/bot{api_key}/sendMessage?chat_id={chat_id}&text={text}'
        requests.get(url)

    while True:
        init()
        time.sleep(5)
        schedule_appointment()
        time.sleep(30)
        if not check_validation_error():
            time.sleep(10)
            browser.refresh()
            time.sleep(10)
        else:
            send_to_telegram(
                user.get(creds.TELEGRAM_KEY),
                user.get(creds.MESSAGE_ID),
                f'Please visit {url} Has been found free date'
            )
            browser.quit()
            browser.close()




