import streamlit as st
import folium
from streamlit_folium import folium_static
import pandas as pd

# CSVファイルを読み込む
df = pd.read_csv('./UNIV_MST.csv')

# 必要なカラムを抽出
columns_to_select = ['UNIV_NAME', 'LATITUDE', 'LONGITUDE', 'FACULTY', 'KEITOU_NM']
selected_data = df[columns_to_select]

universities = {}
for index, row in selected_data.iterrows():
    name = row['UNIV_NAME']
    location = [row['LATITUDE'], row['LONGITUDE']]
    faculty = row['FACULTY']
    keitou_nm = row['KEITOU_NM']
    universities[name] = {"location": location, "faculty": faculty, "keitou_nm": keitou_nm}

# 日本地図を表示する関数
def show_map(selected_keitou=None):
    # 地図の中心を日本に設定
    map_center = [36.2048, 138.2529]
    japan_map = folium.Map(
        location=map_center,
        zoom_start=5
        # width = 1000, height = 1000 # 地図のサイズ
    )

    # 学部系統による色の辞書
    keitou_colors = {
        "人文学系": "red",
        "教育学系": "orange",
        "法律・政治系": "purple",
        "経済・経営・商学系": "pink",
        "社会・国際学系": "blue",
        "理工系": "green",
        "農・水産・獣医系": "darkgreen",
        "医学系": "darkblue",
        "芸術・スポーツ科学系": "gray",
        "総合・環境・情報・人間学系": "lightgreen",
        "大学院大学": "black"
    }

    # 大学の位置にピンを立てる
    for uni, info in universities.items():
        if selected_keitou is None or info["keitou_nm"] == selected_keitou:
            color = keitou_colors.get(info["keitou_nm"], "red")  # 学部系統に対応する色を取得
            folium.Marker(
                location=info["location"],
                popup=f"{uni}",
                icon=folium.Icon(color=color)
            ).add_to(japan_map)

    # Streamlitに地図を表示
    folium_static(japan_map)

# Streamlitアプリの設定
st.set_page_config(layout="wide")

# 日本地図を表示
st.title("日本の国立大学位置情報")

# ボタンを追加
selected_keitou = st.radio("表示する分類を選択してください", options=[
    "人文学系",
    "教育学系",
    "法律・政治系",
    "経済・経営・商学系",
    "社会・国際学系",
    "理工系",
    "農・水産・獣医系",
    "医学系",
    "芸術・スポーツ科学系",
    "総合・環境・情報・人間学系",
    "大学院大学"
], horizontal=True)

# 選択された学部系統に応じて地図を表示
show_map(selected_keitou)
