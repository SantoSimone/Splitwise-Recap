# Splitwise-Recap

A simple script that contacts Splitwise API, downloads expenses between certain date range and produces a recap of
them, specifically: a csv file, a pie chart for shared expenses and a pie chart for each desired user.

### Usage

- Ensure you have python installed
- `pip install -r requirements.txt`
- Modify `globals.py` with desired settings
- Run `python splitwise_recurrent.py`

### Parameters

All parameters are explained below, some hints:

- Splitwise credentials can be found following this flow:
    - Go to Splitwise website (https://www.splitwise.com/)
    - Login
    - Upper right corner (Your account)
    - "Your apps" (in the security panel)
    - Register a new application (you can use this repo as the homepage URL)

- Email secret for Gmail can be created at https://myaccount.google.com/apppasswords
    - Email secret for other providers has not been tested

| Parameter                 |                                                 Description                                                 |
|:--------------------------|:-----------------------------------------------------------------------------------------------------------:|
| SPLITWISE_CONSUMER_KEY    |                                      Splitwise consumer key, see above                                      |
| SPLITWISE_CONSUMER_SECRET |                                    Splitwise consumer secret, see above                                     |
| SPLITWISE_API_KEY         |                                        Splitwise api key, see above                                         |
| SAVE_LOCAL                |                           Whether to save data in a local folder (True or False)                            |
| OUTPUT_FOLDER             |                        Folder to which pie charts are saved, if `SAVE_LOCAL` is True                        |
| GROUP_TO_CHECK            |                                   Name of the group to check on Splitwise                                   |
| LAST_MONTH_RECAP          | Automatically check last month (True or False) - This has precedence on start/end date (useful for cronjob) |
| START_DATE                |                             Start date to check, if `LAST_MONTH_RECAP` is False                             |
| END_DATE                  |                              End date to check, if `LAST_MONTH_RECAP` is False                              |
| TRACKED_USERS             |                                  Users to track for individual pie charts                                   |
| EMAIL_FROM_NAME           |                                          Name of the FROM address                                           |
| EMAIL_FROM_ADDRESS        |                                      Address that will send the email                                       |
| EMAIL_TO                  |                                   Address(es) that will receive the email                                   |
| EMAIL_SECRET              |                                 Secret for email authentication, see above                                  |
| EMAIL_INCLUDE_ORDERED_CSV |                 Whether to include a CSV ordered by category (then price) in the email body                 |

### Help and/or Contributions

If you find any problems or you want to improve this tool, feel free to open an issue.


----

#### And if you want, you can buy me a cup of tea :)

[!["Buy Me A Coffee"](https://www.buymeacoffee.com/assets/img/custom_images/orange_img.png)](https://www.buymeacoffee.com/sismosantillo)

