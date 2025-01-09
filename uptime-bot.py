from mastodon import Mastodon
from os.path import exists
import io, json

## Secrets
client_id = ''
client_secret = ''
api_base_url = ''
access_token = ''

mods = ''


## Config
test = True
number_of_statuses = 20
threshold_of_errors = 5

## Logging in
mastodon = Mastodon(client_id=client_id, client_secret=client_secret, api_base_url=api_base_url, access_token=access_token)

## Getting user-id of altbot & dict of last statuses
altbot_id = mastodon.account_lookup(acct='altbot')['id']
altbot_statuses = mastodon.account_statuses(id=altbot_id, limit=number_of_statuses)

## Getting all localized altTextError-messages
localizations = json.load(io.open("localizations.json", mode="r", encoding="utf-8"))
temp1 = 'responses'
temp2 = 'altTextError'
responses = [val[temp1] for key, val in localizations.items() if temp1 in val]
error_responses = [val[temp2] for val in responses if temp2 in val]

## Checking every status_content if it contains of one altTextError-message
error_count = 0
for i in range(number_of_statuses):
    content = altbot_statuses[i]['content']
    for error in error_responses:
        if error in content:
            error_count += 1

if error_count >= threshold_of_errors:
    status = "@altbot is throwing errors.\n Pinging " + mods
else:
    status = "All is fine"


if test:
    mastodon.status_post(status, spoiler_text="testing")
else:
    mastodon.status_post(status)
