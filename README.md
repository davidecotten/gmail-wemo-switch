# Gmail WeMo Switch
This simple script watches a Gmail label for unread messages and toggles a networked WeMo device.

## Setup
- Clone a local copy of the repo and install dependencies
`git clone https://github.com/davidecotten/gmail-wemo-switch.git`
`cd gmail-wemo-switch`
`pip install -r requirements.txt`
- Follow directions on this page to enable the Gmail API and save the credentials file to the working directory.
https://developers.google.com/gmail/api/quickstart/python#step_1_turn_on_the

## First run
`python3 gmail_wemo.py`
- Visit URL to authorize script. It is not verified by Google so you will receive a warning.
- Click 'Advanced' and then 'Go to Quickstart (unsafe)'. You will be prompted to click "Allow'.
- Once authenticated, the script will list out your Gmail labels. Select the label you wish to monitor.
- Next, the script will discover WeMo devices that are already setup on your network. Type the name of the device you wish to control.
-Done. The label will now be monitored. If any messages with that label are unread, the device will be switched on.
