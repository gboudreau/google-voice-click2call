import urllib
import re
import mechanize
import sys
import simplejson as json
import os.path

GV_USERNAME = "you@gmail.com"
GV_PASSWORD = "your_google_password"

class Error:
	pass

def main():
	GV_CALLBACK_NUMBER = "+1205551212"
	GV_CALLBACK_NUMBER_TYPE = "1" # Don't change
	for arg in sys.argv:
		if arg.startswith('f:'):
			GV_CALLBACK_NUMBER = "+" + arg[2:]
		if arg.startswith('t:'):
			NUMBER_TO_CALL = arg[2:]
	print "Calling " + NUMBER_TO_CALL + " using Google Voice Click2Call<br/>"

	cj = mechanize.LWPCookieJar()
	if os.path.isfile("cookies.txt"):
		cj.revert("cookies.txt")

	browser = mechanize.Browser()
	browser.set_cookiejar(cj)
	
	response = browser.open('https://www.google.com/voice')
	html = response.read()
	m = re.search(r'name="_rnr_se" type="hidden" value="([^"]+)"', html)
	if not m:
		# Need to login first maybe?
		print "Will login now... "
		browser.open('https://accounts.google.com/ServiceLogin')
		browser.select_form(nr=0)
		browser['Email'] = GV_USERNAME
		browser['Passwd'] = GV_PASSWORD
		response = browser.submit()

		# If you have problems logging in ('Login failed' below), de-comment this line, copy-paste what it outputs into a temp.html file, and open that file in a browser. You will probably understand why the login fails from this.
		# print response.read()

		print "Loading Google Voice... "
		browser = mechanize.Browser()
		browser.set_cookiejar(cj)
		response = browser.open('https://www.google.com/voice')
		html = response.read()

		m = re.search(r'name="_rnr_se" type="hidden" value="([^"]+)"', html)
		if not m:
			print "[ERROR] Login failed.<br/>"
			return
	else:
		print "Already logged in. "

	cj.save("cookies.txt")
	magic_rnr_se = m.group(1)
	print "OK. Sending Click2Call request... "
		
	postdata = { "outgoingNumber": NUMBER_TO_CALL, "forwardingNumber": GV_CALLBACK_NUMBER, "subscriberNumber": "undefined", "phoneType": GV_CALLBACK_NUMBER_TYPE, "remember": "0", "_rnr_se": magic_rnr_se }
	data = urllib.urlencode(postdata)
	req = mechanize.Request('https://www.google.com/voice/call/connect/', data)
	cj.add_cookie_header(req)
	resp = mechanize.urlopen(req).read()
	try:
		result = json.loads(resp)
		if result['ok']:
			print "Success!<br/>"
	except:
		print "[ERROR] Google Voice returned an error: " + resp + "<br/>"

if __name__ == '__main__':
	main()
