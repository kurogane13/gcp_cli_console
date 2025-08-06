import os
import runpy
import sys
import datetime
from datetime import datetime
import subprocess
import json

now=datetime.now()

def validate_gcloud_authentication():
    """Validate if user is authenticated with gcloud and has active project"""
    try:
        print("🔍 Validating gcloud authentication...")
        
        # Check if user is logged in
        auth_check_cmd = "gcloud auth list --filter=status:ACTIVE --format='value(account)'"
        print(f"📋 Checking authentication: {auth_check_cmd}")
        
        result = subprocess.run(auth_check_cmd, shell=True, capture_output=True, text=True)
        
        if result.returncode != 0 or not result.stdout.strip():
            print("❌ No active gcloud authentication found!")
            return False, None, None
            
        active_account = result.stdout.strip()
        print(f"✅ Active account: {active_account}")
        
        # Check active project
        project_check_cmd = "gcloud config get-value project"
        print(f"📋 Checking active project: {project_check_cmd}")
        
        result = subprocess.run(project_check_cmd, shell=True, capture_output=True, text=True)
        
        if result.returncode != 0:
            print("⚠️ No active project set!")
            return True, active_account, None
            
        active_project = result.stdout.strip()
        if active_project and active_project != "(unset)":
            # ADDITIONAL CHECK: Test if authentication actually works with a resource access command
            print("🔍 Testing authentication with actual GCP resource access...")
            test_cmd = f"gcloud projects describe {active_project} --format='value(projectId)' --quiet"
            test_result = subprocess.run(test_cmd, shell=True, capture_output=True, text=True)
            
            if test_result.returncode != 0:
                # Authentication validation failed - tokens might be expired
                print("❌ Authentication test failed - tokens may be expired!")
                print("🔍 Error details:")
                print(f"   {test_result.stderr.strip()}")
                if "refresh token has expired" in test_result.stderr.lower() or "invalid_grant" in test_result.stderr.lower():
                    print("🚨 REFRESH TOKEN EXPIRED - Re-authentication required!")
                return False, None, None
            else:
                print("✅ Authentication test passed!")
                print(f"✅ Active project: {active_project}")
                return True, active_account, active_project
        else:
            print("⚠️ No active project set!")
            return True, active_account, None
            
    except Exception as e:
        print(f"❌ Error checking authentication: {str(e)}")
        return False, None, None

def prompt_authentication():
    """Prompt user to authenticate when not logged in"""
    print("\n" + "=" * 70)
    print("🔐 AUTHENTICATION REQUIRED")
    print("=" * 70)
    print("You need to authenticate with gcloud before running commands.")
    print("\nOptions:")
    print("1. Go to Main Menu → option 'l' (Login/Authentication)")
    print("2. Then use:")
    print("   - option 'l' (Login to gcloud)")  
    print("   - option 'c' (Set active project)")
    print("\n" + "=" * 70)
    
    choice = input("Would you like to go to the authentication menu now? (y/n): ").strip().lower()
    
    if choice == 'y':
        return True
    else:
        print("⚠️ Operation cancelled. Please authenticate before running gcloud commands.")
        return False

def execute_gcloud_command_with_auth_check(command, description=""):
    """Execute gcloud command after validating authentication"""
    print(f"🔧 {description}")
    
    # Validate authentication first
    is_authenticated, account, project = validate_gcloud_authentication()
    
    if not is_authenticated:
        print("❌ Authentication validation failed!")
        print("🚫 Command execution cancelled - authentication required")
        print("💡 Please authenticate using Main Menu → 'l' (Login/Authentication)")
        return 1  # Return error code without executing command
    
    print(f"✅ Authentication validated - Account: {account}")
    if project:
        print(f"✅ Active project: {project}")
    else:
        print("⚠️ Warning: No active project set. Some commands may fail.")
        print("💡 Consider setting a project using Main Menu → '5' (Set a project)")
        
        continue_anyway = input("Continue without active project? (y/n): ").strip().lower()
        if continue_anyway != 'y':
            print("🚫 Command execution cancelled by user")
            return 1
    
    # Execute the command if authentication is valid
    print(f"📋 Executing command: {command}")
    print("=" * 80)
    result = os.system(command)
    print("=" * 80)
    return result

def execute_gcloud_command(command, description=""):
    """Execute gcloud command and display it to the user"""
    print(f"🔧 {description}")
    print(f"📋 Executing command: {command}")
    print("=" * 80)
    result = os.system(command)
    print("=" * 80)
    return result

def test_case_module_menu():
    from gcp_test_case_cli import test_case_module
    test_case_module()
def free_command_input_menu():
    from gcp_cli_input_scripts import free_command_input
    free_command_input()

gcp_scripts_dir='gcp_automation_test_scripts'
os.system('mkdir -p '+gcp_scripts_dir)

operations_dir = "compute_operations_logs"
os.system('mkdir -p '+operations_dir)

def check_billing_project():
    now = datetime.now()
    with open(gcp_system_log_file, 'a') as logfile:
        logfile.write(str(now) + " --> Accessed DESCRIBE PROJECT BILLING DATA mode\n")
        logfile.close()
    print('- Mode 1 accessed.\n')
    project_name=input('Provide a valid project name and press enter: ')
    print("\nRetrieving billing data for project name: "+project_name+'\n')
    execute_gcloud_command_with_auth_check(f'gcloud beta billing projects describe {project_name}', 
                          f"Retrieving billing data for project: {project_name}")
    with open(gcp_system_log_file, 'a') as logfile:
        logfile.write(str(now) + " - Executed command: gcloud beta billing projects describe " +project_name+ "\n")
        logfile.close()
    input('\nOperation executed. Press enter to get back to main menu: ')
    now = datetime.now()
    with open(gcp_system_log_file, 'a') as logfile:
        logfile.write(str(now) + " <-- Exited DESCRIBE PROJECT BILLING DATA mode\n")
        logfile.close()
    main_menu()

def describe_specific_project():
    now = datetime.now()
    with open(gcp_system_log_file, 'a') as logfile:
        logfile.write(str(now) + " --> Accessed DESCRIBE PROJECT mode\n")
        logfile.close()
    print('- Mode 2 Accessed\n')
    project_to_describe=input('Type a project name to describe it: ')
    execute_gcloud_command_with_auth_check(f'gcloud projects describe {project_to_describe}', 
                          f"Describing project: {project_to_describe}")
    now = datetime.now()
    with open(gcp_system_log_file, 'a') as logfile:
        logfile.write(str(now) + " - Executed command: gcloud projects describe "+project_to_describe+"\n")
        logfile.close()
    input('\nOperation executed. Press enter to get back to main menu: ')
    now = datetime.now()
    with open(gcp_system_log_file, 'a') as logfile:
        logfile.write(str(now) + " <-- Exited DESCRIBE PROJECT mode\n")
        logfile.close()
    main_menu()

def get_cconfigurations_list():
    now = datetime.now()
    with open(gcp_system_log_file, 'a') as logfile:
        logfile.write(str(now) + " --> Accessed GET CONFIGURATION LIST mode\n")
        logfile.close()
    print('- Mode 3 Accessed\n')
    print('Getting configuration list...\n')
    execute_gcloud_command_with_auth_check('gcloud config configurations list', 
                          "Listing all gcloud configuration profiles")
    now = datetime.now()
    with open(gcp_system_log_file, 'a') as logfile:
        logfile.write(str(now) + " - Executed command: gcloud config configurations list\n")
        logfile.close()
    input('\nOperation executed. Press enter to get back to main menu: ')
    now = datetime.now()
    with open(gcp_system_log_file, 'a') as logfile:
        logfile.write(str(now) + " <-- Exited GET CONFIGURATION LIST mode\n")
        logfile.close()
    main_menu()

def get_active_project():
    now = datetime.now()
    with open(gcp_system_log_file, 'a') as logfile:
        logfile.write(str(now) + " --> Accessed GET ACTIVE PROJECT mode\n")
        logfile.close()
    print('- Mode 4 accessed.\n')
    print('Active project is: \n')
    execute_gcloud_command_with_auth_check('gcloud config get-value project', 
                          "Getting current active project")
    now = datetime.now()
    with open(gcp_system_log_file, 'a') as logfile:
        logfile.write(str(now) + " - Executed command: gcloud config get-value project"+"\n")
        logfile.close()
    input('\nOperation executed. Press enter to get back to main menu: ')
    now = datetime.now()
    with open(gcp_system_log_file, 'a') as logfile:
        logfile.write(str(now) + " <-- Exited GET ACTIVE PROJECT mode\n")
        logfile.close()
    main_menu()

def set_project():
    print('- Mode 5 accessed.\n')
    now = datetime.now()
    with open(gcp_system_log_file, 'a') as logfile:
        logfile.write(str(now) + " --> Accessed SET PROJECT mode\n")
        logfile.close()
    project_name=input('Provide a valid project name to set up, and press enter: ')
    print("\nSetting up project: "+project_name+'\n')
    print(f"🔧 Setting active project to: {project_name}")
    os.system(f'gcloud config set project {project_name}')
    now = datetime.now()
    with open(gcp_system_log_file, 'a') as logfile:
        logfile.write(str(now) + " - Executed command: gcloud config set project "+project_name+"\n")
        logfile.close()
    input('\nOperation executed. Press enter to get back to main menu: ')
    now = datetime.now()
    with open(gcp_system_log_file, 'a') as logfile:
        logfile.write(str(now) + " <-- Exited SET PROJECT mode\n")
        logfile.close()
    main_menu()

def get_all_projects():
    print('- Mode 6 accessed.\n')
    now = datetime.now()
    with open(gcp_system_log_file, 'a') as logfile:
        logfile.write(str(now) + " --> Accessed LIST ALL PROJECTS mode\n")
        logfile.close()
    print('Listing all projects....\n')
    execute_gcloud_command_with_auth_check('gcloud projects list', 
                          "Listing all projects in your account")
    now = datetime.now()
    with open(gcp_system_log_file, 'a') as logfile:
        logfile.write(str(now) + " - Executed command: gcloud projects list\n")
        logfile.close()
    input('\nOperation executed. Press enter to get back to main menu: ')
    now = datetime.now()
    with open(gcp_system_log_file, 'a') as logfile:
        logfile.write(str(now) + " <-- Exited LIST ALL PROJECTS mode\n")
        logfile.close()
    main_menu()

def get_all_organizations():
    now = datetime.now()
    with open(gcp_system_log_file, 'a') as logfile:
        logfile.write(str(now) + " --> Accessed LIST ALL ORGANIZATIONS mode\n")
        logfile.close()
    print('- Mode 7 accessed.\n')
    print('Listing all organizations....\n')
    execute_gcloud_command_with_auth_check('gcloud organizations list', 
                          "Listing all organizations in your account")
    now = datetime.now()
    with open(gcp_system_log_file, 'a') as logfile:
        logfile.write(str(now) + " - Executed command: gcloud organizations list\n")
        logfile.close()
    input('\nOperation executed. Press enter to get back to main menu: ')
    now = datetime.now()
    with open(gcp_system_log_file, 'a') as logfile:
        logfile.write(str(now) + " <-- Exited LIST ALL ORGANIZATIONS mode\n")
        logfile.close()
    main_menu()

def alpha_interactive_cli():
    now = datetime.now()
    with open(gcp_system_log_file, 'a') as logfile:
        logfile.write(str(now) + " --> Accessed ALPHA INTERACTIVE mode\n")
        logfile.close()
    print('Mode A accessed.\n')
    print("You have accessed the alpha gcloud cli interactive mode. Once inside the console, to exit, type exit and enter.")
    input("\nPress enter to access the interactive console now:  ")
    execute_gcloud_command_with_auth_check('gcloud alpha interactive', 
                          "Starting gcloud interactive mode")
    input('\nPress enter to get back to the main menu: ')
    now = datetime.now()
    with open(gcp_system_log_file, 'a') as logfile:
        logfile.write(str(now) + " <-- Exited ALPHA INTERACTIVE menu\n")
        logfile.close()
    main_menu()

