import os
import sys

def interactive_sign_in():
    #Interactive gcloud login
    global LOGIN_CONFIG_FILE
    WORKFORCE_POOL_ID=input("\nPlease type the name of the workforce pool and provider ID: ")
    LOGIN_CONFIG_FILE=input('\nProvide a name for the login configuration file (example: login.json): ')
    global_var='gcloud iam workforce-pools create-login-config '+WORKFORCE_POOL_ID+' --output-file='+LOGIN_CONFIG_FILE+' --activate'
    print('\nCreating sign in config file...\n')
    os.system(global_var)
    print('\nReading created file '+LOGIN_CONFIG_FILE+' metadata: \n')
    with open(LOGIN_CONFIG_FILE, 'r') as filedata:  # Opening the given file in read-only mode
        for line in filedata:
                print(line)
    filedata.close()
    input('\nPress enter to proceed to the main menu: ')
    main_login_set_unset_property_menu()

def proceed_to_login():
    EXISTING_LOGIN_CONFIG_FILE = input('\nProvide an existing valid name to log in to you provider and press enter: ')
    pwd_path=os.getcwd()
    gcloud_auth_login_var = 'gcloud auth login --login-config='
    if EXISTING_LOGIN_CONFIG_FILE == "":
        input('\nNothing was typed. Press enter to retry...')
        proceed_to_login()
    if os.path.isfile(EXISTING_LOGIN_CONFIG_FILE):
        print("\nFile " + EXISTING_LOGIN_CONFIG_FILE + " was found...")
        os.system('\n' + gcloud_auth_login_var + EXISTING_LOGIN_CONFIG_FILE)
        print("\nShowing active account: ")
        os.system('\ngcloud config list account --format "value(core.account)"')
        input('\nPress enter to proceed to the main menu: ')
        main_login_set_unset_property_menu()
    else:
        print("\nFile "+EXISTING_LOGIN_CONFIG_FILE+" not found")
        print('\nUnable to login. Retry again generating a new one.')
        input('\nPress enter to proceed to the main menu: ')
        main_login_set_unset_property_menu()

def set_property():
    set_prop_var='gcloud config set auth/login_config_file '+LOGIN_CONFIG_FILE
    print('\nSetting property based on '+LOGIN_CONFIG_FILE+' ...')
    os.system(set_prop_var)
    input('\nPress enter to proceed to the main menu: ')
    main_login_set_unset_property_menu()

def unset_property():
    unset_prop_var = 'gcloud config unset auth/login_config_file '
    print('\nUnsetting property based on ' + LOGIN_CONFIG_FILE+' ...')
    os.system(unset_prop_var)
    input('\nPress enter to proceed to the main menu: ')
    main_login_set_unset_property_menu()

def gcloud_init():
    input('\nPress enter to init gcloud now: ')
    gcloud_init = '\ngcloud init'
    os.system(gcloud_init)
    input('\nPress enter to proceed to the main menu: ')
    main_login_set_unset_property_menu()

def gcloud_auth():
    input('\nPress enter to run gcloud auth login: ')
    gcloud_auth='\ngcloud auth login'
    os.system(gcloud_auth)
    input('\nPress enter to proceed to the main menu: ')
    main_login_set_unset_property_menu()

def main_login_set_unset_property_menu():
    print('\n###########################################################\n')
    print('GCP short-lived tokens for workforce identity federation. \n')
    print(' a - Run gcloud auth login')
    print(' i - Initiate gcloud - gcloud init')
    print(' g - Generate config file based on workforce pool provider')
    print(' l - Log in to your provider, by providing an existing valid config file')
    print(' s - To set the property to use the config file')
    print(' u - To unset the property')
    print(' x - To terminate this program')
    selection=input('\nPlease provide a valid option from the menu to operate: ')
    if selection=="i":
        gcloud_init()
    if selection=="a":
        gcloud_auth()
    if selection=="g":
        interactive_sign_in()
    if selection=="l":
        proceed_to_login()
    if selection=="s":
        set_property()
    if selection=="u":
        unset_property()
    if selection=="x":
        sys.exit(0)
    else:
        main_login_set_unset_property_menu()

main_login_set_unset_property_menu()

