from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time

# Cài đặt trình duyệt ẩn
options = Options()
options.add_argument("--headless")
options.add_argument("--disable-gpu")
driver = webdriver.Chrome(options=options)

# Đọc tất cả các link từ file
with open("movie_links.txt", "r", encoding="utf-8") as f:
    movie_links = [line.strip() for line in f.readlines() if line.strip()]

for link in movie_links:
    print(f"🔗 Đang xử lý phim: {link}")
    eng_all = []
    vie_all = []

    for episode in range(1, 3):  # Có thể thay đổi số tập tùy phim
        episode_url = f"{link}/play?episode={episode}"
        print(f"   ▶️ Tập {episode}: {episode_url}")
        
        try:
            driver.get(episode_url)
            time.sleep(4)

            cues = driver.find_elements(By.XPATH, "//span[starts-with(@id, 'cue')]")
            if not cues:
                print("     ⚠️ Không có phụ đề, bỏ qua.")
                continue

            for cue in cues:
                try:
                    eng = cue.find_element(By.CLASS_NAME, "js-textEn").text.strip()
                    vie = cue.find_element(By.CLASS_NAME, "js-textVi").text.strip()
                    if eng and vie:
                        eng_all.append(eng)
                        vie_all.append(vie)
                except:
                    continue

        except Exception as e:
            print(f"     ❌ Lỗi tập {episode}: {e}")
            continue

    # ✅ Ghi ra file sau khi hoàn tất 1 phim
    with open("engcraw3.txt", "a", encoding="utf-8") as f_eng, open("viecraw3.txt", "a", encoding="utf-8") as f_vie:
        for e, v in zip(eng_all, vie_all):
            f_eng.write(e + "\n")
            f_vie.write(v + "\n")

    print(f"   💾 Đã lưu xong phim: {link}")

driver.quit()
print("✅ Xong! Đã lưu toàn bộ phụ đề vào engcrawfull.txt và viecrawfull.txt")
