import imp
import os
import runpy
import sys
import random
import importlib
from datetime import datetime

gcp_scripts_dir='gcp_automation_test_scripts'
os.system('mkdir -p gcp_automation_test_scripts')

def select_menu():
    print('\n- m - Main menu')
    print('- c - Compute engine menu')
    selector=input('\nType the option of the menu from which you want to add a test case: ')
    if selector=='m':
        create_case_main_menu()
    if selector=='c':
        create_case_compute_menu()

def add_another_step_main_menu():
    add_step_or_not=input("\nDo you want to add another step to this test case?. y/n: ")
    if add_step_or_not == "y":
        select_menu()
    if add_step_or_not == "n":
        input("\nYou decided not to add more steps for this test case. Press enter to get back to the test case module menu: ")
        test_case_module()
    else:
        input('\nInvalid input. Type either "y" or "n" and press enter.')
        add_another_step_main_menu()

def add_another_step_compute_menu():
    add_step_or_not = input("\nDo you want to add another step to this test case?. y/n: ")
    if add_step_or_not == "y":
        select_menu()
    if add_step_or_not == "n":
        input("\nYou decided not to add more steps for this test case. Press enter to get back to the test case module menu: ")
        test_case_module()
    else:
        input('\nInvalid input. Type either "y" or "n" and press enter.')
        add_another_step_main_menu()

def timestamp():
    now=datetime.now()
    print("\nTest case termination timestamp: "+str(now))

