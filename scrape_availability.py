import sys
import time
import json
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.options import Options

settings = json.load(open("settings.json"))  # 读取配置文件

if settings['browser'] == '1':
    chrome_options = Options()
    if (settings['headless']):
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument(
            "user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.114 Safari/537.36")
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option("useAutomationExtension", False)

        driver = webdriver.Chrome(options=chrome_options)
        driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

else:
    # raise ValueError("无效的浏览器配置！请在 settings.json 中设置 browser=1（Chrome）或 2（Safari）。")
    # Safari 配置
    safari_options = webdriver.SafariOptions()
    if (settings['headless']):
        print("警告：Safari 不支持原生无头模式！")
    safari_options.add_argument("--disable-gpu")  # 可选

    driver = webdriver.Safari(options=safari_options)
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    print("Safari 浏览器已启动！")

# safari_options = webdriver.SafariOptions()
# driver = webdriver.Safari(options=safari_options)#当使用Safari时激活这里，不使用时请注释掉
# driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")


try:
    # driver.get("https://www.myrta.com/wps/portal/extvp/myrta/login/")#在这个地方打开RTA的网页（这一行是原生代码）
    driver.get("https://www.myrta.com/wps/portal/extvp/myrta/licence/tbs/tbs-login/")  # 在这个地方打开RTA的网页（这一行是修改后的代码代码）
    time.sleep(10)
    print("Web Open - Done")
    # driver.find_element(By.ID,"widget_cardNumber").send_keys(settings['username'])#这个地方是识别输入框的地方，在F12里找对应输入框的ID值
    driver.find_element(By.ID, "widget_input_familyName").send_keys(
        settings['username'])  # 从setting.json读取Family Name（这一行是修改后的代码代码）
    print("Type in Family Name - Done")
    # driver.find_element(By.ID,"widget_password").send_keys(settings['password'])
    driver.find_element(By.ID, "widget_rms_noLogin-input-RMSnumb").send_keys(
        settings['password'])  # 从setting.json读取RMS Customer NO.(8位代码)（这一行是修改后的代码代码）
    print("Type in Customer NO. - Done")
    time.sleep(5)#
    # driver.find_element(By.ID, "nextButton").click()  # 这个地方是识别登录框的地方，在F12里找对应输入框的ID值
    driver.find_element(By.ID, "submitNoLogin").click()  # 自动点击登录（submitNoLogin）
    print("Click Login - Done")
    if (settings['have_booking']):
        driver.find_element(By.XPATH, '//*[text()="Manage booking"]').click()
        driver.find_element(By.ID, "changeLocationButton").click()
        time.sleep(settings['wait_timer'])
    else:
        driver.find_element(By.XPATH, '//*[text()="Book test"]').click()
        driver.find_element(By.ID, "CAR").click()
        time.sleep(settings['wait_timer_car'])
        driver.find_element(By.XPATH, "//fieldset[@id='DC']/span[contains(@class, 'rms_testItemResult')]").click()
        time.sleep(settings['wait_timer'])
        driver.find_element(By.ID, "nextButton").click()
        time.sleep(settings['wait_timer'])
        driver.find_element(By.ID, "checkTerms").click()
        time.sleep(settings['wait_timer'])
        driver.find_element(By.ID, "nextButton").click()
        time.sleep(settings['wait_timer'])
        driver.find_element(By.ID, "rms_batLocLocSel").click()
        time.sleep(settings['wait_timer'])
    driver.find_element(By.ID, "rms_batLocLocSel").click()
    time.sleep(settings['wait_timer'])
    select_box = driver.find_element(By.ID, "rms_batLocationSelect2")
    Select(select_box).select_by_value(sys.argv[1])
    time.sleep(settings['wait_timer'])
    driver.find_element(By.ID, "nextButton").click()
    if (driver.find_element(By.ID, "getEarliestTime").size != 0):
        if (driver.find_element(By.ID, "getEarliestTime").is_displayed()):
            if (driver.find_element(By.ID, "getEarliestTime").is_enabled()):
                driver.find_element(By.ID, "getEarliestTime").click()
    result = driver.execute_script('return timeslots')
    results_file = open(sys.argv[2], "a")
    results_file.write('{"location":"' + sys.argv[1] + '","result":' + json.dumps(result) + '}\n')
    results_file.close()
    driver.quit()
except:
    driver.quit()
    print("Code working done!")
    exit(1)
