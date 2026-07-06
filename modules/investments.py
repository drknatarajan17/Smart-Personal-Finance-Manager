
import streamlit as st
import pandas as pd
import os
from datetime import date

def investments():
    st.title("📈 Investment Portfolio Manager")

    os.makedirs("data", exist_ok=True)
    filename = "data/investments.csv"
    cols = ["Date","Investment Type","Investment Name","Invested Amount","Current Value","Remarks"]

    if (not os.path.exists(filename)) or os.path.getsize(filename)==0:
        pd.DataFrame(columns=cols).to_csv(filename,index=False)

    try:
        df = pd.read_csv(filename)
    except Exception:
        df = pd.DataFrame(columns=cols)
        df.to_csv(filename,index=False)

    if list(df.columns)!=cols:
        df = pd.DataFrame(columns=cols)
        df.to_csv(filename,index=False)

    st.subheader("Add Investment")

    with st.form("investment_form", clear_on_submit=True):
        inv_date = st.date_input("Investment Date", value=date.today())
        inv_type = st.selectbox("Investment Type",[
            "Stocks","Mutual Fund","SIP","Fixed Deposit","Gold",
            "PPF","EPF","Cryptocurrency","Real Estate","Other"
        ])
        inv_name = st.text_input("Investment Name")
        invested = st.number_input("Invested Amount (₹)", min_value=0.0, step=100.0)
        current = st.number_input("Current Value (₹)", min_value=0.0, step=100.0)
        remarks = st.text_input("Remarks")
        submit = st.form_submit_button("➕ Add Investment")

    if submit:
        new = pd.DataFrame([{
            "Date":inv_date,
            "Investment Type":inv_type,
            "Investment Name":inv_name,
            "Invested Amount":invested,
            "Current Value":current,
            "Remarks":remarks
        }])
        df = pd.concat([df,new], ignore_index=True)
        df.to_csv(filename,index=False)
        st.success("Investment added successfully.")
        st.rerun()

    df = pd.read_csv(filename)

    if df.empty:
        st.info("No investment records available.")
        return

    df["Profit/Loss"] = df["Current Value"] - df["Invested Amount"]
    df["ROI (%)"] = ((df["Current Value"]-df["Invested Amount"]) /
                     df["Invested Amount"].replace(0,1))*100

    st.subheader("Investment Portfolio")
    st.dataframe(df, use_container_width=True)

    total_invested = df["Invested Amount"].sum()
    current_value = df["Current Value"].sum()
    profit = current_value - total_invested
    roi = (profit/total_invested*100) if total_invested>0 else 0

    c1,c2,c3,c4 = st.columns(4)
    c1.metric("Total Invested", f"₹{total_invested:,.0f}")
    c2.metric("Current Value", f"₹{current_value:,.0f}")
    c3.metric("Profit / Loss", f"₹{profit:,.0f}")
    c4.metric("Overall ROI", f"{roi:.2f}%")

    st.progress(min(max((roi+100)/200,0),1))

    st.markdown("---")
    st.subheader("Investment Distribution")
    st.bar_chart(df.groupby("Investment Type")["Invested Amount"].sum())

    st.subheader("Current Portfolio Value")
    st.bar_chart(df.groupby("Investment Type")["Current Value"].sum())

    st.subheader("Top Performing Investments")
    top = df.sort_values("ROI (%)", ascending=False)[
        ["Investment Name","Investment Type","ROI (%)","Profit/Loss"]
    ]
    st.dataframe(top, use_container_width=True)

    csv = df.to_csv(index=False).encode("utf-8")
    st.download_button(
        "📥 Download Investment Report",
        csv,
        file_name="investment_report.csv",
        mime="text/csv"
    )

    st.markdown("---")
    idx = st.selectbox(
        "Delete Investment",
        df.index,
        format_func=lambda i: f"{i} | {df.loc[i,'Investment Name']} | {df.loc[i,'Investment Type']}"
    )

    if st.button("🗑 Delete Selected Investment"):
        df = df.drop(idx).reset_index(drop=True)
        df.to_csv(filename,index=False)
        st.success("Investment deleted successfully.")
        st.rerun()
