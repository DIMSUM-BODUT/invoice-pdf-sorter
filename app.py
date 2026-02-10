import streamlit as st

st.set_page_config(page_title="Invoice PDF Sorter", layout="wide")
st.title("Invoice PDF Sorter (Draft)")

uploaded = st.file_uploader("Upload PDF invoice", type=["pdf"])

mode = st.selectbox("Sort berdasarkan", ["Total Qty", "SKU (A-Z)"])

if uploaded:
    st.success("PDF berhasil di-upload. Next: parsing SKU + QTY dan generate PDF output.")
    st.write("Mode:", mode)
