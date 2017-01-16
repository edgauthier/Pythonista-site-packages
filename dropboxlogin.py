# coding: utf-8
# Based on https://gist.github.com/4034526
# Modified to prompt for app key/secret and store in keychain

# YOU NEED TO FILL IN YOUR APP KEY AND SECRET WHEN FIRST RUN!
# Go to dropbox.com/developers/apps to create an app.

# To reset app key & secret, change RESET_APP_SETTINGS to True and
# run this script. Remember to set it back out to False afterwards.
RESET_APP_SETTINGS = False

# access_type can be 'app_folder' or 'dropbox', depending on
# how you registered your app.
access_type = 'app_folder'

import webbrowser
from dropbox import client, rest, session
import keychain
import pickle
import console

def get_app_key():
  app_key = keychain.get_password('dropbox', 'app_key')
  if app_key:
    return app_key
  app_key = console.secure_input('Enter Dropbox App key: ').rstrip()
  keychain.set_password('dropbox','app_key',app_key)
  return app_key

def get_app_secret():
  app_secret = keychain.get_password('dropbox', 'app_secret')
  if app_secret:
    return app_secret
  app_secret = console.secure_input('Enter Dropbox App secret: ').rstrip()
  keychain.set_password('dropbox','app_secret',app_secret)
  return app_secret

def get_request_token():
  app_key = get_app_key()
  app_secret = get_app_secret()
  console.clear()
  print('Getting request token...')
  sess = session.DropboxSession(app_key, app_secret, access_type)
  request_token = sess.obtain_request_token()
  url = sess.build_authorize_url(request_token)
  console.clear()
  webbrowser.open(url, modal=True)
  return request_token

def get_access_token():
  app_key = get_app_key()
  app_secret = get_app_secret()
  token_str = keychain.get_password('dropbox', app_key)
  if token_str:
    key, secret = pickle.loads(token_str)
    return session.OAuthToken(key, secret)
  request_token = get_request_token()
  sess = session.DropboxSession(app_key, app_secret, access_type)
  access_token = sess.obtain_access_token(request_token)
  token_str = pickle.dumps((access_token.key, access_token.secret))
  keychain.set_password('dropbox', app_key, token_str)
  return access_token

def get_client():
  app_key = get_app_key()
  app_secret = get_app_secret()
  access_token = get_access_token()
  sess = session.DropboxSession(app_key, app_secret, access_type)
  sess.set_token(access_token.key, access_token.secret)
  dropbox_client = client.DropboxClient(sess)
  return dropbox_client

def reset_app_settings():
  app_key = keychain.get_password('dropbox', 'app_key')
  if app_key:
    keychain.delete_password('dropbox', app_key)
  keychain.delete_password('dropbox', 'app_key')
  keychain.delete_password('dropbox', 'app_secret')

def main():
  if RESET_APP_SETTINGS:
    reset_app_settings()
    print('App settings reset...')
    print('Change RESET_APP_SETTINGS to false to continue.')
    return
  # Demo if started run as a script...
  # Just print the account info to verify that the authentication worked:
  print('Getting account info...')
  dropbox_client = get_client()
  account_info = dropbox_client.account_info()
  print('linked account: {}'.format(account_info))

if __name__ == '__main__':
  main()

