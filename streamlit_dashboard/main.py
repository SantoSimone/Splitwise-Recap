import datetime

import splitwise
import streamlit as st
import plotly.express as px

from globals import SPLITWISE_CONSUMER_KEY, SPLITWISE_CONSUMER_SECRET, SPLITWISE_API_KEY
from streamlit_dashboard.dashboard_utils import read_from_splitwise, filter_df_by_categories, filter_df_by_months
from streamlit_dashboard.personal import personal_page
from streamlit_dashboard.changes_over_time import changes_page


def recap_page():
    df = st.session_state.df

    st.write(f'Recap of expenses from {st.session_state.start_date} to {st.session_state.end_date}')

    col1, col2 = st.columns([1, 1])
    with col1:
        st.title('Per category')
        by_category_df = filter_df_by_categories(df)
        st.dataframe(by_category_df, use_container_width=True, hide_index=True)
        fig = px.pie(by_category_df, values='Sum', names='Category', title='Per category')
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.title('Per month')
        by_months_df = filter_df_by_months(df)
        st.dataframe(by_months_df, use_container_width=True, hide_index=True)
        fig = px.pie(by_months_df, values='Sum', names='Month', title='Per month')
        st.plotly_chart(fig, use_container_width=True)

    st.title('Raw data')
    st.dataframe(df, use_container_width=True, hide_index=True)


if __name__ == '__main__':
    st.set_page_config(layout='wide')
    st.session_state.splitwise_instance = splitwise.Splitwise(
        consumer_key=SPLITWISE_CONSUMER_KEY,
        consumer_secret=SPLITWISE_CONSUMER_SECRET,
        api_key=SPLITWISE_API_KEY
    )
    groups = st.session_state.splitwise_instance.getGroups()
    st.session_state.group = st.sidebar.selectbox(label='Group', options=[g.name for g in groups], index=1)

    col1, col2, col3 = st.sidebar.columns([1, 1, 1], vertical_alignment='center')
    with col1:
        if st.button(label='Last month', key='last_month_button'):
            first_day_of_current_month = datetime.datetime.today().replace(day=1)
            last_day_of_previous_month = first_day_of_current_month - datetime.timedelta(days=1)
            last_day_of_previous_month = last_day_of_previous_month.replace(hour=23, minute=59, second=59)
            first_day_of_previous_month = last_day_of_previous_month.replace(day=1, hour=0, minute=0, second=0)

            st.session_state.start_date = first_day_of_previous_month.date()
            st.session_state.end_date = last_day_of_previous_month.date()

    with col2:
        if st.button(label='Last year', key='last_year_button'):
            first_day_of_current_year = datetime.datetime.today().replace(day=1, month=1)
            last_day_of_previous_year = first_day_of_current_year - datetime.timedelta(days=1)
            last_day_of_previous_year = last_day_of_previous_year.replace(hour=23, minute=59, second=59)
            first_day_of_previous_year = last_day_of_previous_year.replace(day=1, month=1, hour=0, minute=0, second=0)

            st.session_state.start_date = first_day_of_previous_year.date()
            st.session_state.end_date = last_day_of_previous_year.date()

    with col3:
        if st.button(label='This year', key='this_year_button'):
            first_day_of_current_year = datetime.datetime.today().replace(day=1, month=1)
            last_day = datetime.datetime.today().replace(hour=23, minute=59, second=59)
            last_day += datetime.timedelta(days=1)

            st.session_state.start_date = first_day_of_current_year.date()
            st.session_state.end_date = last_day.date()

    start_date = st.sidebar.date_input('Start Date', min_value=datetime.date(1970, 1, 1),
                                       value=datetime.date(1970, 1, 1),
                                       max_value=datetime.date.today() + datetime.timedelta(days=1),
                                       format="DD/MM/YYYY", key='start_date')
    end_date = st.sidebar.date_input('End Date', value=datetime.date.today(),
                                     max_value=datetime.date.today() + datetime.timedelta(days=1),
                                     format="DD/MM/YYYY", key='end_date')

    read_from_splitwise(start_date, end_date)
    filter_txt = st.sidebar.text_input(label='Filter expenses', value='')
    if filter_txt != '':
        filtering = st.session_state.df['desc'].str.lower().str.contains(filter_txt.lower())
        st.session_state.df = st.session_state.df[filtering]

    pages = st.navigation([
        st.Page(recap_page, title='Shared', url_path='/'),
        st.Page(personal_page, title='Personal', url_path='/personal'),
        st.Page(changes_page, title='Changes over time', url_path='/aggregated'),
    ])
    pages.run()
