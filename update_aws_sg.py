import json
import requests
import sys
import getopt


# Path to AWS CLI
awscli = '/usr/local/bin/aws'
config_file = os.path.expanduser('~/.config/.aws_sg_ddns.conf')


def print_usage():
    print "usage: " + sys.argv[0] + " [-c <config file>] \ "
    print "             -s <security group> [-f] \ "
    print "		[-n <ip address>] \ "
    print "             [-p <profile name>] "
    print """
-c <config_file>     	Run using the config file, if provided.  If the 
			config file is empty or does not exist, the 
			config will run and save values in the specified 
			file.  The script will run without arguments when 
			the config file is found at: 
                        """ + config_file + """

-s <security group>     Security Group to update.  Required argument if
                        config file is not provided.  If config file and
         		this argument are provided, this argument will 
			SUPERCEDE the config file.

-f              	Force IP address update, even if the record is 
			the same as the current IP address.

-n <ip address>		Use the specified IP address instead of the IP 
			address that this script is running on.  CIDR 
			notation /32 is added automatically.

-p <profile name>	Run the AWS CLI as the named profile, similiar to
			running aws --profile <profile name>


AWS CLI must already be configured with the appropriate credentials.  At
minimum, the AWS CLI must have the following rights:

* ec2:DescribeSecurityGroups
* ec2:AuthorizeSecurityGroupIngress
* ec2:RevokeSecurityGroupIngress

The last two rights (AuthorizeSecurityGroupIngress, RevokeSecurityGroupIngress)
can be restricted to the specific security group that holds your Dynamic IP.
Please see the github page for this project for additional details."""

    sys.exit(2)