def login_account():
    now = datetime.now()
    with open(gcp_system_log_file, 'a') as logfile:
        logfile.write(str(now) + " --> Accessed LOGIN menu\n")
        logfile.close()
    print('Mode L accessed.\n')
    print('\nAccount login/switch mode.\n')
    def account_types():
        def interactive_sign_in():
            # Interactive gcloud login
            global LOGIN_CONFIG_FILE
            WORKFORCE_POOL_ID = input("\nPlease type the name of the workforce pool and provider ID: ")
            LOGIN_CONFIG_FILE = input('\nProvide a name for the login configuration file (example: login.json): ')
            global_var = 'gcloud iam workforce-pools create-login-config ' + WORKFORCE_POOL_ID + ' --output-file=' + LOGIN_CONFIG_FILE + ' --activate'
            print('\nCreating sign in config file...\n')
            os.system(global_var)
            print('\nReading created file ' + LOGIN_CONFIG_FILE + ' metadata: \n')
            with open(LOGIN_CONFIG_FILE, 'r') as filedata:  # Opening the given file in read-only mode
                for line in filedata:
                    print(line)
            filedata.close()
            input('\nPress enter to proceed to the main menu: ')
            account_types()

        def proceed_to_login():
            EXISTING_LOGIN_CONFIG_FILE = input('\nProvide an existing valid name to log in to you provider and press enter: ')
            pwd_path = os.getcwd()
            gcloud_auth_login_var = 'gcloud auth login --login-config='
            if EXISTING_LOGIN_CONFIG_FILE == "":
                input('\nNothing was typed. Press enter to retry...')
                proceed_to_login()
            if os.path.isfile(EXISTING_LOGIN_CONFIG_FILE):
                print("\nFile " + EXISTING_LOGIN_CONFIG_FILE + " was found...")
                print(f"🔧 Logging in with config file: {EXISTING_LOGIN_CONFIG_FILE}")
                os.system(f'{gcloud_auth_login_var}{EXISTING_LOGIN_CONFIG_FILE}')
                print("\nShowing active account: ")
                print("🔧 Getting current active account")
                os.system('gcloud config list account --format "value(core.account)"')
                input('\nPress enter to proceed to the main menu: ')
                account_types()
            else:
                print("\nFile " + EXISTING_LOGIN_CONFIG_FILE + " not found")
                print('\nUnable to login. Retry again generating a new one.')
                input('\nPress enter to proceed to the main menu: ')
                account_types()

        def set_property():
            property_file=input("Provide valid .json file to set the property to login: ")
            if os.path.isfile(property_file):
                print("\nFile " + property_file + " was found...")
                set_prop_var = 'gcloud config set auth/login_config_file ' + property_file
                print('\nSetting property based on ' + property_file + ' ...')
                os.system(set_prop_var)
                input('\nPress enter to proceed to the main menu: ')
                account_types()

            else:
                print("\nFile " + property_file + " not found")
                print('\nUnable to login. Retry again generating a new one.')
                input('\nPress enter to proceed to the main menu: ')
                account_types()

        def unset_property():
            unset_prop_var = 'gcloud config unset auth/login_config_file '
            print('\nUnsetting property...')
            os.system(unset_prop_var)
            input('\nPress enter to proceed to the main menu: ')
            account_types()

        def gcloud_auth():
            input('\nPress enter to run gcloud auth login: ')
            gcloud_auth = 'gcloud auth login'
            print("🔧 Initiating Google Cloud authentication")
            os.system(gcloud_auth)
            input('\nPress enter to proceed to the main menu: ')
            account_types()

        print('\n- a - Show active logged in account')
        print('- i - Initiate gcloud - gcloud init')
        print('- c - Run gcloud auth login')
        print('- f - Generate config file based on workforce pool provider')
        print('- g - To login with a corporate GOOGLE account')
        print('- l - Log in to your provider, by providing an existing valid .json config file')
        print('- s - Set active account')
        print('- p - To set the property to use the config file')
        print('- u - To unset the property')
        print('- b - < Back to main menu')
        selection=input('\nType an option from the menu and press enter: ')
        if selection == "i":
            input('\nPress enter to init gcloud now: ')
            gcloud_init = 'gcloud init'
            print("🔧 Initializing Google Cloud configuration")
            os.system(gcloud_init)
            input('\nPress enter to proceed to the main menu: ')
            account_types()
        if selection  == "f":
            interactive_sign_in()
        if selection == "c":
            gcloud_auth()
        if selection  == 'a':
            input('\nPress enter to view the current active account: ')
            print('\nThe current logged in set account is: \n')
            print("🔧 Getting current active account")
            os.system('gcloud config list account --format "value(core.account)"')
            input('\nPress enter to get back to the main menu: ')
            account_types()
        if selection == 'g':
            account = input("\nPlease provide the name of the GOOGLE account you want to login with: ")
            print(f"🔧 Logging in with Google account: {account}")
            os.system(f'gcloud auth login {account}')
            input('\nPress enter to get back to the main menu: ')
            account_types()
        if selection == 's':
            set_active_account=input("Provide the name of the account you want to set: ")
            print(f"🔧 Setting active account to: {set_active_account}")
            os.system(f'gcloud config set account {set_active_account}')
            input('\nPress enter to get back to the main menu: ')
            account_types()
        if selection ==  'l':
            proceed_to_login()
        if selection == 'p':
            set_property()
        if selection == 'u':
            unset_property()
        if selection == 'b':
            input('\nYou decided to go back to the main menu. Press enter to get back there: ')
            now = datetime.now()
            with open(gcp_system_log_file, 'a') as logfile:
                logfile.write(str(now) + " <-- Exited LOGIN menu\n")
                logfile.close()
            main_menu()
        else:
            account_types()
    account_types()

