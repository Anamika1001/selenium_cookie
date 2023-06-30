from selenium import webdriver
from selenium.webdriver.common.by import By
import time

chrome_driver_path = "CHROME_DRIVER_PATH"
driver = webdriver.Chrome(executable_path=chrome_driver_path)

driver.get("http://orteil.dashnet.org/experiments/cookie/")

cookie = driver.find_element(By.ID, "cookie")

items = driver.find_elements(By.CSS_SELECTOR, "#store div")

# first method
# item_ids = []
# for item in items:
#     item_ids = item.get_attribute("id")

# other method
item_ids = [item.get_attribute("id") for item in items]

time_out = time.time()+5  # first 5 sec
one_min = time.time() + 60*1  # 5minutes


while True:
    cookie.click()

    # Every 5 seconds
    if time.time() > time_out:

        # get all upgrade <b> tags
        all_prices = driver.find_elements(By.CSS_SELECTOR, "#store b")
        item_prices = []

        # convert <b> text into an integer price
        for price in all_prices:
            element_text = price.text
            # print(element_text)
            if element_text != "":
                cost = int(element_text.split("-")[1].strip().replace(",", ""))
                # print(cost)
                item_prices.append(cost)

        # Create dictionary of store items and prices
        cookie_upgrade = {}
        for n in range(len(item_prices)):
            cookie_upgrade[item_prices[n]] = item_ids[n]

        # print(cookie_upgrade)

        # Get current cookie count
        money_element = driver.find_element(By.ID, "money").text
        if "," in money_element:
            money_element = money_element.replace(",", "")
        cookie_count = int(money_element)

        print(money_element)

        # find upgrades that we can currently afford
        affordable_upgrades = {}
        for cost, id in cookie_upgrade.items():
            if cookie_count > cost:
                affordable_upgrades[cost] = id

        # purchase the most expensive affordable upgrade

        highest_price_affordable_upgrade = max(affordable_upgrades)
        print(highest_price_affordable_upgrade)
        to_purchase_id = affordable_upgrades[highest_price_affordable_upgrade]

        driver.find_element(By.ID, to_purchase_id).click()

        time_out = time.time()+5

    # After 1 minutes stop the bot and check the cookies per second count.
    if time.time() > one_min:
        cookie_per_s = driver.find_element(By.ID, "cps").text
        print(cookie_per_s)
        break
