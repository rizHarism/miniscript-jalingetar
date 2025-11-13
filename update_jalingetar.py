from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoAlertPresentException, TimeoutException
import pandas as pd
import csv
import pyautogui
import time
import os
import shutil


options = Options()
options.add_argument("--start-maximized")
options.headless = False  # Pastikan GUI aktif

# --- 1️⃣ Load CSV with pandas ---
df = pd.read_csv(r"I:\PROJECT\GIS LEGER PERKIM\09. AUTOMASI UPDATE GIS JALAN 2025\data_upload\sample_data.csv")

driver = webdriver.Chrome(options=options)
driver.get('http://localhost:8000/')



# # Cari elemen <a> dengan onclick="opm(5);"
login_link = driver.find_element(By.XPATH, "//a[@data-bs-target='#loginModal']")
driver.execute_script("arguments[0].click();", login_link)  # klik link login
time.sleep(2) 

#proses Login
driver.find_element(By.CSS_SELECTOR, "div.modal input#username").send_keys("admin")
driver.find_element(By.ID, "password").send_keys("password")
time.sleep(2) 
login_btn = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "div.modal button.float-end"))
        )
login_btn.click()

# iterasi terhadap hasil survey

wait = WebDriverWait(driver, 20)

for i, row in df.iterrows():
    print(f"Processing row {i+1}/{len(df)}")

    print("Row index:", i)
    print("Row data:", row)
    no_ruas = row['nomor_ruas']
    driver.get('http://localhost:8000/ruas/kelurahan/')
    time.sleep(2)
    driver.get('http://localhost:8000/ruas/kelurahan/'+ no_ruas +'/edit')
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
        
        pyautogui.write(r"C:\Users\Ablasa\Pictures\marker.png")
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
# upload_page = "https://petadasar.atrbpn.go.id/main/upload/"

# #masuk langsung ke halaman upload
# driver.get(upload_page)

# #path file yang nantinya sebagai acuan
# path_file = r"\\Desktop-fsisf4q\ssd\MBTILES\UPLOAD 3\\"

# with open(path_file+"list_file.csv", newline='') as csvfile:
#     reader = csv.reader(csvfile)
#     for row in reader:
        
#         file_path = row[0]  # Baris pertama di CSV = path file mbtiles
        
#         if not os.path.exists(file_path):
#             print(f"File tidak ditemukan: {file_path}")
#             continue
        
#         #klik upload mbtiles jika file ada
#         upload_btn = WebDriverWait(driver, 20).until(
#             EC.element_to_be_clickable((By.XPATH, '//input[@type="button" and @value="Mbtiles Peta Foto Drones"]'))
#         )
#         # Tunggu tombol upload Mbtiles muncul
#         upload_btn.click()
#         time.sleep(1)


#         # Kirim path file ke file explorer (pyautogui)
#         pyautogui.write(file_path)
#         pyautogui.press('enter')
#         print(f"Sedang mengupload: {file_path}")

#         # Tunggu upload selesai (kamu bisa ganti dengan WebDriverWait untuk sesuatu yang spesifik)
#         time.sleep(2)

#         # Tunggu dan klik link ke metadata jika perlu
#         try:
#             metadata_link = WebDriverWait(driver, 600).until(
#                 EC.element_to_be_clickable((By.XPATH, '//a[contains(text(),"Registrasi Metadata")]'))
#             )
#             metadata_link.click()

#             try:
#                 alamat_input = WebDriverWait(driver, 10).until(
#                     EC.presence_of_element_located((By.NAME, "alamat"))  # ganti "alamat" dengan name/id sebenarnya dari input alamat
#                 )
                
#                 alamat_value = alamat_input.get_attribute("value").strip()
                
#                 if not alamat_value:
#                     print(f"[INFO] alamat kosong untuk file {file_path}, lewati metadata dan pemindahan.")
#                     no_location_folder = path_file + "/NOLOCATION"
#                     os.makedirs(no_location_folder, exist_ok=True)
#                     new_path = os.path.join(no_location_folder, os.path.basename(file_path))
#                     shutil.move(file_path, new_path)
#                     print(f"File {file_path} dipindahkan ke {new_path}")
#                     driver.get(upload_page) 
#                     continue  # lompat ke iterasi selanjutnya
#             except TimeoutException:
#                 print(f"[ERROR] Form alamat tidak ditemukan untuk file {file_path}, lewati metadata dan pemindahan.")
#                 driver.get(upload_page) 
#                 continue

#             # Isi form metadata (isi sesuai struktur situs kamu)
#             # contoh: driver.find_element(By.NAME, "judul").send_keys("Nama Peta")
#             driver.find_element(By.NAME, "resolusi").send_keys("0.0512")
#             driver.find_element(By.NAME, "akurasi").send_keys("0.187")
#             driver.find_element(By.NAME, "tahunpemotretan").send_keys("2025")
#             driver.find_element(By.NAME, "sumber").send_keys("Lain2")
#             driver.find_element(By.NAME, "hp").send_keys("085859099010")

#             # Submit metadata
#             submit_btn = WebDriverWait(driver, 10).until(
#                 EC.element_to_be_clickable((By.XPATH, '//button[contains(text(),"SUBMIT")]'))
#             )
#             time.sleep(2) # Tunggu halaman selesai
#             submit_btn.click()

#             time.sleep(1) # Tunggu halaman selesai

#         except Exception as e:
#             print(f"Gagal isi metadata untuk: {file_path} - {e}")
#             continue

#         # Pindahkan file yang berhasil diupload ke folder uploaded/
#         uploaded_folder = path_file + "/UPLOADED"
#         os.makedirs(uploaded_folder, exist_ok=True)
#         new_path = os.path.join(uploaded_folder, os.path.basename(file_path))
#         shutil.move(file_path, new_path)
#         print(f"File {file_path} dipindahkan ke {new_path}")

#         # Kembali ke halaman upload lagi
#         try:
#             driver.get(upload_page) 
#         except:
#             driver.get(upload_page)  # Atau URL langsung upload
#         time.sleep(2)

# input("Press Enter to close...")