def create_case_main_menu():
    global new_line, quote, pyext, print_string, right_bracket, left_bracket, import_os_module, import_sys_module, os_system, space, plus, test_case_file_name, equals, colons, running
    new_line=('\n')
    quote="'"
    pyext=".py"
    print_string=("print")
    left_bracket="("
    right_bracket=")"
    os_system="os.system"
    import_os_module="import os"
    import_sys_module="import sys"
    space=" "
    plus="+"
    equals="="
    colon=":"
    dots="..."
    running="Running"
    carriage_return="\n"
    gcloud_billing_project_describe="gcloud beta billing projects describe "
    gcloud_projects_describe="gcloud projects describe "
    gcloud_config_configurations_list="gcloud config configurations list "
    gcloud_config_get_value_project="gcloud config get-value project "
    gcloud_config_set_project_byoid_project="gcloud config set project byoid-ui-testing-project"
    gcloud_config_set_project='gcloud config set project '
    gcloud_projects_list='gcloud projects list'
    gcloud_organizations_list='gcloud organizations list'
    #string_to_write=
    print("*******************************************")
    print('      GCP TEST CASE CREATION MAIN MENU   \n')
    print('1 - Retrieve billing data for default project: byoid-ui-testing-project')
    print('2 - Retrieve billing data for another project')
    print('3 - Describe project: byoid-ui-testing-project')
    print('4 - Describe specific project')
    print('5 - Get configuration list - Lists account name and project data')
    print('6 - Get active project')
    print('7 - Set project byoid-ui-testing-project')
    print('8 - Set another project')
    print('9 - Get a list of all projects')
    print('10 - Get a list of all organizations')
    print('b - < Back to test case module menu')
    selection=input('\nPlease provide the action item you want to add to the test case.\nType a number or letter from the menu and press enter to operate: ')
    if selection == '1':
        with open (gcp_scripts_dir+"/"+test_case_file_name+pyext, 'a') as file:
            def m1_build_python_case_file():
                step_string_var="step_string"
                step_string="Step: Main menu: - 1 - Retrieve billing data for default project: byoid-ui-testing-project"
                byoid_ui_testing_project="byoid-ui-testing-project"
                new_line=('\n')
                file.write(new_line+step_string_var+equals+quote+step_string+quote+new_line)
                file.write(print_string+left_bracket+quote+quote+right_bracket+new_line)
                file.write(print_string+left_bracket+quote+running+space+quote+plus+step_string_var+plus+quote+dots+quote+right_bracket+new_line)
                file.write('byoid_ui_testing_project='+quote+byoid_ui_testing_project+quote+new_line)
                file.write(print_string+left_bracket+quote+'Retrieving billing data for project name: '+quote+plus+'byoid_ui_testing_project'+right_bracket+new_line)
                file.write(os_system+left_bracket+quote+gcloud_billing_project_describe+quote+plus+'byoid_ui_testing_project'+right_bracket+new_line)
                file.close()
                print('\nAdded '+step_string)
            m1_build_python_case_file()
        add_another_step_main_menu()
    if selection == '2':
        with open (gcp_scripts_dir+"/"+test_case_file_name+pyext, 'a') as file:
            def m2_build_python_case_file():
                step_string_var="step_string"
                step_string="Step: Main menu: - 2 - Retrieve billing data for another project"
                project_name=input("\nProvide a valid project name to retrieve in the script: ")
                project_name_var="project_name"
                new_line=('\n')
                file.write(new_line+step_string_var+equals+quote+step_string+quote+new_line)
                file.write(print_string+left_bracket+quote+quote+right_bracket+new_line)
                file.write(print_string+left_bracket+quote+running+space+quote+plus+step_string_var+plus+quote+dots+quote+right_bracket+new_line)
                file.write(new_line+"project_name="+quote+project_name+quote+new_line)
                file.write(print_string+left_bracket+quote+'Retrieving billing data for project name: '+quote+plus+project_name_var+right_bracket+new_line)
                file.write(os_system+left_bracket+quote+gcloud_billing_project_describe+quote+plus+project_name_var+right_bracket+new_line)
                file.close()
                print('\nAdded '+step_string)
            m2_build_python_case_file()
        add_another_step_main_menu()
    if selection == '3':
        with open (gcp_scripts_dir+"/"+test_case_file_name+pyext, 'a') as file:
            def m3_build_python_case_file():
                step_string_var="step_string"
                step_string="Step: Main menu: - 3 - Describe project byoid-ui-testing-project"
                project_name_var="project_name"
                project_name="byoid-ui-testing-project"
                new_line=('\n')
                file.write(new_line+step_string_var+equals+quote+step_string+quote+new_line)
                file.write(print_string+left_bracket+quote+quote+right_bracket+new_line)
                file.write(print_string+left_bracket+quote+running+space+quote+plus+step_string_var+plus+quote+dots+quote+right_bracket+new_line)
                file.write(new_line+"project_name="+quote+project_name+quote+new_line)
                file.write(print_string+left_bracket+quote+'Describing project: '+quote+plus+project_name_var+right_bracket+new_line)
                file.write(os_system+left_bracket+quote+gcloud_projects_describe+quote+plus+project_name_var+right_bracket+new_line)
                file.close()
                print('\nAdded '+step_string)
            m3_build_python_case_file()
        add_another_step_main_menu()
    if selection == '4':
        with open (gcp_scripts_dir+"/"+test_case_file_name+pyext, 'a') as file:
            def m4_build_python_case_file():
                step_string_var="step_string"
                step_string="Step: Main menu: - 4 - Describe specific project"
                project_name=input("\nProvide a valid project name to describe in the script: ")
                project_name_var="project_name"
                new_line=('\n')
                file.write(new_line+step_string_var+equals+quote+step_string+quote+new_line)
                file.write(print_string+left_bracket+quote+quote+right_bracket+new_line)
                file.write(print_string+left_bracket+quote+running+space+quote+plus+step_string_var+plus+quote+dots+quote+right_bracket+new_line)
                file.write(new_line+project_name_var+equals+quote+project_name+quote+new_line)
                file.write(print_string+left_bracket+quote+'Describing project: '+quote+plus+project_name_var+right_bracket+new_line)
                file.write(os_system+left_bracket+quote+gcloud_projects_describe+quote+plus+project_name_var+right_bracket+new_line)
                file.close()
                print('\nAdded '+step_string)
            m4_build_python_case_file()
        add_another_step_main_menu()
    if selection == '5':
        with open (gcp_scripts_dir+"/"+test_case_file_name+pyext, 'a') as file:
            def m5_build_python_case_file():
                step_string_var="step_string"
                step_string="Step: Main menu: - 5 - Get configuration list - Lists account name and project data"
                new_line=('\n')
                file.write(new_line+step_string_var+equals+quote+step_string+quote+new_line)
                file.write(print_string+left_bracket+quote+quote+right_bracket+new_line)
                file.write(print_string+left_bracket+quote+running+space+quote+plus+step_string_var+plus+quote+dots+quote+right_bracket+new_line)
                file.write(print_string+left_bracket+quote+'Getting configuration list for project data: '+quote+right_bracket+new_line+new_line)
                file.write(os_system+left_bracket+quote+gcloud_config_configurations_list+quote+right_bracket+new_line)
                file.close()
                print('\nAdded '+step_string)
            m5_build_python_case_file()
        add_another_step_main_menu()
    if selection == '6':
        with open (gcp_scripts_dir+"/"+test_case_file_name+pyext, 'a') as file:
            def m6_build_python_case_file():
                step_string_var="step_string"
                step_string="Step: Main menu: - 6 - Get active project"
                new_line=('\n')
                file.write(new_line+step_string_var+equals+quote+step_string+quote+new_line)
                file.write(print_string+left_bracket+quote+quote+right_bracket+new_line)
                file.write(print_string+left_bracket+quote+running+space+quote+plus+step_string_var+plus+quote+dots+quote+right_bracket+new_line)
                file.write(print_string+left_bracket+quote+'Getting active project... '+quote+right_bracket+new_line+new_line)
                file.write(os_system+left_bracket+quote+gcloud_config_get_value_project+quote+right_bracket+new_line)
                file.close()
                print('\nAdded '+step_string)
            m6_build_python_case_file()
        add_another_step_main_menu()
    if selection == '7':
        with open (gcp_scripts_dir+"/"+test_case_file_name+pyext, 'a') as file:
            def m7_build_python_case_file():
                step_string_var="step_string"
                step_string="Step: Main menu: - 7 - Set project byoid-ui-testing-project"
                new_line=('\n')
                file.write(new_line+step_string_var+equals+quote+step_string+quote+new_line)
                file.write(print_string+left_bracket+quote+quote+right_bracket+new_line)
                file.write(print_string+left_bracket+quote+running+space+quote+plus+step_string_var+plus+quote+dots+quote+right_bracket+new_line)
                file.write(print_string+left_bracket+quote+'Setting project byoid-ui-testing-project...'+quote+right_bracket+new_line+new_line)
                file.write(os_system+left_bracket+quote+gcloud_config_set_project_byoid_project+quote+right_bracket+new_line)
                file.close()
                print('\nAdded '+step_string)
            m7_build_python_case_file()
        add_another_step_main_menu()
    if selection == '8':
        with open (gcp_scripts_dir+"/"+test_case_file_name+pyext, 'a') as file:
            def m8_build_python_case_file():
                    step_string_var="step_string"
                    step_string="Step: Main menu: - 8 - Set another project"
                    new_line=('\n')
                    project_name=input("\nProvide a valid project name to set in the script: ")
                    project_name_var="project_name"
                    file.write(new_line+step_string_var+equals+quote+step_string+quote+new_line)
                    file.write(print_string+left_bracket+quote+quote+right_bracket+new_line)
                    file.write(print_string+left_bracket+quote+running+space+quote+plus+step_string_var+plus+quote+dots+quote+right_bracket+new_line)
                    file.write(new_line+project_name_var+equals+quote+project_name+quote+new_line)
                    file.write(print_string+left_bracket+quote+'Setting project: '+quote+plus+project_name_var+right_bracket+new_line)
                    file.write(os_system+left_bracket+quote+gcloud_config_set_project+quote+plus+project_name_var+right_bracket+new_line)
                    file.close()
                    print('\nAdded '+step_string)
            m8_build_python_case_file()
        add_another_step_main_menu()
    if selection == '9':
        with open (gcp_scripts_dir+"/"+test_case_file_name+pyext, 'a') as file:
            def m9_build_python_case_file():
                step_string_var="step_string"
                step_string="Step: Main menu: - 9 - Get a list of all projects"
                new_line=('\n')
                file.write(new_line+step_string_var+equals+quote+step_string+quote+new_line)
                file.write(print_string+left_bracket+quote+quote+right_bracket+new_line)
                file.write(print_string+left_bracket+quote+running+space+quote+plus+step_string_var+plus+quote+dots+quote+right_bracket+new_line)
                file.write(print_string+left_bracket+quote+'Listing all projects... '+quote+right_bracket+new_line+new_line)
                file.write(os_system+left_bracket+quote+gcloud_projects_list+quote+right_bracket+new_line)
                file.close()
                print('\nAdded '+step_string)
            m9_build_python_case_file()
        add_another_step_main_menu()
    if selection == '10':
        with open (gcp_scripts_dir+"/"+test_case_file_name+pyext, 'a') as file:
            def m10_build_python_case_file():
                step_string_var="step_string"
                step_string="Step: Main menu: - 10 - Get a list of all organizations"
                new_line=('\n')
                file.write(new_line+step_string_var+equals+quote+step_string+quote+new_line)
                file.write(print_string+left_bracket+quote+quote+right_bracket+new_line)
                file.write(print_string+left_bracket+quote+running+space+quote+plus+step_string_var+plus+quote+dots+quote+right_bracket+new_line)
                file.write(print_string+left_bracket+quote+'Listing all organizations... '+quote+right_bracket+new_line+new_line)
                file.write(os_system+left_bracket+quote+gcloud_organizations_list+quote+right_bracket+new_line)
                file.close()
                print('\nAdded '+step_string)
            m10_build_python_case_file()
        add_another_step_main_menu()
    if selection == 'b':
        test_case_module()
    else:
        input('\nInvalid option provided. Press enter to get back to the main menu.')
        create_case_main_menu()

