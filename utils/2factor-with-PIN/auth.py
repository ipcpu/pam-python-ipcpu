import random, string, hashlib, requests
import pwd, syslog


def auth_log(msg):
	"""Send errors to default auth log"""
	syslog.openlog(facility=syslog.LOG_AUTH)
	syslog.syslog("IPCPU-PAM-AUTH: " + msg)
	syslog.closelog()


def get_user_number(user):
	"""Extract user's phone number for pw entry"""
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
		
	
def pam_sm_authenticate(pamh, flags, argv):
	try:
		user = pamh.get_user()
		user_number = get_user_number(user)
	except pamh.exception, e:
		return e.pam_result
	
	if user is None or user_number == -1:
		msg = pamh.Message(pamh.PAM_ERROR_MSG, "Unable to send one time PIN.\nPlease contact your System Administrator")
		pamh.conversation(msg)
		return pamh.PAM_AUTH_ERR
		###""return pamh.PAM_ABORT""
		
		
	for attempt in range(0,3): # 3 attempts to enter the one time PIN
		msg = pamh.Message(pamh.PAM_PROMPT_ECHO_OFF, "Enter Your PIN: ")
		resp = pamh.conversation(msg)

		if resp.resp == user_number:
			return pamh.PAM_SUCCESS
		else:
			continue
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
