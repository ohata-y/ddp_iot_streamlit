import streamlit as st
import pandas as pd
from io import BytesIO
import zipfile


# Settings
st.set_page_config(
    page_title="データアップロード", 
    layout="centered",
    initial_sidebar_state="expanded",
    menu_items={
        'Get help': "https://www.example.com/help", 
        'Report a bug': "https://www.example.com/bug",
        'About': "#### 可視化アプリ（仮）"
    }
)


# Functions
def load_uploaded_zip_files(zip_files):
    df_checkouts = pd.DataFrame()
    df_items = pd.DataFrame()
    df_payments = pd.DataFrame()

    for zip_file in zip_files:
        with zipfile.ZipFile(zip_file) as zf:
            for file in zf.namelist():
                if file == "checkouts.csv":
                    with zf.open(file) as f:
                        tmp = pd.read_csv(BytesIO(f.read()), encoding="shift-jis")
                        df_checkouts = pd.concat([df_checkouts, tmp], axis="index")
                elif file == "items.csv":
                    with zf.open(file) as f:
                        tmp = pd.read_csv(BytesIO(f.read()), encoding="shift-jis")
                        df_items = pd.concat([df_items, tmp], axis="index")
                elif file == "payments.csv":
                    with zf.open(file) as f:
                        tmp = pd.read_csv(BytesIO(f.read()), encoding="shift-jis")
                        df_payments = pd.concat([df_payments, tmp], axis="index")
    
    return df_checkouts, df_items, df_payments


def cleanup_pos(df_checkouts: pd.DataFrame, df_items: pd.DataFrame, df_payments: pd.DataFrame):
    df_checkouts = df_checkouts[["アカウント名", "会計ID", "開始日時", "会計日時", 
                                 "削除日時", "金額", "客数"]]
    df_items = df_items[["アカウント名", "会計ID", "SKU", "バーコード", 
                         "名前", "数量", "金額", "部門"]]
    df_payments = df_payments[["アカウント名", "会計ID", "支払い方法"]]

    # 会計が取り消されたものを削除
    cancelled = df_checkouts[["会計ID", "削除日時"]]
    df_checkouts = df_checkouts[df_checkouts["削除日時"].isna()].drop(columns=["削除日時"])
    df_items = pd.merge(df_items, cancelled, on="会計ID", how="left")
    df_items = df_items[df_items["削除日時"].isna()].drop(columns=["削除日時"])
    df_payments = pd.merge(df_payments, cancelled, on="会計ID", how="left")
    df_payments = df_payments[df_payments["削除日時"].isna()].drop(columns=["削除日時"])

    # paymentsの支払い方法が空欄の部分はおつりなので取り除く
    df_payments = df_payments[df_payments["支払い方法"].notna()]

    # itemsの数量がゼロ以下のものを取り除く
    # 会計が終わった後に取り消されたものだと思われる
    invalid_cnt = df_items.query('数量 <= 0')["会計ID"].to_list()
    df_checkouts = df_checkouts[~df_checkouts["会計ID"].isin(invalid_cnt)]
    df_items = df_items[~df_items["会計ID"].isin(invalid_cnt)]
    df_payments = df_payments[~df_payments["会計ID"].isin(invalid_cnt)]

    # 西と東でわける
    df_checkouts_w = df_checkouts[df_checkouts["アカウント名"] == "ub396203"].drop(columns=["アカウント名"])
    df_checkouts_e = df_checkouts[df_checkouts["アカウント名"] == "ub396207"].drop(columns=["アカウント名"])
    df_items_w = df_items[df_items["アカウント名"] == "ub396203"].drop(columns=["アカウント名"])
    df_items_e = df_items[df_items["アカウント名"] == "ub396207"].drop(columns=["アカウント名"])
    df_payments_w = df_payments[df_payments["アカウント名"] == "ub396203"].drop(columns=["アカウント名"])
    df_payments_e = df_payments[df_payments["アカウント名"] == "ub396207"].drop(columns=["アカウント名"])

    # paymentsの支払い方法をOne-Hot Encodingし、まとめる
    # これによって、複数支払いの場合も1つの会計IDにまとめられる
    df_payments_w = pd.get_dummies(df_payments_w, columns=["支払い方法"], 
                                   prefix="", prefix_sep="", dtype="int")
    df_payments_w = df_payments_w.groupby("会計ID").sum().reset_index()
    df_payments_e = pd.get_dummies(df_payments_e, columns=["支払い方法"], 
                                   prefix="", prefix_sep="", dtype="int")
    df_payments_e = df_payments_e.groupby("会計ID").sum().reset_index()

    # データ型を修正
    df_checkouts_w["開始日時"] = pd.to_datetime(df_checkouts_w["開始日時"]).map(lambda x: x.tz_localize(None))
    df_checkouts_w["会計日時"] = pd.to_datetime(df_checkouts_w["会計日時"]).map(lambda x: x.tz_localize(None))
    df_checkouts_w = df_checkouts_w.astype({"会計ID": "str", "金額": "int", "客数": "int"})
    df_checkouts_e["開始日時"] = pd.to_datetime(df_checkouts_e["開始日時"]).map(lambda x: x.tz_localize(None))
    df_checkouts_e["会計日時"] = pd.to_datetime(df_checkouts_e["会計日時"]).map(lambda x: x.tz_localize(None))
    df_checkouts_e = df_checkouts_e.astype({"会計ID": "str", "金額": "int", "客数": "int"})
    df_items_w = df_items_w.astype({"会計ID": "str", "SKU": "str", "バーコード": "str", 
                                    "名前": "str", "数量": "int", "金額": "int", "部門": "str"})
    df_items_e = df_items_e.astype({"会計ID": "str", "SKU": "str", "バーコード": "str", 
                                    "名前": "str", "数量": "int", "金額": "int", "部門": "str"})
    df_payments_w = df_payments_w.astype({"会計ID": "str"})
    df_payments_e = df_payments_e.astype({"会計ID": "str"})

    return df_checkouts_w, df_items_w, df_payments_w, df_checkouts_e, df_items_e, df_payments_e


