import streamlit as st
import pandas as pd
import requests
import json
from datetime import datetime

# 設定網頁標題與排版
st.set_page_config(page_title="個案復能訓練紀錄系統-官方雲端版", layout="wide")

# ================= 🛡️ 安全性改裝：從雲端保險箱讀取網址 =================
# 在雲端部署時，我們會把網址填在 Streamlit Cloud 後台的 Secrets 設定中
try:
    SHEET_API_URL = st.secrets["api_url"]
except:
    # 這是為了讓您在本機測試時，如果沒設定 Secrets 也不會直接當機
    SHEET_API_URL = "尚未設定雲端保險箱網址"

SHEET_API_URLS = {
    "同心園": SHEET_API_URL,
    "大願如來": SHEET_API_URL
}
# =========================================================================

# 初始化學員資料 (這裡保持不變，略過不重複貼，請使用您手中那份完整的名單資料)
if 'member_db' not in st.session_state:
    st.session_state.member_db = [
        # ...這裡請保留您原本那份 11402001 到 11401026 的完整學員名單...
    ]

# ... 下方所有的 send_to_google_sheet 和 st.form 邏輯都保持不變 ...
# (請直接將您上一版成功的程式碼中，除了 API 網址設定以外的部分全部接在下面即可)