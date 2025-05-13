import streamlit as st
import json
import os
from transformers import MarianMTModel, MarianTokenizer
import re

# 📥 Load từ điển slang đã được tạo sẵn
def load_slang_dict():
    filename = "slang_dict.json"
    if not os.path.exists(filename):
        st.error("⚠️ slang_dict.json chưa tồn tại. Hãy chạy script update_slang_json.py trước.")
        return {}
    with open(filename, "r", encoding="utf-8") as f:
        return json.load(f)

# 🔠 Dịch tiếng Việt → tiếng Anh
@st.cache_resource
def load_model():
    model_name = "Helsinki-NLP/opus-mt-en-vi"
    tokenizer = MarianTokenizer.from_pretrained(model_name)
    model = MarianMTModel.from_pretrained(model_name)
    return tokenizer, model

def translate_vi_to_en(text, tokenizer, model):
    inputs = tokenizer([text], return_tensors="pt", padding=True)
    translated = model.generate(**inputs)
    return tokenizer.decode(translated[0], skip_special_tokens=True)

# 🌐 Streamlit UI
st.set_page_config(page_title="Vietnamese Slang Translator")
st.title("🇻🇳 Vietnamese Slang Translator 🇺🇸")
st.write("Nhập hoặc chọn từ lóng tiếng Việt để xem nghĩa và bản dịch tiếng Anh.")

slang_dict = load_slang_dict()
if slang_dict:
    tokenizer, model = load_model()
    selected_slang = st.selectbox("Chọn hoặc gõ từ lóng:", options=sorted(slang_dict.keys()))

    if selected_slang:
        vi_meaning = slang_dict[selected_slang]
        en_translation = translate_vi_to_en(vi_meaning, tokenizer, model)

        st.markdown(f"### 📝 Nghĩa tiếng Việt:\n> {en_translation}")
        st.markdown(f"### 🌐 English Translation:\n> {vi_meaning}")
