# Update your AWS Security Group with your Dynamic IP address

**Current Version: v1.1 (Released Dec 27, 2019)**

Build Type|Processor|Status
----------|---------|------
Linux, Windows, Mac|amd64|[![Github Actions CI/CD](https://github.com/sohmc/aws-update-sg-dynip/actions/workflows/building.yaml/badge.svg)](https://github.com/sohmc/aws-update-sg-dynip/actions/workflows/building.yaml)
Linux|arm64|[![Build Status](https://travis-ci.com/sohmc/cloudflare-ddns-py.svg?branch=main)](https://travis-ci.com/sohmc/cloudflare-ddns-py)

(arm64 builds have not yet been tested due to Travis CI implimenting 
a new pricing model without giving Open-Source developers credits to 
build.  **Be advised that arm64 builds will move to Github as soon as 
it's supported.**)

Core source is tested weekly.  Binaries are only tested during 
releases.

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
* Python (script was developed on Python 3.9.x)
* Python Libraries:
    * requests
* [AWS cli](https://docs.aws.amazon.com/cli/latest/userguide/install-cliv2.html) (Script tested with version 2 but version 1 should work)

If you wish to not install Python, you may download the binary that is
posted in the
["Releases"](https://github.com/sohmc/aws-update-sg-dynip/releases).

# Support

Please note that this script, if not used correctly or if I made a typo, 
can lock you out of your EC2 instance.  Your method of recovery is to 
use the AWS Console and update your security groups manually.  I do not 
work for AWS, Amazon, or any of their affiliates.

# Licensing

This repository is licensed using the [GNU Public License (GNU) 
v.3](https://choosealicense.com/licenses/gpl-3.0/).  If you require a 
different license, please feel free to contact me.

