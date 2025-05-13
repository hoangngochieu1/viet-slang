from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time

# Thiết lập trình duyệt ẩn (headless)
options = Options()
options.add_argument("--headless")
options.add_argument("--disable-gpu")

# Khởi tạo driver
driver = webdriver.Chrome(options=options)
driver.get("https://www.studyphim.vn/")

# Đợi trang load hoàn tất
time.sleep(5)

# Lấy tất cả các link phim từ thẻ <h4 class="movie-title"><a href=...>
elements = driver.find_elements(By.XPATH, '//h4[@class="movie-title"]/a')
movie_links = {el.get_attribute('href') for el in elements if el.get_attribute('href')}

# Kết thúc trình duyệt
driver.quit()

# Ghi ra file (danh sách đã loại trùng)
with open('movie_links.txt', 'w', encoding='utf-8') as f:
    for link in sorted(movie_links):  # sorted để file ổn định, có thể bỏ nếu không cần
        f.write(link + '\n')

print(f"✅ Đã cào {len(movie_links)} link phim (đã loại trùng). Lưu vào file 'movie_links.txt'")