def compute_engine_module():

    def compute_regions_show():
        now = datetime.now()
        with open(gcp_system_log_file, 'a') as logfile:
            logfile.write(str(now) + " --> Accessed COMPUTE REGION SHOW mode\n")
            logfile.close()
        print("\nCompute show region mode accessed.\n")
        print('Showing current region...  \n')
        execute_gcloud_command_with_auth_check('gcloud config list compute/region', 
                              "Showing current compute region")
        now = datetime.now()
        with open(gcp_system_log_file, 'a') as logfile:
            logfile.write(str(now) + " - Executed command: gcloud config list compute/region\n")
            logfile.close()
        input('\nPress enter to get back to the compute engine menu: ')
        now = datetime.now()
        with open(gcp_system_log_file, 'a') as logfile:
            logfile.write(str(now) + " <-- Exited COMPUTE REGION SHOW mode\n")
            logfile.close()
        compute_engine_module()

    def compute_regions_set():
        now = datetime.now()
        with open(gcp_system_log_file, 'a') as logfile:
            logfile.write(str(now) + " --> Accessed COMPUTE REGION SET mode\n")
            logfile.close()
        print('\nRegion set mode accesed.\n')
        region_set = input('Provide the name of the region to set/change: ')
        execute_gcloud_command_with_auth_check(f'gcloud config set compute/region {region_set}', 
                              f"Setting compute region to: {region_set}")
        now = datetime.now()
        with open(gcp_system_log_file, 'a') as logfile:
            logfile.write(
                str(now) + " - Executed command: gcloud compute set compute/region " + region_set + "\n")
            logfile.close()
        input('\nPress enter to get back to the compute engine menu: ')
        now = datetime.now()
        with open(gcp_system_log_file, 'a') as logfile:
            logfile.write(str(now) + " <-- Exited COMPUTE REGION SET mode\n")
            logfile.close()
        compute_engine_module()

    def compute_regions_list():
        now = datetime.now()
        with open(gcp_system_log_file, 'a') as logfile:
            logfile.write(str(now) + " --> Accessed COMPUTE REGIONS LIST mode\n")
            logfile.close()
        print("\nCompute list regions mode accessed.\n")
        print('Listing compute regions...  \n')
        execute_gcloud_command_with_auth_check('gcloud compute regions list', 
                              "Listing all available compute regions")
        now = datetime.now()
        with open(gcp_system_log_file, 'a') as logfile:
            logfile.write(str(now) + " - Executed command: gcloud compute zones list\n")
            logfile.close()
        input('\nPress enter to get back to the compute engine menu: ')
        now = datetime.now()
        with open(gcp_system_log_file, 'a') as logfile:
            logfile.write(str(now) + " <-- Exited COMPUTE REGIONS LIST mode\n")
            logfile.close()
        compute_engine_module()

    def compute_zones():
        now = datetime.now()
        with open(gcp_system_log_file, 'a') as logfile:
            logfile.write(str(now) + " --> Accessed COMPUTE ZONES LIST mode\n")
            logfile.close()
        print("\nCompute zones mode accessed.\n")
        print('Listing compute zones...  \n')
        execute_gcloud_command_with_auth_check('gcloud compute zones list', "Listing all available compute zones")
        now = datetime.now()
        with open(gcp_system_log_file, 'a') as logfile:
            logfile.write(str(now) + " - Executed command: gcloud compute zones list\n")
            logfile.close()
        input('\nPress enter to get back to the compute engine menu: ')
        now = datetime.now()
        with open(gcp_system_log_file, 'a') as logfile:
            logfile.write(str(now) + " <-- Exited COMPUTE ZONES LIST mode\n")
            logfile.close()
        compute_engine_module()

    def compute_zone_describe():
        now = datetime.now()
        with open(gcp_system_log_file, 'a') as logfile:
            logfile.write(str(now) + " --> Accessed COMPUTE ZONES DESCRIBE mode\n")
            logfile.close()
        print("\nCompute zones describe mode accessed.\n")
        describe_zone=input('Provide a valid zone to describe:  ')
        box_format = ' --format "[box]"'
        execute_gcloud_command_with_auth_check(f'gcloud compute zones describe {describe_zone}{box_format}', 
                              f"Describing compute zone: {describe_zone}")
        now = datetime.now()
        with open(gcp_system_log_file, 'a') as logfile:
            logfile.write(str(now) + " - Executed command: gcloud compute zones describe "+describe_zone+box_format+"\n")
            logfile.close()
        input('\nPress enter to get back to the compute engine menu: ')
        now = datetime.now()
        with open(gcp_system_log_file, 'a') as logfile:
            logfile.write(str(now) + " <-- Exited COMPUTE ZONES DESCRIBE mode\n")
            logfile.close()
        compute_engine_module()

    def compute_list_running_os_instances():
        now = datetime.now()
        with open(gcp_system_log_file, 'a') as logfile:
            logfile.write(str(now) + " --> Accessed COMPUTE LIST RUNNING OS INSTANCES mode\n")
            logfile.close()
        print("\nList running os instances mode accessed.\n")
        execute_gcloud_command_with_auth_check('gcloud compute instances os-inventory list-instances', 
                              "Listing running OS instances")
        now = datetime.now()
        with open(gcp_system_log_file, 'a') as logfile:
            logfile.write(str(now) + " - Executed command: gcloud compute instances os-inventory list-instances\n")
            logfile.close()
        input('\nPress enter to get back to the compute engine menu: ')
        now = datetime.now()
        with open(gcp_system_log_file, 'a') as logfile:
            logfile.write(str(now) + " <-- Exited COMPUTE LIST RUNNING OS INSTANCES mode\n")
            logfile.close()
        compute_engine_module()

    def compute_describe_runnning_os_instances():
        now = datetime.now()
        with open(gcp_system_log_file, 'a') as logfile:
            logfile.write(str(now) + " --> Accessed COMPUTE DESCRIBE RUNNING OS INSTANCES mode\n")
            logfile.close()
        print("\nDescribe running vm os instance mode accessed.\n")
        describe_running_os=input('Provide a valid vm name to describe the os instance: ')
        execute_gcloud_command_with_auth_check(f'gcloud compute instances os-inventory describe {describe_running_os}', 
                              f"Describing OS inventory for VM: {describe_running_os}")
        now = datetime.now()
        with open(gcp_system_log_file, 'a') as logfile:
            logfile.write(str(now) + " - Executed command: gcloud compute instances os-inventory describe "+describe_running_os+"\n")
            logfile.close()
        input('\nPress enter to get back to the compute engine menu: ')
        now = datetime.now()
        with open(gcp_system_log_file, 'a') as logfile:
            logfile.write(str(now) + " <-- Exited COMPUTE DESCRIBE RUNNING OS INSTANCES mode\n")
            logfile.close()
        compute_engine_module()

    def compute_zone_filter():
        now = datetime.now()
        with open(gcp_system_log_file, 'a') as logfile:
            logfile.write(str(now) + " --> Accessed COMPUTE FIND VM mode\n")
            logfile.close()
        filter_name_zone = input('\nProvide a valid vm name to find:  ')
        compute_filter='gcloud compute instances list --filter="name='
        quote='"'
        box_format=' --format "[box]"'
        os.system(compute_filter+filter_name_zone+quote+box_format)
        now = datetime.now()
        with open(gcp_system_log_file, 'a') as logfile:
            logfile.write(
                str(now) + " - Executed command: gcloud compute instances list "+'--filter="name='+filter_name_zone+quote+box_format+"\n")
            logfile.close()
        input('\nPress enter to get back to the compute engine menu: ')
        now = datetime.now()
        with open(gcp_system_log_file, 'a') as logfile:
            logfile.write(str(now) + " <-- Exited COMPUTE FIND VM mode\n")
            logfile.close()
        compute_engine_module()

    def compute_list_images():
        now = datetime.now()
        with open(gcp_system_log_file, 'a') as logfile:
            logfile.write(str(now) + " --> Accessed COMPUTE LIST IMAGES mode\n")
            logfile.close()
        print('Listing compute images...  \n')
        execute_gcloud_command_with_auth_check('gcloud compute images list', 
                              "Listing all available compute images")
        now = datetime.now()
        with open(gcp_system_log_file, 'a') as logfile:
            logfile.write(
                str(now) + " - Executed command: gcloud compute images list\n")
            logfile.close()
        input('\nPress enter to get back to the compute engine menu: ')
        now = datetime.now()
        with open(gcp_system_log_file, 'a') as logfile:
            logfile.write(str(now) + " <-- Exited COMPUTE LIST IMAGES mode\n")
            logfile.close()
        compute_engine_module()

    def compute_vm_name():
        now = datetime.now()
        with open(gcp_system_log_file, 'a') as logfile:
            logfile.write(str(now) + " --> Accessed COMPUTE FIND VM IMAGE mode\n")
            logfile.close()
        filter_vm_name = input('\nProvide a valid vm image name to find:  ')
        compute_filter = 'gcloud compute images list --filter="name='
        quote = '"'
        box_format = ' --format "[box]"'
        os.system(compute_filter + filter_vm_name + quote + box_format)
        now = datetime.now()
        with open(gcp_system_log_file, 'a') as logfile:
            logfile.write(str(now) + " - Executed command: gcloud compute images list " + '--filter="name=' + filter_vm_name + quote + box_format + "\n")
            logfile.close()
        input('\nPress enter to get back to the compute engine menu: ')
        now = datetime.now()
        with open(gcp_system_log_file, 'a') as logfile:
            logfile.write(str(now) + " <-- Exited COMPUTE FIND VM IMMAGE mode\n")
            logfile.close()
        compute_engine_module()

    def compute_ssh_vm_simple():
        now = datetime.now()
        with open(gcp_system_log_file, 'a') as logfile:
            logfile.write(str(now) + " --> Accessed COMPUTE SSH VM SIMPLE mode\n")
            logfile.close()
        print('\nSSH vm simple mode accessed.\n')
        
        # List all VM instances with details first
        print('Fetching VM instance information...\n')
        try:
            # Get VM instances in JSON format for detailed parsing
            result = subprocess.run(['gcloud', 'compute', 'instances', 'list', '--format=json'], 
                                  capture_output=True, text=True, check=True)
            instances_data = json.loads(result.stdout)
            
            if not instances_data:
                print('No VM instances found in the current project.')
                input('\nPress enter to get back to the compute engine menu: ')
                compute_engine_module()
                return
            
            # Display instances in a formatted table
            print('=' * 120)
            print(f"{'NAME':<20} {'ZONE':<25} {'MACHINE TYPE':<15} {'STATUS':<10} {'INTERNAL IP':<15} {'EXTERNAL IP':<15}")
            print('=' * 120)
            
            for instance in instances_data:
                name = instance.get('name', 'N/A')
                zone = instance.get('zone', 'N/A').split('/')[-1]  # Extract zone name from full path
                machine_type = instance.get('machineType', 'N/A').split('/')[-1]  # Extract machine type name
                status = instance.get('status', 'N/A')
                
                # Extract IP addresses
                internal_ip = 'N/A'
                external_ip = 'N/A'
                network_interfaces = instance.get('networkInterfaces', [])
                if network_interfaces:
                    internal_ip = network_interfaces[0].get('networkIP', 'N/A')
                    access_configs = network_interfaces[0].get('accessConfigs', [])
                    if access_configs:
                        external_ip = access_configs[0].get('natIP', 'N/A')
                
                print(f"{name:<20} {zone:<25} {machine_type:<15} {status:<10} {internal_ip:<15} {external_ip:<15}")
            
            print('=' * 120)
            print()
            
        except subprocess.CalledProcessError as e:
            print(f'Error fetching VM instances: {e.stderr}')
            print('Proceeding with manual VM name input...\n')
        except json.JSONDecodeError as e:
            print(f'Error parsing VM instance data: {e}')
            print('Proceeding with manual VM name input...\n')
        except Exception as e:
            print(f'Unexpected error: {e}')
            print('Proceeding with manual VM name input...\n')
        
        vm_name = input("Provide the VM instance name to connect to: ")
        print("\nAttempting to connect to vm instance...")
        ssh_vm_instance_simple=f'gcloud compute ssh {vm_name}'
        execute_gcloud_command_with_auth_check(ssh_vm_instance_simple, 
                              f"Connecting via SSH to VM: {vm_name}")
        now = datetime.now()
        with open(gcp_system_log_file, 'a') as logfile:
            logfile.write(
                str(now) + " - Executed command: gcloud compute ssh "+vm_name+"\n")
            logfile.close()
        input('\nPress enter to get back to the compute engine menu: ')
        now = datetime.now()
        with open(gcp_system_log_file, 'a') as logfile:
            logfile.write(str(now) + " <-- Exited COMPUTE SSH VM SIMPLE mode\n")
            logfile.close()
        compute_engine_module()

    def compute_create_vm_instance():
        now = datetime.now()
        with open(gcp_system_log_file, 'a') as logfile:
            logfile.write(str(now) + " --> Accessed COMPUTE CREATE VM INSTANCE mode\n")
            logfile.close()
        print('\nVM instance creation mode accesed.\n')
        vm_instance_name=input('Provide the name/s of the vm instance/s to create: ')
        default_zone=' --zone=northamerica-northeast1-a'
        print('\nAttempting to create vm instances: '+ vm_instance_name + "...")
        execute_gcloud_command_with_auth_check(f'gcloud compute instances create {vm_instance_name}{default_zone}', 
                              f"Creating VM instance: {vm_instance_name}")
        now = datetime.now()
        with open(gcp_system_log_file, 'a') as logfile:
            logfile.write(str(now) + " - Executed command: gcloud compute instances create "+vm_instance_name+default_zone+"\n")
            logfile.close()
        input('\nPress enter to get back to the compute engine menu: ')
        now = datetime.now()
        with open(gcp_system_log_file, 'a') as logfile:
            logfile.write(str(now) + " <-- Exited COMPUTE CREATE VM INSTANCE mode\n")
            logfile.close()
        compute_engine_module()

    def compute_delete_vm_instance():
        now = datetime.now()
        with open(gcp_system_log_file, 'a') as logfile:
            logfile.write(str(now) + " --> Accessed COMPUTE DELETE VM INSTANCE mode\n")
            logfile.close()
        print('\nVM instance deletion mode accesed.\n')
        vm_instance_name=input('Provide the name/s of the vm instance/s to delete: ')
        delete_quiet=' --zone=northamerica-northeast1-a --quiet'
        print('\nAttempting to delete vm instances: '+vm_instance_name+"...")
        execute_gcloud_command_with_auth_check(f'gcloud compute instances delete {vm_instance_name}{delete_quiet}', 
                              f"Deleting VM instance: {vm_instance_name}")
        now = datetime.now()
        with open(gcp_system_log_file, 'a') as logfile:
            logfile.write(str(now) + " - Executed command: gcloud compute instances delete " + vm_instance_name + delete_quiet + "\n")
            logfile.close()
        input('\nPress enter to get back to the compute engine menu: ')
        now = datetime.now()
        with open(gcp_system_log_file, 'a') as logfile:
            logfile.write(str(now) + " <-- Exited COMPUTE DELETE VM INSTANCE mode\n")
            logfile.close()
        compute_engine_module()

    def compute_create_instance_template():
        now = datetime.now()
        with open(gcp_system_log_file, 'a') as logfile:
            logfile.write(str(now) + " --> Accessed COMPUTE CREATE INSTANCE TEMPLATE mode\n")
            logfile.close()
        print('\nInstance template creation mode accesed.\n')
        instance_template_name_create = input('Provide the name of the instance template to create: ')
        execute_gcloud_command_with_auth_check(f'gcloud compute instance-templates create {instance_template_name_create}', 
                              f"Creating instance template: {instance_template_name_create}")
        now = datetime.now()
        with open(gcp_system_log_file, 'a') as logfile:
            logfile.write(
                str(now) + " - Executed command: gcloud instance-templates create "+instance_template_name_create+"\n")
            logfile.close()
        input('\nPress enter to get back to the compute engine menu: ')
        now = datetime.now()
        with open(gcp_system_log_file, 'a') as logfile:
            logfile.write(str(now) + " <-- Exited COMPUTE CREATE INSTANCE TEMPLATE mode\n")
            logfile.close()
        compute_engine_module()

    def compute_delete_instance_template():
        now = datetime.now()
        with open(gcp_system_log_file, 'a') as logfile:
            logfile.write(str(now) + " --> Accessed COMPUTE DELETE INSTANCE TEMPLATE mode\n")
            logfile.close()
        print('\nInstance template deletion mode accesed.\n')
        instance_template_name_delete = input('Provide the name of the instance template to delete: ')
        execute_gcloud_command_with_auth_check(f'gcloud compute instance-templates delete {instance_template_name_delete}', 
                              f"Deleting instance template: {instance_template_name_delete}")
        now = datetime.now()
        with open(gcp_system_log_file, 'a') as logfile:
            logfile.write(
                str(now) + " - Executed command: gcloud instance-templates delete "+instance_template_name_delete+"\n")
            logfile.close()
        input('\nPress enter to get back to the compute engine menu: ')
        now = datetime.now()
        with open(gcp_system_log_file, 'a') as logfile:
            logfile.write(str(now) + " <-- Exited COMPUTE DELETE INSTANCE TEMPLATE mode\n")
            logfile.close()
        compute_engine_module()

    def compute_list_instance_template():
        now = datetime.now()
        with open(gcp_system_log_file, 'a') as logfile:
            logfile.write(str(now) + " --> Accessed COMPUTE LIST INSTANCE TEMPLATE mode\n")
            logfile.close()
        print('\nInstance template listing mode accesed.\n')
        print('Listing instance templates...  \n')
        execute_gcloud_command_with_auth_check('gcloud compute instance-templates list', 
                              "Listing all instance templates")
        now = datetime.now()
        with open(gcp_system_log_file, 'a') as logfile:
            logfile.write(
                str(now) + " - Executed command: gcloud compute instance-templates list\n")
            logfile.close()
        input('\nPress enter to get back to the compute engine menu: ')
        now = datetime.now()
        with open(gcp_system_log_file, 'a') as logfile:
            logfile.write(str(now) + " <-- Exited COMPUTE LIST INSTANCE TEMPLATE mode\n")
            logfile.close()
        compute_engine_module()

    def compute_find_instance_template():
        now = datetime.now()
        with open(gcp_system_log_file, 'a') as logfile:
            logfile.write(str(now) + " --> Accessed COMPUTE FIND INSTANCE TEMPLATE mode\n")
            logfile.close()
        print('\nInstance template finding mode accesed.\n')
        instance_template_find_name = input('Provide the name of the instance template to find: ')
        quote='"'
        execute_gcloud_command_with_auth_check(f'gcloud compute instance-templates list --filter="name={instance_template_find_name}{quote} --format "[box]"', 
                              f"Finding instance template: {instance_template_find_name}")
        now = datetime.now()
        with open(gcp_system_log_file, 'a') as logfile:
            logfile.write(str(now) + " - Executed command: gcloud compute images list " + '--filter="name=' + instance_template_find_name + quote + box_format + "\n")
            logfile.close()
        input('\nPress enter to get back to the compute engine menu: ')
        now = datetime.now()
        with open(gcp_system_log_file, 'a') as logfile:
            logfile.write(str(now) + " <-- Exited COMPUTE FIND INSTANCE TEMPLATE mode\n")
            logfile.close()
        compute_engine_module()

    def compute_describe_instance_template():
        now = datetime.now()
        with open(gcp_system_log_file, 'a') as logfile:
            logfile.write(str(now) + " --> Accessed COMPUTE DESCRIBE INSTANCE TEMPLATE mode\n")
            logfile.close()
        print('\nInstance template description mode accesed.\n')
        instance_template_describe_name = input('Provide the name of the instance template to describe: ')
        execute_gcloud_command_with_auth_check(f'gcloud compute instance-templates describe {instance_template_describe_name}', 
                              f"Describing instance template: {instance_template_describe_name}")
        now = datetime.now()
        with open(gcp_system_log_file, 'a') as logfile:
            logfile.write(str(now) + " - Executed command: gcloud -templates describe "+instance_template_describe_name+"\n")
            logfile.close()
        input('\nPress enter to get back to the compute engine menu: ')
        now = datetime.now()
        with open(gcp_system_log_file, 'a') as logfile:
            logfile.write(str(now) + " <-- Exited COMPUTE DESCRIBE INSTANCE TEMPLATE mode\n")
            logfile.close()
        compute_engine_module()

    def compute_operations_list_describe():
        operations_dir="compute_operations_logs"
        os.system('mkdir -p '+operations_dir)
        now = datetime.now()
        with open(gcp_system_log_file, 'a') as logfile:
            logfile.write(str(now) + " --> Accessed COMPUTE OPERATIONS main mode\n")
            logfile.close()
        def compute_operations_list_json():
            now = datetime.now()
            with open(gcp_system_log_file, 'a') as logfile:
                logfile.write(str(now) + " --> Accessed COMPUTE OPERATIONS JSON format list mode\n")
                logfile.close()
            list_operation_name = input('\nProvide the name of the user, to list all of the executed operations in compute: ')
            quotes='"'
            execute_gcloud_command_with_auth_check(f'gcloud compute operations list --filter="user={list_operation_name}{quotes} --format=json', 
                                  f"Listing operations for user: {list_operation_name}")
            with open(gcp_system_log_file, 'a') as logfile:
                logfile.write(str(now) + ' - Executed command: gcloud compute operations list --filter='+"user="+list_operation_name+quotes+' --format=json'+"\n")
                logfile.close()
            script_timestamp = datetime.now()
            format_script_timestamp = str(script_timestamp).replace(" ", "_")
            query_api_log=format_script_timestamp+"_"+"list_json_"+list_operation_name+".log"
            operations_dir="compute_operations_logs"
            with open(operations_dir+"/"+query_api_log, 'a') as logfile:
                try:
                    logfile.close()
                    execute_gcloud_command_with_auth_check(f'gcloud compute operations list --filter="user={list_operation_name}{quotes} --format=json | tee -a {operations_dir}/{query_api_log}', 
                                          f"Listing operations for user {list_operation_name} (JSON format)")
                    print("\nGenerated log file: "+operations_dir+"/"+query_api_log+" which you can view and query from the compute operations menu")
                    input('\nPress enter to get back to the compute operations menu: ')
                    now = datetime.now()
                    with open(gcp_system_log_file, 'a') as logfile:
                        logfile.write(str(now) + " + Generated log file: "+operations_dir+"/"+query_api_log+"\n")
                        logfile.close()
                    now = datetime.now()
                    with open(gcp_system_log_file, 'a') as logfile:
                        logfile.write(str(now) + " <-- Exited COMPUTE OPERATIONS JSON format list mode\n")
                        logfile.close()
                    compute_operations_list_describe()
                except:
                    print("\nGenerated log file: " + operations_dir+"/"+query_api_log + " which you can view and query from the compute operations menu")
                    input('\nPress enter to get back to the compute operations menu: ')
                    now = datetime.now()
                    with open(gcp_system_log_file, 'a') as logfile:
                        logfile.write(str(now) + " + Generated log file: "+operations_dir+"/"+query_api_log+"\n")
                        logfile.close()
                    now = datetime.now()
                    with open(gcp_system_log_file, 'a') as logfile:
                        logfile.write(str(now) + " <-- Exited COMPUTE OPERATIONS JSON format list mode\n")
                        logfile.close()
                    compute_operations_list_describe()

        def compute_operations_list_text():
            now = datetime.now()
            with open(gcp_system_log_file, 'a') as logfile:
                logfile.write(str(now) + " --> Accessed COMPUTE OPERATIONS TEXT format list mode\n")
                logfile.close()
            list_operation_name = input('\nProvide the name of the user, to list all of the executed operations in compute: ')
            quotes='"'
            execute_gcloud_command_with_auth_check(f'gcloud compute operations list --filter="user={list_operation_name}{quotes}', 
                                  f"Listing operations for user: {list_operation_name}")
            with open(gcp_system_log_file, 'a') as logfile:
                logfile.write(str(now) + ' - Executed command: gcloud compute operations list --filter='+"user="+list_operation_name+quotes+"\n")
                logfile.close()
            script_timestamp = datetime.now()
            format_script_timestamp = str(script_timestamp).replace(" ", "_")
            query_api_log = format_script_timestamp + "_" + "list_text_" + list_operation_name + ".log"
            operations_dir = "compute_operations_logs"
            with open(operations_dir+"/"+query_api_log, 'a') as logfile:
                try:
                    logfile.close()
                    execute_gcloud_command_with_auth_check(f'gcloud compute operations list --filter="user={list_operation_name}{quotes} | tee -a {operations_dir}/{query_api_log}', 
                                          f"Listing operations for user {list_operation_name} (text format)")
                    print("\nGenerated log file: " +query_api_log + " which you can view and query from the compute operations menu")
                    input('\nPress enter to get back to the compute operations menu: ')
                    now = datetime.now()
                    with open(gcp_system_log_file, 'a') as logfile:
                        logfile.write(str(now) + " + Generated log file: " +query_api_log + "\n")
                        logfile.close()
                    now = datetime.now()
                    with open(gcp_system_log_file, 'a') as logfile:
                        logfile.write(str(now) + " <-- Exited COMPUTE OPERATIONS TEXT format list mode\n")
                        logfile.close()
                    compute_operations_list_describe()
                except:
                    print("\nGenerated log file: " +query_api_log + " which you can view and query from the compute operations menu")
                    input('\nPress enter to get back to the compute operations menu: ')
                    now = datetime.now()
                    with open(gcp_system_log_file, 'a') as logfile:
                        logfile.write(str(now) + " + Generated log file: " +"/"+query_api_log + "\n")
                        logfile.close()
                    now = datetime.now()
                    with open(gcp_system_log_file, 'a') as logfile:
                        logfile.write(str(now) + " <-- Exited COMPUTE OPERATIONS TEXT format list mode\n")
                        logfile.close()
                    compute_operations_list_describe()

        def compute_operations_describe():
            now = datetime.now()
            with open(gcp_system_log_file, 'a') as logfile:
                logfile.write(str(now) + " --> Accessed COMPUTE OPERATIONS describe mode\n")
                logfile.close()
            describe_operation_name = input('\nProvide the name of the operation to describe: ')
            quotes = '"'
            execute_gcloud_command_with_auth_check(f'gcloud compute operations describe {describe_operation_name}', 
                                  f"Describing operation: {describe_operation_name}")
            with open(gcp_system_log_file, 'a') as logfile:
                logfile.write(str(now) + ' - Executed command: gcloud compute operations describe '+describe_operation_name+"\n")
                logfile.close()
            input('\nPress enter to get back to the compute operations menu: ')
            now = datetime.now()
            with open(gcp_system_log_file, 'a') as logfile:
                logfile.write(str(now) + " <-- Exited COMPUTE OPERATIONS describe mode\n")
                logfile.close()
            compute_operations_list_describe()

        def compute_operations_show_generated_logs():
            now = datetime.now()
            with open(gcp_system_log_file, 'a') as logfile:
                logfile.write(str(now) + " --> Accessed COMPUTE OPERATIONS show all logs mode\n")
                logfile.close()
            operations_dir = "compute_operations_logs"
            logs_string_var = "_list_"
            print('\nView compute operations logs menu accessed')
            dir_path = os.path.dirname(os.path.realpath(__file__))
            check_file = os.path.isfile(logs_string_var)
            print('\nListing generated logs in path: ' + dir_path + "/" + operations_dir + ': \n')
            for i in os.listdir(path=dir_path + "/" + operations_dir):
                if logs_string_var in i:
                    print(i)
            with open(gcp_system_log_file, 'a') as logfile:
                logfile.write(str(now) + ' - Listed all user generated logfiles in system.' +"\n")
                logfile.close()
            input('\nPress enter to get back to the main menu: ')
            now = datetime.now()
            with open(gcp_system_log_file, 'a') as logfile:
                logfile.write(str(now) + " <-- Exited COMPUTE OPERATIONS show all logs mode\n")
                logfile.close()
            compute_operations_list_describe()

        def compute_operations_read_log_file():
            dir_path = os.path.dirname(os.path.realpath(__file__))
            operations_dir = "compute_operations_logs"
            now = datetime.now()
            with open(gcp_system_log_file, 'a') as logfile:
                logfile.write(str(now) + " --> Accessed COMPUTE OPERATIONS read logs mode\n")
                logfile.close()
            logs_string_var = "_list_"
            read_log_file=input('\nType the compute log file you want to read: ')
            if read_log_file in os.listdir(path=dir_path+"/"+operations_dir):
                    read_file=open(operations_dir+"/"+read_log_file, 'r')
                    log_read=read_file.readlines()
                    for line in log_read:
                        print(line)
                    with open(gcp_system_log_file, 'a') as logfile:
                        logfile.write(str(now) + ' - Read logfile: '+read_log_file+"\n")
                        logfile.close()
                    input('\nPress enter to get back to the main menu: ')
                    with open(gcp_system_log_file, 'a') as logfile:
                        logfile.write(str(now) + " <-- Exited COMPUTE OPERATIONS read logs mode\n")
                        logfile.close()
                    compute_operations_list_describe()
            else:
                print('\nLog file '+read_log_file+' not found.')
                input('\nPress enter to get back to the main menu: ')
                with open(gcp_system_log_file, 'a') as logfile:
                    logfile.write(str(now) + " <-- Exited COMPUTE OPERATIONS read logs mode\n")
                    logfile.close()
                compute_operations_list_describe()

        def compute_operations_find_regexp():
            now = datetime.now()
            with open(gcp_system_log_file, 'a') as logfile:
                logfile.write(str(now) + " --> Accessed COMPUTE OPERATIONS find regexp logs mode\n")
                logfile.close()
            operations_dir = "compute_operations_logs"
            global check_file, dir_path, test_case_string_var
            logs_string_var = "_list_"
            print('\nView compute operations logs menu accessed')
            dir_path = os.path.dirname(os.path.realpath(__file__))
            check_file = os.path.isfile(logs_string_var)
            provide_log=input('\nProvide the name of the log, in which you want to find a regexp: ')
            if provide_log in os.listdir(path=dir_path + "/" + operations_dir):
                print('\nLogfile: '+provide_log+' found.')
                loop=0
                while loop==0:
                    compute_log_regexp=input("\nType the regexp you want to find in this logfile: ")
                    read_file = open(operations_dir + "/" + provide_log, 'r')
                    log_read = read_file.readlines()
                    for line in log_read:
                        if compute_log_regexp in line:
                            print(line)
                    with open(gcp_system_log_file, 'a') as logfile:
                        logfile.write(str(now) + ' ? Searched for regexp: '+"'"+compute_log_regexp+"'"+" in logfile: "+provide_log+"\n")
                        logfile.close()
                    print('\nTo find another regular expresion in log file: '+provide_log+' press enter.')
                    find_again=input('\nTo get back to main menu type "b": ')
                    if find_again == "b":
                        print('\nYou decided to stop searching in '+provide_log)
                        input('\nPress enter to get back to the main menu: ')
                        now = datetime.now()
                        with open(gcp_system_log_file, 'a') as logfile:
                            logfile.write(str(now) + " <-- Exited COMPUTE OPERATIONS find regexp mode\n")
                            logfile.close()
                        compute_operations_list_describe()
            else:
                print('\nUnable to find log: '+provide_log)
                input('\nPress enter to get back to the main menu: ')
                with open(gcp_system_log_file, 'a') as logfile:
                    logfile.write(str(now) + " <-- Exited COMPUTE OPERATIONS find regexp mode\n")
                    logfile.close()
                compute_operations_list_describe()

        def compute_operations_delete_log():
            now = datetime.now()
            with open(gcp_system_log_file, 'a') as logfile:
                logfile.write(str(now) + " --> Accessed COMPUTE OPERATIONS delete logs mode\n")
                logfile.close()
            logs_string_var = "_list_"
            operations_dir = "compute_operations_logs"
            print('\nNOTE: only compute log files containing syntax: ' + logs_string_var + ' will be removed.')
            delete_compute_log_files = input("\nType the compute log file to delete. If it is more than one, separate them with spaces: ")
            logs_to_delete = []
            for log in delete_compute_log_files.split():
                logs_to_delete.append(log)
            for log in logs_to_delete:
                if logs_string_var in log:
                    try:
                        os.remove(operations_dir + "/" + log)
                        print('\nRemoved file: ' + log)
                        with open(gcp_system_log_file, 'a') as logfile:
                            logfile.write(str(now) + ' - Deleted compute log file '+log+"\n")
                            logfile.close()
                    except:
                        print('\n ! ERROR - File: '+str(log)+' was not found in '+operations_dir)
                        input('\nPress enter to get back to the main menu: ')
                        with open(gcp_system_log_file, 'a') as logfile:
                            logfile.write('\n'+str(now) + " ! ERROR - File: "+"'"+str(log)+"'"+' was not found in '+operations_dir)
                            logfile.close()
                        now = datetime.now()
                        with open(gcp_system_log_file, 'a') as logfile:
                            logfile.write('\n'+str(now) + " <-- Exited COMPUTE OPERATIONS delete logs mode\n")
                            logfile.close()
                        compute_operations_list_describe()

                else:
                    print('\n! ERROR - File: '+str(log)+' was not found in '+operations_dir)
                    input('\nPress enter to get back to the main menu: ')
                    now = datetime.now()
                    with open(gcp_system_log_file, 'a') as logfile:
                        logfile.write(str(now) + " ! ERROR - File: "+"'"+str(log)+"'"+' was not found in '+operations_dir)
                        logfile.close()
                    now = datetime.now()
                    with open(gcp_system_log_file, 'a') as logfile:
                        logfile.write('\n'+str(now) + " <-- Exited COMPUTE OPERATIONS delete logs mode\n")
                        logfile.close()
                    compute_operations_list_describe()
            if "" in delete_compute_log_files:
                input('\nPress enter to get back to the main menu: ')
                now = datetime.now()
                with open(gcp_system_log_file, 'a') as logfile:
                    logfile.write(str(now) + " <-- Exited COMPUTE OPERATIONS delete logs mode\n")
                    logfile.close()
                    compute_operations_list_describe()

        def compute_operations_delete_all_logs():
            operations_dir = "compute_operations_logs"
            logs_string_var = "_list_"
            now = datetime.now()
            with open(gcp_system_log_file, 'a') as logfile:
                logfile.write(str(now) + " --> Accessed COMPUTE OPERATIONS delete ALL logs mode\n")
                logfile.close()
            dir_path = os.path.dirname(os.path.realpath(__file__))
            loop=0
            while loop==0:
                provide_log = input('\nWARNING, this will delete all the compute generated logs in the system. Confirm y/n? : ')
                if provide_log=='y':
                    for log in os.listdir(path=dir_path + "/" + operations_dir):
                        if logs_string_var in log:
                            os.remove(path=dir_path + "/" + operations_dir+"/"+log)
                            print('\nRemoved compute logfile: ' + log)
                            with open(gcp_system_log_file, 'a') as logfile:
                                logfile.write(str(now) + ' - Deleted compute log file '+log+"\n")
                                logfile.close()
                    input('\nPress enter to get back to the main menu: ')
                    now = datetime.now()
                    with open(gcp_system_log_file, 'a') as logfile:
                        logfile.write(str(now) + " <-- Exited COMPUTE OPERATIONS delete ALL logs mode\n")
                        logfile.close()
                    compute_operations_list_describe()
                if provide_log == 'n':
                    print('\nAborted operation to delete all log files from the system.')
                    input('\nPress enter to get back to the main menu: ')
                    now = datetime.now()
                    with open(gcp_system_log_file, 'a') as logfile:
                        logfile.write(str(now) + " <-- Exited COMPUTE OPERATIONS delete ALL logs mode\n")
                        logfile.close()
                    compute_operations_list_describe()
                else:
                    loop=0
                    
        def compute_operations_delete_logs_with_regexp():
            operations_dir = "compute_operations_logs"
            now = datetime.now()
            with open(gcp_system_log_file, 'a') as logfile:
                logfile.write(str(now) + " --> Accessed COMPUTE OPERATIONS delete logs based on regexp mode\n")
                logfile.close()
            dir_path = os.path.dirname(os.path.realpath(__file__))
            loop=0
            while loop==0:
                provide_regexp= input('\nType a regular expression, to delete all the file names that contain it: ')
                if provide_regexp== "":
                        print('\nNothing was typed')
                        input('\nPress enter to re-attempt: ')
                        now = datetime.now()
                        with open(gcp_system_log_file, 'a') as logfile:
                            logfile.write(str(now)+" ! Nothing was typed. No regexp was provided to find and delete log files"+"\n")
                            logfile.close()
                        compute_operations_delete_logs_with_regexp()
                items_to_delete = []
                for log in os.listdir(path=dir_path + "/" + operations_dir):
                    if provide_regexp in log:
                        items_to_delete.append(str(log))

                for i in items_to_delete:
                    os.remove(path=dir_path + "/" + operations_dir+"/"+i)
                    print('\nFound regexp '+"'"+provide_regexp+"'"+' in logfile: '+str(i))
                    print('\nRemoved compute logfile: ' + i)
                    now = datetime.now()
                    with open(gcp_system_log_file, 'a') as logfile:
                        logfile.write(str(now) + " ! Found regexp "+"'"+provide_regexp+"'"+' in logfile: '+str(i)+"\n")
                        logfile.write(str(now) + ' - Deleted compute log file '+i+"\n")
                        logfile.close()

                if not items_to_delete:
                    print('\nRegular expresion '+str(provide_regexp)+' was not found in any files. No log file was deleted')
                    input('\nOperation executed, press enter to get back to the main menu: ')
                    now = datetime.now()
                    with open(gcp_system_log_file, 'a') as logfile:
                        logfile.write(str(now) + " <-- Exited COMPUTE OPERATIONS delete logs based on regexp mode"+"\n")
                        logfile.write(str(now)+' ! Regular expresion '+str(provide_regexp)+' was not found in any files. No log file was deleted'+"\n")
                        logfile.close()
                    compute_operations_list_describe()
                else:
                    print('\nLog files containing regexp '+"'"+str(provide_regexp)+"'"+' were deleted')
                    input('\nOperation executed, press enter to get back to the main menu: ')
                    now = datetime.now()
                    with open(gcp_system_log_file, 'a') as logfile:
                        logfile.write(str(now) +' ! Log files containing regexp '+"'"+str(provide_regexp)+"'"+' were deleted'+"\n")
                        logfile.write(str(now) + " <-- Exited COMPUTE OPERATIONS delete logs based on regexp mode"+"\n")
                        logfile.close()
                    compute_operations_list_describe()

        print('\nCompute operations mode accessed.\n')
        print('************************************************')
        print('       COMPUTE OPERATIONS MAIN MENU            \n')
        print('   Compute query and log generation section\n')
        print('NOTE: options  1 and 2 generate log files based on a username,')
        print('which show compute operations executed by the searched user.\n')
        print('- 1 - JSON format - List compute operations - filter by username')
        print('- 2 - TEXT format - List compute operations - filter by username')
        print('\n Read and search section\n')
        print('- 3 - Describe a specific compute operation')
        print('- 4 - Show all user generated compute log files in system')
        print('- 5 - Read a log file')
        print('- 6 - Find a regular expresion in a log')
        print('\n Logfiles deletion section\n')
        print('- 7 - Delete a log')
        print('- 8 - Delete all log files, which contain a regexp in its filename')
        print('- 9 - Delete all generated logs in system')
        print(' ')
        print('- c <-- Back to compute engine main menu')
        print('- b <-- Back to main menu')
        selection=input('\nType an option from the menu and press enter: ')
        if selection=='1':
            compute_operations_list_json()
        if selection=='2':
            compute_operations_list_text()
        if selection=='3':
            compute_operations_describe()
        if selection=='4':
            compute_operations_show_generated_logs()
        if selection=='5':
            compute_operations_read_log_file()
        if selection=='6':
            compute_operations_find_regexp()
        if selection=='7':
            compute_operations_delete_log()
        if selection=='8':
            compute_operations_delete_logs_with_regexp()
        if selection=='9':
            compute_operations_delete_all_logs()
        if selection=='c':
            compute_engine_module()
        if selection=='b':
            main_menu()
        else:
            compute_operations_list_describe()
        with open(gcp_system_log_file, 'a') as logfile:
            logfile.write(str(now) + " <-- Exited COMPUTE OPERATIONS main mode\n")
            logfile.close()

    def compute_advanced_module():
        now = datetime.now()
        with open(gcp_system_log_file, 'a') as logfile:
            logfile.write(str(now) + " --> Accessed ADVANCED COMPUTE MODULE menu\n")
            logfile.close()
        def compute_ssh_vm_advanced():
            now = datetime.now()
            with open(gcp_system_log_file, 'a') as logfile:
                logfile.write(str(now) + " --> Accessed SSH VM ADVANCED COMPUTE MODULE menu\n")
                logfile.close()
            print('\nSSH vm advanced mode accesed.\n')
            zone = input("Vm instance zone name: ")
            vm_name = input("\nVm instance name: ")
            username = input("\nGCP account name: ")
            project_name = input("\nProject name: ")
            print("\nAttempting to connect to vm instance...")
            ssh_vm_instance = 'gcloud compute ssh ' + username + "@" + vm_name + str(' --zone ') + '"' + str(zone) + '"' + str(' --project ') + '"' + project_name + '"'
            os.system(ssh_vm_instance)
            now = datetime.now()
            with open(gcp_system_log_file, 'a') as logfile:
                logfile.write(str(now) + " - Executed command: gcloud compute ssh " + username + "@" + vm_name + str(' --zone ') + '"' + str(zone) + '"' + str(' --project ') + '"' + project_name + "\n")
                logfile.close()
            input('\nPress enter to get back to the compute engine menu: ')
            now = datetime.now()
            with open(gcp_system_log_file, 'a') as logfile:
                logfile.write(str(now) + " <-- Exited SSH VM ADVANCED COMPUTE mode\n")
                logfile.close()
            compute_advanced_module()

        def compute_create_custom_vm():
            now = datetime.now()
            with open(gcp_system_log_file, 'a') as logfile:
                logfile.write(str(now) + " --> Accessed CREATE CUSTOM VM menu\n")
                logfile.close()
            print('\nCreate custom vm mode accesed.\n')
            print('To operate with this module you need to pass the following parammters to successfully create the vm:\n')
            print('- Vm name')
            print('- Image family')
            print('- Image project')
            print('- Machine type')
            print('- Amount of cpus')
            print('- Amount of RAM')
            loop = 0
            while True:
                confirm_known_data=input('\nConfirm you know the parameters data to provide? y/n: ')
                if confirm_known_data == 'y':
                    print('Provide the data requested above:  \n')
                    vm_name=input('Vm name?: ')
                    image_family=input('Image family?: ')
                    image_project=input('Image project?: ')
                    machine_type=input('Machine type?: ')
                    loop = 1
                    while True:
                        cpus_amount=input('Amount of cpus?: ')
                        if not cpus_amount.isdigit():
                            print('\nInvalid format. Only provide numbers for the amount of cpus.')
                            loop = 1
                        if cpus_amount.isdigit():
                            cpus_amount=str(cpus_amount)
                            loop = 2
                            while True:
                                ram_amount=input('Amount of RAM? expresed in GB: ')
                                if not ram_amount.isdigit():
                                    print('\nInvalid format. Only provide numbers for the amount of ram.')
                                    loop = 2
                                if ram_amount.isdigit():
                                    ram_amount=int(ram_amount)*1024
                                    ram_amount=str(ram_amount)
                                    loop =  3
                                    while True:

                                        print('Provided data is as follows:\n')
                                        print('Vm name: '+vm_name)
                                        print('Image family: '+image_family)
                                        print('Image project:  '+image_project)
                                        print('Machine type?: '+machine_type)
                                        print('RAM amount: '+ram_amount+'MB')
                                        print('CPUs amount: '+cpus_amount)
                                        print('\nVM creation instance confirmation: \n')
                                        print('- y - to confirm')
                                        print('- n - To deny and go back')
                                        print('- a - < back to compute advanced menu')
                                        print('- s - < back to compute simple menu')
                                        print('- b - < back to main menu')
                                        confirm_correct_provided_data=input('\nDo you confirm all the provided data is correct?: ')
                                        if confirm_correct_provided_data == 'y':
                                            print('Attemping to create the vm with the provided data...\n')
                                            execute_gcloud_command_with_auth_check(f'gcloud compute instances create {vm_name} --image-family={image_family} --image-project={image_project} --machine-type={machine_type}-custom-{cpus_amount}-{ram_amount}', 
                                                                  f"Creating custom VM: {vm_name}")
                                            now = datetime.now()
                                            with open(gcp_system_log_file, 'a') as logfile:
                                                logfile.write(str(now) + " - Executed command: gcloud compute instances create "+vm_name+' --image-family='+image_family+' --image-project='+image_project+' --machine-type='+machine_type+'-custom-'+cpus_amount+'-'+ram_amount+"\n")
                                                logfile.close()
                                                input('\nPress enter to get back to the compute advanced engine menu: ')
                                                now = datetime.now()
                                                with open(gcp_system_log_file, 'a') as logfile:
                                                    logfile.write(str(now) + " <-- Exited CREATE CUSTOM VM mode\n")
                                                logfile.close()
                                            compute_advanced_module()
                                        if confirm_correct_provided_data == 'n':
                                            print('\nYou decided to abort the operation by confirming incorrect data.\n')
                                            input('Press enter to get back to the compute advanced module...  ')
                                            compute_advanced_module()
                                        if confirm_correct_provided_data == 'a':
                                            compute_advanced_module()
                                        if confirm_correct_provided_data==  's':
                                            compute_engine_module()
                                        if confirm_correct_provided_data == 'b':
                                            main_menu()

                    if confirm_provided_data == 'n':
                        loop = 0
                if confirm_known_data == 'n':
                    print('\nPlease gather the correct data for the parameters. You can get back here when you have them.')
                    input('\nPress enter to get back to the main menu: ')
                    compute_advanced_module()

            input('\nPress enter to get back to the main menu: ')
            compute_advanced_module()


        print("*******************************************")
        print('      COMPUTE ENGINE ADVANCED MODULE      \n')
        print('1 - SSH into vm providing advanced parameters - zone, username, project, vm name')
        print('2 - Create a custom vm')
        print('s - < Back to compute engine simple mode')
        print('b - < Back to main menu')
        compute_selection_advanced=input('\nType a number or letter from the menu and press enter to operate: ')
        if compute_selection_advanced == '1':
            compute_ssh_vm_advanced()
        if compute_selection_advanced == '2':
            compute_create_custom_vm()
        if compute_selection_advanced == 's':
            compute_engine_module()
        if compute_selection_advanced =='b':
            main_menu()
        else:
            input('\nInvalid option selected, you must type a number or letter from the menu. Press enter to get back to the menu: ')
            compute_advanced_module()

    def compute_ssh_key_management():
        now = datetime.now()
        with open(gcp_system_log_file, 'a') as logfile:
            logfile.write(str(now) + " --> Accessed SSH KEY MANAGEMENT mode\n")
            logfile.close()
        
        print('\nSSH Key Management mode accessed.\n')
        print('This function will list all VM instances and allow you to add SSH keys for authentication.\n')
        
        # List all VM instances with details
        print('Fetching VM instance information...\n')
        try:
            # Get VM instances in JSON format for detailed parsing
            result = subprocess.run(['gcloud', 'compute', 'instances', 'list', '--format=json'], 
                                  capture_output=True, text=True, check=True)
            instances_data = json.loads(result.stdout)
            
            if not instances_data:
                print('No VM instances found in the current project.')
                input('\nPress enter to get back to the compute engine menu: ')
                compute_engine_module()
                return
            
            # Display instances in a formatted table
            print('=' * 120)
            print(f"{'NAME':<20} {'ZONE':<25} {'MACHINE TYPE':<15} {'STATUS':<10} {'INTERNAL IP':<15} {'EXTERNAL IP':<15}")
            print('=' * 120)
            
            for instance in instances_data:
                name = instance.get('name', 'N/A')
                zone = instance.get('zone', 'N/A').split('/')[-1]  # Extract zone name from full path
                machine_type = instance.get('machineType', 'N/A').split('/')[-1]  # Extract machine type name
                status = instance.get('status', 'N/A')
                
                # Extract IP addresses
                internal_ip = 'N/A'
                external_ip = 'N/A'
                network_interfaces = instance.get('networkInterfaces', [])
                if network_interfaces:
                    internal_ip = network_interfaces[0].get('networkIP', 'N/A')
                    access_configs = network_interfaces[0].get('accessConfigs', [])
                    if access_configs:
                        external_ip = access_configs[0].get('natIP', 'N/A')
                
                print(f"{name:<20} {zone:<25} {machine_type:<15} {status:<10} {internal_ip:<15} {external_ip:<15}")
            
            print('=' * 120)
            print()
            
            # Prompt for VM selection
            vm_name = input('Enter the VM instance name to add SSH keys to (or "b" to go back): ')
            
            if vm_name.lower() == 'b':
                compute_engine_module()
                return
            
            # Verify the VM exists and get its zone
            selected_vm = None
            for instance in instances_data:
                if instance.get('name') == vm_name:
                    selected_vm = instance
                    break
            
            if not selected_vm:
                print(f'\nError: VM instance "{vm_name}" not found.')
                input('\nPress enter to try again: ')
                compute_ssh_key_management()
                return
            
            # Extract zone from the selected VM
            vm_zone = selected_vm.get('zone', '').split('/')[-1]  # Extract zone name from full path
            if not vm_zone:
                print(f'\nError: Could not determine zone for VM instance "{vm_name}".')
                input('\nPress enter to try again: ')
                compute_ssh_key_management()
                return
            
            # Check if SSH key exists
            ssh_key_path = os.path.expanduser('~/.ssh/google_compute_engine.pub')
            if not os.path.exists(ssh_key_path):
                print(f'\nSSH public key not found at {ssh_key_path}')
                generate_key = input('Would you like to generate a new SSH key pair? (y/n): ')
                
                if generate_key.lower() == 'y':
                    print('\nGenerating SSH key pair...')
                    key_result = subprocess.run(['ssh-keygen', '-t', 'rsa', '-f', 
                                               os.path.expanduser('~/.ssh/google_compute_engine'), 
                                               '-C', 'gus', '-N', ''], 
                                              capture_output=True, text=True)
                    if key_result.returncode == 0:
                        print('SSH key pair generated successfully.')
                    else:
                        print(f'Error generating SSH key: {key_result.stderr}')
                        input('\nPress enter to get back to the compute engine menu: ')
                        compute_engine_module()
                        return
                else:
                    print('\nSSH key generation cancelled.')
                    input('\nPress enter to get back to the compute engine menu: ')
                    compute_engine_module()
                    return
            
            # Read the public key
            try:
                with open(ssh_key_path, 'r') as key_file:
                    public_key = key_file.read().strip()
                print(f'\nSSH public key found: {ssh_key_path}')
                print(f'Key preview: {public_key[:50]}...')
            except Exception as e:
                print(f'\nError reading SSH key: {e}')
                input('\nPress enter to get back to the compute engine menu: ')
                compute_engine_module()
                return
            
            # Confirm SSH key addition
            print(f'\nReady to add SSH key to VM instance: {vm_name}')
            confirm = input('Do you want to proceed? (y/n): ')
            
            if confirm.lower() != 'y':
                print('\nSSH key addition cancelled.')
                input('\nPress enter to get back to the compute engine menu: ')
                compute_engine_module()
                return
            
            # Add SSH key to VM metadata
            print(f'\nAdding SSH key to VM instance {vm_name} in zone {vm_zone}...')
            ssh_metadata = f'gus:{public_key}'
            
            metadata_result = subprocess.run([
                'gcloud', 'compute', 'instances', 'add-metadata', vm_name,
                '--zone', vm_zone,
                '--metadata', f'ssh-keys={ssh_metadata}'
            ], capture_output=True, text=True)
            
            if metadata_result.returncode == 0:
                print(f'SSH key successfully added to VM instance: {vm_name}')
                print('\nYou can now connect to the VM using:')
                print(f'  gcloud compute ssh gus@{vm_name} --zone={vm_zone}')
                external_ip = 'N/A'
                network_interfaces = selected_vm.get('networkInterfaces', [])
                if network_interfaces:
                    access_configs = network_interfaces[0].get('accessConfigs', [])
                    if access_configs:
                        external_ip = access_configs[0].get('natIP', 'N/A')
                if external_ip != 'N/A':
                    print(f'  ssh -i ~/.ssh/google_compute_engine gus@{external_ip}')
                else:
                    print('  ssh -i ~/.ssh/google_compute_engine gus@<EXTERNAL_IP> (no external IP found)')
            else:
                print(f'Error adding SSH key: {metadata_result.stderr}')
            
            # Log the operation
            now = datetime.now()
            with open(gcp_system_log_file, 'a') as logfile:
                logfile.write(str(now) + f" - Executed SSH key addition for VM: {vm_name}\n")
                logfile.close()
                
        except subprocess.CalledProcessError as e:
            print(f'Error fetching VM instances: {e.stderr}')
        except json.JSONDecodeError as e:
            print(f'Error parsing VM instance data: {e}')
        except Exception as e:
            print(f'Unexpected error: {e}')
        
        input('\nPress enter to get back to the compute engine menu: ')
        now = datetime.now()
        with open(gcp_system_log_file, 'a') as logfile:
            logfile.write(str(now) + " <-- Exited SSH KEY MANAGEMENT mode\n")
            logfile.close()
        compute_engine_module()

    print("*******************************************")
    print('          COMPUTE ENGINE MODULE           \n')
    print('1 - List zones')
    print('2 - List regions')
    print('3 - Show set region')
    print('4 - Change/set region')
    print('5 - Describe specific zone')
    print('6 - List running vms - os-instances')
    print('7 - Describe a vm instance - os-instance')
    print('8 - Find vm by name')
    print('9 - Find vm by image name')
    print('10 - List images')
    print('11 - SSH into vm only with vm name - simple mode')
    print('12 - SSH Key Management - List VMs and add SSH keys for authentication')
    print('13 - Create default VM instance/s - To create more than one separate strings by space')
    print('14 - Delete vm instance/s - To delete more than one separate strings by space' )
    print('15 - Create an instance template')
    print('16 - Delete an instance template')
    print('17 - Find an instance template')
    print('18 - List instance templates')
    print('19 - Describe an instance template')
    print('o - Operations menu - Lists and describes operations executed by users')
    print('a - > Advanced mode - requires more advanced knowledge')
    print('b - < Back to main menu')
    print('\n')
    compute_selection = input('Type a number or letter from the menu and press enter to operate: ')
    if compute_selection == '1':
        compute_zones()
    if compute_selection == '2':
        compute_regions_list()
    if compute_selection == '3':
        compute_regions_show()
    if compute_selection == "4":
        compute_regions_set()
    if compute_selection == '5':
        compute_zone_describe()
    if compute_selection == '6':
        compute_list_running_os_instances()
    if compute_selection == '7':
        compute_describe_runnning_os_instances()
    if compute_selection ==  '8':
        compute_zone_filter()
    if compute_selection == '9':
        compute_vm_name()
    if compute_selection == '10':
        compute_list_images()
    if compute_selection == '11':
        compute_ssh_vm_simple()
    if compute_selection == '12':
        compute_ssh_key_management()
    if compute_selection == '13':
        compute_create_vm_instance()
    if compute_selection == '14':
        compute_delete_vm_instance()
    if compute_selection == '15':
        compute_create_instance_template()
    if compute_selection == '16':
        compute_delete_instance_template()
    if compute_selection == '17':
        compute_find_instance_template()
    if compute_selection == '18':
        compute_list_instance_template()
    if compute_selection == '19':
        compute_describe_instance_template()
    if compute_selection == 'o':
        compute_operations_list_describe()
    if compute_selection == 'a':
        compute_advanced_module()
    if compute_selection == 'b':
        main_menu()
    else:
        input('\nInvalid option selected, you must type a number or letter from the menu. Press enter to get back to compute engine menu: ')
        compute_engine_module()

