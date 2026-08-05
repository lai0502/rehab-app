import streamlit as st
import pandas as pd
import requests
import json
from datetime import datetime

# 設定網頁標題與排版
st.set_page_config(page_title="個案復能訓練紀錄系統-官方雲端版", layout="wide")

# 安全性改裝：從雲端保險箱讀取 API 網址
try:
    SHEET_API_URL = st.secrets["api_url"]
except:
    SHEET_API_URL = ""

# -----------------------------------------------------------------------------
# 1. 各場域個案名單資料庫 (已帶入最新完整名單)
# -----------------------------------------------------------------------------

# 1-1. 大願如來學員名單
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
        {"id": "11402026", "name": "張良彰"}, {"id": "11402027", "name": "謝許淑子"},
        {"id": "11402028", "name": "呂牡丹"}, {"id": "11402029", "name": "温阿錦"},
        {"id": "11402030", "name": "呂金山"}, {"id": "11402031", "name": "胡秀月"}
    ]

# 1-2. 同心園學員名單
if 'tongxin_db' not in st.session_state:
    st.session_state.tongxin_db = [
        {"id": "11401001", "name": "陳南都"}, {"id": "11401002", "name": "鍾秀珠"},
        {"id": "11401004", "name": "黃秋妹"}, {"id": "11401005", "name": "鍾燕玉"},
        {"id": "11401006", "name": "蕭兆輝"}, {"id": "11401007", "name": "蔡陳梅鳳"},
        {"id": "11401008", "name": "潘葉玉蘭"}, {"id": "11401009", "name": "劉魏德齡"},
        {"id": "11401010", "name": "楊貴美"}, {"id": "11401011", "name": "陳烈芳"},
        {"id": "11401013", "name": "陳茂源"}, {"id": "11401014", "name": "郭盧碧沼"},
        {"id": "11401015", "name": "張秉宸"}, {"id": "11401016", "name": "王宜樺"},
        {"id": "11401017", "name": "劉陳琅玕"}, {"id": "11401018", "name": "曾錦煌"},
        {"id": "11401019", "name": "林燕香"}, {"id": "11401020", "name": "徐錦星"},
        {"id": "11401021", "name": "吳劉秀蓉"}, {"id": "11401022", "name": "蔡清和"},
        {"id": "11401023", "name": "陳碧洲"}, {"id": "11401024", "name": "林鳳娥"},
        {"id": "11401025", "name": "林政宏"}, {"id": "11401026", "name": "温貴妹"},
        {"id": "11401027", "name": "李秀繁"}, {"id": "11401028", "name": "徐煥俊"},
        {"id": "11401029", "name": "林滄賜"}
    ]

# 1-3. 文山文聖學員名單
if 'wenshan_db' not in st.session_state:
    st.session_state.wenshan_db = [
        {"id": "11503001", "name": "陳舒華"}, {"id": "11503002", "name": "徐煥銘"},
        {"id": "11503003", "name": "吳順隆"}, {"id": "11503004", "name": "陳正義"},
        {"id": "11503005", "name": "陶德賢"}, {"id": "11503006", "name": "羅瑞媛"},
        {"id": "11503007", "name": "鄭武雄"}, {"id": "11503008", "name": "鄭王英妹"},
        {"id": "11503009", "name": "張豪偉"}, {"id": "11503010", "name": "賴秋雄"}
    ]

# -----------------------------------------------------------------------------
# 2. 介面呈現與選擇器
# -----------------------------------------------------------------------------

st.title("🏋️ 個案復能訓練紀錄系統")
st.write("填寫完成後按「送出紀錄」，資料將自動同步至對應機構的 Google 試算表。")

# 機構選擇
location = st.selectbox("請選擇服務機構", ["大願如來", "同心園", "文山文聖"])

# 動態配對資料庫
if location == "大願如來":
    current_db = st.session_state.dayuan_db
elif location == "同心園":
    current_db = st.session_state.tongxin_db
else:
    current_db = st.session_state.wenshan_db

