import os
import json
import random
from time import sleep

from random_words import RandomWords
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, ElementNotInteractableException, \
    InvalidCookieDomainException, TimeoutException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager

# Search terms
TERMS = [
    "define ", "explain ", "example of ", "how to pronounce ", "what is ",
    "what is the ", "what is the definition of ", "what is the example of ",
    "what is the pronunciation of ", "what is the synonym of ",
    "what is the antonym of ", "what is the hypernym of ",
    "what is the meronym of ", "photos of ", "images of ", "pictures of ",
    "pictures of ", "pictures of ", "pictures of ", "pictures of ",
    "pictures of ", "information about ", "information on ",
    "information about the ", "information on the ", "information about the ",
    "synonym of ", "antonym of ", "hypernym of ", "meronym of ",
    "synonym for ", "antonym for ", "hypernym for "
]

PC_SEARCHES = 5

# Profile Details
EMAIL = os.environ['email']
PASSWORD = os.environ['password']


def get_driver():
    chrome_options = Options()
    # chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument(
        "--disable-blink-features=AutomationControlled")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-notifications")


    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    driver.minimize_window()
    return driver


def slow_type(element, text, delay=0.01):
    for character in text:
        element.send_keys(character)
        sleep(delay)


def login(driver):
    driver.implicitly_wait(10)

    try:
        print("Attempting login with cookies...")
        driver.get("https://www.bing.com/myprofile")

        # cookies file saved from previous logins
        with open(f"./cookies/{EMAIL.split('@')[0]}.json", "r") as file:
            cookies = json.load(file)
            for cookie in cookies:
                driver.add_cookie(cookie)

        driver.get("https://www.bing.com/myprofile")

        sleep(random.uniform(4, 6))
        # Check if login successful by verifying presence of reward points element
        reward_points = driver.find_element(
            By.XPATH, "//span[@id='id_rc']").get_attribute('innerHTML')
        print("Login successful with cookies!")
        print(f"Reward Points: {reward_points}")
        return

    except (FileNotFoundError, NoSuchElementException,
            InvalidCookieDomainException):
        print(
            "No cookies found or login with cookies failed, proceeding with normal login..."
        )
        try:
            driver.get("https://www.bing.com/myprofile")

            sign_in_btn = driver.find_element(
                By.XPATH, "//input[@id='id_a' or @value='Sign in']")
            sign_in_btn.click()
            sleep(random.uniform(4, 6))

            # Sign in btn from dropdown for personal account
            sign_in = driver.find_element(By.XPATH, "//span[@class='id_text_signin']")
            sign_in.click()
            sleep(random.uniform(4, 6))

            # Find Email and input it
            username_field = driver.find_element(By.XPATH, '//*[@id="i0116"]')
            slow_type(username_field, EMAIL)
            username_field.send_keys(Keys.ENTER)
            sleep(random.uniform(4, 6))

        except NoSuchElementException:
            driver.find_element(
                By.XPATH, "//input[@id='id_a' or @value='Sign in']").click()
            driver.find_element(By.XPATH,
                                "//span[@class='id_text_signin']").click()
            username_field = driver.find_element(By.XPATH, '//*[@id="i0116"]')
            slow_type(username_field, EMAIL)
            username_field.send_keys(Keys.ENTER)
            sleep(random.uniform(4, 6))

        # Find Password and input it
        try:
            password_field = driver.find_element(By.XPATH,
                                                 "//input[@id='i0118']")
            slow_type(password_field, PASSWORD)
            password_field.send_keys(Keys.ENTER)
        except NoSuchElementException:
            pass
        sleep(random.uniform(4, 6))

        # Stay Signed In - Yes
        try:
            driver.find_element(By.XPATH,
                                "//button[@id='acceptButton']").click()
            sleep(random.uniform(4, 6))
        except NoSuchElementException:
            pass

        driver.refresh()

        # save cookies
        cookies = driver.get_cookies()
        with open(f"./cookies/{EMAIL.split('@')[0]}.json", "w") as f:
            json.dump(cookies, f)

        sleep(random.uniform(4, 6))

        # Verify if login was successful after normal login attempt
        try:
            # Check if login successful by verifying presence of reward points element
            reward_points = driver.find_element(
                By.XPATH, "//span[@id='id_rc']").get_attribute('innerHTML')
            print("Normal login successful!")
            print("Reward Points:", reward_points)
        except NoSuchElementException:
            print("Login failed with both cookies and normal login.")