def update_gcloud():
    now=datetime.now()
    with open(gcp_system_log_file, 'a') as logfile:
        logfile.write(str(now)+" --> Accessed UPDATE GCLOUD menu\n")
        logfile.close()
    print('Mode U accesed. gcloud cli update\n')
    execute_gcloud_command_with_auth_check('gcloud components update', 
                          "Updating gcloud CLI components")
    input('\nPress enter to get back to the main menu: ')
    now = datetime.now()
    with open(gcp_system_log_file, 'a') as logfile:
        logfile.write(str(now) + " - Executed command: gcloud components update\n")
        logfile.close()
    now = datetime.now()
    with open(gcp_system_log_file, 'a') as logfile:
        logfile.write(str(now) + " <-- Exited UPDATE GCLOUD menu\n")
        logfile.close()
    main_menu()

def show_all_gcloud_commands():
    now = datetime.now()
    with open(gcp_system_log_file, 'a') as logfile:
        logfile.write(str(now) + " --> Accessed GCLOUD COMMANDS REFERENCE mode\n")
        logfile.close()
    
    print('=' * 80)
    print('                    GCLOUD COMMANDS REFERENCE')
    print('=' * 80)
    print()
    
    # Define all commands used in the program organized by sections
    commands_sections = {
        "PROJECT MANAGEMENT": [
            {
                "command": "gcloud beta billing projects describe [PROJECT_NAME]",
                "description": "Retrieve billing data for a specific project",
                "example": "gcloud beta billing projects describe my-project-123",
                "usage": "Use this to check billing account association and status for a project"
            },
            {
                "command": "gcloud projects describe [PROJECT_ID]",
                "description": "Get detailed information about a specific project",
                "example": "gcloud projects describe my-project-123",
                "usage": "Shows project metadata, creation time, labels, and lifecycle state"
            },
            {
                "command": "gcloud projects list",
                "description": "List all projects in your Google Cloud account",
                "example": "gcloud projects list",
                "usage": "View all accessible projects with their IDs, names, and numbers"
            },
            {
                "command": "gcloud config get-value project",
                "description": "Get the currently active project",
                "example": "gcloud config get-value project",
                "usage": "Returns the project ID that gcloud commands will target by default"
            },
            {
                "command": "gcloud config set project [PROJECT_ID]",
                "description": "Set the active project for gcloud commands",
                "example": "gcloud config set project my-project-123",
                "usage": "Changes the default project for all subsequent gcloud operations"
            }
        ],
        
        "AUTHENTICATION & CONFIGURATION": [
            {
                "command": "gcloud auth login",
                "description": "Authenticate with Google Cloud using browser-based login",
                "example": "gcloud auth login",
                "usage": "Opens browser to authenticate with your Google account"
            },
            {
                "command": "gcloud auth login [ACCOUNT]",
                "description": "Login with a specific Google account",
                "example": "gcloud auth login user@example.com",
                "usage": "Authenticate using a specific Google account email"
            },
            {
                "command": "gcloud auth login --login-config=[CONFIG_FILE]",
                "description": "Login using a workforce pool configuration file",
                "example": "gcloud auth login --login-config=login.json",
                "usage": "Corporate/enterprise login using workforce identity federation"
            },
            {
                "command": "gcloud config configurations list",
                "description": "List all gcloud configuration profiles",
                "example": "gcloud config configurations list",
                "usage": "Shows all configured profiles with account and project settings"
            },
            {
                "command": "gcloud config list account --format \"value(core.account)\"",
                "description": "Get the currently active account",
                "example": "gcloud config list account --format \"value(core.account)\"",
                "usage": "Returns just the email of the currently authenticated account"
            },
            {
                "command": "gcloud config set account [ACCOUNT]",
                "description": "Set the active account for gcloud commands",
                "example": "gcloud config set account user@example.com",
                "usage": "Switch between multiple authenticated accounts"
            },
            {
                "command": "gcloud init",
                "description": "Initialize gcloud configuration with guided setup",
                "example": "gcloud init",
                "usage": "Interactive setup for authentication, project, and region selection"
            }
        ],
        
        "COMPUTE ENGINE - REGIONS & ZONES": [
            {
                "command": "gcloud compute regions list",
                "description": "List all available compute regions",
                "example": "gcloud compute regions list",
                "usage": "Shows all Google Cloud regions with their quotas and status"
            },
            {
                "command": "gcloud compute zones list",
                "description": "List all available compute zones",
                "example": "gcloud compute zones list",
                "usage": "Shows all zones within regions, their status, and maintenance windows"
            },
            {
                "command": "gcloud config list compute/region",
                "description": "Show the currently configured compute region",
                "example": "gcloud config list compute/region",
                "usage": "Display the default region for compute operations"
            },
            {
                "command": "gcloud config set compute/region [REGION]",
                "description": "Set the default compute region",
                "example": "gcloud config set compute/region us-central1",
                "usage": "Configure default region for compute instances and resources"
            },
            {
                "command": "gcloud compute zones describe [ZONE] --format \"[box]\"",
                "description": "Get detailed information about a specific zone",
                "example": "gcloud compute zones describe us-central1-a --format \"[box]\"",
                "usage": "Shows zone status, available machine types, and maintenance info"
            }
        ],
        
        "COMPUTE ENGINE - INSTANCES": [
            {
                "command": "gcloud compute instances list",
                "description": "List all VM instances in the project",
                "example": "gcloud compute instances list",
                "usage": "Shows all VMs with names, zones, machine types, and status"
            },
            {
                "command": "gcloud compute instances list --filter=\"name=[VM_NAME]\" --format \"[box]\"",
                "description": "Find a specific VM instance by name",
                "example": "gcloud compute instances list --filter=\"name=my-vm\" --format \"[box]\"",
                "usage": "Search for VMs matching a specific name pattern"
            },
            {
                "command": "gcloud compute instances create [INSTANCE_NAME] --zone=[ZONE]",
                "description": "Create a new VM instance with default settings",
                "example": "gcloud compute instances create my-vm --zone=northamerica-northeast1-a",
                "usage": "Creates a standard VM with default machine type and boot disk"
            },
            {
                "command": "gcloud compute instances create [NAME] --image-family=[FAMILY] --image-project=[PROJECT] --machine-type=[TYPE]-custom-[CPUS]-[RAM]",
                "description": "Create a custom VM instance with specific configuration",
                "example": "gcloud compute instances create my-vm --image-family=ubuntu-2004-lts --image-project=ubuntu-os-cloud --machine-type=n1-custom-4-8192",
                "usage": "Create VM with custom CPU, RAM, and OS image specifications"
            },
            {
                "command": "gcloud compute instances delete [INSTANCE_NAME] --zone=[ZONE] --quiet",
                "description": "Delete VM instances without confirmation prompt",
                "example": "gcloud compute instances delete my-vm --zone=northamerica-northeast1-a --quiet",
                "usage": "Permanently removes VM instances and their boot disks"
            },
            {
                "command": "gcloud compute ssh [INSTANCE_NAME]",
                "description": "SSH into a VM instance (simple mode)",
                "example": "gcloud compute ssh my-vm",
                "usage": "Connect to VM using gcloud's built-in SSH with key management"
            },
            {
                "command": "gcloud compute ssh [USER]@[INSTANCE] --zone [ZONE] --project [PROJECT]",
                "description": "SSH with advanced parameters",
                "example": "gcloud compute ssh john@my-vm --zone us-central1-a --project my-project",
                "usage": "Connect to VM with specific user, zone, and project parameters"
            },
            {
                "command": "gcloud compute instances os-inventory list-instances",
                "description": "List running VM instances with OS inventory",
                "example": "gcloud compute instances os-inventory list-instances",
                "usage": "Shows VMs with detailed OS and software inventory information"
            },
            {
                "command": "gcloud compute instances os-inventory describe [INSTANCE]",
                "description": "Get detailed OS inventory for a specific VM",
                "example": "gcloud compute instances os-inventory describe my-vm",
                "usage": "Shows installed packages, OS version, and system details"
            }
        ],
        
        "COMPUTE ENGINE - IMAGES & TEMPLATES": [
            {
                "command": "gcloud compute images list",
                "description": "List all available compute images",
                "example": "gcloud compute images list",
                "usage": "Shows public and custom images available for VM creation"
            },
            {
                "command": "gcloud compute images list --filter=\"name=[IMAGE_NAME]\" --format \"[box]\"",
                "description": "Find specific compute images by name",
                "example": "gcloud compute images list --filter=\"name=ubuntu\" --format \"[box]\"",
                "usage": "Search for images matching a specific name pattern"
            },
            {
                "command": "gcloud compute instance-templates create [TEMPLATE_NAME]",
                "description": "Create an instance template",
                "example": "gcloud compute instance-templates create my-template",
                "usage": "Define reusable VM configuration for managed instance groups"
            },
            {
                "command": "gcloud compute instance-templates delete [TEMPLATE_NAME]",
                "description": "Delete an instance template",
                "example": "gcloud compute instance-templates delete my-template",
                "usage": "Remove template definition (does not affect running instances)"
            },
            {
                "command": "gcloud compute instance-templates list",
                "description": "List all instance templates",
                "example": "gcloud compute instance-templates list",
                "usage": "Shows all template configurations available in the project"
            },
            {
                "command": "gcloud compute instance-templates describe [TEMPLATE_NAME]",
                "description": "Get detailed information about an instance template",
                "example": "gcloud compute instance-templates describe my-template",
                "usage": "Shows complete template configuration including machine type and disks"
            }
        ],
        
        "COMPUTE ENGINE - OPERATIONS": [
            {
                "command": "gcloud compute operations list --filter=\"user=[USERNAME]\" --format=json",
                "description": "List compute operations by user in JSON format",
                "example": "gcloud compute operations list --filter=\"user=john@example.com\" --format=json",
                "usage": "Get detailed operation history for auditing and troubleshooting"
            },
            {
                "command": "gcloud compute operations list --filter=\"user=[USERNAME]\"",
                "description": "List compute operations by user in text format",
                "example": "gcloud compute operations list --filter=\"user=john@example.com\"",
                "usage": "View operation history in human-readable table format"
            },
            {
                "command": "gcloud compute operations describe [OPERATION_NAME]",
                "description": "Get detailed information about a specific operation",
                "example": "gcloud compute operations describe operation-1234567890123-abcd",
                "usage": "Shows operation status, progress, errors, and resource details"
            }
        ],
        
        "ORGANIZATIONS": [
            {
                "command": "gcloud organizations list",
                "description": "List all organizations you have access to",
                "example": "gcloud organizations list",
                "usage": "Shows organization IDs, display names, and lifecycle state"
            }
        ],
        
        "SYSTEM MANAGEMENT": [
            {
                "command": "gcloud components update",
                "description": "Update gcloud CLI components to the latest version",
                "example": "gcloud components update",
                "usage": "Updates core gcloud tools and installed components"
            },
            {
                "command": "gcloud alpha interactive",
                "description": "Start interactive gcloud shell with auto-completion",
                "example": "gcloud alpha interactive",
                "usage": "Interactive shell with command suggestions and help"
            }
        ]
    }
    
    # Display all commands by section
    for section, commands in commands_sections.items():
        print(f"📋 {section}")
        print("=" * len(f"📋 {section}"))
        print()
        
        for cmd_info in commands:
            print(f"🔧 COMMAND: {cmd_info['command']}")
            print(f"📖 DESCRIPTION: {cmd_info['description']}")
            print(f"💡 EXAMPLE: {cmd_info['example']}")
            print(f"🎯 USAGE: {cmd_info['usage']}")
            print("-" * 60)
            print()
    
    print("=" * 80)
    print("                    END OF COMMANDS REFERENCE")
    print("=" * 80)
    
    input('\nPress enter to get back to the main menu: ')
    now = datetime.now()
    with open(gcp_system_log_file, 'a') as logfile:
        logfile.write(str(now) + " <-- Exited GCLOUD COMMANDS REFERENCE mode\n")
        logfile.close()
    main_menu()

