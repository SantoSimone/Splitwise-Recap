from datetime import datetime
from typing import Optional

import streamlit as st
import pandas as pd

from utils import Expense


def read_from_splitwise(start_date: datetime.date, end_date: datetime.date, should_return: bool = False) \
        -> Optional[pd.DataFrame]:
    group = None
    for g in st.session_state.splitwise_instance.getGroups():
        if g.name == st.session_state.group:
            group = g
            break
    else:
        print(f"Group {st.session_state.group} not found")

    expenses = st.session_state.splitwise_instance.getExpenses(
        dated_after=start_date,
        dated_before=end_date,
        group_id=group.id,
        limit=1_000_000
    )

    # filter expenses that have been deleted
    expenses = [x for x in expenses if x.deleted_at is None]

    # filter expenses that are payment between people
    expenses = [x for x in expenses if x.payment is False]

    # transform into our class of Expense
    expenses = [Expense.from_splitwise_api(e) for e in expenses]

    cols = ['date', 'desc', 'category', 'money', 'users']
    df = pd.DataFrame(
        [[getattr(exp, c) for c in cols] for exp in expenses],
        columns=cols
    )

    if should_return:
        return df

    st.session_state.df = df


def filter_df_by_categories(df: pd.DataFrame) -> pd.DataFrame:
    categories = df['category'].unique()
    sums = [df[df['category'] == category]['money'].sum() for category in categories]
    total = sum(sums)
    shares = [s / total * 100 for s in sums]
    by_category_df = pd.DataFrame(list(zip(categories, sums, shares)), columns=['Category', 'Sum', 'Share'])
    by_category_df = by_category_df.sort_values(by='Sum', ascending=False)
    by_category_df['Share'] = by_category_df['Share'].round(2)
    return by_category_df


def filter_df_by_months(df: pd.DataFrame) -> pd.DataFrame:
    df['month'] = df['date'].map(lambda x: int(x[5:7]))
    months = df['month'].unique()

    sums = [df[df['month'] == month]['money'].sum() for month in months]
    total = sum(sums)
    shares = [sum / total * 100 for sum in sums]
    by_months_df = pd.DataFrame(list(zip(months, sums, shares)), columns=['Month', 'Sum', 'Share'])
    by_months_df = by_months_df.sort_values(by='Month', ascending=True)
    by_months_df['Share'] = by_months_df['Share'].round(2)

    return by_months_df
