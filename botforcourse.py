from selenium import webdriver
import time
import yagmail
import os


def get_drv():
    options=webdriver.ChromeOptions()
    options.add_argument("start-maximized")
    options.add_argument("disable-sandbox")
    options.add_argument("disable-infobars")
    options.add_argument("disable-dev-shm-usage")
    options.add_argument("disable-blink-features=AutomationControlled")
    options.add_experimental_option("excludeSwitches",["enable-automation"])
    driver=webdriver.Chrome(options=options)
    driver.get("https://zse.hr/en/indeks-366/365?isin=HRZB00ICBEX6")
    time.sleep(5)
    return driver
def findelement(driver):
    
    currency_text=driver.find_element(by="xpath",value='//*[@id="app_indeks"]/section[1]/div/div/div[2]/span[2]').text
    currency = float(currency_text.replace("%", "").replace(" ", ""))
    time.sleep(5)
    return currency
def sendemail(curren):
    email=os.getenv('email')
    password=os.getenv('password')
    subject=f"Now currency is:{curren}%"
    yag=yagmail.SMTP(user=email,password=password)
    send=yag.send(to=email,subject=subject)
    return 'message send'

def main():
    driver = get_drv()
    
    try:
        # Цикл для регулярної перевірки
        while True:
            try:
                currency = findelement(driver=driver)
                print(f"Current value: {currency}%")
                
                # Перевіряємо, чи модуль значення більше 0.10
                if abs(currency) > 0.10:
                    sendemail(currency)
                    print(f"Email sent. Currency: {currency}%")
                else:
                    print("No significant change.")
                    
            except Exception as e:
                print(f"An error occurred: {e}")
            
            # Затримка на 1 хвилину (60 секунд)
            time.sleep(60)

    except KeyboardInterrupt:
        print("Program interrupted by user. Exiting...")

    finally:
        # Завершуємо роботу з браузером
        driver.quit()
        print("Browser closed and resources cleaned up.")

if __name__ == "__main__":
    main()