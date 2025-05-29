import streamlit as st
import pandas as pd
from io import BytesIO
import zipfile


st.set_page_config(
    page_title="upload page"
)


st.file_uploader(
    label="Upload a `.zip` file / files here.", 
    type=["zip"], 
    accept_multiple_files=True, 
    key="uploaded_zip_files"
)


def cleanup_checkouts(df_checkouts: pd.DataFrame, df_items: pd.DataFrame, df_payments: pd.DataFrame):
    df_deleted = df_checkouts[["会計ID", "削除日時"]]

    df_items = pd.merge(left=df_items, right=df_deleted, on="会計ID", how="left")
    df_payments = pd.merge(left=df_payments, right=df_deleted, on="会計ID", how="left")

    df_checkouts = df_checkouts[pd.isna(df_checkouts["削除日時"])].copy()
    df_items = df_items[pd.isna(df_items["削除日時"])].copy()
    df_payments = df_payments[pd.isna(df_payments["削除日時"])].copy()

    df_checkouts.drop(labels=["預かり金額", "釣銭金額", "レジ担当者", "メモ"], 
                      axis="columns", inplace=True)
    
    df_items.drop(labels=["SKU", "未使用"])
    return None


if st.button(label="Confirm / Revise data"):
    df_checkouts = pd.DataFrame()
    df_items = pd.DataFrame()
    df_payments = pd.DataFrame()
    for zip_file in st.session_state["uploaded_zip_files"]:
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
    
    st.session_state["df_checkouts"] = df_checkouts
    st.session_state["df_items"] = df_items 
    st.session_state["df_payments"] = df_payments


st.write("# Uploaded data")
if "df_checkouts" in st.session_state:
    if st.session_state["df_checkouts"].shape[0] > 0:
        st.session_state["df_checkouts"]
        st.session_state["df_payments"]
        st.session_state["df_items"]
        st.session_state["df_items"]["SKU"].to_list() == st.session_state["df_items"]["バーコード"].to_list()
    else:
        st.write("""
                 DataFrame is empty.\n
                 Please upload a `.zip` file / files.
                 """)
else:
    st.write("df_checkouts not in session state.")
