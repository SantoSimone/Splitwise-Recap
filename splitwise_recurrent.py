import datetime
import email.message
import os
import ssl
import tempfile
from collections import defaultdict
from pathlib import Path
from typing import List, Dict, Tuple

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import splitwise

from utils import Expense


def get_group(
        sw: splitwise.Splitwise
) -> splitwise.Group:
    for g in sw.getGroups():
        if g.name == GROUP_TO_CHECK:
            return g


def retrieve_dates_to_analyze() -> Tuple[datetime.datetime, datetime.datetime]:
    if LAST_MONTH_RECAP:
        first_day_of_current_month = datetime.datetime.today().replace(day=1)
        last_day_of_previous_month = first_day_of_current_month - datetime.timedelta(days=1)
        last_day_of_previous_month = last_day_of_previous_month.replace(hour=23, minute=59, second=59)
        first_day_of_previous_month = last_day_of_previous_month.replace(day=1, hour=0, minute=0, second=0)
        start_date = first_day_of_previous_month
        end_date = last_day_of_previous_month
    else:
        start_date = datetime.datetime.strptime(START_DATE, DATE_FORMAT)
        end_date = datetime.datetime.strptime(END_DATE, DATE_FORMAT)
        start_date = start_date.replace(hour=0, minute=0, second=0)
        end_date = end_date.replace(hour=23, minute=59, second=59)

    return start_date, end_date


def get_group_expenses(
        splitwise_instance: splitwise.Splitwise,
        group: splitwise.Group,
        start_date: datetime.datetime = None,
        end_date: datetime.datetime = None
) -> List[Tuple[str, List[Expense]]]:
    expenses = splitwise_instance.getExpenses(
        dated_after=start_date,
        dated_before=end_date,
        group_id=group.id
    )

    # filter expenses that have been deleted
    expenses = [x for x in expenses if x.deleted_at is None]

    # filter expenses that are payment between people
    expenses = [x for x in expenses if x.payment is False]

    # transform into our class of Expense
    expenses = [Expense.from_splitwise_api(e) for e in expenses]

    shared_expenses = [exp for exp in expenses if len(exp.users) > 1]
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


def plot_aggregations(
        aggregated: Dict,
        result_path: Path,
        name: str
):
    def custom_legend():
        leg = []
        for k, v in aggregated.items():
            leg.append("{} ({:.2f})".format(k, v))

        return leg

    plt.pie(x=np.fromiter(aggregated.values(), dtype=float), labels=aggregated.keys(), radius=1.1)
    plt.legend(labels=custom_legend(), loc='center')
    total = np.sum(list(aggregated.values()))
    plt.xlabel('Total {:.2f}'.format(total))
    plt.title(name)
    plt.savefig(result_path)
    plt.close()


def create_ordered_csv(
        expenses_dict: Dict
) -> pd.DataFrame:
    out_df = pd.DataFrame(columns=['Data', 'Descrizione', 'Categoria', 'Costo'])
    i = 0

    for _, expenses in expenses_dict.items():
        ordered_expenses = sorted(expenses)
        for exp in ordered_expenses:
            out_df.loc[i] = exp.to_csv()
            i += 1

    return out_df


def send_email(
        dataframes: List[pd.DataFrame],
        chart_paths: List[str]
):
    msg = email.message.EmailMessage()

    # generic email headers
    today = datetime.datetime.today()
    period = "12/{}".format(today.year) if today.month == 1 else "{}/{}".format(today.month - 1, today.year)

    msg['Subject'] = "Splitwise report {}".format(period)
    from_nickname = EMAIL_FROM_NAME
    from_address = EMAIL_FROM_ADDRESS
    msg['From'] = f"{from_nickname} <{from_address}>"
    msg['To'] = EMAIL_TO

    from email.utils import make_msgid
    attachment_cid = make_msgid()
    body = f"Recap splitwise del mese scorso"
    if EMAIL_INCLUDE_ORDERED_CSV:
        for df, name in zip(dataframes, ["", "Simo", "Vale"]):
            body += f"\n{name}\n{df.to_html()}"

    msg.set_content('<b>%s</b><br/><img name="pie_chart" src="cid:%s"/><br/>' % (body, attachment_cid), 'html')
    msg.make_mixed()
    from email.mime.image import MIMEImage
    for chart_path in chart_paths:
        with open(chart_path, "rb") as attachment:
            img_attach = MIMEImage(attachment.read())
        # Define the image's ID with counter as you will reference it.
        img_attach.add_header('Content-ID', '<image_id_{}>'.format(attachment_cid))
        img_attach.add_header('Content-Disposition', "attachment; filename= %s" % Path(chart_path).name.split('_')[-1])
        msg.attach(img_attach)

    import smtplib
    context = ssl.create_default_context()

    with smtplib.SMTP("smtp.gmail.com", port=587) as smtp:
        smtp.starttls(context=context)
        smtp.login(from_address, EMAIL_SECRET)
        smtp.send_message(msg)


def main():
    split_instance = splitwise.Splitwise(
        consumer_key=SPLITWISE_CONSUMER_KEY,
        consumer_secret=SPLITWISE_CONSUMER_SECRET,
        api_key=SPLITWISE_API_KEY
    )

    group = get_group(sw=split_instance)
    start_date, end_date = retrieve_dates_to_analyze()

    name_and_expenses = get_group_expenses(split_instance, group, start_date, end_date)
    if SAVE_LOCAL:
        os.makedirs(OUTPUT_FOLDER, exist_ok=True)

    ordered_expenses_dataframes, results_paths = [], []
    for name, expenses in name_and_expenses:
        aggregated, by_category = aggregate_by_categories(expenses)
        formatted_start_date = start_date.strftime(DATE_FORMAT)
        formatted_end_date = end_date.strftime(DATE_FORMAT)
        filename = f"{formatted_start_date}_{formatted_end_date}_{name}.png"
        result_dir = OUTPUT_FOLDER if SAVE_LOCAL else tempfile.gettempdir()
        result_path = Path(result_dir) / filename
        results_paths.append(str(result_path))

        plot_aggregations(aggregated=aggregated, result_path=result_path, name=name)
        ordered_expenses_dataframes.append(create_ordered_csv(expenses_dict=by_category))

    send_email(dataframes=ordered_expenses_dataframes, chart_paths=results_paths)


if __name__ == '__main__':
    from globals import *

    main()
