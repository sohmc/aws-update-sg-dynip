import json
import requests
import os.path
import sys
import getopt
import textwrap
import subprocess
import logging

# Path to AWS CLI
awscli = '/usr/local/bin/aws'
config_file = os.path.expanduser('~/.config/.aws_sg_ddns.conf')

# Configuration
logging.basicConfig(format='%(asctime)s %(process)d %(levelname)s %(message)s',
    level=logging.DEBUG)
dynip_config = dict()
startup_config = dict()
startup_config['force_update'] = "no"
run_config = False
find_ip_jmespath = "SecurityGroups[0].IpPermissions[0].IpRanges[0].CidrIp"

def print_usage():
    print("usage: " + sys.argv[0] + " [-c <config file>] \ ")
    print("             -s <security group> [-f] \ ")
    print("             [-n <ip address>] \ ")
    print("             [-p <profile name>] ")
    print(textwrap.dedent("""
    -c <config_file>        Run using the config file, if provided.  If the 
                            config file is empty or does not exist, the 
                            config will run and save values in the specified 
                            file.  The script will run without arguments when 
                            the config file is found at: """))
    print("\t\t\t\t" + config_file)

    print(textwrap.dedent("""
    -s <security group>     Security Group to update.  Required argument if
                            config file is not provided.  If config file and
                            this argument are provided, this argument will 
                            SUPERCEDE the config file.
    
    -f                      Force IP address update, even if the record is 
                            the same as the current IP address.
    
    -n <ip address>         Use the specified IP address instead of the IP 
                            address that this script is running on.  CIDR 
                            notation /32 is added automatically.
    
    -p <profile name>        Run the AWS CLI as the named profile, similiar to
                             running aws --profile <profile name>
    
    
    AWS CLI must already be configured with the appropriate credentials.  At
    minimum, the AWS CLI must have the following rights:
    
    * ec2:DescribeSecurityGroups
    * ec2:AuthorizeSecurityGroupIngress
    * ec2:RevokeSecurityGroupIngress
    
    The last two rights (AuthorizeSecurityGroupIngress, RevokeSecurityGroupIngress)
    can be restricted to the specific security group that holds your Dynamic IP.
    Please see the github page for this project for additional details."""))
    
    sys.exit(2)


def config():
    print(textwrap.dedent("""\
    The information provided in this configuration will be used to update
    the security group you specify within the region set on your AWS CLI
    profile.  Setting up your AWS CLI is outside the scope of this script
    and details can be found here:
        http://docs.aws.amazon.com/cli/latest/userguide/cli-chap-getting-started.html

    Please keep in mind that absolutely no validation is done during the
    configuration.

    What security group should be updated: """))
    dynip_config['sg'] = input("> ")

    print("Which AWS CLI profile should be used?  Blank is default: ")
    dynip_config['cli-profile'] = input("> ")

    dynip_config['force_update'] = query_yes_no("Should the script always force updates, regardless of what is currently set in the security group?", "no")

    with open(config_file, 'w') as outfile:
        json.dump(dynip_config, outfile, sort_keys=True, indent=2)

    print("Config file save:")
    print("   " + config_file)
    print("\n")
    print("Ready to run")
    sys.exit(0)


def send_aws_cmd(this_config, subcmd, arguments):
    cmd_arg = []
    # build the CLI arguments
    if ('cli-profile' in this_config):
        cmd_arg.extend(['--profile', this_config['cli-profile']])

    cmd_arg.append('ec2')
    cmd_arg.append(subcmd)
    cmd_arg.extend(arguments)

    try:
        # parse the output of the json output, stripping newlines and
        # returning the raw value only (i.e. remove quotes)
        output = subprocess.check_output(['aws'] + cmd_arg,
                     stderr=subprocess.STDOUT).strip()
    except subprocess.CalledProcessError as err:
        logging.warning("aws cli exit code: ", err.returncode)
        logging.warning("Running command:")
        logging.warning(err.cmd)
        logging.warning("Output: ")
        logging.warning(textwrap.fill(err.output.strip()))
        sys.exit(2)
    
    return output



