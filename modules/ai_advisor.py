
import streamlit as st
import pandas as pd
import os

def ai_advisor():

    st.title("🤖 AI Financial Advisor")

    def total(path, column):
        if not os.path.exists(path):
            return 0
        try:
            df = pd.read_csv(path)
            if column in df.columns:
                return df[column].sum()
        except Exception:
            pass
        return 0

    income = total("data/income.csv","Amount")
    expense = total("data/expenses.csv","Amount")
    savings = total("data/savings.csv","Amount")
    emi = total("data/emi.csv","Monthly EMI")
    invested = total("data/investments.csv","Invested Amount")
    current = total("data/investments.csv","Current Value")

    balance = income - expense
    roi = ((current-invested)/invested*100) if invested>0 else 0
    expense_ratio = (expense/income*100) if income>0 else 0
    savings_ratio = (savings/income*100) if income>0 else 0
    emi_ratio = (emi/income*100) if income>0 else 0

    c1,c2,c3,c4 = st.columns(4)
    c1.metric("Income", f"₹{income:,.0f}")
    c2.metric("Expense", f"₹{expense:,.0f}")
    c3.metric("Savings", f"₹{savings:,.0f}")
    c4.metric("Balance", f"₹{balance:,.0f}")

    st.markdown("---")
    st.subheader("📊 Financial Indicators")

    st.metric("Expense Ratio", f"{expense_ratio:.1f}%")
    st.metric("Savings Ratio", f"{savings_ratio:.1f}%")
    st.metric("EMI Burden", f"{emi_ratio:.1f}%")
    st.metric("Investment ROI", f"{roi:.2f}%")

    st.markdown("---")
    st.subheader("🧠 AI Financial Suggestions")

    suggestions=[]

    if income == 0:
        suggestions.append(("⚠️","No income records found. Add your income to receive meaningful advice."))
    else:
        if expense_ratio > 80:
            suggestions.append(("🔴","Expenses exceed 80% of your income. Review discretionary spending."))
        elif expense_ratio > 60:
            suggestions.append(("🟡","Expenses are moderately high. Aim to reduce non-essential purchases."))
        else:
            suggestions.append(("🟢","Your spending is under reasonable control."))

        if savings_ratio < 20:
            suggestions.append(("💰","Try to save at least 20% of your monthly income."))
        else:
            suggestions.append(("✅","Your savings habit is healthy."))

        if emi_ratio > 40:
            suggestions.append(("🏦","EMI commitments are above the recommended 40% of income."))
        else:
            suggestions.append(("🏦","EMI burden is within a comfortable range."))

    if invested == 0:
        suggestions.append(("📈","Consider starting a long-term investment plan such as SIP or PPF."))
    elif roi < 0:
        suggestions.append(("📉","Your portfolio is currently at a loss. Review asset allocation."))
    else:
        suggestions.append(("📈","Your investments are generating positive returns."))

    if balance < 0:
        suggestions.append(("🚨","Monthly cash flow is negative. Reduce expenses or increase income."))
    else:
        suggestions.append(("🎯","Positive cash flow. Continue building your emergency fund."))

    for icon,msg in suggestions:
        st.write(f"{icon} {msg}")

    st.markdown("---")
    st.subheader("⭐ Overall Financial Score")

    score = 100
    if expense_ratio > 80:
        score -= 30
    elif expense_ratio > 60:
        score -= 15

    if savings_ratio < 20:
        score -= 20

    if emi_ratio > 40:
        score -= 20

    if roi < 0:
        score -= 10

    score = max(score,0)

    st.metric("Financial Score", f"{score}/100")
    st.progress(score/100)

    if score >= 85:
        st.success("Excellent financial health.")
    elif score >= 70:
        st.info("Good financial health with room for improvement.")
    elif score >= 50:
        st.warning("Average financial health. Review your budget.")
    else:
        st.error("Financial health needs attention. Focus on reducing expenses and increasing savings.")
