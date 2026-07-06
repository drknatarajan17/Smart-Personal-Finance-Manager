
import streamlit as st
import pandas as pd
import os
from datetime import date

def income():
    st.title("💰 Income Management")
    os.makedirs("data", exist_ok=True)
    filename="data/income.csv"
    cols=["Date","Source","Amount","Remarks"]
    if (not os.path.exists(filename)) or os.path.getsize(filename)==0:
        pd.DataFrame(columns=cols).to_csv(filename,index=False)
    try:
        df=pd.read_csv(filename)
    except:
        df=pd.DataFrame(columns=cols)
        df.to_csv(filename,index=False)
    if list(df.columns)!=cols:
        df=pd.DataFrame(columns=cols)
        df.to_csv(filename,index=False)

    with st.form("income"):
        d=st.date_input("Date",value=date.today())
        src=st.selectbox("Source",["Salary","Business","Freelancing","Rental Income","Interest","Dividend","Bonus","Pension","Other"])
        amt=st.number_input("Amount (₹)",min_value=0.0,step=100.0)
        rem=st.text_input("Remarks")
        ok=st.form_submit_button("➕ Add Income")
    if ok:
        new=pd.DataFrame([{"Date":d,"Source":src,"Amount":amt,"Remarks":rem}])
        df=pd.concat([df,new],ignore_index=True)
        df.to_csv(filename,index=False)
        st.success("Income added.")
        st.rerun()

    df=pd.read_csv(filename)
    if df.empty:
        st.info("No income records.")
        return
    st.dataframe(df,use_container_width=True)
    c1,c2,c3=st.columns(3)
    c1.metric("Total Income",f"₹{df['Amount'].sum():,.0f}")
    c2.metric("Entries",len(df))
    c3.metric("Average",f"₹{df['Amount'].mean():,.0f}")
    st.bar_chart(df.groupby("Source")["Amount"].sum())
    st.line_chart(df.groupby("Date")["Amount"].sum())
    st.download_button("📥 Download CSV",df.to_csv(index=False).encode(),"income_report.csv","text/csv")
    idx=st.selectbox("Delete Record",df.index,format_func=lambda i:f"{i} | {df.loc[i,'Source']} | ₹{df.loc[i,'Amount']:,.0f}")
    if st.button("🗑 Delete"):
        df=df.drop(idx).reset_index(drop=True)
        df.to_csv(filename,index=False)
        st.success("Deleted.")
        st.rerun()
