from imgurpython import ImgurClient
from datetime import datetime

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import ConfigParser

# metadata should include the following strings: album, name, title description
def upload_image(imPath,client,metaData):
  print "Uploading image..."
  image = client.upload_from_path(imPath, config=metadata, anon=False)
  print "Done"
  return image

def authenticate(authFile='auth.ini'):

  # get all credentials and login data
  config = ConfigParser.ConfigParser()
  config.read(authFile)
  credentials = {k:v for k,v in config.items('credentials')}
  loginData = {k:v for k,v in config.items('imgurLogin')}
  client = ImgurClient(credentials['client_id'], credentials['client_secret'])

  authorization_url = client.get_auth_url('pin')

  # use selenium to login to user's account and get the pin
  # there's no better way to do this due to imgur's api limitations
  browser = webdriver.PhantomJS()
  browser.get("https://imgur.com/signin")
  username = browser.find_element_by_xpath("//input[@name='username']")
  username.send_keys(loginData['username'])
  password = browser.find_element_by_xpath("//input[@name='password']")
  password.send_keys(loginData['password'])
  password.send_keys(Keys.ENTER)
  browser.get(authorization_url)
  pin = browser.find_element_by_xpath("//input[@name='pin']").get_attribute('value')

  browser.close()
  browser.quit()

  response = client.authorize(pin, 'pin')
  client.set_user_auth(response['access_token'], response['refresh_token'])

  return client

client = authenticate()
