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

with st.container(border=True):
    col1, col2 = st.columns(2)
    with col1:
        st.metric('Total Loans', f"{loan['id'].count():,.0f}", help = 'Total Number of Loans')
        st.metric('Total Loan Amount', f"${loan['loan_amount'].sum():,.0f}")
    with col2:
        st.metric('Average Interest Rate', f"{loan['interest_rate'].mean():,.2f}%")
        st.metric('Average Loan Amount', f"${loan['loan_amount'].mean():,.0f}")
st.header('Trend Analysis')
with st.container(border=True):
    tab1, tab2, tab3 = st.tabs(['Loan Issued Over Time', 'Loan Amount Over Time', 'Loan per Days Analysis'])
    with tab1:
        loan_date_count = loan.groupby('issue_date')['loan_amount'].count()
        line_count = px.line(loan_date_count,
            markers=True,
        title='Loans Issued Over Time',
        labels={
            'issue_date': 'Issue Date',
            'value': 'Number of Loans'
        }).update_traces(marker = {'color':'red'}).update_layout(showlegend = False)
        st.plotly_chart(line_count)
    with tab2:
        loan_date_sum = loan.groupby('issue_date')['loan_amount'].sum()
        line_sum = px.line(loan_date_sum,
            markers=True,
        title='Loans Amount Over Time',
        labels={
            'issue_date': 'Issue Date',
            'value': 'Number of Loans'
        }).update_traces(marker = {'color':'red'}).update_layout(showlegend = False)
        st.plotly_chart(line_sum)
    with tab3:
        loan_day_count = loan.groupby('issue_weekday')['loan_amount'].count()
        line_day = px.bar(loan_day_count,
        category_orders= {'issue_weekday' : ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']},
        title='Distribution of Loans by Day of the Week',
        labels={
            'value':'Number of Loans',
            'issue_weekday':'Day of the Week'
        },
        template='seaborn'
        ).update_layout(showlegend = False)
        st.plotly_chart(line_day)
st.header('Loan Performance')
with st.expander("Click here to expand"):
    col3, col4 = st.columns(2)
    with col3:
        pie = px.pie(loan,
        names = 'loan_condition',
        hole = 0.5,
        title = "Loans by Condition",
        template='seaborn')
        st.plotly_chart(pie)
    with col4:
        grade = loan['grade'].value_counts().sort_index()
        bar = px.bar(grade,
        title='Distribution of Loans by Grade',
        labels={
            'grade':'Grade',
            'value':'Number of Loans'
        },
        template='seaborn').update_layout(showlegend = False)
        st.plotly_chart(bar)
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
