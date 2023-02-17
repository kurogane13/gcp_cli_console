import imp
import os
import runpy
import sys
import random
import importlib
from datetime import datetime

def add_another_step_main_menu():
    add_step_or_not=input("\nDo you want to add another step to this test case?. y/n: ")
    if add_step_or_not == "y":
        create_case_main_menu()
    if add_step_or_not == "n":
        input("\nYou decided not to add more steps for this test case. Press enter to get back to the test case module menu: ")
        test_case_module()
    else:
        input('\nInvalid input. Type either "y" or "n" and press enter.')
        add_another_step_main_menu()

def add_another_step_compute_menu():
    pass

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
    print('        GCP TEST CASE CREATION MAIN MENU       \n')
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
        with open (test_case_file_name+pyext, 'a') as file:
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
        with open (test_case_file_name+pyext, 'a') as file:
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
        with open (test_case_file_name+pyext, 'a') as file:
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
        with open (test_case_file_name+pyext, 'a') as file:
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
        with open (test_case_file_name+pyext, 'a') as file:
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
        with open (test_case_file_name+pyext, 'a') as file:
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
        with open (test_case_file_name+pyext, 'a') as file:
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
        with open (test_case_file_name+pyext, 'a') as file:
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
        with open (test_case_file_name+pyext, 'a') as file:
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
        with open (test_case_file_name+pyext, 'a') as file:
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
        with open (test_case_file_name+pyext, 'w') as file:
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
                compute_engine_module()
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
            remove_py=test_case_run.replace('.py', '')
            runpy.run_module(remove_py) #run module without importing
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
        print('\nListing test cases in path '+dir_path+': \n')
        for i in os.listdir(path=dir_path):
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
            with open(file_to_read, 'r') as filedata:     # Opening the given file in read-only mode
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

    print('Mode T accessed.\n')
    print("*******************************************")
    print('          TEST CASE MODULE MENU           \n')
    print('1 - Build a new test case')
    print('2 - Run test case/s')
    print('3 - View saved test cases')
    print('4 - Read test case steps from file')
    print('c <- Compute engine module')
    print('b <- Back to Main menu')
    test_case_menu_selection=input('\nSelect an option from the menu and press enter: ')
    if test_case_menu_selection == '1':
        build_new_test_case()
    if test_case_menu_selection == '2':
        run_test_cases()
    if test_case_menu_selection == '3':
        view_test_cases()
    if test_case_menu_selection == "4":
        reading_steps_from_file()
    if test_case_menu_selection == 'c':
        from gcp_interactive_cli_v2 import compute_engine_module
    if test_case_menu_selection == 'b':
        from gcp_interactive_cli_v2 import main_menu
    else:
        #input('\nInvalid option selected, you must type a number or letter from the menu. Press enter to get back to test cases main menu: ')
        test_case_module()

#test_case_module()