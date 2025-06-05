import streamlit as st
import pandas as pd


# Settings
st.set_page_config(
    page_title="可視化", 
    layout="centered",
    initial_sidebar_state="expanded",
    menu_items={
        'Get help': "https://www.example.com/help", 
        'Report a bug': "https://www.example.com/bug",
        'About': "#### 可視化アプリ（仮）"
    }
)


# Functions



# Contents
st.title("データの可視化")

if "df_checkouts_w" not in st.session_state and "df_checkouts_e" not in st.session_state:
    st.error("データがアップロードされていません。最初のページでデータをアップロードしてください。")
else:
    df_checkouts_w = st.session_state["df_checkouts_w"]
    df_items_w = st.session_state["df_items_w"]
    df_payments_w = st.session_state["df_payments_w"]
    df_checkouts_e = st.session_state["df_checkouts_e"]
    df_items_e = st.session_state["df_items_e"]
    df_payments_e = st.session_state["df_payments_e"]

    st.write("以下の項目に答えてください。")
    with st.container(border=True):
        category = st.radio(
            label="可視化の種類", 
            options=["客数の可視化", "売上の可視化"], 
            captions=["例：時間帯ごと、1日ごとの客数", "例：部門ごと、商品ごとの売上"], 
            index=None
        )
    
    if category == "客数の可視化":
        with st.container(border=True):
            sub_category = st.radio(
                label="客数の可視化の種類", 
                options=["ある1日の時間帯ごとの客数の推移", 
                         "1日の合計客数の推移"], 
                captions=["例：5/25の10分ごとの客数の推移", "例：5/1から5/15までの1日の合計客数の推移"], 
                index=None
            )
        
        if sub_category == "ある1日の時間帯ごとの客数の推移":
            with st.container(border=True):
                if df_checkouts_w.shape[0] > 0:
                    if df_checkouts_e.shape[0] > 0:
                        place = st.radio(
                            label="西食堂と東カフェテリアのいずれかを選択してください。", 
                            options=["西食堂", "東カフェテリア"], 
                            index=None
                        )
                    else:
                        place = st.radio(
                            label="西食堂と東カフェテリアのいずれかを選択してください。", 
                            options=["西食堂", "東カフェテリア"], 
                            index=0, 
                            disabled=True
                        )
                else:
                    place = st.radio(
                        label="西食堂と東カフェテリアのいずれかを選択してください。", 
                        options=["西食堂", "東カフェテリア"], 
                        index=1, 
                        disabled=True
                    )

            if place == "西食堂":
                st.date_input(
                    label="日付を選択してください。", 
                    value=st.session_state["west_date_min"], 
                    min_value=st.session_state["west_date_min"],
                    max_value=st.session_state["west_date_max"]
                )
            else:
                st.date_input(
                    label="日付を選択してください。", 
                    value=st.session_state["east_date_min"], 
                    min_value=st.session_state["east_date_min"],
                    max_value=st.session_state["east_date_max"]
                )

            with st.container(border=True):
                st.radio(
                    label="昼営業と夜営業のいずれかを選択してください。", 
                    options=["昼営業", "夜営業"], 
                    captions=["11:00～14:00", "17:30～19:30"], 
                    index=None
                )

                st.radio(
                    label="何分ごとの客数を表示しますか？", 
                    options=["5分ごと", "10分ごと", "15分ごと", "30分ごと", "1時間ごと"],
                )

    elif category == "売上の可視化":
        pass

