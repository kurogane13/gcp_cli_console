import os
import runpy
import sys
import datetime
from datetime import datetime

now=datetime.now()

def test_case_module_menu():
    from gcp_test_case_cli import test_case_module
    test_case_module()
def free_command_input_menu():
    from gcp_cli_input_scripts import free_command_input
    free_command_input()

gcp_scripts_dir='gcp_automation_test_scripts'
os.system('mkdir -p '+gcp_scripts_dir)

byoid_project='byoid-ui-testing-project'

def check_billing_byoid():

    print('- Mode 1 accessed.\n')
    print("Retrieving billing data for project name: "+byoid_project+'\n')
    os.system('gcloud beta billing projects describe '+byoid_project)
    input('\nOperation executed. Press enter to get back to main menu: ')
    main_menu()

def check_billing_project():

    print('- Mode 2 accessed.\n')
    project_name=input('Provide a valid project name and press enter: ')
    print("\nRetrieving billing data for project name: "+project_name+'\n')
    os.system('gcloud beta billing projects describe '+project_name)
    input('\nOperation executed. Press enter to get back to main menu: ')
    main_menu()

def describe_byoid_project():
    print('- Mode 3 Accessed\n')
    print('Describing project: '+byoid_project)
    os.system('gcloud projects describe '+byoid_project)
    input('\nOperation executed. Press enter to get back to main menu: ')
    main_menu()

def describe_specific_project():
    print('- Mode 4 Accessed\n')
    project_to_describe=input('Type a project name to describe it: ')
    os.system('gcloud projects describe '+project_to_describe)
    input('\nOperation executed. Press enter to get back to main menu: ')
    main_menu()

def get_cconfigurations_list():
    print('- Mode 5 Accessed\n')
    print('Getting configuration list...\n')
    os.system('gcloud config configurations list')
    input('\nOperation executed. Press enter to get back to main menu: ')
    main_menu()

def get_active_project():
    print('- Mode 6 accessed.\n')
    print('Active project is: \n')
    os.system('gcloud config get-value project')
    input('\nOperation executed. Press enter to get back to main menu: ')
    main_menu()

def set_byoid():
    print('- Mode 7 accessed.\n')
    print("\nSetting up project: "+byoid_project+'\n')
    os.system('gcloud config set project '+byoid_project)
    input('\nOperation executed. Press enter to get back to main menu: ')
    main_menu()

def set_project():
    print('- Mode 8 accessed.\n')
    project_name=input('Provide a valid project name to set up, and press enter: ')
    print("\nSetting up project: "+project_name+'\n')
    os.system('gcloud config set project '+project_name)
    input('\nOperation executed. Press enter to get back to main menu: ')
    main_menu()

def get_all_projects():
    print('- Mode 9 accessed.\n')
    print('Listing all projects....\n')
    os.system('gcloud projects list')
    input('\nOperation executed. Press enter to get back to main menu: ')
    main_menu()

def get_all_organizations():
    print('- Mode 10 accessed.\n')
    print('Listing all organizations....\n')
    os.system('gcloud organizations list')
    input('\nOperation executed. Press enter to get back to main menu: ')
    main_menu()

def alpha_interactive_cli():
    print('Mode A accessed.\n')
    print("You have accessed the alpha gcloud cli interactive mode. Once inside the console, to exit, type exit and enter.")
    input("\nPress enter to access the interactive console now:  ")
    os.system('gcloud alpha interactive')
    input('\nPress enter to get back to the main menu: ')
    main_menu()

