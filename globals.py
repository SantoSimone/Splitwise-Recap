# --- Splitwise Data
# Go to Splitwise website (https://www.splitwise.com/) -> Login -> Upper right corner (Your account)
# -> "Your apps" (in the security panel) -> Register a new application (you can use this repo as the homepage URL)
SPLITWISE_CONSUMER_KEY = "splitwise-consumer-key"
SPLITWISE_CONSUMER_SECRET = "splitwise-consumer-secret"
SPLITWISE_API_KEY = "splitwise-api-key"

# --- Data saving
# Whether to save data in a local folder (True or False)
SAVE_LOCAL = False
# Where to save data if SAVE_LOCAL is True
OUTPUT_FOLDER = "/path/to/the/output/folder"

# --- General Settings
# Name of group on splitwise
GROUP_TO_CHECK = "AwesomeGroup"
# Automatically check last month (True or False) - This has precedence on start/end date (useful for cronjob)
LAST_MONTH_RECAP = True
# Otherwise specify start and end date
START_DATE = "01-09-2023"
END_DATE = "30-09-2023"
# Users to track for individual expenses
TRACKED_USERS = ["Genitore1", "Genitore2"]

# --- Email Settings
# Name of the FROM address
EMAIL_FROM_NAME = "Maschio Alpha"
# Address that will send the email
EMAIL_FROM_ADDRESS = "maschio.alpha@gmail.com"
# Address that will receive the email
EMAIL_TO = ["donna.preda@gmail.com"]
# Secret for email authentication
# Create secret here -> https://myaccount.google.com/apppasswords
EMAIL_SECRET = "gmail-secret"
# Whether to include a CSV ordered by category - price in the email body
EMAIL_INCLUDE_ORDERED_CSV = True

######## END USER INPUTS ########


# Do not touch this
DATE_FORMAT = "%d-%m-%Y"
