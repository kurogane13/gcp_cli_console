import os
import sys
import random
import runpy
import datetime
from datetime import datetime

gcp_system_log_file='gcp_system_log.log'  # System event log file var

def timestamp():
    now=datetime.now()
    print("\nTest case termination timestamp: "+str(now))

def return_to_main_menu():
    gcp_system_log_file = 'gcp_system_log.log'
    now = datetime.now()
    with open(gcp_system_log_file, 'a') as logfile:
        logfile.write(str(now) + " <-- Exited FREE COMMAND LINE MAIN menu\n")
        logfile.close()
    from gcp_python_interactive_cli_v2 import main_menu
    main_menu()

def return_to_compute_menu():
    gcp_system_log_file = 'gcp_system_log.log'
    now = datetime.now()
    with open(gcp_system_log_file, 'a') as logfile:
        logfile.write(str(now) + " <-- Exited FREE COMMAND LINE MAIN menu\n")
        logfile.close()
    from gcp_python_interactive_cli_v2 import compute_engine_module
    compute_engine_module()

def free_command_input():
    gcp_system_log_file = 'gcp_system_log.log'
    now = datetime.now()
    with open(gcp_system_log_file, 'a') as logfile:
        logfile.write(str(now) + " --> Accessed FREE COMMAND LINE MAIN menu\n")
        logfile.close()
    gcp_scripts_dir = 'gcp_automation_test_scripts'
    def build_new_cli_test_case():
        gcp_system_log_file = 'gcp_system_log.log'
        now = datetime.now()
        with open(gcp_system_log_file, 'a') as logfile:
            logfile.write(str(now) + " --> Accessed CREATE NEW CLI TEST mode\n")
            logfile.close()
        free_test_case_string_var = "_cli_tst_k_s_"
        pyext = ".py"
        new_line = ('\n')
        import_os_module = "import os"
        import_sys_module = "import sys"
        quote = "'"
        pyext = ".py"
        print_string = ("print")
        left_bracket = "("
        right_bracket = ")"
        os_system = "os.system"
        space = " "
        plus = "+"
        equals = "="
        colon = ":"
        dots = "..."
        double_quotes = '"'
        running = "Running"
        print('\nBuild script using your own gcloud commands.\n')
        print('NOTE: you may include many commands into a single test case script')
        new_test_case_input = input('\nPlease provide a name for your test case: ')
        random_id = random.randint(0, 100000)
        random_id = str(random_id)
        id = "id_"
        free_test_case_file_name = new_test_case_input + free_test_case_string_var + id + random_id
        command_string = "Attempting to run gcloud command instance..."
        print('\nThe test case will be saved in a python file format with the following name: ' + free_test_case_file_name + '.py')
        with open(gcp_scripts_dir+"/"+free_test_case_file_name+pyext, 'w') as file:
            file.write(import_os_module+new_line+import_sys_module+new_line+new_line)
            file.close()
        with open(gcp_system_log_file, 'a') as logfile:
            logfile.write(str(now) + " + Created test case "+free_test_case_file_name)
            logfile.close()
        print('\nTest case ' + free_test_case_file_name + pyext + ' was created and is empty.\n')
        input("Press enter to continue: ")
        def add_more_commands():
            provide_command = input('\nPlease provide the desired gcloud command you wish to add to the script test case, and press enter: ')
            with open(gcp_scripts_dir+"/"+free_test_case_file_name+pyext, 'a') as file:
                file.write(new_line+print_string+left_bracket+quote+command_string+quote+right_bracket+new_line)
                file.write(new_line+os_system+left_bracket+quote+provide_command+quote+right_bracket+new_line)
                file.close()
                print('\nAdded command: '+'"'+provide_command+'"'+' to script : '+free_test_case_file_name+pyext)
                gcp_system_log_file = 'gcp_system_log.log'
                with open(gcp_system_log_file, 'a') as logfile:
                    logfile.write("\n"+str(now)+" Added command: "+'"'+provide_command+'"'+" to script : "+free_test_case_file_name+pyext)
                    logfile.close()
                def add_command_prompt():
                    add_more_command_prompt = input("\nWould you like to add another command to the script?: y/n?:  ")
                    if add_more_command_prompt == "y":
                        add_more_commands()
                    if add_more_command_prompt == "n":
                        input('\nYou decided not to add more commands to the script:  '+free_test_case_file_name+pyext+". Press enter to continue: ")
                        now = datetime.now()
                        gcp_system_log_file = 'gcp_system_log.log'
                        with open(gcp_system_log_file, 'a') as logfile:
                            logfile.write(str(now) + " <-- Exited CREATE NEW CLI TEST mode\n")
                            logfile.close()
                        free_command_input()
                    else:
                        add_command_prompt()
                add_command_prompt()
        add_more_commands()

    def run_test_cases():
        now = datetime.now()
        gcp_system_log_file = 'gcp_system_log.log'
        with open(gcp_system_log_file, 'a') as logfile:
            logfile.write(str(now) + " --> Accessed RUN CLI TEST CASE mode\n")
            logfile.close()
        print('\nRun test case/s menu Accessed\n')
        test_case_run=input("Provide a valid test case name, and press enter to run it: ")
        print("\nAttempting to run test case "+test_case_run+'...\n')
        dir_path = os.path.dirname(os.path.realpath(__file__))
        if test_case_run in os.listdir(path=dir_path+"/"+gcp_scripts_dir):
            runpy.run_path(path_name=gcp_scripts_dir+"/"+test_case_run) #run module without importing
            now = datetime.now()
            with open(gcp_system_log_file, 'a') as logfile:
                logfile.write(str(now) + " ! Executed test case script: "+gcp_scripts_dir+"/"+test_case_run+"\n")
                logfile.close()
            timestamp()
        else:
            print("The provided file name was invalid or not found. Please retry.")
            with open(gcp_system_log_file, 'a') as logfile:
                logfile.write(str(now) + " - ERROR: Unable to run test case script: "+gcp_scripts_dir+"/"+test_case_run+". Check for errors in the cli script if  found in path.\n")
                logfile.close()
        input('\nPress enter to get back to the main menu: ')
        with open(gcp_system_log_file, 'a') as logfile:
            logfile.write(str(now) + " <-- Exited RUN CLI TEST CASE mode mode\n")
            logfile.close()
        free_command_input()

    def view_test_cases():
        gcp_system_log_file = 'gcp_system_log.log'
        with open(gcp_system_log_file, 'a') as logfile:
            logfile.write(str(now) + " --> Accessed VIEW CLI TEST CASES mode\n")
            logfile.close()
        global check_file, dir_path, test_case_string_var
        test_case_string_var="_cli_tst_k_s_"
        print('\nView test cases menu Accessed')
        dir_path = os.path.dirname(os.path.realpath(__file__))
        check_file=os.path.isfile(test_case_string_var)
        print('\nListing test cases in path '+dir_path+"/"+gcp_scripts_dir+': \n')
        for i in os.listdir(path=dir_path+"/"+gcp_scripts_dir):
            if test_case_string_var in i:
                print(i)
        with open(gcp_system_log_file, 'a') as logfile:
            logfile.write(str(now) + " - Listed test cases in path: "+dir_path+"/"+gcp_scripts_dir+": \n")
            logfile.close()
        input('\nPress enter to get back to the main menu: ')
        with open(gcp_system_log_file, 'a') as logfile:
            logfile.write(str(now) + " <-- Exited VIEW CLI TEST CASES mode\n")
            logfile.close()
        free_command_input()

    def invalid_file_provided():
        invalid_input=input('\nInvalid filename provided. Retry? y/n: ')
        if invalid_input == "y":
            reading_steps_from_file()
        if invalid_input == "n":
            print("Redirecting to menu")
            free_command_input()
        else:
            print("\nPlease type either 'y' or 'n'")
            invalid_file_provided()

    def reading_steps_from_file():
        dir_path = os.path.dirname(os.path.realpath(__file__))
        gcp_system_log_file = 'gcp_system_log.log'
        with open(gcp_system_log_file, 'a') as logfile:
            logfile.write(str(now) + " --> Accessed VIEW CLI TEST CASE COMMANDS mode\n")
            logfile.close()
        file_to_read=input('\nProvide file name to read: ')
        string_to_read="'gcloud"
        if file_to_read == "":
            input('\nYou typed nothing. Press enter to retry: ')
            reading_steps_from_file()
        if file_to_read in os.listdir(path=dir_path+"/"+gcp_scripts_dir):
            print("\nListing commands added to file: "+file_to_read+'\n')
            gcloud_instances=[]
            with open(gcp_scripts_dir+"/"+file_to_read, 'r') as filedata:     # Opening the given file in read-only mode
               for line in filedata:
                    if string_to_read in line:
                        replace_string=line.replace("os.system('", "")
                        gcloud_instances.append(replace_string)
               for instance in gcloud_instances:
                   print(instance.replace("')", ""))
            filedata.close()
            with open(gcp_system_log_file, 'a') as logfile:
                logfile.write(str(now) + " - Listed commands added to file: "+file_to_read+"\n")
                logfile.close()
            input("\nPress enter to get back to the menu: ")
            with open(gcp_system_log_file, 'a') as logfile:
                logfile.write(str(now) + " <-- Exited VIEW CLI TEST CASE COMMANDS mode\n")
                logfile.close()
            free_command_input()
        else:
            print("\nFile: " + file_to_read + " not found")
            input('\nMake sure the file name is correct, and is in the path and retry. Press enter to return back to the menu: ')
            free_command_input()

    def delete_cases():
        gcp_system_log_file = 'gcp_system_log.log'
        with open(gcp_system_log_file, 'a') as logfile:
            logfile.write(str(now) + " <-- Accessed DELETE TEST CASES mode\n")
            logfile.close()
        test_case_string_var = "_cli_tst_k_s_"
        print('\nNOTE: only test case files containing syntax: ' + test_case_string_var + ' will be removed.')
        delete_test_cases=input("\nType the test case file to delete. If it is more than one, separate them with spaces: ")
        cases_to_delete = []
        for case in delete_test_cases.split():
            cases_to_delete.append(case)
        for case in cases_to_delete:
            if test_case_string_var in case:
                os.remove(gcp_scripts_dir+"/"+case)
                print('\nRemoved file: '+delete_test_cases)
                with open(gcp_system_log_file, 'a') as logfile:
                    logfile.write(str(now) + " - DELETED test case script: "+gcp_scripts_dir+"/"+case+"\n")
                    logfile.close()
        input('\nPress enter to get back to the main menu: ')
        with open(gcp_system_log_file, 'a') as logfile:
            logfile.write(str(now) + " <-- Exited DELETE TEST CASES mode\n")
            logfile.close()
        free_command_input()

    def delete_all_test_cases():
        gcp_system_log_file = 'gcp_system_log.log'
        with open(gcp_system_log_file, 'a') as logfile:
            logfile.write(str(now) + " <-- Accessed DELETE ALL TEST CASES mode\n")
            logfile.close()
        test_case_string_var = "_cli_tst_k_s_"
        dir_path = gcp_scripts_dir+"/"
        delete_all=input('\nWARNING. You are about to delete all the test cases. Confirm? y/n: ')
        if delete_all == 'y':
            for case in os.listdir(path=dir_path):
                if test_case_string_var in case:
                    os.remove(gcp_scripts_dir+"/"+case)
                    print('\nRemoved test case: '+case)
                    with open(gcp_system_log_file, 'a') as logfile:
                        logfile.write(str(now) + " DELETED test case script: "+gcp_scripts_dir+"/"+case+"\n")
                        logfile.close()
            enter=input('\nPress enter to get back to the main menu: ')
            with open(gcp_system_log_file, 'a') as logfile:
                logfile.write(str(now) + " <-- Accessed DELETE ALL TEST CASES mode\n")
                logfile.close()
            free_command_input()
        if delete_all == 'n':
            print('\nAborted deletion of all the test case files.')
            input('\nPress enter to get back to the main menu: ')
            with open(gcp_system_log_file, 'a') as logfile:
                logfile.write(str(now) + " <-- Exited DELETE ALL TEST CASES mode\n")
                logfile.close()
            free_command_input()
        else:
            delete_all_test_cases()
    print('Mode F accesed. Free command line input mode.\n')
    print("***************************************************************")
    print('      GCP FREE COMMAND LINE INPUT - SCRIPT/TEST CASE BUILDER  \n')
    print('1 - Build a new test case by directly inputting your commands')
    print('2 - Run test case/s')
    print('3 - Delete test case file/s')
    print('4 - Delete all test case files')
    print('5 - View saved test cases')
    print('6 - Read test case commands from file')
    print('c <- Compute engine module')
    print('b <- Back to Main menu')
    free_command_menu_selection=input('\nSelect an option from the menu and press enter: ')
    if free_command_menu_selection == '1':
        build_new_cli_test_case()
    if free_command_menu_selection == '2':
        run_test_cases()
    if free_command_menu_selection == '3':
        delete_cases()
    if free_command_menu_selection == '4':
        delete_all_test_cases()
    if free_command_menu_selection == '5':
        view_test_cases()
    if free_command_menu_selection == '6':
        reading_steps_from_file()
    if free_command_menu_selection == 'c':
        return_to_compute_menu()
    if free_command_menu_selection == 'b':
        return_to_main_menu()
    else:
        free_command_input()
free_command_input()