# -----------------------------------------------------------------------------
# 3. 表單輸入介面
# -----------------------------------------------------------------------------

with st.form("rehab_form", clear_on_submit=True):
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**🩸 基本生理狀態**")
        member_options = [f"{m['id']} - {m['name']}" for m in current_db]
        selected_member = st.selectbox("學員姓名 (序號)", member_options)
        
        selected_id = selected_member.split(" - ")[0]
        selected_name = selected_member.split(" - ")[1]
        
        date_str = st.date_input("日期", datetime.today()).strftime("%Y/%m/%d")
        bp_systolic = st.number_input("血壓-收縮壓 (mmHg)", min_value=50, max_value=250, value=120)
        bp_diastolic = st.number_input("血壓-舒張壓 (mmHg)", min_value=30, max_value=150, value=80)
        spo2 = st.number_input("血氧 (%)", min_value=50, max_value=100, value=98)
        
        st.markdown("---")
        st.markdown("**⚙️ 系統設定與阻力項目**")
        setup_count = st.number_input("設定次數", min_value=1, max_value=50, value=1)
        
        resistance_options = ["無", "彈力帶", "沙袋", "自訂輸入..."]
        selected_res = st.selectbox("徒手訓練阻力", resistance_options)
        if selected_res == "自訂輸入...":
            free_res_text = st.text_input("請輸入自訂徒手阻力說明", value="")
            manual_resistance = free_res_text
        else:
            manual_resistance = selected_res
            
        machine_resistance = st.number_input("器材訓練阻力", min_value=0, max_value=200, value=0)

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
        ex13 = st.number_input("13. 腹/背核心機", min_value=0, max_value=200, value=0)
        
        st.markdown("**📊 執行成效評估**")
        evaluation = st.selectbox("執行評值", ["佳", "可", "差"])
        rpe = st.slider("RPE 運動自覺強度 (0分極輕鬆 ~ 10分力竭)", min_value=0, max_value=10, value=3)
        
        note = st.text_input("備註說明", "")

    submit_btn = st.form_submit_button("送出紀錄")

# -----------------------------------------------------------------------------
# 4. 資料傳送邏輯
# -----------------------------------------------------------------------------

if submit_btn:
    if not SHEET_API_URL or "sheetdb.io" not in SHEET_API_URL:
        st.error("⚠️ 請確認 Streamlit 後台 Secrets 有正確填入 sheetdb 網址！")
    else:
        payload = {
            "data": [{
                "日期": date_str,
                "個案": f"{selected_id} - {selected_name}",
                "收縮壓": bp_systolic,
                "舒張壓": bp_diastolic,
                "血氧": spo2,
                "設定次數": setup_count,
                "徒手訓練阻力": manual_resistance,
                "器材訓練阻力": machine_resistance,
                "坐姿抬腿": ex1, "坐姿踩腳踏車": ex2, "坐姿腿開合": ex3, "坐姿踢腿": ex4, "椅子深蹲": ex5, "坐姿v型腿上舉": ex6,
                "腿開合機": ex7, "踢腿機": ex8, "腿推機": ex9, "划船機": ex10, "肩推機": ex11, "蝴蝶機": ex12,
                "腹/背核心機": ex13,
                "執行評值": evaluation,
                "RPE": rpe,
                "其他說明": note
            }]
        }
        
        target_url = f"{SHEET_API_URL}?sheet={location}"
        
        with st.spinner("正在安全傳送紀錄至雲端..."):
            try:
                headers = {"Content-Type": "application/json"}
                response = requests.post(target_url, data=json.dumps(payload), headers=headers, timeout=10)
                if response.status_code in [200, 201, 21]:
                    st.success(f"🎉 成功！【{location} - {selected_name}】的紀錄已寫入 Google 試算表！")
                else:
                    st.error(f"❌ 傳送失敗，錯誤碼: {response.status_code}，請確認試算表中是否有「{location}」分頁且欄位標題正確。")
            except Exception as e:
                st.error(f"❌ 連線異常: {str(e)}")
