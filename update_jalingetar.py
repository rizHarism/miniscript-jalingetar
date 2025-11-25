from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoAlertPresentException, TimeoutException
import pandas as pd
import pyautogui
import time
import os
import shutil


options = Options()
options.add_argument("--start-maximized")
options.headless = False  # Pastikan GUI aktif

# --- 1️⃣ Load CSV with pandas ---
# change path to the real path of csv from your computer
df = pd.read_csv(r"D:\00. ARUNIKA\00. PROJECT EKSTERNAL\KDR\DINAS PERKIM KABUPATEN\UPDATE DATA WEBGIS 2025\SCRIPT UPDATE\miniscript-jalingetar\data_upload\sample_data.csv")

driver = webdriver.Chrome(options=options)
# change the url with the real webbsite
base_url = 'http://localhost:8000/'
driver.get(base_url)



# # Cari elemen <a> dengan onclick="opm(5);"
login_link = driver.find_element(By.XPATH, "//a[@data-bs-target='#loginModal']")
driver.execute_script("arguments[0].click();", login_link)  # klik link login
time.sleep(2) 

# proses Login
# change the actual user and password
driver.find_element(By.CSS_SELECTOR, "div.modal input#username").send_keys("Admin")
driver.find_element(By.ID, "password").send_keys("perkim2022")
time.sleep(2) 
login_btn = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "div.modal button.float-end")))
login_btn.click()

# iterasi with the csv (survey data)

wait = WebDriverWait(driver, 20)
driver.get(base_url + 'ruas/kelurahan/')

for i, row in df.iterrows():
    print(f"Processing row {i+1}/{len(df)}")

    print("Row index:", i)
    print("Row data:", row)
    no_ruas = row['nomor_ruas']
    time.sleep(2)
    driver.get(base_url + '/ruas/kelurahan/' + no_ruas + '/edit')
    time.sleep(1.5)

    try:
        # Replace with your real field IDs
        wait.until(EC.visibility_of_element_located((By.ID, "lebar"))).clear()
        driver.find_element(By.ID, "lebar").send_keys(row['lebar'])

        select_kondisi = Select(driver.find_element(By.ID, "kondisi"))
        select_kondisi.select_by_visible_text(row['kondisi_jalan'].strip().upper())

        select_perkerasan = Select(driver.find_element(By.ID, "perkerasan"))
        select_perkerasan.select_by_visible_text(row['perkerasan'].strip().upper())

        wait.until(EC.visibility_of_element_located((By.ID, "utilitas"))).clear()
        driver.find_element(By.ID, "utilitas").send_keys(row['keterangan_utilitas'].strip().upper())

        driver.find_element(By.ID, "foto-ruas").click()
        time.sleep(1.0)
        
        #change the image path with the image column value by iteration
        pyautogui.write(r"C:\Users\rizqi\Downloads\marker.png")
        pyautogui.press("enter")

        time.sleep(1.5)
        # Submit form
        # wait.until(EC.element_to_be_clickable((By.ID, "submit"))).click()

        # print(f"✅ Submitted: {row['name']}")

        # Wait a bit to avoid overloading the server
        # time.sleep(1000)

        # Optional: refresh or navigate back to the form
        # driver.get("https://example.com/survey_form")

    except Exception as e:
        print(f"⚠️ Error on row {i+1}: {e}")
        continue

# --- 4️⃣ Done ---

time.sleep(10)


# # halaman Upload

# input("Press Enter to close...")