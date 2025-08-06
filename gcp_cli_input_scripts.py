import os
import sys
import random
import runpy
import datetime
from datetime import datetime
import subprocess

gcp_system_log_file='gcp_system_log.log'  # System event log file var

def validate_gcloud_authentication():
    """Validate if user is authenticated with gcloud and has active project"""
    try:
        # Check if user is logged in
        auth_check_cmd = "gcloud auth list --filter=status:ACTIVE --format='value(account)'"
        result = subprocess.run(auth_check_cmd, shell=True, capture_output=True, text=True)
        
        if result.returncode != 0 or not result.stdout.strip():
            return False, None, None
            
        active_account = result.stdout.strip()
        
        # Check active project
        project_check_cmd = "gcloud config get-value project"
        result = subprocess.run(project_check_cmd, shell=True, capture_output=True, text=True)
        
        if result.returncode != 0:
            return True, active_account, None
            
        active_project = result.stdout.strip()
        if active_project and active_project != "(unset)":
            # ADDITIONAL CHECK: Test if authentication actually works with a resource access command
            test_cmd = f"gcloud projects describe {active_project} --format='value(projectId)' --quiet"
            test_result = subprocess.run(test_cmd, shell=True, capture_output=True, text=True)
            
            if test_result.returncode != 0:
                # Authentication validation failed - tokens might be expired
                if "refresh token has expired" in test_result.stderr.lower() or "invalid_grant" in test_result.stderr.lower():
                    # Definitely expired tokens
                    return False, None, None
                return False, None, None
            else:
                return True, active_account, active_project
        else:
            return True, active_account, None
            
    except Exception as e:
        return False, None, None