def login_account():
    print('Mode L accessed.\n')
    print('\nAccount login/switch mode.\n')
    def account_types():
        print('\n- a - Show active logged in account')
        print('- g - To login with a corporate GOOGLE account')
        print('- t - To login to OKTA THIRD PARTY account - byoid-ui-testing-project')
        print('- k - Set new token key for your OKTA THIRD PARTY account - byoid-ui-testing-project')
        print('- p - Log in directly to your third party account  - Must provide a valid ,json token key file name')
        print('- c - Set new token and log in to a provider/project')
        print('- s - Set active account')
        print('- b - < Back to main menu')
        selection=input('\nType an option from the menu and press enter: ')
        if selection  == 'a':
            input('\nPress enter to view the current active account: ')
            print('\nThe current logged in set account is: \n')
            os.system('gcloud config list account --format "value(core.account)"')
            input('\nPress enter to get back to the main menu: ')
            account_types()
        if selection == 'g':
            account = input("\nPlease provide the name of the GOOGLE account you want to login with: ")
            os.system('gcloud auth login ' + account)
            input('\nPress enter to get back to the main menu: ')
            account_types()
        if selection ==  't':
            os.system('\ngcloud auth login --cred-file=config.json')
            print("\nShowing active account: ")
            os.system('gcloud config list account --format "value(core.account)"')
            input('\nPress enter to get back to the main menu: ')
            account_types()
        if selection == 'k':
            source_file=input('\nProvide a file name to save the token: ')
            paste_key=input('\nNow paste the key to write to the file: '+source_file+': ')
            global_var='gcloud iam workforce-pools create-cred-config locations/global/workforcePools/byoid-ui-test-pool/providers/okta-provider --subject-token-type=urn:ietf:params:oauth:token-type:id_token --credential-source-file='+source_file+" "+'--workforce-pool-user-project=byoid-ui-testing-project --output-file=config.json'
            try:
                with open(source_file, 'w') as file:
                    file.write(paste_key)
                    file.close()
                os.system(global_var)
                os.system('\ngcloud auth login --cred-file=config.json')
                print("\nShowing active account: ")
                os.system('gcloud config list account --format "value(core.account)"')
                input('\nPress enter to get back to the main menu: ')
                account_types()
            except:
                print('\nUnable to parse the provided data.  Please check that all the fields, and metadata was parsed correctly and retry.')
                account_types()
        if selection == 'c':
            print('\nLog in to specific provider project mode accessed: ')
            print('\nFor this mode you will need to provide the specific data:')
            print('\n - Workforce pool name')
            print(' - Workforce pool user project')
            print(' - Third party provider name')
            print(' - A file name (to save the token key)')
            print(' - Token key in string format')
            data=input('\nOnce you have gathered all the data, press enter to begin: ')
            workforce_pool_name=input('\nType the workforce pool name: ')
            workforce_user_project=input('\nType the workforce user project name: ')
            third_party_provider_name=input('\nType the  third party provider name: ')
            token_filename=input('\nProvide a token file name to save the key - NOTE: Do not type an extension: ')
            token_key=input('\nCopy and paste the token key in string format: ')
            input('\nOnce ready press enter to process the gathered data, and attempt to set the project: ')
            try:
                with open(token_filename, 'w') as file:
                    file.write(token_key)
                    file.close()
                global_var='gcloud iam workforce-pools create-cred-config locations/global/workforcePools/'+workforce_pool_name+'/providers/'+third_party_provider_name+' --subject-token-type=urn:ietf:params:oauth:token-type:id_token --credential-source-file='+token_filename+" "+'--workforce-pool-user-project='+workforce_user_project+' --output-file='+third_party_provider_name+'_config.json'
                os.system(global_var)
                os.system('\ngcloud auth login --cred-file='+third_party_provider_name+'_config.json')
                print("\nShowing active account: ")
                os.system('gcloud config list account --format "value(core.account)"')
                input('\nPress enter to get back to the main menu: ')
                account_types()
            except:
                print('\nUnable to parse the provided data. Please check that all the fields, and metadata was parsed correctly and retry.')
                account_types()
        if selection == 's':
            set_active_account=input("Provide the name of the account you want to set: ")
            os.system('gcloud config set account '+set_active_account)
            input('\nPress enter to get back to the main menu: ')
            account_types()
        if selection ==  'p':
            key_file_name=input('\nPlease provide a valid .json key file name to attempt to login to your account project: ')
            os.system('\ngcloud auth login --cred-file='+key_file_name)
            print("\nShowing active account: ")
            os.system('gcloud config list account --format "value(core.account)"')
            input('\nPress enter to get back to the main menu: ')
            account_types()
        if selection == 'b':
            input('\nYou decided to go back to the main menu. Press enter to get back there: ')
            main_menu()
        else:
            account_types()
    account_types()

