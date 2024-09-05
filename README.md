# SlackTokens
Extract personal tokens and authentication cookie from the Slack app, to use with the Slack API.

---

# Description

`slacktokens` is a tool for providing programmatic access to the [Slack](https://slack.com/) ecosystem.

***This project is not endorsed or authorised in any way by Slack Technologies LLC.***

The Slack API is how all Slack clients, including the official desktop app and third-party
bots, read and write data that constitutes the Slack user experience. All clients much
provide authorisation to access the API.

As of July 2021, individual user access to the Slack API (as opposed to bot access) is
granted by providing a personal token (beginning with `xoxc-`) and a cookie called `d`.
Each Slack Workspace has its own personal token, but the cookie is the same for all.

If you use the Slack desktop app, these details will be stored on your local machine.
This script extracts them from the app's local store so you can use them for purposes not
provided for by the app itself.

# Usage

Calling `get_tokens_and_cookie()` will return the necessary authorisation details as a
Python dictionary, in the following format:

```
{
  'tokens': [
    'Workspace name': { token: <personal-token>, url: <URL of Workspace> }
    ]
  'cookie': { 'name': 'd', 'value': <value-of-d-cookie> }
}
```

This data can be used for calls to the Slack API. For example:

```
curl 'https://slack.com/api/team.info?token=<personal-token>' --header 'Cookie: d=<value-of-d-cookie>'
```

# Details

Your personal tokens are extracted by querying the Slack app's HTML Web Storage database. The token for each Workspace is stored in a dictionary in the `localStorage` object, in a `LevelDB` database. The useful fields extracted from the dictionary, other than the token itself, are the human readable Workspace name, and the Workspace URL.

The cookie is extracted from the Slack app's cookie store. The cookie of interest is
stored encrypted, so a modified version of `pycookiecheat` is used to decrypt the
contents. The decryption process will prompt you for your user password, which is used
only to pull out the cookie store encryption secret from your keychain.

# Shortcomings
- macOS and Linux only.
	- Windows support contributions welcome.
- Slack Desktop App only.
	- Browser support contributions welcome. Preferred implementation: failover to looking through browsers if the app access method fails.
- Might require the app to be closed, because LevelDB is not a multi-user database and there are no read-only access options.
- No established method for persisting the token data. Thought long and hard about this, and decided to keep the interface flexible and to leave suitable persistance methods as an exercise for the user.
	- It turns out the script is fast and read-only, so if the user is another Python script, then perhaps no persistance is required.
