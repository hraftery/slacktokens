"""slacktokens.py :: Extract personal tokens and authentication cookie from the Slack app.

A tool for providing programmatic access to the [Slack](https://slack.com/) ecosystem.
This project is not endorsed or authorised in any way by Slack Technologies LLC.

The Slack API is how all Slack clients, including the official desktop app and third-party
bots, read and write data that constitutes the Slack user experience. All clients much
provide authorisation to access the API.

As of July 2021, individual user access to the Slack API (as opposed to bot access) is
granted by providing a personal token (beginning with `xoxc-`) and a cookie called `d`.
Each Slack Workspace has its own personal token, but the cookie is the same for all.

If you use the Slack desktop app, these details will be stored on your local machine.
This script extracts them from the app's local store so you can use them for purposes not
provided for by the app itself.

Calling `get_tokens_and_cookie()` will return the necessary authorisation details as a
Python dictionary, in the following format:

```
{
  'tokens': [
    'Workspace URL': { token: <personal-token>, name: <friendly name of Workspace> }
    ]
  'cookie': { 'name': 'd', 'value': <value-of-d-cookie> }
}
```

The tokens are extracted by querying the Slack app's HTML Web Storage database. The tokens
are stored in the `localStorage` object, in a `LevelDB` database.

The cookie is extracted from the Slack app's cookie store. The cookie of interest is
stored encrypted, so a modified version of `pycookiecheat` is used to decrypt the
contents. The decryption process will prompt you for your user password, which is used
only to pull out the cookie store encryption secret from your keychain.

"""

__author__ = "Heath Raftery <heath@empirical.ee>"


def get_tokens_and_cookie():
  """Return a dictionary containing the Slack personal tokens and cookie."""
  return { 'tokens': get_tokens(), 'cookie': get_cookie() }

def get_tokens():
  """Return a dictionary containing the token and name for each Slack Workspace."""
  import leveldb
  import sys
  import pathlib
  import json

  if sys.platform == "darwin":
#    LEVELDB_PATH='~/Library/Application Support/Slack/Local Storage/leveldb'
    LEVELDB_PATH='~/Library/Containers/com.tinyspeck.slackmacgap/Data/Library/Application Support/Slack/Local Storage/leveldb'
  elif sys.platform.startswith("linux"):
    LEVELDB_PATH='~/.config/Slack/Local Storage/leveldb'
  else:
    raise OSError("slacktokens only works on macOS or Linux.")

  db = None
  try:
    db = leveldb.LevelDB(str(pathlib.Path(LEVELDB_PATH).expanduser()))
  except Exception as e:
    if "lock" in str(e):
      raise RuntimeError("Slack's Local Storage database appears to be locked. Have you quit Slack?") from e
    else:
      raise
  else:
    try:
      cfg = next(v for k,v in db.RangeIter() if bytearray(b'localConfig_v2') in k)
    except StopIteration as e:
      raise RuntimeError("Slack's Local Storage not recognised: localConfig not found. Aborting.") from e

    try:
      d = json.loads(cfg[1:])
    except Exception as e:
      raise RuntimeError("Slack's Local Storage not recognised: localConfig not in expected format. Aborting.") from e


    tokens = {}
    for v in d['teams'].values():
      tokens[v['url']] = { 'token': v['token'], 'name': v['name'] }
  
    return tokens
  finally:
    if db:
      del db # attempt to clean up our lock


def get_cookie():
  """Return a dictionary containing the name and value of the authentication cookie."""
  import pycookiecheat

  cookies = pycookiecheat.chrome_cookies("http://slack.com", browser="Slack")
  
  return { 'name': 'd', 'value': cookies['d'] }
