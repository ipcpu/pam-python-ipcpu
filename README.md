# pam-python-ipcpu

Linux 的PAM模块，安装后可以调用python脚本执行PAM模块的相关逻辑。

##安装

编译依赖，依赖于pam、pam-devel模块
```
yum install pam pam-devel -y
```

编译
```
make lib
```

找到编译后的.so文件，拷贝到/lib64/security/目录

##使用
可以参照案例 utils/2factor-with-PIN/的相关内容