def global_help():
    now = datetime.now()
    with open(gcp_system_log_file, 'a') as logfile:
        logfile.write(str(now) + " --> Accessed GLOBAL HELP mode\n")
        logfile.close()
    
    print('=' * 80)
    print('                    GCP PYTHON INTERACTIVE CLI - GLOBAL HELP')
    print('=' * 80)
    print()
    
    print("🚀 PROGRAM OVERVIEW")
    print("=" * 40)
    print("This interactive CLI tool provides a user-friendly interface for Google Cloud")
    print("Platform (GCP) operations. It organizes gcloud commands into logical sections")
    print("and provides guided workflows for common cloud management tasks.")
    print()
    print("✨ KEY FEATURES:")
    print("• Project and billing management")
    print("• Account authentication and switching") 
    print("• Compute Engine VM operations")
    print("• Comprehensive logging and audit trails")
    print("• Advanced scripting capabilities")
    print("• Operations tracking and analysis")
    print()
    
    print("📋 MAIN MENU GUIDE")
    print("=" * 40)
    print()
    
    sections_help = {
        "PROJECT MANAGEMENT (Options 1-7)": {
            "description": "Core project operations for GCP resource management",
            "options": [
                "1️⃣  Billing Data: Check project billing account associations and status",
                "2️⃣  Project Info: Get detailed metadata about specific projects", 
                "3️⃣  Configurations: View all configured gcloud profiles and settings",
                "4️⃣  Active Project: Display currently selected default project",
                "5️⃣  Set Project: Change the active project for operations",
                "6️⃣  List Projects: View all accessible projects in your account",
                "7️⃣  Organizations: List organization resources you can access"
            ],
            "usage": "Start here to set up your project context before other operations"
        },
        
        "AUTHENTICATION (Option L)": {
            "description": "Account management and authentication workflows",
            "options": [
                "🔐 Multiple login methods: Google accounts, workforce pools, corporate SSO",
                "👤 Account switching between multiple authenticated users", 
                "⚙️  Configuration management for different environments",
                "🔧 Property management for workforce identity federation"
            ],
            "usage": "Use when switching between accounts or setting up authentication"
        },
        
        "COMPUTE ENGINE (Option C)": {
            "description": "Complete VM and infrastructure management suite",
            "submenu_sections": {
                "Basic Operations (1-10)": [
                    "Zone/Region management and configuration",
                    "VM instance discovery and listing",
                    "Image catalog browsing and search"
                ],
                "VM Management (11-19)": [
                    "SSH connectivity with key management",
                    "Instance creation with default settings", 
                    "Instance deletion and cleanup",
                    "Template creation for scaling"
                ],
                "Advanced Features": [
                    "🔧 Operations Menu (O): Audit trails and operation tracking",
                    "🎓 Advanced Mode (A): Custom VM creation with detailed specs",
                    "🔑 SSH Key Management: Automated key provisioning"
                ]
            },
            "usage": "Primary interface for all VM and compute operations"
        },
        
        "SYSTEM TOOLS": {
            "description": "Maintenance, logging, and advanced functionality", 
            "options": [
                "🔄 Update (U): Keep gcloud CLI components current",
                "📊 System Logs (S): View program activity and audit trails", 
                "🎯 Test Cases (T): Build and execute custom test scenarios",
                "💻 Free Input (F): Direct gcloud command execution",
                "🔬 Interactive (A): Alpha gcloud shell with auto-completion"
            ],
            "usage": "Maintenance tasks and advanced scripting operations"
        }
    }
    
    for section, info in sections_help.items():
        print(f"📂 {section}")
        print("-" * len(f"📂 {section}"))
        print(f"📖 {info['description']}")
        print()
        
        if 'options' in info:
            for option in info['options']:
                print(f"   {option}")
            print()
        
        if 'submenu_sections' in info:
            for subsection, items in info['submenu_sections'].items():
                print(f"   📋 {subsection}:")
                for item in items:
                    print(f"      • {item}")
                print()
        
        print(f"💡 USAGE: {info['usage']}")
        print()
        print("-" * 60)
        print()
    
    print("🔧 SPECIAL FEATURES GUIDE")
    print("=" * 40)
    print()
    
    features_guide = {
        "LOGGING SYSTEM": {
            "description": "All operations are automatically logged with timestamps",
            "features": [
                "📝 System event logging in gcp_system_log.log",
                "🔍 Operation-specific logs in compute_operations_logs/",
                "🔎 Regex search capabilities across all log files",
                "🗑️  Log cleanup and management tools"
            ],
            "usage": "Monitor program usage and troubleshoot issues"
        },
        
        "OPERATIONS TRACKING": {
            "description": "Detailed audit trails for compute operations",
            "features": [
                "👤 User-based operation filtering",
                "📊 JSON and text format exports",
                "🔍 Log file search and analysis",
                "📅 Timestamp-based organization"
            ],
            "usage": "Compliance, auditing, and operations analysis"
        },
        
        "ADVANCED SSH MANAGEMENT": {
            "description": "Automated SSH key provisioning and management",
            "features": [
                "🔑 Automatic SSH key generation",
                "📋 VM listing with network details",
                "⚡ One-click key deployment to instances",
                "🔧 Both gcloud and direct SSH connection options"
            ],
            "usage": "Streamlined VM access without manual key management"
        }
    }
    
    for feature, info in features_guide.items():
        print(f"⚡ {feature}")
        print("-" * len(f"⚡ {feature}"))
        print(f"📖 {info['description']}")
        print()
        
        for item in info['features']:
            print(f"   {item}")
        print()
        
        print(f"💡 USAGE: {info['usage']}")
        print()
        print("-" * 60)
        print()
    
    print("🎯 WORKFLOW RECOMMENDATIONS")
    print("=" * 40)
    print()
    print("🏁 GETTING STARTED:")
    print("   1. Start with option 'L' to authenticate")
    print("   2. Use option '4' to verify your active project")
    print("   3. Set correct project with option '5' if needed")
    print("   4. Access Compute Engine (C) for VM operations")
    print()
    print("🔧 TYPICAL VM WORKFLOW:")
    print("   1. Check regions/zones (Compute → 1,2)")
    print("   2. Set appropriate region (Compute → 4)")
    print("   3. List existing VMs (Compute → 6)")
    print("   4. Create new VMs (Compute → 13)")
    print("   5. Setup SSH access (Compute → 12)")
    print("   6. Connect to VMs (Compute → 11)")
    print()
    print("📊 MONITORING & MAINTENANCE:")
    print("   1. Review system logs regularly (S)")
    print("   2. Check operations audit trails (Compute → O)")
    print("   3. Update gcloud components (U)")
    print("   4. Clean up old log files as needed")
    print()
    
    print("⚠️  IMPORTANT NOTES")
    print("=" * 40)
    print("🔐 SECURITY:")
    print("   • All operations require proper GCP authentication")
    print("   • SSH keys are generated securely with proper permissions")
    print("   • Operations are logged for audit compliance")
    print()
    print("💰 COST AWARENESS:")
    print("   • VM creation incurs compute charges")
    print("   • Always delete unused instances to avoid costs")
    print("   • Monitor billing through option '1'")
    print()
    print("🛠️  TROUBLESHOOTING:")
    print("   • Check system logs (S) for error details")
    print("   • Verify authentication with configuration list (3)")
    print("   • Use interactive mode (A) for command debugging")
    print("   • Operations menu (Compute → O) shows detailed command history")
    print()
    
    print("=" * 80)
    print("                    END OF GLOBAL HELP")
    print("=" * 80)
    
    input('\nPress enter to get back to the main menu: ')
    now = datetime.now()
    with open(gcp_system_log_file, 'a') as logfile:
        logfile.write(str(now) + " <-- Exited GLOBAL HELP mode\n")
        logfile.close()
    main_menu()

