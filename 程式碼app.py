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

# 初始化兩家機構的正確學員名單
if 'dayuan_db' not in st.session_state:
    st.session_state.dayuan_db = [
        {"id": "11402001", "name": "李水來"}, {"id": "11402003", "name": "莊笑"},
        {"id": "11402005", "name": "林秀"}, {"id": "11402006", "name": "張王阿春"},
        {"id": "11402007", "name": "吳哲彥"}, {"id": "11402008", "name": "鄭吳春枝"},
        {"id": "11402009", "name": "黃張桂英"}, {"id": "11402010", "name": "羅立明"},
        {"id": "11402011", "name": "葉徐粉妹"}, {"id": "11402013", "name": "吳阿在"},
        {"id": "11402014", "name": "陳缪桂花"}, {"id": "11402015", "name": "王綉庚"},
        {"id": "11402016", "name": "蔡阮有妹"}, {"id": "11402017", "name": "吳添福"},
        {"id": "11402018", "name": "余水木"}, {"id": "11402019", "name": "鄭勝田"},
        {"id": "11402020", "name": "李呂桂月"}, {"id": "11402021", "name": "李燕香"},
        {"id": "11402022", "name": "李隆德"}, {"id": "11402023", "name": "甘松琳"},
        {"id": "11402024", "name": "黃吳秀蘭"}, {"id": "11402025", "name": "蔡秋宗"},
        {"id": "11402026", "name": "張良彰"}
    ]

if 'tongxin_db' not in st.session_state:
    st.session_state.tongxin_db = [
        {"id": "11401001", "name": "陳南都"}, {"id": "11401004", "name": "黃秋妹"},
        {"id": "11401005", "name": "鍾燕玉"}, {"id": "11401006", "name": "蕭兆輝"},
        {"id": "11401007", "name": "蔡陳梅鳳"}, {"id": "11401008", "name": "潘葉玉蘭"},
        {"id": "11401009", "name": "劉魏德齡"}, {"id": "11401010", "name": "楊貴美"},
        {"id": "11401011", "name": "陳烈芳"}, {"id": "11401013", "name": "陳茂源"},
        {"id": "11401014", "name": "郭盧碧沼"}, {"id": "11401015", "name": "張秉宸"},
        {"id": "11401016", "name": "王宜樺"}, {"id": "11401017", "name": "劉陳琅玕"},
        {"id": "11401018", "name": "曾錦煌"}, {"id": "11401019", "name": "林燕香"},
        {"id": "11401020", "name": "徐錦星"}, {"id": "11401021", "name": "吳劉秀蓉"},
        {"id": "11401022", "name": "蔡清和"}, {"id": "11401023", "name": "陳碧洲"},
        {"id": "11401024", "name": "林鳳娥"}, {"id": "11401025", "name": "林政宏"},
        {"id": "11401026", "name": "温貴妹"}
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
location = st.selectbox("請選擇服務機構", ["大願如來", "同心園"])

# 根據選擇的機構，自動帶出不同的學員名單
if location == "大願如來":
    current_db = st.session_state.dayuan_db
else:
    current_db = st.session_state.tongxin_db

# 表單開始
with st.form("rehab_form", clear_on_submit=True):
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**🩸 基本生理狀態**")
        member_options = [f"{m['id']} - {m['name']}" for m in current_db]
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
        st.markdown("**📋 復能項目紀錄 (請輸入完成次數)**")
        st.caption("🔹 中醫勾稽訓練項目")
        ex1 = st.number_input("1. 坐姿抬腿", min_value=0, max_value=200, value=0)
        ex2 = st.number_input("2. 坐姿踩腳踏車", min_value=0, max_value=200, value=0)
        ex3 = st.number_input("3. 坐姿腿開合", min_value=0, max_value=200, value=0)
        ex4 = st.number_input("4. 坐姿踢腿", min_value=0, max_value=200, value=0)
        ex5 = st.number_input("5. 椅子深蹲", min_value=0, max_value=200, value=0)
        ex6 = st.number_input("6. 坐姿v型腿上舉", min_value=0, max_value=200, value=0)
        
        st.caption("🔹 器材訓練")
        ex7 = st.number_input("7. 腿開合機", min_value=0, max_value=200, value=0)
        ex8 = st.number_input("8. 踢腿機", min_value=0, max_value=200, value=0)
        ex9 = st.number_input("9. 腿推機", min_value=0, max_value=200, value=0)
        ex10 = st.number_input("10. 划船機", min_value=0, max_value=200, value=0)
        ex11 = st.number_input("11. 肩推機", min_value=0, max_value=200, value=0)
        ex12 = st.number_input("12. 蝴蝶機", min_value=0, max_value=200, value=0)
        
        st.markdown("**📊 執行成效評估**")
        evaluation = st.selectbox("執行評值", ["佳", "可", "差"])
        rpe = st.slider("RPE 運動自覺強度 (0分極輕鬆 ~ 10分力竭)", min_value=0, max_value=10, value=3)
        
        note = st.text_input("備註說明", "")

    # 提交按鈕
    submit_btn = st.form_submit_button("送出紀錄")

# 當按下送出
if submit_btn:
    current_api = SHEET_API_URLS.get(location)
    
    if not current_api or "https" not in current_api:
        st.error("⚠️ 偵測到雲端保險箱未設定或設定錯誤，請確認 Streamlit 後台的 Secrets 有填入 api_url！")
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
            "ex1": ex1, "ex2": ex2, "ex3": ex3, "ex4": ex4, "ex5": ex5, "ex6": ex6,
            "ex7": ex7, "ex8": ex8, "ex9": ex9, "ex10": ex10, "ex11": ex11, "ex12": ex12,
            "evaluation": evaluation,
            "rpe": rpe,
            "note": note
        }
        
        with st.spinner("正在將資料上傳至雲端試算表..."):
            # 修正處：正確傳入 current_api 與 payload 兩個參數
            success, msg = send_to_google_sheet(current_api, payload)
            if success:
                st.success(f"🎉 成功！【{location} - {selected_name}】的復能紀錄已穩穩寫入試算表！")
            else:
                st.error(f"❌ 傳送失敗：{msg}")
