
import streamlit as st
import pandas as pd
import os

def analytics():

    st.title("📊 Financial Analytics Dashboard")

    def total_from_csv(file_path, column):
        if not os.path.exists(file_path):
            return 0
        try:
            df = pd.read_csv(file_path)
            if column in df.columns:
                return df[column].sum()
        except Exception:
            pass
        return 0

    income = total_from_csv("data/income.csv", "Amount")
    expense = total_from_csv("data/expenses.csv", "Amount")
    savings = total_from_csv("data/savings.csv", "Amount")
    invested = total_from_csv("data/investments.csv", "Invested Amount")
    current_value = total_from_csv("data/investments.csv", "Current Value")
    emi = total_from_csv("data/emi.csv", "Monthly EMI")

    balance = income - expense
    investment_profit = current_value - invested

    c1,c2,c3,c4 = st.columns(4)

    c1.metric("💰 Income", f"₹{income:,.0f}")
    c2.metric("💸 Expenses", f"₹{expense:,.0f}")
    c3.metric("💵 Balance", f"₹{balance:,.0f}")
    c4.metric("🏦 Monthly EMI", f"₹{emi:,.0f}")

    st.markdown("---")

    c5,c6,c7 = st.columns(3)

    c5.metric("💳 Savings", f"₹{savings:,.0f}")
    c6.metric("📈 Investments", f"₹{invested:,.0f}")
    c7.metric("💹 Investment Profit", f"₹{investment_profit:,.0f}")

    st.markdown("---")

    st.subheader("Income vs Expense")

    compare = pd.DataFrame({
        "Category":["Income","Expense","Savings","Investment"],
        "Amount":[income,expense,savings,invested]
    })

    st.bar_chart(compare.set_index("Category"))

    st.markdown("---")

    st.subheader("Financial Health")

    if income == 0:
        health = 0
    else:
        health = ((income-expense)/income)*100

    st.metric("Financial Health Score", f"{health:.1f}%")

    if health >= 40:
        st.success("🟢 Excellent Financial Health")

    elif health >= 20:
        st.info("🟡 Good Financial Health")

    elif health >= 10:
        st.warning("🟠 Average Financial Health")

    else:
        st.error("🔴 Improve Savings and Reduce Expenses")

    st.markdown("---")

    st.subheader("Expense Ratio")

    if income > 0:
        ratio = (expense/income)*100
    else:
        ratio = 0

    st.progress(min(ratio/100,1.0))

    st.write(f"Expense Ratio : **{ratio:.2f}%**")

    st.markdown("---")

    st.subheader("Net Worth Summary")

    networth = savings + current_value + balance

    st.metric(
        "Estimated Net Worth",
        f"₹{networth:,.0f}"
    )

    st.markdown("---")

    st.subheader("AI Financial Suggestions")

    if expense > income:
        st.error("⚠ Expenses are higher than your income.")

    elif ratio > 70:
        st.warning("Reduce discretionary expenses.")

    else:
        st.success("Your spending is under control.")

    if emi > income*0.4:
        st.warning("Monthly EMI is more than 40% of your income.")

    if investment_profit > 0:
        st.success("Your investments are generating positive returns.")

    if savings < income*0.2:
        st.info("Try to save at least 20% of your monthly income.")