def system_logs_events():
    now=datetime.now()
    with open(gcp_system_log_file, 'a') as logfile:
        logfile.write(str(now)+" --> Accessed SYSTEM LOG FILE menu\n")
        logfile.close()
    gcp_logs_file='gcp_system_log.log'  # System event log file var
    print('Mode S accesed. System and events loger\n')
    print('************************************************\n')
    print('           GCP CLI EVENT LOGGING MODE           \n')
    print('1 - View system and events log file ')
    print('2 - Find regular expresion in the logs file')
    print('3 - Delete the log file')
    print('b - < Back to main menu')
    system_log_select=input("\nType an option from the menu and press enter: ")
    if system_log_select=="1":
        now=datetime.now()
        with open(gcp_system_log_file, 'a') as logfile:
            logfile.write(str(now)+" --> Accessed SYSTEM LOG FILE Viewing mode. You are now viewing the logs file\n")
            logfile.close()
        input('\nGCP cli log file viewing mode accessed. Press enter to view the log file: \n')
        openfile = open(gcp_logs_file, 'r')
        print(openfile.read())
        openfile.close()
        input('\nPress enter to get back to the main menu: ')
        now=datetime.now()
        with open(gcp_system_log_file, 'a') as logfile:
            logfile.write(str(now)+" <-- Exited SYSTEM LOG FILE Viewing mode. You are now viewing the logs file\n")
            logfile.close()
    if system_log_select=="2":
        now=datetime.now()
        with open(gcp_system_log_file, 'a') as logfile:
            logfile.write(str(now)+" --> Accessed SYSTEM LOG FILE Regexp mode. You are now viewing the logs file\n")
            logfile.close()
        regexp=input("\nPlease type the regular expresion you want to find in the log file: ")
        print("\nShowing regexp: '"+regexp+"', in logfile file: "+'\n')
        with open(gcp_system_log_file, 'a') as logfile:
            logfile.write(str(now)+" ? - Searched for regexp: "+"'"+regexp+"'"+" in system logfile"+"\n")
            logfile.close()
        with open(gcp_logs_file, 'r') as filedata:     # Opening the given file in read-only mode
           for line in filedata:
                if regexp in line:
                    print(line)
        filedata.close()
        input('\nPress enter to get back to the main menu: ')
        now=datetime.now()
        with open(gcp_system_log_file, 'a') as logfile:
            logfile.write(str(now)+" <-- Exited SYSTEM LOG FILE Regexp mode.\n")
            logfile.close()
        system_logs_events()
    if system_log_select=="3":
        def delete_log_file():
            now=datetime.now()
            with open(gcp_system_log_file, 'a') as logfile:
                logfile.write(str(now)+" --> Accessed SYSTEM LOG FILE DELETION mode. You are now viewing the logs file\n")
                logfile.close()
            delete_logfile=input("\nWARNING: You are about to delete the GCP cli logs and events from the system. Proceed?. y/n?: ")
            if delete_logfile=="y":
                print("\nRemoving the "+gcp_logs_file+" log file from the system...")
                os.remove(gcp_logs_file)
                input('\nPress enter to get back to the main menu: ')
                now=datetime.now()
                with open(gcp_system_log_file, 'a') as logfile:
                    logfile.write(str(now)+" <-- Exited SYSTEM LOG FILE DELETION mode\n")
                    logfile.close()
                system_logs_events()
            if delete_logfile=="n":
                print("\nYou decided not to delete the log file from the system.")
                input('\nPress enter to get back to the main menu: ')
                with open(gcp_system_log_file, 'a') as logfile:
                    logfile.write(str(now)+" <-- Exited SYSTEM LOG FILE DELETION mode\n")
                    logfile.close()
                system_logs_events()
            else:
                input("\nOnly type either 'y' or 'n'. Press enter to get back to the prompt: ")
                delete_log_file()
        delete_log_file()
    if system_log_select=="b":
        now=datetime.now()
        with open(gcp_system_log_file, 'a') as logfile:
            logfile.write(str(now)+" <-- Exited SYSTEM LOG FILE menu\n")
            logfile.close()
        main_menu()
    else:
        system_logs_events()

