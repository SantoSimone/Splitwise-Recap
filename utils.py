import datetime
from typing import List

import pandas
import pandas as pd
import splitwise


class Expense:
    def __init__(
            self,
            date: str,
            desc: str,
            category: str,
            money: float,
            users: List[str]
    ):
        self.date = date
        self.desc = desc
        self.category = category
        self.money = money
        self.users = users

    def __lt__(self, other):
        return self.money < other.money

    def to_csv(self):
        return [
            self.date,
            self.desc,
            self.category,
            self.money
        ]

    @staticmethod
    def from_splitwise_row(
            row: pd.Series
    ):
        return Expense(date=date_from_string(row['Data']),
                       desc=row['Descrizione'],
                       category=row['Categorie'],
                       money=float(row['Costo']))

    @staticmethod
    def from_splitwise_api(
            exp: splitwise.Expense
    ):
        return Expense(
            date=exp.date[:10],  # only AAAA-MM-dd
            desc=exp.description,
            category=exp.category.name,
            money=float(exp.cost),
            users=[user.first_name for user in exp.users]
        )


def date_from_string(
        date_str: str
):
    """
    Convert date coming from Splitwise csv (or any date string following the format '%Y-%m-%d').
    :param date_str: string compliant to '%Y-%m-%d' format.
    :return: datetime object. If the format is not compliant a MIN_DATE is outputted
    """
    try:
        return datetime.datetime.strptime(date_str, '%Y-%m-%d')
    except:
        print("Provided date ({}) was not compliant with format '%Y-%m-%d'.".format(date_str))
        return datetime.datetime.min


def filter_dataframe_by_date(
        df: pd.DataFrame,
        month: int,
        min_date: datetime.date,
        max_date: datetime.date
):
    """
    Filter Splitwise csv by desired month or custom range of dates
    :param df: DataFrame to be filtered
    :param month: number of month desired, belonging to current year
    :param min_date: start date of the custom range desired
    :param max_date: end date of the custom range desired
    :return: pandas dataframe filtered by date
    """

    if month is not None and (min_date is not None or max_date is not None):
        print("Provide only one between \'month\' and custom range (\'min_date\' and \'max_date\'")
        return pandas.DataFrame()
    if (min_date is not None and max_date is None) or (min_date is None and max_date is not None):
        print("Custom date range is made of \'min_date\' and \'max_date\', please provide both.")
        return pandas.DataFrame()

    custom_df = df.copy()
    custom_df['Data'] = [date_from_string(x) for x in custom_df['Data']]

    if month is not None:
        return df[custom_df['Data'].dt.month == month]
    else:
        return df[
            (custom_df['Data'] >= min_date) & (custom_df['Data'] <= max_date)
            ]
