import streamlit as st
import pandas as pd
import requests
import json
from datetime import datetime

# 設定網頁標題與排版
st.set_page_config(page_title="個案復能訓練紀錄系統-官方雲端版", layout="wide")

# ================= 🛡️ 安全性改裝：從雲端保險箱讀取網址 =================
try:
    SHEET_API_URL = st.secrets["api_url"]
except:
    SHEET_API_URL = "尚未設定雲端保險箱網址"

SHEET_API_URLS = {
    "同心園": SHEET_API_URL,
    "大願如來": SHEET_API_URL
}
# =========================================================================

# 初始化學員資料
if 'member_db' not in st.session_state:
    st.session_state.member_db = [
        {"id": "11402001", "name": "湯O珍"}, {"id": "11402002", "name": "鄧O英"}, 
        {"id": "11402003", "name": "徐O梅"}, {"id": "11402004", "name": "羅O鳳"}, 
        {"id": "11402005", "name": "林O嬌"}, {"id": "11402006", "name": "陳O春"}, 
        {"id": "11402007", "name": "江O秀"}, {"id": "11402008", "name": "陳O珠"}, 
        {"id": "11402009", "name": "范O英"}, {"id": "11402010", "name": "謝O妹"}, 
        {"id": "11402011", "name": "周O生"}, {"id": "11402012", "name": "張O基"}, 
        {"id": "11402013", "name": "溫O妹"}, {"id": "11402014", "name": "陳O妹"}, 
        {"id": "11402015", "name": "魏O清"}, {"id": "11402016", "name": "何O銘"}, 
        {"id": "11402017", "name": "黃O鳳"}, {"id": "11402018", "name": "張O琴"}, 
        {"id": "11402019", "name": "陳O泉"}, {"id": "11402020", "name": "劉O富"}, 
        {"id": "11402021", "name": "李O英"}, {"id": "11402022", "name": "陳O宇"}, 
        {"id": "11402023", "name": "徐O金"}, {"id": "11402024", "name": "劉O祥"}, 
        {"id": "11402025", "name": "葉O清"}, {"id": "11402026", "name": "陳O明"}, 
        {"id": "11402027", "name": "徐O美"}, {"id": "11402028", "name": "蕭O蓮"}, 
        {"id": "11402029", "name": "何O妹"}, {"id": "11402030", "name": "古O錦"}, 
        {"id": "11402031", "name": "廖O妹"}, {"id": "11402032", "name": "李O英"}, 
        {"id": "11402033", "name": "徐O進"}, {"id": "11402034", "name": "鍾O利"}, 
        {"id": "11401001", "name": "張O玉"}, {"id": "11401002", "name": "黃O鳳"}, 
        {"id": "11401003", "name": "胡O蘭"}, {"id": "11401004", "name": "林O雄"}, 
        {"id": "11401005", "name": "徐O妹"}, {"id": "11401006", "name": "趙O美"}, 
        {"id": "11401007", "name": "何O光"}, {"id": "11401008", "name": "曾O盛"}, 
        {"id": "11401009", "name": "黃O嬌"}, {"id": "11401010", "name": "林O春"}, 
        {"id": "11401011", "name": "張O枝"}, {"id": "11401012", "name": "鍾O珍"}, 
        {"id": "11401013", "name": "黃O達"}, {"id": "11401014", "name": "彭O英"}, 
        {"id": "11401015", "name": "黃O發"}, {"id": "11401016", "name": "林O福"}, 
        {"id": "11401017", "name": "蘇O妹"}, {"id": "11401018", "name": "黃O水"}, 
        {"id": "11401019", "name": "陳O安"}, {"id": "11401020", "name": "林O秀"}, 
        {"id": "11401021", "name": "江O蓮"}, {"id": "11401022", "name": "林O珍"}, 
        {"id": "11401023", "name": "解O英"}, {"id": "11401024", "name": "胡O治"}, 
        {"id": "11401025", "name": "林O妹"}, {"id": "11401026", "name": "張O新"}
    ]

