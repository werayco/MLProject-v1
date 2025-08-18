## How to set up ssh for a server

use the below command
```bash
ssh -i /path/to/key.pem username@server_ip
```

ssh → Secure Shell command.

-i /path/to/key.pem → Path to your private key (the .pem file you downloaded, e.g., from AWS).

username → The SSH user (depends on server type):

AWS EC2 Ubuntu → ubuntu

AWS EC2 Amazon Linux → ec2-user

AWS EC2 CentOS → centos

Custom VPS → whatever your provider gives you

server_ip → The public IP address or DNS name of your server.