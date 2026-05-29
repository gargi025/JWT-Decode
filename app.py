# app.py
import streamlit as st
import jwt
import json
import pandas as pd

FIELD_NAMES = {
    "SellerGstin": "Seller GSTIN",
    "BuyerGstin": "Buyer GSTIN",
    "DocNo": "Invoice Number",
    "DocType": "Document Type",
    "DocDt": "Invoice Date",
    "TotInvVal": "Total Invoice Value",
    "ItemCnt": "Item Count",
    "MainHsnCode": "Main HSN Code",
    "Irn": "IRN",
    "IrnDt": "IRN Date/Time",
}

st.set_page_config(page_title="GST e-Invoice QR Decoder", page_icon="🧾", layout="wide")

st.title("🧾 GST e-Invoice QR Decoder")

token = st.text_area("Paste scanned QR/JWT text here", height=180)

if st.button("Decode Invoice"):
    try:
        decoded = jwt.decode(token.strip(), options={"verify_signature": False})

        data = decoded.get("data", decoded)

        if isinstance(data, str):
            data = json.loads(data)

        st.success("Decoded successfully")

        st.subheader("Invoice Details")

        rows = []
        for key, value in data.items():
            rows.append({
                "Field": FIELD_NAMES.get(key, key),
                "Value": value
            })

        df = pd.DataFrame(rows)
        st.dataframe(df, use_container_width=True, hide_index=True)

        st.subheader("Full Decoded JSON")
        st.json(data)

        with st.expander("JWT Header / Metadata"):
            st.json(decoded)

    except Exception as e:
        st.error(f"Could not decode this QR/JWT: {e}")
