import streamlit as st
import pandas as pd
import os
import matplotlib.pyplot as plt


def dashboard():

    st.title("💰 Smart Personal Finance Manager")

    st.subheader("🏠 Financial Dashboard")

    # -----------------------------
    # Check Income File
    # -----------------------------

    import os
    import pandas as pd

    def get_total(filename):

        if not os.path.exists(filename):
            return 0

        try:

            df = pd.read_csv(filename)

            if df.empty:
                return 0

            if "Amount" not in df.columns:
                return 0

            return df["Amount"].sum()

        except Exception:
            return 0


    total_income = get_total("data/income.csv")

    total_expense = get_total("data/expenses.csv")

    total_savings = get_total("data/savings.csv")

    balance = total_income - total_expense

    # -----------------------------
    # KPI Cards
    # -----------------------------

    c1, c2, c3, c4 = st.columns(4)

    c1.metric(
        "💰 Total Income",
        f"₹{total_income:,.0f}"
    )

    c2.metric(
        "💸 Total Expenses",
        f"₹{total_expense:,.0f}"
    )

    c3.metric(
        "💳 Savings",
        f"₹{total_savings:,.0f}"
    )

    c4.metric(
        "💵 Balance",
        f"₹{balance:,.0f}"
    )

    st.markdown("---")

    # -----------------------------
    # Financial Health
    # -----------------------------

    st.subheader("📊 Financial Health")

    if total_income == 0:

        st.info("No financial data available.")

        return

    savings_rate = (balance / total_income) * 100

    st.metric(
        "Savings Rate",
        f"{savings_rate:.2f}%"
    )

    if savings_rate >= 30:
        st.success("🟢 Excellent Financial Health")

    elif savings_rate >= 20:
        st.info("🟡 Good Financial Health")

    elif savings_rate >= 10:
        st.warning("🟠 Average Financial Health")

    else:
        st.error("🔴 Financial Risk")

    st.markdown("---")

    # -----------------------------
    # Income vs Expense
    # -----------------------------

    st.subheader("📈 Income vs Expenses")

    chart = pd.DataFrame({

        "Category": [
            "Income",
            "Expense",
            "Savings"
        ],

        "Amount": [
            total_income,
            total_expense,
            total_savings
        ]

    })

    fig, ax = plt.subplots(figsize=(7,4))

    ax.bar(
        chart["Category"],
        chart["Amount"]
    )

    ax.set_ylabel("Amount (₹)")

    st.pyplot(fig)

    st.markdown("---")

    # -----------------------------
    # Expense Ratio
    # -----------------------------

    expense_ratio = (total_expense / total_income) * 100

    st.metric(
        "Expense Ratio",
        f"{expense_ratio:.2f}%"
    )

    st.progress(min(expense_ratio / 100, 1.0))

    st.markdown("---")

    st.subheader("📌 Financial Summary")

    summary = pd.DataFrame({

        "Item": [

            "Income",

            "Expenses",

            "Savings",

            "Balance"

        ],

        "Amount": [

            total_income,

            total_expense,

            total_savings,

            balance

        ]

    })

    st.dataframe(
        summary,
        use_container_width=True
    )
