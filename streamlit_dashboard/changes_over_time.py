import itertools
import datetime

import streamlit as st
import plotly.express as px

from streamlit_dashboard.dashboard_utils import read_from_splitwise


def changes_page():
    full_df = read_from_splitwise(
        datetime.date(1970, 1, 1),
        datetime.date.today() + datetime.timedelta(days=1),
        should_return=True
    )

    full_df['year'] = full_df['date'].map(lambda x: x[:4])
    full_df['month'] = full_df['date'].map(lambda x: x[5:7]).astype(int)
    full_df['type'] = full_df.apply(lambda x: 'Shared' if len(x['users']) > 1 else x['users'][0], axis=1)

    # st.dataframe(full_df, use_container_width=True, hide_index=True)
    all_years = full_df['year'].unique().tolist()
    all_users = ['Shared'] + list(set(itertools.chain(*full_df['users'].tolist())))
    all_categories = full_df['category'].unique().tolist()

    st.title('Changes over time')
    time_period = st.selectbox(options=['Years', 'Months'], label='Time period', index=0, key='time_select')
    year = st.selectbox(options=all_years, label='Select Years', index=all_years.index(max(all_years)),
                        key='year_select')
    user = st.selectbox(options=all_users, label='Select Users', index=0, key='user_select')
    category = st.selectbox(options=all_categories, label='Select Categories', index=0)

    if time_period == 'Months':
        full_df = full_df[full_df['year'] == year]

    full_df = full_df[(full_df['type'] == user) & (full_df['category'] == category)]
    # full_df.drop(labels=['users', 'type', 'year', 'desc'], axis=1, inplace=True)

    group_col = 'month' if time_period == 'Months' else 'year'
    grouped = full_df.groupby(group_col, as_index=False).sum()
    fig = px.bar(grouped, x=group_col, y='money')
    if time_period == 'Years':
        fig.update_xaxes(type='category')
    st.plotly_chart(fig, use_container_width=True)

    # # Sankey diagram
    # import plotly.graph_objects as go
    # links = collections.defaultdict(list)
    # totals = collections.defaultdict(float)
    # for _, row in df.iterrows():
    #     if len(row['users']) < 2:
    #         continue
    #
    #     totals[row['category']] += row['money']
    #
    # for cat, val in totals.items():
    #     links['source'].append('All expenses')
    #     links['target'].append(cat)
    #     links['value'].append(val)
    #
    # for user in set(itertools.chain(*df['users'].tolist())):
    #     user_totals = collections.defaultdict(float)
    #     user_df = df[df.apply(lambda r: user in r['users'] and len(r['users']) == 1, axis=1)]
    #     for _, row in user_df.iterrows():
    #         user_totals[row['category']] += row['money']
    #
    #     for cat, val in user_totals.items():
    #         links['source'].append(user)
    #         links['target'].append(f"{cat}_{user}")
    #         links['value'].append(val)
    #
    # nodes = list(set([v for k in ['source', 'target'] for v in links[k]]))
    # links_as_indices = collections.defaultdict(list)
    # for cat in links['source']:
    #     links_as_indices['source'].append(nodes.index(cat))
    # for cat in links['target']:
    #     links_as_indices['target'].append(nodes.index(cat))
    #
    # links_as_indices['value'] = links['value']
    #
    # fig = go.Figure(data=[go.Sankey(
    #     valueformat=".0f",
    #     valuesuffix="€",
    #     node=dict(
    #         pad=15,
    #         thickness=10,
    #         line=dict(color="black", width=0.5),
    #         label=nodes,
    #         color='blue'
    #     ),
    #     link=links_as_indices,
    # )], layout={'height': 1000})
    #
    # st.plotly_chart(fig, use_container_width=True, title='All expenses')
