
import streamlit as st
import pandas as pd
import os

def reports():
    st.title("📑 Financial Reports")

    def load(path):
        if os.path.exists(path):
            try:
                return pd.read_csv(path)
            except:
                pass
        return pd.DataFrame()

    income=load("data/income.csv")
    expense=load("data/expenses.csv")
    savings=load("data/savings.csv")
    emi=load("data/emi.csv")
    invest=load("data/investments.csv")

    total_income=income["Amount"].sum() if "Amount" in income.columns else 0
    total_expense=expense["Amount"].sum() if "Amount" in expense.columns else 0
    total_savings=savings["Amount"].sum() if "Amount" in savings.columns else 0
    total_emi=emi["Monthly EMI"].sum() if "Monthly EMI" in emi.columns else 0
    total_invested=invest["Invested Amount"].sum() if "Invested Amount" in invest.columns else 0
    current_value=invest["Current Value"].sum() if "Current Value" in invest.columns else 0

    balance=total_income-total_expense
    profit=current_value-total_invested
    networth=balance+total_savings+current_value

    c1,c2,c3=st.columns(3)
    c1.metric("Income",f"₹{total_income:,.0f}")
    c2.metric("Expense",f"₹{total_expense:,.0f}")
    c3.metric("Balance",f"₹{balance:,.0f}")

    c4,c5,c6=st.columns(3)
    c4.metric("Savings",f"₹{total_savings:,.0f}")
    c5.metric("Monthly EMI",f"₹{total_emi:,.0f}")
    c6.metric("Net Worth",f"₹{networth:,.0f}")

    st.markdown("---")
    st.subheader("Financial Summary")

    summary=pd.DataFrame({
        "Part":[
            "Income","Expense","Balance","Savings",
            "Monthly EMI","Investment","Current Value",
            "Investment Profit","Net Worth"
        ],
        "Amount":[
            total_income,total_expense,balance,total_savings,
            total_emi,total_invested,current_value,
            profit,networth
        ]
    })

    st.dataframe(summary,use_container_width=True)

    st.subheader("Financial Overview")
    st.bar_chart(summary.set_index("Part"))

    st.markdown("---")
    st.subheader("Individual Reports")

    tabs=st.tabs(["Income","Expenses","Savings","EMI","Investments"])

    with tabs[0]:
        st.dataframe(income,use_container_width=True)
    with tabs[1]:
        st.dataframe(expense,use_container_width=True)
    with tabs[2]:
        st.dataframe(savings,use_container_width=True)
    with tabs[3]:
        st.dataframe(emi,use_container_width=True)
    with tabs[4]:
        st.dataframe(invest,use_container_width=True)

    st.markdown("---")
    st.subheader("Download Reports")

    for name,df in [("Income",income),("Expense",expense),("Savings",savings),("EMI",emi),("Investment",invest)]:
        if not df.empty:
            st.download_button(
                f"📥 Download {name} Report",
                df.to_csv(index=False).encode("utf-8"),
                file_name=f"{name.lower()}_report.csv",
                mime="text/csv"
            )

    st.download_button(
        "📥 Download Financial Summary",
        summary.to_csv(index=False).encode("utf-8"),
        file_name="financial_summary.csv",
        mime="text/csv"
    )
