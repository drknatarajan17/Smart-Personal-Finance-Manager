
import streamlit as st
import pandas as pd
import os
from datetime import date

def expense():
    st.title("💸 Expense Management")

    os.makedirs("data", exist_ok=True)
    filename = "data/expenses.csv"
    cols = ["Date","Category","Amount","Remarks"]

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

    categories=[
        "House Rent","EMI","Petrol","Groceries","Provisions",
        "Milk","Vegetables","Electricity","Water Bill","Internet",
        "Mobile Recharge","Medical","School Fees","Shopping",
        "Entertainment","Insurance","Travel","Vehicle Maintenance",
        "Donations","Miscellaneous"
    ]

    with st.form("expense_form", clear_on_submit=True):
        d = st.date_input("Expense Date", value=date.today())
        cat = st.selectbox("Category", categories)
        amt = st.number_input("Amount (₹)", min_value=0.0, step=100.0)
        rem = st.text_input("Remarks")
        ok = st.form_submit_button("➕ Add Expense")

    if ok:
        new = pd.DataFrame([{
            "Date": d,
            "Category": cat,
            "Amount": amt,
            "Remarks": rem
        }])
        df = pd.concat([df,new], ignore_index=True)
        df.to_csv(filename,index=False)
        st.success("Expense added successfully.")
        st.rerun()

    df = pd.read_csv(filename)

    if df.empty:
        st.info("No expense records available.")
        return

    st.subheader("Expense History")
    st.dataframe(df, use_container_width=True)

    st.markdown("---")
    c1,c2,c3 = st.columns(3)
    c1.metric("Total Expense", f"₹{df['Amount'].sum():,.0f}")
    c2.metric("Entries", len(df))
    c3.metric("Average Expense", f"₹{df['Amount'].mean():,.0f}")

    st.markdown("---")
    filt = st.selectbox("Filter Category", ["All"]+sorted(df["Category"].unique().tolist()))
    show = df if filt=="All" else df[df["Category"]==filt]
    st.dataframe(show, use_container_width=True)

    st.subheader("Expense by Category")
    st.bar_chart(df.groupby("Category")["Amount"].sum())

    st.subheader("Daily Expense Trend")
    st.line_chart(df.groupby("Date")["Amount"].sum())

    st.subheader("Top Expense Categories")
    top = df.groupby("Category")["Amount"].sum().sort_values(ascending=False).head(5)
    st.dataframe(top)

    csv = df.to_csv(index=False).encode("utf-8")
    st.download_button(
        "📥 Download Expense Report",
        csv,
        file_name="expense_report.csv",
        mime="text/csv"
    )

    st.markdown("---")
    idx = st.selectbox(
        "Delete Record",
        df.index,
        format_func=lambda i: f"{i} | {df.loc[i,'Category']} | ₹{df.loc[i,'Amount']:,.0f}"
    )

    if st.button("🗑 Delete Selected Expense"):
        df = df.drop(idx).reset_index(drop=True)
        df.to_csv(filename,index=False)
        st.success("Expense deleted successfully.")
        st.rerun()
