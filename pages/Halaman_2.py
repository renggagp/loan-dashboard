import streamlit as st
import pandas as pd
import plotly.express as px
st.set_page_config(page_title="Loan Analytic Dashboard", page_icon="🐱‍🐉")
loan = pd.read_pickle('data_input/loan_clean')
loan['purpose'] = loan['purpose'].str.replace("_", " ")

st.title("Financial Insights Dashboard: Loan Performance & Trend")
st.markdown("---")
st.sidebar.header("Dashboard Filters and Features")

st.sidebar.markdown('''
- **Overview**: Provides a summary of key loan metrics.
- **Time-Based Analysis**: Shows trends over time and loan amounts.
- **Loan Performance**: Analyzes loan conditions and distributions.
- **Financial Analysis**: Examines loan amounts and distributions based on conditions.''')

st.header('Financial Analysis')
condition  = st.selectbox('Select Loan Condition', ["Good Loan", "Bad Loan"])
loan_condition = loan[loan['loan_condition'] == condition]
tab4, tab5 = st.tabs(['Loan Amount Distribution', 'Loan Amount Distribution by Purpose'])
with tab4:
    distribution = px.histogram(loan_condition,
             x = 'loan_amount', color = 'term', nbins = 20,
              title = 'Loan Amount Distribution',
              template='seaborn',
    labels={
        'loan_amount':'Loan Amount',
        'term':'Loan Term'}
              )
    st.plotly_chart(distribution)
with tab5:
    distributionbypurpose = px.box(loan_condition,
       x = 'purpose',
       y = 'loan_amount',
       color = 'term',
       title="Loan Amount Distribution by Purpose",
    template='seaborn',
    labels={
        'purpose':'Loan Purpose',
        'loan_amount':'Loan Amount'})
    st.plotly_chart(distributionbypurpose)