def create_case_compute_menu():
    global new_line, quote, pyext, print_string, right_bracket, left_bracket, import_os_module, import_sys_module, os_system, space, plus, test_case_file_name, equals, colons, running, double_quotes
    new_line = ('\n')
    quote = "'"
    pyext = ".py"
    print_string = ("print")
    left_bracket = "("
    right_bracket = ")"
    os_system = "os.system"
    import_os_module = "import os"
    import_sys_module = "import sys"
    space = " "
    plus = "+"
    equals = "="
    colon = ":"
    dots = "..."
    double_quotes='"'
    running = "Running"
    gcloud_compute_list_zones='gcloud compute zones list'
    gcloud_compute_describe_zone='gcloud compute zones describe '
    gcloud_compute_instances_os_inventory_list_instances='gcloud compute instances os-inventory list-instances'
    gcloud_compute_describe_vm_instance='gcloud compute instances os-inventory describe '
    gcloud_compute_vm_instances_find='gcloud compute instances list --filter="name='
    gcloud_compute_vm_image_find='gcloud compute images list --filter="name='
    gcloud_compute_images_list='gcloud compute images list'
    gcloud_compute_ssh_simmple='gcloud compute ssh '
    gcloud_compute_create_vm_instance='gcloud compute instances create '
    gcloud_compute_delete_vm_instance='gcloud compute instances delete '
    gcloud_compute_instance_templates_create='gcloud compute instance-templates create '
    gcloud_compute_instance_templates_delete='gcloud compute instance-templates delete '
    gcloud_compute_instance_templates_find='gcloud compute instance-templates list --filter="name='
    gcloud_compute_instance_templates_describe='gcloud compute instance-templates describe '
    gcloud_compute_instance_templates_list='gcloud compute instance-templates list'
    box='[box]'
    gcloud_format_box="' --format "+double_quotes+box+double_quotes
    print("*******************************************")
    print('   GCP TEST CASE COMPUTE CREATION MENU   \n')
    print('1 - List zones')
    print('2 - Describe specific zone')
    print('3 - List running vms - os-instances')
    print('4 - Describe a vm instance - os-instance')
    print('5 - Find vm by name')
    print('6 - Find vm by image name')
    print('7 - List images')
    print('8 - SSH into vm only with vm name - simple mode')
    print('9 - Create default VM instance/s - To create more than one separate strings by space')
    print('10 - Delete vm instance/s - To delete more than one separate strings by space')
    print('11 - Create an instance template')
    print('12 - Delete an instance template')
    print('13 - Find an instance template')
    print('14 - List instance templates')
    print('15 - Describe an instance template')
    selection = input(
        '\nPlease provide the action item you want to add to the test case.\nType a number or letter from the menu and press enter to operate: ')
    if selection == '1':
        with open(gcp_scripts_dir+"/"+test_case_file_name+pyext, 'a') as file:
            def c1_build_python_case_file():
                step_string_var = "step_string"
                step_string = "Step: Compute menu: - 1 - List zones"
                new_line = ('\n')
                file.write(new_line+step_string_var+equals+quote+step_string+quote+new_line)
                file.write(print_string+left_bracket+quote+quote+right_bracket+new_line)
                file.write(print_string+left_bracket+quote+running+space+quote+plus+step_string_var+plus+quote+dots+quote+right_bracket+new_line)
                file.write(print_string+left_bracket+quote+'Listing compute zones: '+quote+right_bracket+new_line)
                file.write(os_system+left_bracket+quote+gcloud_compute_list_zones+quote+right_bracket+new_line)
                file.close()
                print('\nAdded ' + step_string)
            c1_build_python_case_file()
        add_another_step_compute_menu()
    if selection == '2':
        with open(gcp_scripts_dir+"/"+test_case_file_name+pyext, 'a') as file:
            def c2_build_python_case_file():
                step_string_var = "step_string"
                step_string = "Step: Compute menu: - 2 - Describe specific zone"
                zone_to_describe=input('Provide a valid zone name to describe: ')
                zone_to_describe_var='zone_to_describe'
                new_line = ('\n')
                file.write(new_line+step_string_var+equals+quote+step_string+quote+new_line)
                file.write(print_string+left_bracket+quote+quote+right_bracket+new_line)
                file.write(zone_to_describe_var+equals+quote+zone_to_describe+quote+new_line)
                file.write(print_string+left_bracket+quote+running+space+quote+plus+step_string_var+plus+quote+dots+quote+right_bracket+new_line)
                file.write(print_string+left_bracket+quote+'Describing zone: '+quote+plus+zone_to_describe_var+right_bracket+new_line)
                file.write(os_system+left_bracket+quote+gcloud_compute_describe_zone+quote+plus+zone_to_describe_var+right_bracket+new_line)
                file.close()
                print('\nAdded ' + step_string)
            c2_build_python_case_file()
        add_another_step_compute_menu()
    if selection == '3':
        with open(gcp_scripts_dir+"/"+test_case_file_name+pyext, 'a') as file:
            def c3_build_python_case_file():
                step_string_var = "step_string"
                step_string = "Step: Compute menu: - 3 - List running vms - os-instances"
                new_line = ('\n')
                file.write(new_line+step_string_var+equals+quote+step_string+quote+new_line)
                file.write(print_string+left_bracket+quote+quote+right_bracket+new_line)
                file.write(print_string+left_bracket+quote+running+space+quote+plus+step_string_var+plus+quote+dots+quote+right_bracket+new_line)
                file.write(print_string+left_bracket+quote+'Listing running os instances: '+quote+right_bracket+new_line)
                file.write(os_system+left_bracket+quote+gcloud_compute_instances_os_inventory_list_instances+quote+right_bracket+new_line)
                file.close()
                print('\nAdded ' + step_string)
            c3_build_python_case_file()
        add_another_step_compute_menu()
    if selection == '4':
        with open(gcp_scripts_dir+"/"+test_case_file_name+pyext, 'a') as file:
            def c4_build_python_case_file():
                step_string_var = "step_string"
                step_string = "Step: Compute menu: - 4 - Describe a vm instance - os-instance"
                vm_instance_to_describe=input('Provide a valid vm instance name to describe: ')
                vm_instance_to_describe_var='vm_instance_description'
                new_line = ('\n')
                file.write(new_line+step_string_var+equals+quote+step_string+quote+new_line)
                file.write(print_string+left_bracket+quote+quote+right_bracket+new_line)
                file.write(vm_instance_to_describe_var+equals+quote+vm_instance_to_describe+quote+new_line)
                file.write(print_string+left_bracket+quote+running+space+quote+plus+step_string_var+plus+quote+dots+quote+right_bracket+new_line)
                file.write(print_string+left_bracket+quote+'Describing vm instance: '+quote+plus+vm_instance_to_describe_var+right_bracket+new_line)
                file.write(os_system+left_bracket+quote+gcloud_compute_describe_vm_instance+quote+plus+vm_instance_to_describe_var+right_bracket+new_line)
                file.close()
                print('\nAdded ' + step_string)
            c4_build_python_case_file()
        add_another_step_compute_menu()
    if selection == '5':
        with open(gcp_scripts_dir+"/"+test_case_file_name+pyext, 'a') as file:
            def c5_build_python_case_file():
                step_string_var = "step_string"
                step_string = "Step: Compute menu: - 5 - Find a vm instance - os-instance"
                vm_instance_to_find=input('Provide a valid vm instance name to find: ')
                vm_instance_to_find_var='vm_instance_to_find'
                new_line = ('\n')
                file.write(new_line+step_string_var+equals+quote+step_string+quote+new_line)
                file.write(print_string+left_bracket+quote+quote+right_bracket+new_line)
                file.write(vm_instance_to_find_var+equals+quote+vm_instance_to_find+quote+new_line)
                file.write(print_string+left_bracket+quote+running+space+quote+plus+step_string_var+plus+quote+dots+quote+right_bracket+new_line)
                file.write(print_string+left_bracket+quote+'Finding vm instance: '+quote+plus+vm_instance_to_find_var+right_bracket+new_line)
                file.write(os_system+left_bracket+quote+gcloud_compute_vm_instances_find+vm_instance_to_find+double_quotes+quote+right_bracket+new_line)
                file.close()
                print('\nAdded ' + step_string)
            c5_build_python_case_file()
        add_another_step_compute_menu()
    if selection == '6':
        with open(gcp_scripts_dir+"/"+test_case_file_name+pyext, 'a') as file:
            def c6_build_python_case_file():
                step_string_var = "step_string"
                step_string = "Step: Compute menu: - 6 - Find vm by image name"
                vm_image_to_find=input('Provide a valid vm image name to find: ')
                vm_image_to_find_var='vm_instance_to_find'
                new_line = ('\n')
                file.write(new_line+step_string_var+equals+quote+step_string+quote+new_line)
                file.write(print_string+left_bracket+quote+quote+right_bracket+new_line)
                file.write(vm_image_to_find_var+equals+quote+vm_image_to_find+quote+new_line)
                file.write(print_string+left_bracket+quote+running+space+quote+plus+step_string_var+plus+quote+dots+quote+right_bracket+new_line)
                file.write(print_string+left_bracket+quote+'Finding vm image name: '+quote+plus+vm_image_to_find_var+right_bracket+new_line)
                file.write(os_system+left_bracket+quote+gcloud_compute_vm_image_find+vm_image_to_find+double_quotes+quote+right_bracket+new_line)
                file.close()
                print('\nAdded ' + step_string)
            c6_build_python_case_file()
        add_another_step_compute_menu()
    if selection == '7':
        with open(gcp_scripts_dir+"/"+test_case_file_name+pyext, 'a') as file:
            def c7_build_python_case_file():
                step_string_var = "step_string"
                step_string = "Step: Compute menu: - 7 - List images"
                new_line = ('\n')
                file.write(new_line+step_string_var+equals+quote+step_string+quote+new_line)
                file.write(print_string+left_bracket+quote+quote+right_bracket+new_line)
                file.write(print_string+left_bracket+quote+running+space+quote+plus+step_string_var+plus+quote+dots+quote+right_bracket+new_line)
                file.write(print_string+left_bracket+quote+'Listing images: '+quote+right_bracket+new_line)
                file.write(os_system+left_bracket+quote+gcloud_compute_images_list+quote+right_bracket+new_line)
                file.close()
                print('\nAdded ' + step_string)
            c7_build_python_case_file()
        add_another_step_compute_menu()
    if selection == '8':
        with open(gcp_scripts_dir+"/"+test_case_file_name+pyext, 'a') as file:
            def c8_build_python_case_file():
                step_string_var = "step_string"
                step_string = "Step: Compute menu: - 8 - SSH into vm only with vm name - simple mode"
                ssh_to_vm=input('Provide a valid vm name to ssh into: ')
                ssh_to_vm_var='ssh_to_vm'
                new_line = ('\n')
                file.write(new_line+step_string_var+equals+quote+step_string+quote+new_line)
                file.write(print_string+left_bracket+quote+quote+right_bracket+new_line)
                file.write(ssh_to_vm_var+equals+quote+ssh_to_vm+quote+new_line)
                file.write(print_string+left_bracket+quote+running+space+quote+plus+step_string_var+plus+quote+dots+quote+right_bracket+new_line)
                file.write(print_string+left_bracket+quote+'Attempting to log in via ssh to vm: '+quote+plus+ssh_to_vm_var+right_bracket+new_line)
                file.write(os_system+left_bracket+quote+gcloud_compute_ssh_simmple+quote+plus+ssh_to_vm_var+right_bracket+new_line)
                file.close()
                print('\nAdded ' + step_string)
            c8_build_python_case_file()
        add_another_step_compute_menu()
    if selection == '9':
        #CREATE MANY INSTANCES OF VMS
        with open(gcp_scripts_dir+"/"+test_case_file_name+pyext, 'a') as file:
            def c9_build_python_case_file():
                global step_string_var, step_string
                step_string_var = "step_string"
                step_string = "Step: Compute menu: - 9 - Create vm instance"
                create_vm_instance=input('Provide a name to create a vm instance. If more than one is needed, separate them  with spaces: ')
                create_vm_instance_var='vm_instances_create=['
                vm_instances_list=[]
                file.write(new_line+step_string_var+equals+quote+step_string+quote+new_line)
                file.write(create_vm_instance_var)
                for create_vm in create_vm_instance.split():
                    vm_instances_list.append(create_vm)
                for vm_instance_created in vm_instances_list:
                    file.write(quote+vm_instance_created+quote)
            c9_build_python_case_file()
        file.close()
        def c9_2_build_python_case_file():
            out = '_'
            test_case_file_name_out = test_case_file_name + out
            quotes = "''"
            quotes_coma = "', '"
            input_file = open(gcp_scripts_dir+"/"+test_case_file_name+pyext, "rt")
            # Open the output file
            out_file = open(test_case_file_name_out + pyext, "wt")
            # Iterate through the lines of the first file
            for line in input_file:
                # Write onto the output file.
                out_file.write(line.replace(quotes, quotes_coma))
            # Close both files.
            input_file.close()
            out_file.close()
            create_vm_instance_var_close = "]"
            out_file=open(test_case_file_name_out + pyext, "a")
            out_file.write(create_vm_instance_var_close+new_line)
            for_vm_instance_var = 'for vm_to_create in vm_instances_create: '
            vm_to_create_var='vm_to_create'
            zone_creation_var=' --zone=northamerica-northeast1-a'
            out_file.write(print_string+left_bracket+quote+quote+right_bracket+new_line)
            out_file.write(print_string+left_bracket+quote+running+space+quote+plus+step_string_var+plus+quote+dots+quote+right_bracket+new_line)
            out_file.write(print_string+left_bracket+quote+'Attempting to create vm instances: '+quote+right_bracket+new_line)
            out_file.write(for_vm_instance_var+new_line)
            out_file.write("    "+print_string+left_bracket+quote+"Creating vm instance: "+quote+plus+vm_to_create_var+plus+quote+dots+quote+right_bracket+new_line)
            out_file.write("    "+os_system+left_bracket+quote+gcloud_compute_create_vm_instance+quote+plus+vm_to_create_var+plus+quote+zone_creation_var+quote+right_bracket+new_line)
            file.close()
            os.remove(test_case_file_name+pyext)
            rename_file=test_case_file_name_out+pyext
            new_filename=test_case_file_name+pyext
            os.rename(rename_file, new_filename)
            print('\nAdded ' + step_string)
        c9_2_build_python_case_file()
        add_another_step_compute_menu()
    if selection == '10':
        #DELETE MANY INSTANCES OF VMS
        with open(gcp_scripts_dir+"/"+test_case_file_name+pyext, 'a') as file:
            def c10_build_python_case_file():
                global step_string_var, step_string
                step_string_var = "step_string"
                step_string = "Step: Compute menu: - 10 - Delete vm instance"
                delete_vm_instance=input('Provide a name to delete a vm instance. If more than one is needed, separate them  with spaces: ')
                delete_vm_instance_var='vm_instances_delete=['
                vm_instances_list=[]
                file.write(new_line+step_string_var+equals+quote+step_string+quote+new_line)
                file.write(delete_vm_instance_var)
                for delete_vm in delete_vm_instance.split():
                    vm_instances_list.append(delete_vm)
                for vm_instance_deleted in vm_instances_list:
                    file.write(quote+vm_instance_deleted+quote)
            c10_build_python_case_file()
        file.close()
        def c10_2_build_python_case_file():
            out = '_'
            test_case_file_name_out = test_case_file_name + out
            quotes = "''"
            quotes_coma = "', '"
            input_file = open(gcp_scripts_dir+"/"+test_case_file_name+pyext, "rt")
            # Open the output file
            out_file = open(test_case_file_name_out + pyext, "wt")
            # Iterate through the lines of the first file
            for line in input_file:
                # Write onto the output file.
                out_file.write(line.replace(quotes, quotes_coma))
            # Close both files.
            input_file.close()
            out_file.close()
            delete_vm_instance_var_close = "]"
            out_file=open(test_case_file_name_out + pyext, "a")
            out_file.write(delete_vm_instance_var_close+new_line)
            for_vm_instance_var = 'for vm_to_delete in vm_instances_delete: '
            vm_to_delete_var='vm_to_delete'
            zone_deletion_var=' --zone=northamerica-northeast1-a --quiet'
            out_file.write(print_string+left_bracket+quote+quote+right_bracket+new_line)
            out_file.write(print_string+left_bracket+quote+running+space+quote+plus+step_string_var+plus+quote+dots+quote+right_bracket+new_line)
            out_file.write(print_string+left_bracket+quote+'Attempting to delete vm instances: '+quote+right_bracket+new_line)
            out_file.write(for_vm_instance_var+new_line)
            out_file.write("    "+print_string+left_bracket+quote+"Deleting vm instance: "+quote+plus+vm_to_delete_var+plus+quote+dots+quote+right_bracket+new_line)
            out_file.write("    "+os_system+left_bracket+quote+gcloud_compute_delete_vm_instance+quote+plus+vm_to_delete_var+plus+quote+zone_deletion_var+quote+right_bracket+new_line)
            file.close()
            os.remove(test_case_file_name+pyext)
            rename_file=test_case_file_name_out+pyext
            new_filename=test_case_file_name+pyext
            os.rename(rename_file, new_filename)
            print('\nAdded ' + step_string)
        c10_2_build_python_case_file()
        add_another_step_compute_menu()
    if selection == '11':
        with open(gcp_scripts_dir+"/"+test_case_file_name+pyext, 'a') as file:
            def c11_build_python_case_file():
                step_string_var = "step_string"
                step_string = "Step: Compute menu: - 11 - Create an instance template"
                create_instance_template=input('Provide a name to create the instance template: ')
                create_instance_template_var='create_instance_template'
                new_line = ('\n')
                file.write(new_line+step_string_var+equals+quote+step_string+quote+new_line)
                file.write(print_string+left_bracket+quote+quote+right_bracket+new_line)
                file.write(create_instance_template_var+equals+quote+create_instance_template+quote+new_line)
                file.write(print_string+left_bracket+quote+running+space+quote+plus+step_string_var+plus+quote+dots+quote+right_bracket+new_line)
                file.write(print_string+left_bracket+quote+'Creating instance template: '+quote+plus+create_instance_template_var+right_bracket+new_line)
                file.write(os_system+left_bracket+quote+gcloud_compute_instance_templates_create+quote+plus+create_instance_template_var+right_bracket+new_line)
                file.close()
                print('\nAdded ' + step_string)
            c11_build_python_case_file()
        add_another_step_compute_menu()
    if selection == '12':
        with open(gcp_scripts_dir+"/"+test_case_file_name+pyext, 'a') as file:
            def c12_build_python_case_file():
                step_string_var = "step_string"
                step_string = "Step: Compute menu: - 12 - Delete an instance template"
                delete_instance_template=input('Provide the name of an existing instance template to delete: ')
                delete_instance_template_var='delete_instance_template'
                quiet_delete=" --quiet"
                new_line = ('\n')
                file.write(new_line+step_string_var+equals+quote+step_string+quote+new_line)
                file.write(print_string+left_bracket+quote+quote+right_bracket+new_line)
                file.write(delete_instance_template_var+equals+quote+delete_instance_template+quote+new_line)
                file.write(print_string+left_bracket+quote+running+space+quote+plus+step_string_var+plus+quote+dots+quote+right_bracket+new_line)
                file.write(print_string+left_bracket+quote+'Deleting instance template: '+quote+plus+delete_instance_template_var+right_bracket+new_line)
                file.write(os_system+left_bracket+quote+gcloud_compute_instance_templates_delete+quote+plus+delete_instance_template_var+plus+quote+quiet_delete+quote+right_bracket+new_line)
                file.close()
                print('\nAdded ' + step_string)
            c12_build_python_case_file()
        add_another_step_compute_menu()
    if selection == '13':
        with open(gcp_scripts_dir+"/"+test_case_file_name+pyext, 'a') as file:
            def c13_build_python_case_file():
                step_string_var = "step_string"
                step_string = "Step: Compute menu: - 13 - Find an instance template"
                instance_template_to_find=input('Provide a valid instance template name to find: ')
                instance_template_to_find_var='instance_template_to_find'
                new_line = ('\n')
                file.write(new_line+step_string_var+equals+quote+step_string+quote+new_line)
                file.write(print_string+left_bracket+quote+quote+right_bracket+new_line)
                file.write(instance_template_to_find_var+equals+quote+instance_template_to_find+quote+new_line)
                file.write(print_string+left_bracket+quote+running+space+quote+plus+step_string_var+plus+quote+dots+quote+right_bracket+new_line)
                file.write(print_string+left_bracket+quote+'Finding instance template name: '+quote+plus+instance_template_to_find_var+right_bracket+new_line)
                file.write(os_system+left_bracket+quote+gcloud_compute_instance_templates_find+quote+plus+instance_template_to_find_var+plus+gcloud_format_box+double_quotes+quote+right_bracket+new_line)
                file.close()
                print('\nAdded ' + step_string)
            c13_build_python_case_file()
        add_another_step_compute_menu()
    if selection == '14':
        with open(gcp_scripts_dir+"/"+test_case_file_name+pyext, 'a') as file:
            def c14_build_python_case_file():
                step_string_var = "step_string"
                step_string = "Step: Compute menu: - 14 - List instance templates"
                new_line = ('\n')
                file.write(new_line+step_string_var+equals+quote+step_string+quote+new_line)
                file.write(print_string+left_bracket+quote+quote+right_bracket+new_line)
                file.write(print_string+left_bracket+quote+running+space+quote+plus+step_string_var+plus+quote+dots+quote+right_bracket+new_line)
                file.write(print_string+left_bracket+quote+'Listing instance templates...'+quote+right_bracket+new_line)
                file.write(os_system+left_bracket+quote+gcloud_compute_instance_templates_list+quote+right_bracket+new_line)
                file.close()
                print('\nAdded ' + step_string)
            c14_build_python_case_file()
        add_another_step_compute_menu()
    if selection == '15':
        with open(gcp_scripts_dir+"/"+test_case_file_name+pyext, 'a') as file:
            def c15_build_python_case_file():
                step_string_var = "step_string"
                step_string = "Step: Compute menu: - 15 - Describe an instance template"
                instance_template_to_describe=input('Provide a valid instance template name to describe: ')
                instance_template_to_describe_var='instance_template_to_find'
                new_line = ('\n')
                file.write(new_line+step_string_var+equals+quote+step_string+quote+new_line)
                file.write(print_string+left_bracket+quote+quote+right_bracket+new_line)
                file.write(instance_template_to_describe_var+equals+quote+instance_template_to_describe+quote+new_line)
                file.write(print_string+left_bracket+quote+running+space+quote+plus+step_string_var+plus+quote+dots+quote+right_bracket+new_line)
                file.write(print_string+left_bracket+quote+'Describing instance template name: '+quote+plus+instance_template_to_describe_var+right_bracket+new_line)
                file.write(os_system+left_bracket+quote+gcloud_compute_instance_templates_describe+quote+plus+instance_template_to_describe_var+right_bracket+new_line)
                file.close()
                print('\nAdded ' + step_string)
            c15_build_python_case_file()
        add_another_step_compute_menu()
