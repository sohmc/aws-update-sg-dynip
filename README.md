# Update your AWS Security Group with your Dynamic IP address

This script is a sister to [CloudFlare DDNS 
Updater](https://github.com/sohmc/cloudflare-ddns-py/)
but can be run independently.

The goal for this script is to update an AWS Security Group with your 
dynamically-assigned IP address.  Typical use case is that you have 
an IP address at home that is assigned by your ISP and is not assigned 
to you.  You use this IP address to secure your AWS Virtual Private 
Cloud by only allowing traffic from this IP address.

Directions on how to set this up is in the
[Wiki](https://github.com/sohmc/cloudflare-ddns-py/wiki).

# Requirements
* Python (script was developed on Python 3.6.9)
* Python Libraries:
    * requests

# Support

Please note that this script, if not used correctly or if I made a typo, 
can lock you out of your EC2 instance.  Your method of recovery is to 
use the AWS Console and update your security groups manually.  I do not 
work for AWS, Amazon, or any of their affiliates.

# Licensing

This repository is licensed using the [GNU Public License (GNU) 
v.3](https://choosealicense.com/licenses/gpl-3.0/).  If you require a 
different license, please feel free to contact me.