# 輔助函式：發送資料到 Google Sheet
def send_to_google_sheet(api_url, payload):
    try:
        headers = {"Content-Type": "application/json"}
        response = requests.post(api_url, data=json.dumps(payload), headers=headers, timeout=10)
        if response.status_code == 200:
            res_json = response.json()
            if res_json.get("status") == "success":
                return True, "資料成功寫入 Google 試算表！"
            else:
                return False, f"試算表後端錯誤: {res_json.get('message')}"
        else:
            return False, f"連線失敗，HTTP 狀態碼: {response.status_code}"
    except Exception as e:
        return False, f"連線發生異常: {str(e)}"

# 介面標題
st.title("🏋️ 個案復能訓練紀錄系統")
st.write("填寫完成後按「送出紀錄」，資料將自動同步至對應機構的 Google 試算表。")

# 機構選擇
location = st.selectbox("請選擇服務機構", ["同心園", "大願如來"])

# 表單開始
with st.form("rehab_form", clear_on_submit=True):
    col1, col2 = st.columns(2)
    
    with col1:
        member_options = [f"{m['id']} - {m['name']}" for m in st.session_state.member_db]
        selected_member = st.selectbox("學員姓名 (序號)", member_options)
        
        # 拆分序號與姓名
        selected_id = selected_member.split(" - ")[0]
        selected_name = selected_member.split(" - ")[1]
        
        date_str = st.date_input("日期", datetime.today()).strftime("%Y/%m/%d")
        bp_systolic = st.number_input("血壓-收縮壓 (mmHg)", min_value=50, max_value=250, value=120)
        bp_diastolic = st.number_input("血壓-舒張壓 (mmHg)", min_value=30, max_value=150, value=80)
        pulse = st.number_input("脈搏 (次/分)", min_value=30, max_value=200, value=75)
        spo2 = st.number_input("血氧 (%)", min_value=50, max_value=100, value=98)

    with col2:
        st.markdown("**復能項目紀錄 (請輸入完成次數)**")
        ex1 = st.number_input("1. 握力訓練", min_value=0, max_value=200, value=0)
        ex2 = st.number_input("2. 徒手肌力（上肢）", min_value=0, max_value=200, value=0)
        ex3 = st.number_input("3. 彈力帶訓練（上肢）", min_value=0, max_value=200, value=0)
        ex4 = st.number_input("4. 徒手肌力（下肢）", min_value=0, max_value=200, value=0)
        ex5 = st.number_input("5. 彈力帶訓練（下肢）", min_value=0, max_value=200, value=0)
        ex6 = st.number_input("6. 關節活動度訓練", min_value=0, max_value=200, value=0)
        ex7 = st.number_input("7. 站立平衡訓練", min_value=0, max_value=200, value=0)
        ex8 = st.number_input("8. 步態平衡訓練", min_value=0, max_value=200, value=0)
        
        note = st.text_input("備註說明", "")

    # 提交按鈕
    submit_btn = st.form_submit_with_arrow("送出紀錄")

# 當按下送出
if submit_btn:
    current_api = SHEET_API_URLS.get(location)
    
    if "https" not in current_api:
        st.error("⚠️ 偵測到雲端保險箱未設定或設定錯誤，請檢查 Streamlit Cloud 後台的 Secrets！")
    else:
        # 打包資料
        payload = {
            "location": location,
            "id": selected_id,
            "name": selected_name,
            "date": date_str,
            "bp_systolic": bp_systolic,
            "bp_diastolic": bp_diastolic,
            "pulse": pulse,
            "spo2": spo2,
            "ex1": ex1,
            "ex2": ex2,
            "ex3": ex3,
            "ex4": ex4,
            "ex5": ex5,
            "ex6": ex6,
            "ex7": ex7,
            "ex8": ex8,
            "note": note
        }
        
        with st.spinner("正在將資料上傳至雲端試算表..."):
            success, msg = send_to_google_sheet(current_api, payload)
            if success:
                st.success(f"🎉 【{selected_name}】的紀錄已成功送出！")
            else:
                st.error(f"❌ 傳送失敗：{msg}")