def check_sg_ip(this_config):
    global find_ip_jmespath
    cmd_arg = []

    cmd_arg.extend(['--group-id', this_config['sg']])
    cmd_arg.extend(['--query', find_ip_jmespath])

    return send_aws_cmd(this_config, 'describe-security-groups', cmd_arg)


def get_current_dyip():
    r_params = {'format': 'json'}
    r = requests.get('http://api.ipify.org', params=r_params)
    return str(r.json()['ip'])


def update_sg(this_config, old_ip, new_ip):
    #  aws --profile galactica-sg ec2 revoke-security-group-ingress
    #  --group-id sg-f9519788 --protocol all --cidr 108.45.27.121/32
    revoke_args = []

    # First, revoke the ingress
    revoke_args.extend(['--group-id', this_config['sg']])
    revoke_args.extend(['--protocol', 'all'])

    # Copy what we have so we don't have to do it again
    authorize_args = list(revoke_args)

    # Finish the revoke command
    # The old IP should have the CIDR notation at the end,
    # so no need to add it here.
    revoke_args.extend(['--cidr', old_ip])
    # Finish the authorize command
    authorize_args.extend(['--cidr', new_ip + '/32'])

    # If old_ip is set, then we need to revoke it first
    if (old_ip != 'null'):
        send_aws_cmd(this_config, 'revoke-security-group-ingress', revoke_args)

    # Send the new security group
    send_aws_cmd(this_config, 'authorize-security-group-ingress', authorize_args)



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
        choice = input().lower()
        if default and not choice:
            return default
        elif choice in valid:
            return valid[choice]
        else:
            print("Please respond with 'yes' or 'no' (or 'y' or 'n').\n")
## end of http://code.activestate.com/recipes/577058/ }}}

def main():
    global config_file
    global startup_config

    if (len(sys.argv) > 1):
        try:
            opts, args = getopt.getopt(sys.argv[1:], "fhc:s:n:p:")
        except getopt.GetoptError as err:
            logging.warning(str(err))
            logging.warning("For help, run with '-h'")
            sys.exit(2)

        for option, argument in opts:
            if (option == '-c'):
                run_config = True
                if (argument):
                    config_file = argument
            elif (option == '-f'):
                startup_config['force_update'] = "yes"
            elif (option == '-s'):
                startup_config['sg'] = argument
            elif (option == '-h'):
                run_config = False
                print_usage()


    # read the configuration or force config if config file is empty
    logging.debug("Trying config file: " + config_file)
    if (os.path.isfile(config_file) or (run_config == True)):
        try:
            with open(config_file) as datafile:
                dynip_config = json.load(datafile)
                logging.debug("Read config.")

                if 'force_update' in startup_config:
                    logging.info("-f declared in the command.  Forcing update.")
                    dynip_config['force_update'] = startup_config['force_update']
                if 'sg' in startup_config:
                    logging.info("-s declared in the command.  Using declared security group.")
                    dynip_config['sg'] = startup_config['sg']

        except:
            logging.debug("Config file not found or unreadable.  Running config.")
            if (run_config):
                config()
        
        sg_ip = check_sg_ip(dynip_config).decode('utf-8')
        dynip = get_current_dyip()

        # If there is no security group, aws will return a null.  In
        # that case, do not strip the quotes.
        if (sg_ip != 'null'):
            sg_ip = sg_ip[1:-1]

        logging.debug("sg_ip: " + str(sg_ip) + " vs dynip: " + dynip)
        if (dynip in sg_ip):
            logging.info("Dynamic IP " + dynip + " matches security group entry " + sg_ip)

            logging.debug("Checking forced status: " + dynip_config['force_update'])

            if (dynip_config['force_update'] == "yes"):
                logging.info("Forcing security group change.")
                update_sg(dynip_config, sg_ip, dynip)
            else:
                logging.info("Nothing to update")
        else:
            logging.info("Dynamic IP update detected!")
            logging.info("Changing from " + sg_ip + " to " + dynip)
            update_sg(dynip_config, sg_ip, dynip)
        

if __name__ == "__main__":
    main()
