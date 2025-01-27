from typing import List, Tuple
from collections import defaultdict

import splitwise
import datetime
import numpy as np

from utils import Expense


def get_group(
        sw: splitwise.Splitwise
) -> splitwise.Group:
    from globals import GROUP_TO_CHECK
    
    for g in sw.getGroups():
        if g.name == GROUP_TO_CHECK:
            return g


def get_group_expenses(
        splitwise_instance: splitwise.Splitwise,
        group: splitwise.Group,
        start_date: datetime.datetime = None,
        end_date: datetime.datetime = None
) -> List[Tuple[str, List[Expense]]]:
    expenses = splitwise_instance.getExpenses(
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

    shared_expenses = [exp for exp in expenses if len(exp.users) > 1]
    
    from globals import TRACKED_USERS
    tracked_users = TRACKED_USERS
    if len(tracked_users) == 0:
        tracked_users = set(user for exp in expenses for user in exp.users)

    single_user_expenses = []
    for user in tracked_users:
        single_user_expenses.append(
            (user, [exp for exp in expenses if len(exp.users) == 1 and exp.users[0] == user])
        )

    return [("Shared", shared_expenses)] + single_user_expenses



def aggregate_by_categories(
        expenses: List[Expense]
):
    expenses_by_category = defaultdict(list)
    for exp in expenses:
        expenses_by_category[exp.category].append(exp)

    aggregations = {}
    for category, expenses in expenses_by_category.items():
        total = np.sum(
            [x.money for x in expenses]
        )
        aggregations[category] = total

    return aggregations, expenses_by_category