def compute_engine_module():
    def compute_zones():
        now = datetime.now()
        with open(gcp_system_log_file, 'a') as logfile:
            logfile.write(str(now) + " --> Accessed COMPUTE ZONES LIST mode\n")
            logfile.close()
        print("\nCompute zones mode accessed.\n")
        print('Listing compute zones...  \n')
        os.system('gcloud compute zones list')
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
        os.system('\ngcloud compute zones describe '+describe_zone+box_format)
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
        os.system('\ngcloud compute instances os-inventory list-instances')
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
        os.system('\ngcloud compute instances os-inventory describe '+describe_running_os)
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
        os.system('gcloud compute images list')
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
        print('\nSSH vm simple mode accesed.\n')
        vm_name = input("Provide the Vm instance name to connect to: ")
        print("\nAttempting to connect to vm instance...")
        ssh_vm_instance_simple='gcloud compute ssh '+vm_name
        os.system(ssh_vm_instance_simple)
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
        os.system('gcloud compute instances create '+vm_instance_name+default_zone)
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
        os.system('gcloud compute instances delete '+vm_instance_name+delete_quiet)
        now = datetime.now()
        with open(gcp_system_log_file, 'a') as logfile:
            logfile.write(str(now) + " - Executed command: gcloud compute instances delete " + vm_instance_name + default_zone + "\n")
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
        os.system('gcloud compute instance-templates create '+instance_template_name_create)
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
        os.system('gcloud compute instance-templates delete '+instance_template_name_delete)
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
        os.system('gcloud compute instance-templates list')
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
        os.system('gcloud compute instance-templates list --filter="name='+instance_template_find_name+quote+' --format "[box]"')
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
        os.system('gcloud compute instance-templates describe '+instance_template_describe_name)
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
                                            os.system('gcloud compute instances create '+vm_name+' --image-family='+image_family+' --image-project='+image_project+' --machine-type='+machine_type+'-custom-'+cpus_amount+'-'+ram_amount)
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

    print("*******************************************")
    print('          COMPUTE ENGINE MODULE           \n')
    print('1 - List zones')
    print('2 - Describe specific zone')
    print('3 - List running vms - os-instances')
    print('4 - Describe a vm instance - os-instance')
    print('5 - Find vm by name')
    print('6 - Find vm by image name')
    print('7 - List images')
    print('8 - SSH into vm only with vm name - simple mode')
    print('9 - Create default VM instance/s - To create more than one separate strings by space')
    print('10 - Delete vm instance/s - To delete more than one separate strings by space' )
    print('11 - Create an instance template')
    print('12 - Delete an instance template')
    print('13 - Find an instance template')
    print('14 - List instance templates')
    print('15 - Describe an instance template')
    print('a - > Advanced mode - requires more advanced knowledge')
    print('b - < Back to main menu')
    print('\n')
    compute_selection = input('Type a number or letter from the menu and press enter to operate: ')
    if compute_selection == '1':
        compute_zones()
    if compute_selection == '2':
        compute_zone_describe()
    if compute_selection == '3':
        compute_list_running_os_instances()
    if compute_selection == '4':
        compute_describe_runnning_os_instances()
    if compute_selection ==  '5':
        compute_zone_filter()
    if compute_selection == '6':
        compute_vm_name()
    if compute_selection == '7':
        compute_list_images()
    if compute_selection == '8':
        compute_ssh_vm_simple()
    if compute_selection == '9':
        compute_create_vm_instance()
    if compute_selection == '10':
        compute_delete_vm_instance()
    if compute_selection == '11':
        compute_create_instance_template()
    if compute_selection == '12':
        compute_delete_instance_template()
    if compute_selection == '13':
        compute_find_instance_template()
    if compute_selection == '14':
        compute_list_instance_template()
    if compute_selection == '15':
        compute_describe_instance_template()
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
    os.system('gcloud components update')
    input('\nPress enter to get back to the main menu: ')
    main_menu()

def system_logs_events():
    now=datetime.now()
    with open(gcp_system_log_file, 'a') as logfile:
        logfile.write(str(now)+" --> Accessed SYSTEM LOG FILE menu\n")
        logfile.close()
    gcp_logs_file='gcp_system_log.log'
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
    print('1 - Retrieve billing data for default project: byoid-ui-testing-project')
    print('2 - Retrieve billing data for another project')
    print('3 - Describe project: '+byoid_project)
    print('4 - Describe specific project')
    print('5 - Get configuration list - Lists account name and project data')
    print('6 - Get active project')
    print('7 - Set project byoid-ui-testing-project')
    print('8 - Set another project')
    print('9 - Get a list of all projects')
    print('10 - Get a list of all organizations')
    print('l - Login/switch account')
    print('a - Interactive alpha gcloud command line')
    print('u - Update gcloud console components')
    print('c - Compute module')
    print('t - Test case builder')
    print('f - Free command line input - advanced script module. Requires knowledge on gcloud cli.')
    print('s - System logs and events mode')
    print('\n')
    selection=input('Type a number or letter from the menu and press enter to operate: ')
    if selection == '1':
        check_billing_byoid()
    if selection == '2':
        check_billing_project()
    if selection == '3':
        describe_byoid_project()
    if selection == '4':
        describe_specific_project()
    if selection == '5':
        get_cconfigurations_list()
    if selection == '6':
        get_active_project()
    if selection == '7':
        set_byoid()
    if selection == '8':
        set_project()
    if selection == '9':
        get_all_projects()
    if selection == '10':
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
    else:
         #input('\nInvalid option selected, you must type a number or letter from the menu. Press enter to get back to main menu: ')
         main_menu()

main_menu()
