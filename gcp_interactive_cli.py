#from google.cloud import storage
import os
import sys

def check_billing_project():

    print('- Mode 1 accessed.\n')
    project_name=input('Provide a valid project name and press enter: ')
    print("\nRetrieving billing data for project name: "+project_name+'\n')
    os.system('gcloud beta billing projects describe '+project_name)
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

def test_case_module():
    def build_new_test_case():
        print('Build new test case/s menu accessed\n')
        input('\nPress enter to get back to the main menu: ')
        test_case_module()
        pass
    def run_test_cases():
        print('Run test case/s menu accessed\n')
        input('\nPress enter to get back to the main menu: ')
        test_case_module()
        pass
    def view_test_cases():
        print('View test cases menu accessed\n')
        input('\nPress enter to get back to the main menu: ')
        test_case_module()
        pass

    print('Mode T accessed.\n')
    print("*******************************************")
    print('          TEST CASE MODULE MENU           \n')
    print('1 - Build a new test case')
    print('2 - Run test case/s')
    print('3 - View saved test cases')
    print('b <- Back to Main menu')
    test_case_menu_selection=input('\nSelect an option from the menu and press enter: ')
    if test_case_menu_selection == '1':
        build_new_test_case()
    if test_case_menu_selection == '2':
        run_test_cases()
    if test_case_menu_selection == '3':
        view_test_cases()
    if test_case_menu_selection == 'b':
        main_menu()
    else:
        input('\nInvalid option selected, you must type a number or letter from the menu. Press enter to get back to main menu: ')
        test_case_module()

def main_menu():

    print("*******************************************")
    print('        GCP PYTHON TESTING CONSOLE         \n')
    print('1 - Retrieve billing data for specific project')
    print('2 - Describe specific project')
    print('3 - Get configuration list - Lists account name and project data')
    print('4 - Get active project')
    print('5 - Set another project')
    print('6 - Get a list of all projects')
    print('7 - Get a list of all organizations')
    print('a - Interactive alpha gcloud command line')
    print('t - test case builder')
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
        test_case_module()
    else:
        input('\nInvalid option selected, you must type a number or letter from the menu. Press enter to get back to main menu: ')
        main_menu()

main_menu()
