import random, string, hashlib, requests
import pwd, syslog, json
import urllib, urllib2


def auth_log(msg):
	syslog.syslog("IPCPU-PAM-AUTH: " + msg)


def get_user_number(user):
	try:
		comments = pwd.getpwnam(user).pw_gecos
	except KeyError: # Bad user name
		auth_log("No local user (%s) found." % user)
		return -1
	
	try:
		return comments.split(',')[2] # Return Office Phone
	except IndexError: # Bad comment section format
		auth_log("Invalid comment block for user %s. Phone number must be listed as Office Phone" % (user))
		return -1

def genotp(length):
    chars=string.ascii_letters+string.digits
    return ''.join([random.choice(chars) for i in range(length)])


def sendsms(mobile,content):
    	url = 'http://sms.alibaba.com/smsapi'
    	SMS_USER = 'alixixi'
    	SMS_PASS = 'alixixi'

    	param = {
        	'UserName': SMS_USER,
        	'UserPass': SMS_PASS,
        	'Mobile': mobile,
        	'Content' : content,
    	}

    	res = requests.post(url,data=param)		
	
def pam_sm_authenticate(pamh, flags, argv):
	try:
		user = pamh.get_user()
		user_number = get_user_number(user)
		user_otp = genotp(4)
	except pamh.exception, e:
		return e.pam_result
	
	try:
		sendsms(user_number,user_otp)	
	except pamh.exception, e:
        	return e.pam_result	
	
		
	for attempt in range(0,3): # 3 attempts to enter the one time PIN
		msg = pamh.Message(pamh.PAM_PROMPT_ECHO_OFF, "Enter Your PIN: ")
		resp = pamh.conversation(msg)

		if resp.resp == user_otp:
			auth_log("user: " + user + " login successful with PIN.")
			return pamh.PAM_SUCCESS
		else:
			continue
			auth_log("user: " + user + " login failed with PIN.")
			return pamh.PAM_AUTH_ERR


def pam_sm_setcred(pamh, flags, argv):
	return pamh.PAM_SUCCESS

def pam_sm_acct_mgmt(pamh, flags, argv):
	return pamh.PAM_SUCCESS

def pam_sm_open_session(pamh, flags, argv):
	return pamh.PAM_SUCCESS

def pam_sm_close_session(pamh, flags, argv):
	return pamh.PAM_SUCCESS

def pam_sm_chauthtok(pamh, flags, argv):
	return pamh.PAM_SUCCESS
