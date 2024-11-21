import json

from selenium import webdriver

import os

from threads_likes.web_scraping import (
    load_cookies,
    save_cookies,
    get_all_threads_of_user,
    get_likes_per_thread
)

from src.threads_likes import COOKIES_PATH, DATA_PATH

COOKIES_FILE = COOKIES_PATH / "session_cookies.json"
DATA_FILE = DATA_PATH / "likes_data.json"

USERNAME = "USERNAME"

if __name__ == "__main__":
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    driver = webdriver.Chrome(options=options)

    if os.path.exists(COOKIES_FILE):
        driver.get("https://www.threads.net/")
        load_cookies(driver, COOKIES_FILE)
        driver.refresh()
    else:
        driver.get("https://www.threads.net/login")
        input("Please log in to Threads in the opened browser. Press Enter after completing the login process.")
        save_cookies(driver, COOKIES_FILE)

    thread_urls = get_all_threads_of_user(driver=driver, username=USERNAME)

    result_data = {}

    for i, thread_url in enumerate(thread_urls):
        try:
            likes = get_likes_per_thread(
                thread_url=thread_url,
                driver=driver,
                username=USERNAME,
            )
            if len(likes) < 100:
                print(likes)
                result_data[i] = likes
        except Exception as e:
            print(f"{thread_url} at index {i} failed due to {e}")

    with open(DATA_FILE, "w") as f:
        json.dump(result_data, f, indent=4)

    driver.quit()
