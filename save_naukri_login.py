# save_naukri_session_per_user.py
from playwright.sync_api import sync_playwright

email = input("Enter candidate email: ")
storage_path = f"naukri_login_{email.split('@')[0]}.json"

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()

    page.goto("https://www.naukri.com")
    print("Please log in manually in the browser.")
    print(" Then visit: https://www.naukri.com/mnjuser/profile")
    input(" After resume section loads, press ENTER to save session...")

    context.storage_state(path=storage_path)
    browser.close()
    print(f" Session saved to: {storage_path}")

