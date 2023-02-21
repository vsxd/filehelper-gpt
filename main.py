import time
import logging

from playwright.sync_api import sync_playwright
from chat_session import ChatSession

KEYWORD_CLEAN_MEMORY = "#清除记忆"
KEYWORD_LOGOUT = "#退出对话"

logging.basicConfig(
    format="%(asctime)s %(name)s:%(levelname)s:%(message)s",
    datefmt="%d-%M-%Y %H:%M:%S",
    level=logging.INFO
)


def run(playwright):
    browser = playwright.chromium.launch()  # or "firefox" or "webkit".
    page = browser.new_page()
    url = "https://filehelper.weixin.qq.com/"
    page.goto(url)
    page.wait_for_timeout(5000)
    print("browser title:", page.title())
    qr_url = page.locator('.qrcode-img').get_attribute('src', timeout=3*1000)
    print("login qrcode url:", qr_url)
    nickname = page.wait_for_selector('.chat-panel__header__main__nickname', timeout=1*60*1000).text_content()
    print("user nickname:", nickname)
    last_msg = ""

    with ChatSession() as session:
        while True:
            time.sleep(1)
            # CSS selector:
            # .msg-list
            # li.msg-list__item:nth-child(1)
            msg = page.locator('li.msg-list__item').last.text_content()
            if msg.startswith('[bot]') or msg == last_msg:
                continue
            if msg == KEYWORD_LOGOUT:
                break
            last_msg = msg
            print('msg:', msg)
            answer_str = session.ask_question(msg)

            page.get_by_role("textbox").fill("[bot] "+answer_str)
            page.locator('.chat-send__button').click()
            print('ans:', answer_str)

    browser.close()


def main():
    with sync_playwright() as playwright:
        run(playwright)


if __name__ == "__main__":
    main()
