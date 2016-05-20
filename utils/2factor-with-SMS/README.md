#HELP

##1.Add a comment with your account.
```
usermod -c ',,555-555-5555,' youraccount
```

you can check it in /etc/passwd

##2.put pam_python.so and stampauth.py 

put these files into directory /lib64/security/ .

##3.replace /etc/pam.d/sshd 

remember to backup you file.

##4.turn on ChallengeResponseAuthentication  

in file /etc/ssh/sshd_config,and then restart sshd server.

##5.test.

##6.preview
```
[root@IPCPU-11 ~]# ssh ipcpu@192.168.110.11
Enter Your PIN: 
Password: 
Last login: Mon Mar 21 00:04:37 2016 from 192.168.110.11
[ipcpu@IPCPU-11 ~]$ 
```
if the account have no PIN,you will get this
```
[root@IPCPU-11 ~]# ssh root@192.168.110.11
root@192.168.110.11's password: 
Permission denied, please try again.
root@192.168.110.11's password: 
Permission denied, please try again.
root@192.168.110.11's password: 
Permission denied (publickey,gssapi-keyex,gssapi-with-mic,password,keyboard-interactive).
```

##7.the end.