def main_menu():
    now=datetime.now()
    global gcp_system_log_file
    gcp_system_log_file='gcp_system_log.log'
    with open(gcp_system_log_file, 'a') as logfile:
        logfile.write(str(now)+" --> Accessed GCP PYTHON TESTING CONSOLE main menu\n")
        logfile.close()
    print("*******************************************")
    print('        GCP PYTHON TESTING CONSOLE         \n')
    print('WELCOME, YOU ARE IN THE MAIN MENU\n')
    print('1 - Retrieve billing data for a project')
    print('2 - Describe a project')
    print('3 - Get configuration list - Lists account name and project data')
    print('4 - Get active project')
    print('5 - Set a project')
    print('6 - Get a list of all projects')
    print('7 - Get a list of all organizations')
    print('l - Login/switch account')
    print('a - Interactive alpha gcloud command line')
    print('u - Update gcloud console components')
    print('c - Compute module')
    print('t - Test case builder')
    print('f - Free command line input - advanced script module. Requires knowledge on gcloud cli.')
    print('s - System logs and events mode')
    print('r - Show all gcloud commands reference with examples and usage')
    print('h - Global help - Program guide and workflow instructions')
    print('\n')
    selection=input('Type a number or letter from the menu and press enter to operate: ')
    if selection == '1':
        check_billing_project()
    if selection == '2':
        describe_specific_project()
    if selection == '3':
        get_cconfigurations_list()
    if selection == '4':
        get_active_project()
    if selection == '5':
        set_project()
    if selection == '6':
        get_all_projects()
    if selection == '7':
        get_all_organizations()
    if selection == 'a':
        alpha_interactive_cli()
    if selection == 't':
        test_case_module_menu()
    if selection == 'c':
        compute_engine_module()
    if selection == 'u':
        update_gcloud()
    if selection == 'l':
        login_account()
    if selection == 'f':
        free_command_input_menu()
    if selection == 's':
        system_logs_events()
    if selection == 'r':
        show_all_gcloud_commands()
    if selection == 'h':
        global_help()
    else:
         #input('\nInvalid option selected, you must type a number or letter from the menu. Press enter to get back to main menu: ')
         main_menu()

main_menu()
