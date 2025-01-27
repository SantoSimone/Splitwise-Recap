import itertools

import streamlit as st
import plotly.express as px

from streamlit_dashboard.dashboard_utils import filter_df_by_categories, filter_df_by_months


def personal_page():
    df = st.session_state.df

    users = set(itertools.chain(*df['users'].tolist()))
    user = st.selectbox(options=users, label='Select User', index=None)

    if user:
        user_df = df[df.apply(lambda r: user in r['users'] and len(r['users']) == 1, axis=1)]

        col1, col2 = st.columns([1, 1])

        with col1:
            st.title('Per category')
            by_category_df = filter_df_by_categories(user_df)
            st.dataframe(by_category_df, use_container_width=True, hide_index=True)
            fig = px.pie(by_category_df, values='Sum', names='Category', title='Per category')
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            st.title('Per month')
            by_months_df = filter_df_by_months(user_df)
            st.dataframe(by_months_df, use_container_width=True, hide_index=True)
            fig = px.pie(by_months_df, values='Sum', names='Month', title='Per month')
            st.plotly_chart(fig, use_container_width=True)

        st.title('Raw data')
        st.dataframe(user_df, use_container_width=True, hide_index=True)

        st.title('Search expenses')
        txt = st.text_input(label='Search text', value='')
        if txt != '':
            user_df.filter(like=txt, axis=0)
            st.dataframe(user_df, use_container_width=True, hide_index=True)