def check_authentication_before_test_execution():
    """Check authentication before running test cases and prompt user if needed"""
    print("🔐 Checking gcloud authentication before test execution...")
    
    is_authenticated, account, project = validate_gcloud_authentication()
    
    if not is_authenticated:
        print("❌ No active gcloud authentication found!")
        print("🚨 Test execution halted - authentication required!")
        print("\n" + "=" * 70)
        print("AUTHENTICATION REQUIRED")
        print("=" * 70)
        print("Please authenticate with gcloud before running test cases.")
        print("\nTo authenticate:")
        print("1. Return to Main Menu")
        print("2. Select option 'l' (Login/Authentication)")
        print("3. Use option 'l' (Login to gcloud)")
        print("4. Use option 'c' (Set active project)")
        print("=" * 70)
        
        choice = input("\nWould you like to return to the main menu to authenticate? (y/n): ").strip().lower()
        
        if choice == 'y':
            from gcp_python_interactive_cli_v2 import main_menu
            main_menu()
        else:
            print("⚠️ Test execution cancelled. Please authenticate to run test cases.")
            free_command_input()
        return False
    
    print(f"✅ Authenticated as: {account}")
    
    if not project:
        print("⚠️ Warning: No active project set!")
        print("💡 Some gcloud commands may fail without an active project.")
        print("\nTo set a project:")
        print("1. Main Menu → 'l' (Login/Authentication) → 'c' (Set active project)")
        
        continue_anyway = input("\nContinue test execution without active project? (y/n): ").strip().lower()
        if continue_anyway != 'y':
            choice = input("Return to main menu to set project? (y/n): ").strip().lower()
            if choice == 'y':
                from gcp_python_interactive_cli_v2 import main_menu
                main_menu()
            else:
                free_command_input()
            return False
    else:
        print(f"✅ Active project: {project}")
    
    print("🔓 Authentication validated - proceeding with test execution...\n")
    return True

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
            file.write(import_os_module+new_line+import_sys_module)
            file.close()
        with open(gcp_system_log_file, 'a') as logfile:
            logfile.write(str(now) + " + Created test case "+free_test_case_file_name)
            logfile.close()
        print('\nTest case ' + free_test_case_file_name + pyext + ' was created and is empty.\n')
        input("Press enter to continue: ")
        def add_more_commands():
            provide_command = input('\nPlease provide the desired gcloud command you wish to add to the script test case, and press enter: ')
            with open(gcp_scripts_dir+"/"+free_test_case_file_name+pyext, 'a') as file:
                file.write(new_line+print_string+left_bracket+quote+command_string+quote+right_bracket)
                file.write(new_line+os_system+left_bracket+quote+provide_command+quote+right_bracket)
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
        
        print('\n🚀 Run test case/s menu Accessed\n')
        
        # AUTHENTICATION CHECK - Validate before running any test cases
        if not check_authentication_before_test_execution():
            return  # Authentication failed, function handles user direction
        
        print('*' * 70)
        print('      ENHANCED TEST CASE RUNNER WITH LISTING FUNCTIONALITY')
        print('*' * 70)
        print()
        
        # Enhanced functionality: Use the function from menu 5 to list saved test cases first
        print("📋 AVAILABLE TEST CASES:")
        print("=" * 50)
        
        # Use the view_test_cases functionality but without returning to menu
        test_case_string_var="_cli_tst_k_s_"
        dir_path = os.path.dirname(os.path.realpath(__file__))
        available_test_cases = []
        
        print('🔍 Listing test cases in path: ' + dir_path + "/" + gcp_scripts_dir + '\n')
        
        try:
            for i, filename in enumerate(os.listdir(path=dir_path+"/"+gcp_scripts_dir), 1):
                if test_case_string_var in filename:
                    print(f"{i:2d}. 📄 {filename}")
                    available_test_cases.append(filename)
                    
            if not available_test_cases:
                print("📭 No test cases found with the pattern '_cli_tst_k_s_'")
                print("💡 Create test cases using menu option 1 first")
                input('\n⏎ Press enter to get back to the main menu: ')
                free_command_input()
                return
                
            print(f"\n📊 Total available test cases: {len(available_test_cases)}")
            
        except FileNotFoundError:
            print(f"📁 Directory {gcp_scripts_dir} not found. Please create test cases first.")
            input('\n⏎ Press enter to get back to the main menu: ')
            free_command_input()
            return
        
        print("\n" + "=" * 50)
        print("🎯 TEST CASE EXECUTION OPTIONS:")
        print("=" * 50)
        print("📝 You can now:")
        print("   • Enter the exact filename to run a specific test case")
        print("   • Enter the number (e.g., '1', '2', '3') to run by index")
        print("   • Enter 'all' to run all available test cases")
        print("   • Enter 'list' to refresh the list")
        print("   • Enter 'back' to return to main menu")
        print()
        
        while True:
            selection = input("👉 Enter your choice: ").strip()
            
            if selection.lower() == 'back':
                print("🔙 Returning to main menu...")
                free_command_input()
                return
            elif selection.lower() == 'list':
                print("🔄 Refreshing test case list...")
                run_test_cases()  # Recursive call to refresh the list
                return
            elif selection.lower() == 'all':
                print(f"\n🚀 Running all {len(available_test_cases)} test cases...")
                print("=" * 60)
                for i, test_case in enumerate(available_test_cases, 1):
                    print(f"\n📋 Executing Test Case {i}/{len(available_test_cases)}: {test_case}")
                    print("-" * 40)
                    try:
                        runpy.run_path(path_name=gcp_scripts_dir+"/"+test_case)
                        print(f"✅ Test case {test_case} completed successfully!")
                        with open(gcp_system_log_file, 'a') as logfile:
                            logfile.write(str(datetime.now()) + f" ! Executed test case script: {gcp_scripts_dir}/{test_case}\n")
                            logfile.close()
                    except Exception as e:
                        print(f"❌ Error running {test_case}: {str(e)}")
                        with open(gcp_system_log_file, 'a') as logfile:
                            logfile.write(str(datetime.now()) + f" - ERROR: Failed to run {test_case}: {str(e)}\n")
                            logfile.close()
                    print("-" * 40)
                
                print(f"\n🎉 Completed execution of all {len(available_test_cases)} test cases!")
                timestamp()
                break
                
            elif selection.isdigit():
                test_index = int(selection)
                if 1 <= test_index <= len(available_test_cases):
                    test_case_run = available_test_cases[test_index - 1]
                    print(f"\n🎯 Selected test case #{test_index}: {test_case_run}")
                    print(f"🚀 Attempting to run test case {test_case_run}...")
                    print("=" * 50)
                    
                    try:
                        runpy.run_path(path_name=gcp_scripts_dir+"/"+test_case_run)
                        print(f"\n✅ Test case {test_case_run} executed successfully!")
                        with open(gcp_system_log_file, 'a') as logfile:
                            logfile.write(str(datetime.now()) + " ! Executed test case script: "+gcp_scripts_dir+"/"+test_case_run+"\n")
                            logfile.close()
                        timestamp()
                    except Exception as e:
                        print(f"❌ Error running test case: {str(e)}")
                        with open(gcp_system_log_file, 'a') as logfile:
                            logfile.write(str(datetime.now()) + " - ERROR: Unable to run test case script: "+gcp_scripts_dir+"/"+test_case_run+f". Error: {str(e)}\n")
                            logfile.close()
                    break
                else:
                    print(f"❌ Invalid selection. Please enter a number between 1 and {len(available_test_cases)}")
                    continue
            else:
                # Treat as filename
                test_case_run = selection
                print(f"\n🎯 Attempting to run test case: {test_case_run}")
                
                if test_case_run in available_test_cases:
                    print("=" * 50)
                    try:
                        runpy.run_path(path_name=gcp_scripts_dir+"/"+test_case_run)
                        print(f"\n✅ Test case {test_case_run} executed successfully!")
                        with open(gcp_system_log_file, 'a') as logfile:
                            logfile.write(str(datetime.now()) + " ! Executed test case script: "+gcp_scripts_dir+"/"+test_case_run+"\n")
                            logfile.close()
                        timestamp()
                    except Exception as e:
                        print(f"❌ Error running test case: {str(e)}")
                        with open(gcp_system_log_file, 'a') as logfile:
                            logfile.write(str(datetime.now()) + " - ERROR: Unable to run test case script: "+gcp_scripts_dir+"/"+test_case_run+f". Error: {str(e)}\n")
                            logfile.close()
                    break
                else:
                    print(f"❌ Test case '{test_case_run}' not found in available test cases.")
                    print("💡 Available test cases are listed above. Try again or enter 'list' to refresh.")
                    continue
        
        # Ask if user wants to run another test case
        print(f"\n{'='*50}")
        run_another = input("🔄 Would you like to run another test case? (y/n): ").strip().lower()
        if run_another == 'y':
            run_test_cases()  # Recursive call to run another test case
        else:
            print("🏁 Test case execution session completed.")
            input('\n⏎ Press enter to get back to the main menu: ')
            with open(gcp_system_log_file, 'a') as logfile:
                logfile.write(str(now) + " <-- Exited RUN CLI TEST CASE mode\n")
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

    def read_script_code():
        try:
            gcp_system_log_file = 'gcp_system_log.log'
            now = datetime.now()
            with open(gcp_system_log_file, 'a') as logfile:
                logfile.write(str(now) + " --> Accessed Read script code mode\n")
                logfile.close()
            file_to_read=input('\nProvide file name to read: ')
            if file_to_read == "":
                print('\nYou tiped nothing. Type a valid script name to read code from.')
                read_script_code()
            print("\nViewing all code in file: "+file_to_read+'\n')
            with open(gcp_scripts_dir+"/"+file_to_read, 'r') as filedata:     # Opening the given file in read-only mode
               for line in filedata:
                    print(line)
            filedata.close()
            input("\nPress enter to get back to the menu: ")
            now = datetime.now()
            with open(gcp_system_log_file, 'a') as logfile:
                logfile.write(str(now) + " - Read test case code in path: "+gcp_scripts_dir+"\n")
                logfile.close()
            now = datetime.now()
            with open(gcp_system_log_file, 'a') as logfile:
                logfile.write(str(now) + " <-- Exited Read script code mode\n")
                logfile.close()
            free_command_input()
        except:
            print(str(now) + " ! ERROR: "+file_to_read+" was not found or was moved from path"+gcp_system_log_file+". Unable to read.\n")
            now = datetime.now()
            with open(gcp_system_log_file, 'a') as logfile:
                logfile.write(str(now) + " ! ERROR: "+file_to_read+" was not found or was moved from path"+gcp_system_log_file+". Unable to read.\n")
                logfile.close()
            input('\nPress enter to get back to the menu: ')
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
    print('7 - View all code in file. Shows entire file content')
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
    if free_command_menu_selection == '7':
        read_script_code()
    if free_command_menu_selection == 'c':
        return_to_compute_menu()
    if free_command_menu_selection == 'b':
        return_to_main_menu()
    else:
        free_command_input()
free_command_input()