# とりあえず今はデータに忠実に処理するため、実装しない
def exclude_outlier():
    return None


# Contents
st.title("データアップロード")
st.write("## POSデータ")

st.file_uploader(
    label="ユビレジアプリからエクスポートした`.zip`ファイル（`.csv`形式）をアップロードしてください。", 
    type=["zip"], 
    accept_multiple_files=True, 
    key="uploaded_zip_files"
)

if "uploaded_zip_files" not in st.session_state:
    st.session_state["button_disabled"] = True
else:
    if len(st.session_state["uploaded_zip_files"]) > 0:
        st.session_state["button_disabled"] = False
    else:
        st.session_state["button_disabled"] = True

if st.button(label="使用するデータを決定する", disabled=st.session_state["button_disabled"]):
    df_checkouts, df_items, df_payments = load_uploaded_zip_files(st.session_state["uploaded_zip_files"])
    if df_checkouts.shape[0] > 0:
        df_checkouts_w, df_items_w, df_payments_w, df_checkouts_e, df_items_e, df_payments_e = cleanup_pos(df_checkouts, df_items, df_payments)
        st.session_state["df_checkouts_w"] = df_checkouts_w
        st.session_state["df_items_w"] = df_items_w 
        st.session_state["df_payments_w"] = df_payments_w
        st.session_state["df_checkouts_e"] = df_checkouts_e
        st.session_state["df_items_e"] = df_items_e
        st.session_state["df_payments_e"] = df_payments_e

        st.session_state["west_date_min"] = df_checkouts_w["会計日時"].min()
        st.session_state["west_date_max"] = df_checkouts_w["会計日時"].max()
        st.session_state["east_date_min"] = df_checkouts_e["会計日時"].min()
        st.session_state["east_date_max"] = df_checkouts_e["会計日時"].max()

        st.success("データのアップロードが完了しました。次のページに進んでください。")

