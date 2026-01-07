# save_naukri_cookies.py
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()

    page.goto("https://www.naukri.com")
    page.click("text=Login", timeout=10000)

    # Fill email and password
    page.fill('input[placeholder="Enter your active Email ID / Username"]', "gattydeekshith39@gmail.com")
    page.fill('input[placeholder="Enter your password"]', "Deekshi@0205")
    page.click("button:has-text('Login')")

    print(" Handle OTP, popups, and ensure you're fully logged in.")
    print(" Then manually go to https://www.naukri.com/mnjuser/profile")
    input(" Press ENTER once the profile page is fully loaded and no popups exist...")

    context.storage_state(path="naukri_login.json")
    print(" Session saved. You can now run the resume upload script.")
    browser.close()
