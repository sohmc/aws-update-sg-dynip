import json
import requests
import os.path
import sys
import getopt
import textwrap
import subprocess

# Path to AWS CLI
awscli = '/usr/local/bin/aws'
config_file = os.path.expanduser('~/.config/.aws_sg_ddns.conf')

# Configuration
dynip_config = dict()
startup_config = dict()
startup_config['force_update'] = False
run_config = False
find_ip_jmespath = "SecurityGroups[0].IpPermissions[0].IpRanges[0].CidrIp"

def print_usage():
    print "usage: " + sys.argv[0] + " [-c <config file>] \ "
    print "             -s <security group> [-f] \ "
    print "		[-n <ip address>] \ "
    print "             [-p <profile name>] "
    print textwrap.dedent("""
    -c <config_file>     	Run using the config file, if provided.  If the 
    			config file is empty or does not exist, the 
    			config will run and save values in the specified 
    			file.  The script will run without arguments when 
    			the config file is found at: """)
    print "\t\t\t\t" + config_file

    print textwrap.dedent("""
    -s <security group>     Security Group to update.  Required argument if
                            config file is not provided.  If config file and
                            this argument are provided, this argument will 
                            SUPERCEDE the config file.
    
    -f              	Force IP address update, even if the record is 
    			the same as the current IP address.
    
    -n <ip address>	Use the specified IP address instead of the IP 
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
    Please see the github page for this project for additional details.""")
    
    sys.exit(2)


def config():
    print textwrap.dedent("""\
    The information provided in this configuration will be used to update
    the security group you specify within the region set on your AWS CLI
    profile.  Setting up your AWS CLI is outside the scope of this script
    and details can be found here:
        http://docs.aws.amazon.com/cli/latest/userguide/cli-chap-getting-started.html

    Please keep in mind that absolutely no validation is done during the
    configuration.

    What security group should be updated: """)
    dynip_config['sg'] = raw_input("> ")

    print "Which AWS CLI profile should be used?  Blank is default: "
    dynip_config['cli-profile'] = raw_input("> ")

    dynip_config['force_update'] = query_yes_no("Should the script always force updates, regardless of what is currently set in the security group?", "no")

    with open(config_file, 'w') as outfile:
        json.dump(dynip_config, outfile, sort_keys=True, indent=2)

    print "Config file save:"
    print "   " + config_file
    print "\n"
    print "Ready to run"
    sys.exit(0)


def check_sg_ip(this_config):
    global find_ip_jmespath
    cmd_arg = []

    # build the CLI arguments
    if ('cli-profile' in this_config):
        cmd_arg.append('--profile ' + this_config['cli-profile'])

    cmd_arg.extend([ 'ec2', 'describe-security-groups' ])

    cmd_arg.append('--group-id ' + this_config['sg'])
    #cmd_arg.append('--query ' + find_ip_jmespath)

    print cmd_arg
    output = subprocess.check_output(['aws'] + cmd_arg)
    print output


## {{{ http://code.activestate.com/recipes/577058/ (r2)
def query_yes_no(question, default = "yes"):
    """Ask a yes/no question via raw_input() and return their answer.

    "question" is a string that is presented to the user.
    "default" is the presumed answer if the user just hits <Enter>.
        It must be "yes" (the default), "no" or None (meaning
        an answer is required of the user).

    The "answer" return value is one of "yes" or "no".
    """
    valid = {"yes":"yes", "y":"yes", "ye":"yes",
             "no":"no", "n":"no"}
    prompt = {None: " [y/n] ",
              "yes": " [Y/n] ",
              "no": " [y/N] "}.get(default, None)
    if not prompt:
        raise ValueError("invalid default answer: '%s'" % default)

    while 1:
        sys.stdout.write(question + prompt)
        # Changed to be cross-python
        choice = raw_input().lower()
        if default and not choice:
            return default
        elif choice in valid:
            return valid[choice]
        else:
            print "Please respond with 'yes' or 'no' (or 'y' or 'n').\n"
## end of http://code.activestate.com/recipes/577058/ }}}

def main():
    global config_file
    global startup_config

    if (len(sys.argv) > 1):
	try:
	    opts, args = getopt.getopt(sys.argv[1:], "fhc:s:n:p:")
	except getopt.GetoptError as err:
            print str(err)
	    print "For help, run with '-h'"
            sys.exit(2)

	for option, argument in opts:
	    if (option == '-c'):
		run_config = True
		if (not argument):
		    config_file = argument
	    elif (option == '-f'):
		startup_config['force_update'] = True
	    elif (option == '-s'):
		startup_config['sg'] = argument
            elif (option == '-h'):
                run_config = False
                print_usage()
    else:
        print_usage()


    # read the configuration or force config if config file is empty
    if (os.path.isfile(config_file) or (run_config == True)):
	try:
	    with open(config_file) as datafile:
		dynip_config = json.load(datafile)

            print dynip_config
	except:
	    if (run_config):
		config()
        
        check_sg_ip(dynip_config);

if __name__ == "__main__":
    main()
