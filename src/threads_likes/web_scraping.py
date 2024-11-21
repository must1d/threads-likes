import json
import time
from pathlib import Path

from threads_likes.helpers import retry

from selenium import webdriver
from selenium.webdriver.common.by import By

_LIKES_BOX = ("html/body/div[2]/div/div/div[3]/div/div/div[1]/div/div[2]"
              "/div/div/div/div[2]/div/div[2]/div/div/div[2]/div[1]")


def save_cookies(driver: webdriver.Chrome, cookies_file: Path) -> None:
    with cookies_file.open("w") as file:
        json.dump(driver.get_cookies(), file)


def load_cookies(driver: webdriver.Chrome, cookies_file: Path):
    with cookies_file.open("r") as file:
        cookies = json.load(file)
        for cookie in cookies:
            driver.add_cookie(cookie)


def get_all_threads_of_user(driver: webdriver.Chrome, username: str) -> list[str]:
    driver.get(f"https://www.threads.net/{username}")

    thread_urls = []
    scroll_pause_time = 2
    last_height = driver.execute_script("return document.body.scrollHeight")

    while True:
        threads = driver.find_elements(By.XPATH, "//a[contains(@href, '/post/')]")
        for thread in threads:
            url = thread.get_attribute("href")
            if url in thread_urls or username not in url:
                continue
            thread_urls.append(url)

        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(scroll_pause_time)

        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

    return thread_urls


def get_likes_per_thread(driver: webdriver.Chrome, thread_url: str, username: str) -> list[str]:
    driver.get(thread_url)

    time.sleep(1)

    view_activity_button = driver.find_element(
        By.XPATH,
        "//span[contains(text(), 'View activity')]/ancestor::div[@role='button']"
    )
    view_activity_button.click()

    time.sleep(3)

    likes_button = driver.find_element(
        By.XPATH,
        "//span[contains(text(), 'Likes')]/ancestor::div[@role='button']"
    )
    likes_button.click()

    time.sleep(3)

    @retry()
    def get_parent():
        return driver.find_element(By.XPATH, _LIKES_BOX)

    parent_element = get_parent()

    child_elements = parent_element.find_elements(By.XPATH, ".//a[contains(@href, '@')]")

    hrefs = [element.get_attribute("href") for element in child_elements]
    return [href[25:] for href in hrefs if username not in href]
