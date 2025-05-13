import requests
from bs4 import BeautifulSoup
import json
import os
import re

# 🔁 Làm sạch từ lóng
def clean_term(text):
    text = re.sub(r'^\s*[\.\d]+(\.\d+)*\s*', '', text)
    text = re.sub(r'\s+[-–—]\s+.*$', '', text)
    text = re.sub(r'\s*\(.*?\)', '', text)
    return text.strip().lower()

# 🌐 Lấy từ trang learningvietnamese.edu.vn
def fetch_slang_from_learningvietnamese():
    url = "https://learningvietnamese.edu.vn/blog/speak-vietnamese/vietnamese-slang-words/?lang=en"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    slang_dict = {}
    headers = soup.find_all("h3")
    for header in headers:
        term = clean_term(header.text.strip())
        explanation_tag = header.find_next_sibling("p")
        if explanation_tag:
            explanation = explanation_tag.text.strip()
            if term and explanation:
                slang_dict[term] = explanation
    return slang_dict

# 🌐 Lấy từ trang talkpal.ai
def fetch_slang_from_talkpal():
    url = "https://talkpal.ai/vocabulary/top-10-vietnamese-gen-z-slang-terms-you-need-to-know/"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    headers = soup.find_all("h2")
    slang_dict = {}
    for header in headers:
        if header.text.strip().startswith(tuple(str(i) for i in range(1, 11))):
            slang_term = header.text.strip().split(". ", 1)[1]
            next_p = header.find_next_sibling("p")
            explanation = next_p.text.strip() if next_p else ""
            slang_dict[clean_term(slang_term)] = explanation
    return slang_dict

# 🧩 Gộp và lưu slang_dict
def update_slang_json():
    filename = "slang_dict.json"
    if os.path.exists(filename):
        with open(filename, "r", encoding="utf-8") as f:
            old_dict = json.load(f)
    else:
        old_dict = {}

    talkpal = fetch_slang_from_talkpal()
    learnvn = fetch_slang_from_learningvietnamese()

    combined = {**old_dict, **talkpal, **learnvn}
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(combined, f, ensure_ascii=False, indent=4)
    print(f"✅ Cập nhật slang_dict.json với {len(combined)} mục.")

if __name__ == "__main__":
    update_slang_json()
