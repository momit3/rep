import time
import pickle
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys


idx = '''
edcde3@cycyip.com
c51f52@cycyip.com
1eaa0b@cycyip.com
b891c2@cycyip.com
be27a0@cycyip.com
045889@cycyip.com
a57926@cycyip.com 
'''
failed = []

mid = idx.split("\n")
midas = [item.strip() for item in mid if item.strip()]
i = 17
for x in midas:
    options = webdriver.ChromeOptions()
    # options.add_argument("--headless=new")
    options.add_argument(f'--user-data-dir=ChromeProfiles\\midasbuy{i}')
    driver = webdriver.Chrome(options=options)
    driver.get("https://www.midasbuy.com/midasbuy/my/login#login")
    time.sleep(2)
    driver.implicitly_wait(60)
    driver.find_element(By.XPATH, '//*[@id="loginUsername"]').send_keys(x)
    time.sleep(1)
    driver.find_element(By.XPATH, '//*[@id="loginPassword"]').send_keys("Noble@1415")
    time.sleep(1)
    driver.find_element(By.XPATH, '//*[@id="rememberMe"]').click()
    time.sleep(1)
    driver.find_element(By.XPATH, '//*[@id="loginButton"]').click()
    time.sleep(1)
    try:
        driver.implicitly_wait(2)
        driver.find_element(By.XPATH, '// *[ @ id = "pop-box"] / div / p[2]').text
        failed.append(x)
        print(f'{failed} -- Login failed')
        #desc
    except:
        print(f'{x} -- Log in Successful')
        i += 1
        print(f'total account = {i}')
    finally:
        driver.get("https://www.midasbuy.com/midasbuy/my/redeem/pubgm")
        try:
            driver.implicitly_wait(5)
            driver.find_element(By.XPATH, '//*[@id="root"]/div/div[7]/div[3]/div[1]/div/div').click()
        except:
            pass
        time.sleep(10)
        driver.quit()




# cookies = driver.get_cookies()
# pickle.dump(cookies, open(f'cookies_subnet255cc', 'wb'))
# print('cookies saved')
# driver.quit()        Please
#         enter
#         the
#         correct
#         password.