def test_case_module():
    def build_new_test_case():
        global new_test_case_input, test_case_string_var, test_case_file_name, pyext, new_line, random_id, id
        test_case_string_var="_tst_k_s_"
        pyext=".py"
        new_line=('\n')
        import_os_module="import os"
        import_sys_module="import sys"
        print('\nBuild new test case/s menu accessed\n')
        print('NOTE: you may include many steps into a single test case')
        new_test_case_input=input('\nPlease provide a name for your test case: ')
        random_id=random.randint(0, 100000)
        random_id=str(random_id)
        id="id_"
        test_case_file_name=new_test_case_input+test_case_string_var+id+random_id
        print('\nThe test case will be saved in a python file format with the following name: '+test_case_file_name+'.py')
        with open (gcp_scripts_dir+"/"+test_case_file_name+pyext, 'w') as file:
            file.write(import_os_module+new_line+import_sys_module+new_line+new_line)
            file.close()
        print('\nTest case '+test_case_file_name+pyext+' was created and is empty.\n')
        input("Press enter to continue: ")
        loop = 0
        while True:

            print('\nSelect a menu from which you want to add test case step: ')
            print('\n- m - Main menu')
            print('- c - Compute engine module')
            print('- b - < Back to test case module menu')
            test_case_menu_step=input('\nType a valid option and press enter: ')
            if test_case_menu_step == 'm':
                create_case_main_menu()
            if test_case_menu_step == 'c':
                create_case_compute_menu()
            if test_case_menu_step == 'b':
                test_case_module()
            else:
                print('\nInvalid input provided. type an option from the menu and press enter: ')
                loop = 0

    def run_test_cases():
        print('\nRun test case/s menu accessed\n')
        test_case_run=input("Provide a valid test case name, and press enter to run it: ")
        try:
            print("\nAttempting to run test case "+test_case_run+'...\n')
            #remove_py=test_case_run.replace('.py', '')
            runpy.run_path(path_name=gcp_scripts_dir+"/"+test_case_run) #run module without importing
            timestamp()
        except:
            print("The provided file name was invalid or not found. Please retry.")

        input('\nPress enter to get back to the main menu: ')
        test_case_module()

    def view_test_cases():
        global check_file, dir_path, test_case_string_var
        test_case_string_var="_tst_k_s_"
        print('\nView test cases menu accessed')
        dir_path = os.path.dirname(os.path.realpath(__file__))
        check_file=os.path.isfile(test_case_string_var)
        print('\nListing test cases in path '+dir_path+"/"+gcp_scripts_dir+': \n')
        for i in os.listdir(path=dir_path+"/"+gcp_scripts_dir):
            if test_case_string_var in i:
                print(i)
        #if not test_case_string_var in i:
        #    print('\nNo test cases where found in path: '+dir_path)
        input('\nPress enter to get back to the main menu: ')
        test_case_module()

    def invalid_file_provided():
        invalid_input=input('\nInvalid filename provided. Retry? y/n: ')
        if invalid_input == "y":
            reading_steps_from_file()
        if invalid_input == "n":
            print("Redirecting to menu")
            test_case_module()
        else:
            print("\nPlease type either 'y' or 'n'")
            invalid_file_provided()

    def reading_steps_from_file():
        try:
            file_to_read=input('\nProvide file name to read: ')
            string_to_read="Step:"
            print("\nListing test case steps for file: "+file_to_read+'\n')
            with open(gcp_scripts_dir+"/"+file_to_read, 'r') as filedata:     # Opening the given file in read-only mode
               for line in filedata:
                    if string_to_read in line:
                        replace_string=line.replace("step_string='", '')
                        replace_string2=line.replace("'", "")
                        print(replace_string)
            filedata.close()
            input("\nPress enter to get back to the menu: ")
            test_case_module()
        except:
            invalid_file_provided()

    def delete_cases():
        test_case_string_var = "_tst_k_s_id_"
        dir_path = os.path.dirname(os.path.realpath(__file__))
        check_file = os.path.isfile(test_case_string_var)
        print('\nNOTE: only test case files containing syntax: ' + test_case_string_var + ' will be removed.')
        delete_test_cases=input("\nType the test case file to delete. If it is more than one, separate them with spaces: ")
        cases_to_delete = []
        for case in delete_test_cases.split():
            cases_to_delete.append(case)
        for case in cases_to_delete:
            if test_case_string_var in case:
                os.remove(gcp_scripts_dir+"/"+case)
                print('\nRemoved file: '+delete_test_cases)
        input('\nPress enter to get back to the main menu: ')
        test_case_module()

    def delete_all_test_cases():
        test_case_string_var = "_tst_k_s_"
        dir_path = gcp_scripts_dir+"/"
        delete_all=input('\nWARNING. You are about to delete all the test cases. Confirm? y/n: ')
        if delete_all == 'y':
            for case in os.listdir(path=dir_path):
                if test_case_string_var in case:
                    os.remove(gcp_scripts_dir+"/"+case)
                    print('\nRemoved test case: '+case)
            enter=input('\nPress enter to get back to the main menu: ')
            test_case_module()
        if delete_all == 'n':
            print('\nAborted deletion of all the test case files.')
            input('\nPress enter to get back to the main menu: ')
            test_case_module()
        else:
            delete_all_test_cases()


    print('\nMode T accessed.\n')
    print("*******************************************")
    print('          TEST CASE MODULE MENU           \n')
    print('1 - Build a new test case')
    print('2 - Run test case/s')
    print('3 - Delete test case file/s')
    print('4 - Delete all test case files')
    print('5 - View saved test cases')
    print('6 - Read test case steps from file')
    print('c <- Compute engine module')
    print('b <- Back to Main menu')
    test_case_menu_selection=input('\nSelect an option from the menu and press enter: ')
    if test_case_menu_selection == '1':
        build_new_test_case()
    if test_case_menu_selection == '2':
        run_test_cases()
    if test_case_menu_selection == '3':
        delete_cases()
    if test_case_menu_selection == '4':
        delete_all_test_cases()
    if test_case_menu_selection == '5':
        view_test_cases()
    if test_case_menu_selection == "6":
        reading_steps_from_file()
    if test_case_menu_selection == 'c':
        from gcp_interactive_cli_v2 import compute_engine_module
    if test_case_menu_selection == 'b':
        from gcp_interactive_cli_v2 import main_menu
    else:
        test_case_module()


