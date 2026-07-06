
import streamlit as st
import pandas as pd
import os
from datetime import date

def savings():
    st.title("💳 Savings Manager")

    os.makedirs("data", exist_ok=True)
    filename="data/savings.csv"
    cols=["Date","Goal","Amount","Target Amount","Remarks"]

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

    st.subheader("Add Savings")

    with st.form("saving_form",clear_on_submit=True):
        d=st.date_input("Date",value=date.today())
        goal=st.selectbox("Savings Goal",[
            "Emergency Fund","House","Car","Education",
            "Vacation","Retirement","Investment","Other"
        ])
        amt=st.number_input("Saved Amount (₹)",min_value=0.0,step=100.0)
        target=st.number_input("Target Amount (₹)",min_value=0.0,step=1000.0)
        remarks=st.text_input("Remarks")
        ok=st.form_submit_button("💾 Save")

    if ok:
        new=pd.DataFrame([{
            "Date":d,
            "Goal":goal,
            "Amount":amt,
            "Target Amount":target,
            "Remarks":remarks
        }])
        df=pd.concat([df,new],ignore_index=True)
        df.to_csv(filename,index=False)
        st.success("Savings record added.")
        st.rerun()

    df=pd.read_csv(filename)

    if df.empty:
        st.info("No savings records available.")
        return

    st.subheader("Savings History")
    st.dataframe(df,use_container_width=True)

    total_saved=df["Amount"].sum()
    total_target=df["Target Amount"].sum()
    progress=(total_saved/total_target*100) if total_target>0 else 0

    c1,c2,c3,c4=st.columns(4)
    c1.metric("Total Saved",f"₹{total_saved:,.0f}")
    c2.metric("Target",f"₹{total_target:,.0f}")
    c3.metric("Progress",f"{progress:.1f}%")
    c4.metric("Goals",df["Goal"].nunique())

    st.progress(min(progress/100,1.0))

    st.markdown("---")
    st.subheader("Savings by Goal")
    st.bar_chart(df.groupby("Goal")["Amount"].sum())

    st.subheader("Savings Trend")
    st.line_chart(df.groupby("Date")["Amount"].sum())

    st.subheader("Goal Progress")
    gp=df.groupby("Goal")[["Amount","Target Amount"]].sum()
    st.dataframe(gp,use_container_width=True)

    csv=df.to_csv(index=False).encode("utf-8")
    st.download_button(
        "📥 Download Savings Report",
        csv,
        file_name="savings_report.csv",
        mime="text/csv"
    )

    st.markdown("---")
    idx=st.selectbox(
        "Delete Savings Record",
        df.index,
        format_func=lambda i:f"{i} | {df.loc[i,'Goal']} | ₹{df.loc[i,'Amount']:,.0f}"
    )

    if st.button("🗑 Delete Selected Record"):
        df=df.drop(idx).reset_index(drop=True)
        df.to_csv(filename,index=False)
        st.success("Savings record deleted.")
        st.rerun()