def attempt_daily_sets(driver):
    driver.get("https://rewards.bing.com/")
    try:
        # Find Email and input it
        username_field = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="i0116"]')))
        slow_type(username_field, EMAIL)
        username_field.send_keys(Keys.ENTER)
        sleep(random.uniform(4, 6))

        # Find Password and input it
        password_field = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//input[@id='i0118']")))
        slow_type(password_field, PASSWORD)
        password_field.send_keys(Keys.ENTER)
        sleep(random.uniform(4, 6))

        # Stay Signed In - Yes
        try:
            driver.find_element(By.XPATH,
                                "//button[@id='acceptButton']").click()
            sleep(random.uniform(4, 6))
        except NoSuchElementException:
            pass

        driver.refresh()

    except (NoSuchElementException, TimeoutException):
        pass

    try:
        driver.find_element(By.XPATH, "//button[@aria-label='Close']").click()
    except (NoSuchElementException, ElementNotInteractableException):
        pass

    # Verify if login was successful after normal login attempt
    try:
        # Check if login successful by verifying presence of reward points element
        reward_points = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located(
                (By.XPATH, "(//p[contains(@class, 'pointsValue')])[1]//span"
                 ))).get_attribute('innerHTML')
        print("Normal login successful!")
        print("Reward Points:", reward_points)

    except NoSuchElementException:
        print("Login failed normal login.")
        return

    # Find the activity cards
    activity_cards = driver.find_elements(
        By.XPATH, "//a[@class='ds-card-sec ng-scope']")
    main_window = driver.window_handles[0]

    # Loop through each activity card and click on it
    for index, card in enumerate(activity_cards, start=1):
        try:
            # Get the class name for the element that indicates whether the activity is available or not
            class_name = driver.find_element(By.XPATH,
                                             value=f"(//a[@class='ds-card-sec ng-scope']//div[@class='ng-scope']//span[1])[{index}]"
                                             ).get_attribute('class')

            # Check if the activity is available
            if (class_name == "mee-icon mee-icon-AddMedium" or class_name == "mee-icon mee-icon-HourGlass"):
                driver.execute_script("arguments[0].click();", card)
                sleep(random.uniform(7, 15))

                # Scroll down some length
                driver.execute_script(f"window.scrollTo(0, {random.randint(50, 500)});")

                sleep(random.uniform(7, 10))
                # Print the position of the card
                print(f"Activity card {index} done!")

                driver.switch_to.window(main_window)
                sleep(random.uniform(3, 7))
        except NoSuchElementException:
            pass

            try:
                driver.find_element(By.XPATH,
                                    "//button[@aria-label='Close']").click()
            except (NoSuchElementException, ElementNotInteractableException):
                pass
    print("Daily Sets done!")


def search(driver):
    # Find search bar and perform searches
    rw = RandomWords()

    for _ in range(PC_SEARCHES):
        try:
            # Clear search bar
            search_bar = driver.find_element(By.ID, value="sb_form_q")
            search_bar.clear()

            # Create string to send
            value = random.choice(TERMS) + rw.random_word()
            print(f"Search term: {value}")

            # Send random keyword
            slow_type(search_bar, value, 0.01)

            sleep(random.uniform(3, 5))
            search_bar.send_keys(Keys.RETURN)
            sleep(random.uniform(7, 10))

            # scroll down some length
            driver.execute_script(
                f"window.scrollTo(0, {random.randint(150, 700)})")
            sleep(random.uniform(3, 5))
        except NoSuchElementException:
            pass
    print("Search done!")


if __name__ == "__main__":
    driver = get_driver()
    login(driver)
    search(driver)
    attempt_daily_sets(driver)
    driver.quit()
