import streamlit as st
import pandas as pd
import os
from datetime import date

def emi():
    st.title("🏦 EMI Manager")

    os.makedirs("data", exist_ok=True)
    filename="data/emi.csv"
    cols=["Loan Type","Bank","Loan Amount","Monthly EMI","Outstanding Balance","Due Date","Remarks"]

    if (not os.path.exists(filename)) or os.path.getsize(filename)==0:
        pd.DataFrame(columns=cols).to_csv(filename,index=False)

    try:
        df=pd.read_csv(filename)
    except Exception:
        df=pd.DataFrame(columns=cols)
        df.to_csv(filename,index=False)

    if list(df.columns)!=cols:
        df=pd.DataFrame(columns=cols)
        df.to_csv(filename,index=False)

    st.subheader("Add EMI / Loan")

    with st.form("emi_form", clear_on_submit=True):
        loan_type=st.selectbox("Loan Type",[
            "Home Loan","Car Loan","Personal Loan","Education Loan","Gold Loan","Business Loan","Other"
        ])
        bank=st.text_input("Bank / Finance Company")
        loan_amount=st.number_input("Loan Amount (₹)",min_value=0.0,step=1000.0)
        monthly_emi=st.number_input("Monthly EMI (₹)",min_value=0.0,step=100.0)
        outstanding=st.number_input("Outstanding Balance (₹)",min_value=0.0,step=1000.0)
        due_date=st.date_input("Next EMI Due Date",value=date.today())
        remarks=st.text_input("Remarks")
        submit=st.form_submit_button("➕ Add Loan")

    if submit:
        new=pd.DataFrame([{
            "Loan Type":loan_type,
            "Bank":bank,
            "Loan Amount":loan_amount,
            "Monthly EMI":monthly_emi,
            "Outstanding Balance":outstanding,
            "Due Date":due_date,
            "Remarks":remarks
        }])
        df=pd.concat([df,new],ignore_index=True)
        df.to_csv(filename,index=False)
        st.success("Loan added successfully.")
        st.rerun()

    df=pd.read_csv(filename)

    if df.empty:
        st.info("No EMI records available.")
        return

    st.subheader("Loan Details")
    st.dataframe(df,use_container_width=True)

    st.markdown("---")
    c1,c2,c3,c4=st.columns(4)
    c1.metric("Total Loans",len(df))
    c2.metric("Total Loan Amount",f"₹{df['Loan Amount'].sum():,.0f}")
    c3.metric("Monthly EMI",f"₹{df['Monthly EMI'].sum():,.0f}")
    c4.metric("Outstanding",f"₹{df['Outstanding Balance'].sum():,.0f}")

    st.markdown("---")
    st.subheader("Loan Type Distribution")
    st.bar_chart(df.groupby("Loan Type")["Loan Amount"].sum())

    st.subheader("Monthly EMI Distribution")
    st.bar_chart(df.groupby("Loan Type")["Monthly EMI"].sum())

    st.subheader("Outstanding Balance")
    st.bar_chart(df.groupby("Loan Type")["Outstanding Balance"].sum())

    st.markdown("---")
    csv=df.to_csv(index=False).encode("utf-8")
    st.download_button(
        "📥 Download EMI Report",
        csv,
        file_name="emi_report.csv",
        mime="text/csv"
    )

    st.markdown("---")
    idx=st.selectbox(
        "Delete Loan",
        df.index,
        format_func=lambda i:f"{i} | {df.loc[i,'Loan Type']} | {df.loc[i,'Bank']}"
    )

    if st.button("🗑 Delete Selected Loan"):
        df=df.drop(idx).reset_index(drop=True)
        df.to_csv(filename,index=False)
        st.success("Loan deleted successfully.")
        st.rerun()

