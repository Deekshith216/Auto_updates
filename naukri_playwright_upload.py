import time
import os
import pandas as pd
from pathlib import Path
from playwright.sync_api import sync_playwright

students = pd.read_csv('students.csv')
log_data = []

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)

    for index, row in students.iterrows():
        email = row['email']
        resume_path = row['resume_path']
        username = email.split('@')[0]
        session_file = f"naukri_login_{username}.json"
        status = "Pending"
        message = ""

        print(f"\nProcessing: {email}")

        if not Path(session_file).exists():
            message = f"Missing login session for {email} ({session_file})"
            print(message)
            status = "Skipped"
            log_data.append({"email": email, "status": status, "message": message})
            continue

        if not Path(resume_path).is_file():
            message = f"Resume file not found: {resume_path}"
            print(message)
            status = "Failed"
            log_data.append({"email": email, "status": status, "message": message})
            continue

        context = browser.new_context(storage_state=session_file)
        page = context.new_page()

        try:
            # Navigate to profile
            page.goto("https://www.naukri.com/mnjuser/profile", wait_until="domcontentloaded")
            print("Landed on:", page.url)

            # Close popup if any
            try:
                page.locator(".crossIcon").click(timeout=3000)
                print("Closed popup")
            except:
                print("No popup")

            page.wait_for_timeout(3000)

            # Try clicking 'Update resume' button (optional)
            try:
                update_btn = page.locator("input[value*='Update']")
                update_btn.wait_for(state="visible", timeout=5000)
                update_btn.click()
                print("Clicked update button")
            except:
                print("Update button not found, skipping click")

            # Upload resume
            file_input = page.locator('input[type="file"]#attachCV')
            file_input.wait_for(state="visible", timeout=10000)
            print("Uploading file:", resume_path)
            file_input.set_input_files(resume_path)

            # Confirm the upload
            try:
                confirm_btn = page.locator("input[type='button'][value='Update resume']")
                confirm_btn.wait_for(state="visible", timeout=5000)
                confirm_btn.click()
                print("Clicked 'Update resume' to confirm upload")
                page.wait_for_timeout(5000)
            except Exception as e:
                print("Failed to click confirm upload:", e)

            status = "Success"
            message = "Resume uploaded"

        except Exception as e:
            message = str(e)
            print(f"Error for {email}: {message}")
            status = "Failed"
            page.screenshot(path=f"{username}_error.png")

        page.close()
        context.close()
        time.sleep(5)

        log_data.append({"email": email, "status": status, "message": message})

    browser.close()

# Save logs
pd.DataFrame(log_data).to_csv("log.csv", index=False)
print(" All uploads complete. Check log.csv for results.")
