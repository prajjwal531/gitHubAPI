# gitHubAPI

This Script is used to get all publicly available gist for any user.

**Usage**: python gitHub.py -gitUser "UserName"

**Description**: This script makes an API call to github and get all publicly available gist for the user.

If this is a first run, script will make the api call and save the latest gist in a data file.
On sub sequent run script will make the api call and compare latest gist's created time with the saved gist time in the file.

if both time are equal then script concludes that there has not been any change.

if saved time in file is lower than latest time from the gist then script concludes that there is newly published gist.
