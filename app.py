import streamlit as st

from modules.dashboard import dashboard
from modules.income import income
from modules.expense import expense
from modules.emi import emi
from modules.savings import savings
from modules.analytics import analytics
from modules.reports import reports
from modules.investments import investments
from modules.ai_advisor import ai_advisor

st.set_page_config(
    page_title="Smart Personal Finance Manager",
    page_icon="💰",
    layout="wide"
)

st.sidebar.title("💰 Smart Personal Finance Manager")

menu = st.sidebar.radio(
    "Navigation",
    [
        "🏠 Dashboard",
        "💰 Income",
        "💸 Expenses",
        "🏦 EMI Manager",
        "💳 Savings",
        "📈 Investments",
        "📊 Analytics",
        "📑 Reports",
        "🤖 AI Advisor",
        "ℹ About"
    ]
)

if menu == "🏠 Dashboard":
    dashboard()

elif menu == "💰 Income":
    income()

elif menu == "💸 Expenses":
    expense()

elif menu == "🏦 EMI Manager":
    emi()

elif menu == "💳 Savings":
    savings()

elif menu == "📈 Investments":
    investments()

elif menu == "📊 Analytics":
    analytics()

elif menu == "📑 Reports":
    reports()

elif menu == "🤖 AI Advisor":
    ai_advisor()

elif menu == "ℹ About":

    st.title("ℹ About")

    st.markdown("""
    ## Smart Personal Finance Manager

    A professional personal finance management application
    developed using Python and Streamlit.

    ### Features

    - Income Management
    - Expense Tracking
    - EMI Management
    - Savings Planner
    - Investment Tracker
    - Financial Analytics
    - Reports
    - AI Financial Advisor

    **Author:** Dr. K. Natarajan
    """)
