import os
import runpy
import sys
import random
import importlib
import subprocess
import re
from datetime import datetime

gcp_scripts_dir='gcp_automation_test_scripts'
test_logs_dir='gcp_test_case_logs'

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
        print("❌ Authentication failed - gcloud tokens may be expired!")
        print("🚨 Test execution halted - authentication required!")
        print("\n" + "=" * 70)
        print("AUTHENTICATION REQUIRED - TOKEN REFRESH NEEDED")
        print("=" * 70)
        print("Your gcloud authentication tokens have expired or are invalid.")
        print("\nTo fix this:")
        print("1. Return to Main Menu")
        print("2. Select option 'l' (Login/Authentication)")
        print("3. Use option 'l' (Login to gcloud) - this will refresh your tokens")
        print("4. Or run: gcloud auth login")
        print("5. Then use option 'c' (Set active project) if needed")
        print("=" * 70)
        
        choice = input("\nWould you like to return to the main menu to authenticate? (y/n): ").strip().lower()
        
        if choice == 'y':
            from gcp_python_interactive_cli_v2 import main_menu
            main_menu()
        else:
            print("⚠️ Test execution cancelled. Please authenticate to run test cases.")
            test_case_module()
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
                test_case_module()
            return False
    else:
        print(f"✅ Active project: {project}")
    
    print("🔓 Authentication validated - proceeding with test execution...\n")
    return True

def generate_command_delimiters(step_description, gcloud_command):
    """Generate start and end delimiters for gcloud commands"""
    delimiter_line = "=" * 80
    timestamp_func = "datetime.now().strftime('%Y-%m-%d %H:%M:%S')"
    
    start_delimiter = f"""
print("{delimiter_line}")
print(f"🚀 EXECUTING: {step_description}")
print(f"📋 Command: {gcloud_command}")
print(f"⏰ Started at: {{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}}")
print("{delimiter_line}")
"""
    
    end_delimiter = f"""
print("{delimiter_line}")
print(f"✅ COMPLETED: {step_description}")
print(f"⏰ Finished at: {{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}}")
print("{delimiter_line}")
print()
"""
    
    return start_delimiter, end_delimiter

def return_to_main_menu():
    from gcp_python_interactive_cli_v2 import main_menu
    main_menu()

def return_to_compute_menu():
    from gcp_python_interactive_cli_v2 import compute_engine_module
    compute_engine_module()

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
    global gcp_system_log_file
    gcp_system_log_file = 'gcp_system_log.log'
    now = datetime.now()
    with open(gcp_system_log_file, 'a') as logfile:
        logfile.write(str(now) + " --> Accessed TEST CASE MAIN MENU mode\n")
        logfile.close()
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
    print('1 - Retrieve project billing data')
    print('2 - Describe a project')
    print('3 - Get configuration list - Lists account name and project data')
    print('4 - Get active project')
    print('5 - Set another project')
    print('6 - Get a list of all projects')
    print('7 - Get a list of all organizations')
    print('b - < Back to test case module menu')
    selection=input('\nPlease provide the action item you want to add to the test case.\nType a number or letter from the menu and press enter to operate: ')
    if selection == '1':
        with open (gcp_scripts_dir+"/"+test_case_file_name+pyext, 'a') as file:
            def m2_build_python_case_file():
                gcp_system_log_file = 'gcp_system_log.log'
                now = datetime.now()
                with open(gcp_system_log_file, 'a') as logfile:
                    logfile.write(str(now) + " --> Accessed Retrieve billing project data mode\n")
                    logfile.close()
                step_string_var="step_string"
                step_string="Step: Main menu: - 1 - Retrieve billing data for a project"
                project_name=input("\nProvide a valid project name to retrieve in the script: ")
                project_name_var="project_name"
                new_line=('\n')
                file.write(new_line+step_string_var+equals+quote+step_string+quote+new_line)
                file.write(print_string+left_bracket+quote+quote+right_bracket+new_line)
                file.write(print_string+left_bracket+quote+running+space+quote+plus+step_string_var+plus+quote+dots+quote+right_bracket+new_line)
                file.write(new_line+"project_name="+quote+project_name+quote+new_line)
                
                # Add start delimiter
                delimiter_line = "=" * 80
                file.write(new_line+print_string+left_bracket+quote+delimiter_line+quote+right_bracket+new_line)
                file.write(print_string+left_bracket+quote+"🚀 EXECUTING: Retrieve billing data for project"+quote+right_bracket+new_line)
                file.write(print_string+left_bracket+"f"+quote+"📋 Command: gcloud beta billing projects describe {project_name}"+quote+right_bracket+new_line)
                file.write(print_string+left_bracket+"f"+quote+"⏰ Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"+quote+right_bracket+new_line)
                file.write(print_string+left_bracket+quote+delimiter_line+quote+right_bracket+new_line)
                
                # Original command execution
                file.write(os_system+left_bracket+quote+gcloud_billing_project_describe+quote+plus+project_name_var+right_bracket+new_line)
                
                # Add end delimiter
                file.write(print_string+left_bracket+quote+delimiter_line+quote+right_bracket+new_line)
                file.write(print_string+left_bracket+quote+"✅ COMPLETED: Retrieve billing data for project"+quote+right_bracket+new_line)
                file.write(print_string+left_bracket+"f"+quote+"⏰ Finished at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"+quote+right_bracket+new_line)
                file.write(print_string+left_bracket+quote+delimiter_line+quote+right_bracket+new_line)
                file.write(print_string+left_bracket+quote+quote+right_bracket+new_line)
                file.close()
                print('\nAdded '+step_string)
                now = datetime.now()
                with open(gcp_system_log_file, 'a') as logfile:
                    logfile.write(str(now) + " + Step added to script: "+test_case_file_name+pyext+" - Retrieve billing data for project name: "+project_name+"\n")
                    logfile.close()
                now = datetime.now()
                with open(gcp_system_log_file, 'a') as logfile:
                    logfile.write(str(now) + " <-- Exited Retrieve billing project data mode\n")
                    logfile.close()
            m2_build_python_case_file()
        add_another_step_main_menu()
    if selection == '2':
        with open (gcp_scripts_dir+"/"+test_case_file_name+pyext, 'a') as file:
            def m4_build_python_case_file():
                now = datetime.now()
                with open(gcp_system_log_file, 'a') as logfile:
                    logfile.write(str(now) + " --> Accessed Describe project data mode\n")
                    logfile.close()
                step_string_var="step_string"
                step_string="Step: Main menu: - 2 - Describe a project"
                project_name=input("\nProvide a valid project name to describe in the script: ")
                project_name_var="project_name"
                new_line=('\n')
                file.write(new_line+step_string_var+equals+quote+step_string+quote+new_line)
                file.write(print_string+left_bracket+quote+quote+right_bracket+new_line)
                file.write(print_string+left_bracket+quote+running+space+quote+plus+step_string_var+plus+quote+dots+quote+right_bracket+new_line)
                file.write(new_line+project_name_var+equals+quote+project_name+quote+new_line)
                
                # Add start delimiter
                delimiter_line = "=" * 80
                file.write(new_line+print_string+left_bracket+quote+delimiter_line+quote+right_bracket+new_line)
                file.write(print_string+left_bracket+quote+"🚀 EXECUTING: Describe project"+quote+right_bracket+new_line)
                file.write(print_string+left_bracket+"f"+quote+"📋 Command: gcloud projects describe {project_name}"+quote+right_bracket+new_line)
                file.write(print_string+left_bracket+"f"+quote+"⏰ Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"+quote+right_bracket+new_line)
                file.write(print_string+left_bracket+quote+delimiter_line+quote+right_bracket+new_line)
                
                # Original command execution
                file.write(os_system+left_bracket+quote+gcloud_projects_describe+quote+plus+project_name_var+right_bracket+new_line)
                
                # Add end delimiter
                file.write(print_string+left_bracket+quote+delimiter_line+quote+right_bracket+new_line)
                file.write(print_string+left_bracket+quote+"✅ COMPLETED: Describe project"+quote+right_bracket+new_line)
                file.write(print_string+left_bracket+"f"+quote+"⏰ Finished at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"+quote+right_bracket+new_line)
                file.write(print_string+left_bracket+quote+delimiter_line+quote+right_bracket+new_line)
                file.write(print_string+left_bracket+quote+quote+right_bracket+new_line)
                file.close()
                print('\nAdded '+step_string)
                now = datetime.now()
                with open(gcp_system_log_file, 'a') as logfile:
                    logfile.write(str(now) + " + Step added to script: "+test_case_file_name+pyext+" - Describe project: "+project_name+"\n")
                    logfile.close()
                now = datetime.now()
                with open(gcp_system_log_file, 'a') as logfile:
                    logfile.write(str(now) + " <-- Exited Describe project data mode\n")
                    logfile.close()
            m4_build_python_case_file()
        add_another_step_main_menu()
    if selection == '3':
        with open (gcp_scripts_dir+"/"+test_case_file_name+pyext, 'a') as file:
            def m5_build_python_case_file():
                now = datetime.now()
                with open(gcp_system_log_file, 'a') as logfile:
                    logfile.write(str(now) + " --> Accessed Get configuration list mode\n")
                    logfile.close()
                step_string_var="step_string"
                step_string="Step: Main menu: - 3 - Get configuration list - Lists account name and project data"
                new_line=('\n')
                file.write(new_line+step_string_var+equals+quote+step_string+quote+new_line)
                file.write(print_string+left_bracket+quote+quote+right_bracket+new_line)
                file.write(print_string+left_bracket+quote+running+space+quote+plus+step_string_var+plus+quote+dots+quote+right_bracket+new_line)
                
                # Add start delimiter
                delimiter_line = "=" * 80
                file.write(new_line+print_string+left_bracket+quote+delimiter_line+quote+right_bracket+new_line)
                file.write(print_string+left_bracket+quote+"🚀 EXECUTING: Get configuration list"+quote+right_bracket+new_line)
                file.write(print_string+left_bracket+quote+"📋 Command: gcloud config configurations list"+quote+right_bracket+new_line)
                file.write(print_string+left_bracket+"f"+quote+"⏰ Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"+quote+right_bracket+new_line)
                file.write(print_string+left_bracket+quote+delimiter_line+quote+right_bracket+new_line)
                
                # Original command execution
                file.write(os_system+left_bracket+quote+gcloud_config_configurations_list+quote+right_bracket+new_line)
                
                # Add end delimiter
                file.write(print_string+left_bracket+quote+delimiter_line+quote+right_bracket+new_line)
                file.write(print_string+left_bracket+quote+"✅ COMPLETED: Get configuration list"+quote+right_bracket+new_line)
                file.write(print_string+left_bracket+"f"+quote+"⏰ Finished at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"+quote+right_bracket+new_line)
                file.write(print_string+left_bracket+quote+delimiter_line+quote+right_bracket+new_line)
                file.write(print_string+left_bracket+quote+quote+right_bracket+new_line)
                file.close()
                print('\nAdded '+step_string)
                now = datetime.now()
                with open(gcp_system_log_file, 'a') as logfile:
                    logfile.write(str(now) + " + Step added to script: "+test_case_file_name+pyext+" - Get configuration list\n")
                    logfile.close()
                now = datetime.now()
                with open(gcp_system_log_file, 'a') as logfile:
                    logfile.write(str(now) + " <-- Exited Get configuration list mode\n")
                    logfile.close()
            m5_build_python_case_file()
        add_another_step_main_menu()
    if selection == '4':
        with open (gcp_scripts_dir+"/"+test_case_file_name+pyext, 'a') as file:
            def m6_build_python_case_file():
                now = datetime.now()
                with open(gcp_system_log_file, 'a') as logfile:
                    logfile.write(str(now) + " --> Accessed Get active project mode\n")
                    logfile.close()
                step_string_var="step_string"
                step_string="Step: Main menu: - 4 - Get active project"
                new_line=('\n')
                file.write(new_line+step_string_var+equals+quote+step_string+quote+new_line)
                file.write(print_string+left_bracket+quote+quote+right_bracket+new_line)
                file.write(print_string+left_bracket+quote+running+space+quote+plus+step_string_var+plus+quote+dots+quote+right_bracket+new_line)
                file.write(print_string+left_bracket+quote+'Getting active project... '+quote+right_bracket+new_line+new_line)
                
                # Generate authentication validation code
                file.write(new_line + '# Authentication validation before gcloud command execution' + new_line)
                file.write('import subprocess' + new_line)
                file.write('def validate_auth():' + new_line)
                file.write('    try:' + new_line)
                file.write('        result = subprocess.run("gcloud config get-value project", shell=True, capture_output=True, text=True)' + new_line)
                file.write('        if result.returncode != 0:' + new_line)
                file.write('            return False' + new_line)
                file.write('        project = result.stdout.strip()' + new_line)
                file.write('        if not project or project == "(unset)":' + new_line)
                file.write('            return False' + new_line)
                file.write('        test_result = subprocess.run(f"gcloud projects describe {project} --format=\\\"value(projectId)\\\" --quiet", shell=True, capture_output=True, text=True)' + new_line)
                file.write('        return test_result.returncode == 0' + new_line)
                file.write('    except:' + new_line)
                file.write('        return False' + new_line)
                file.write(new_line + 'import sys' + new_line)
                file.write('sys.stdout.flush()' + new_line)
                file.write('if validate_auth():' + new_line)
                file.write('    # Add start delimiter with timestamp' + new_line)
                file.write('    print("=" * 60)' + new_line)
                file.write('    print("🚀 START COMMAND EXECUTION - " + datetime.now().strftime("%Y-%m-%d %H:%M:%S"))' + new_line)
                file.write('    print("Command: ' + gcloud_config_get_value_project + '")' + new_line)
                file.write('    print("=" * 60)' + new_line)
                file.write('    # Capture command output and display it between delimiters' + new_line)
                file.write('    result = subprocess.run("' + gcloud_config_get_value_project + '", shell=True, capture_output=True, text=True)' + new_line)
                file.write('    if result.stdout:' + new_line)
                file.write('        print(result.stdout.strip())' + new_line)
                file.write('    if result.stderr:' + new_line)
                file.write('        print(f"STDERR: {result.stderr.strip()}")' + new_line)
                file.write('    # Add end delimiter with timestamp' + new_line)
                file.write('    print("=" * 60)' + new_line)
                file.write('    print("✅ END COMMAND EXECUTION - " + datetime.now().strftime("%Y-%m-%d %H:%M:%S"))' + new_line)
                file.write('    print(f"Command completed with return code: {result.returncode}")' + new_line)
                file.write('    print("=" * 60)' + new_line)
                file.write('else:' + new_line)
                file.write('    print("❌ Authentication failed! Please authenticate using: gcloud auth login")' + new_line)
                file.write('    print("🚫 Command execution cancelled due to authentication failure")' + new_line)
                file.close()
                print('\nAdded '+step_string)
                now = datetime.now()
                with open(gcp_system_log_file, 'a') as logfile:
                    logfile.write(str(now) + " + Step added to script: Get active project\n")
                    logfile.close()
                now = datetime.now()
                with open(gcp_system_log_file, 'a') as logfile:
                    logfile.write(str(now) + " <-- Exited Get active project mode\n")
                    logfile.close()
            m6_build_python_case_file()
        add_another_step_main_menu()
    if selection == '5':
        with open (gcp_scripts_dir+"/"+test_case_file_name+pyext, 'a') as file:
            def m8_build_python_case_file():
                now = datetime.now()
                with open(gcp_system_log_file, 'a') as logfile:
                    logfile.write(str(now) + " --> Accessed Set project mode\n")
                    logfile.close()
                step_string_var="step_string"
                step_string="Step: Main menu: - 5 - Set a project"
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
                now = datetime.now()
                with open(gcp_system_log_file, 'a') as logfile:
                    logfile.write(str(now) + " + Step added to script: Set active project: "+project_name+"\n")
                    logfile.close()
                now = datetime.now()
                with open(gcp_system_log_file, 'a') as logfile:
                    logfile.write(str(now) + " <-- Exited Set project mode\n")
                    logfile.close()
            m8_build_python_case_file()
        add_another_step_main_menu()
    if selection == '6':
        with open (gcp_scripts_dir+"/"+test_case_file_name+pyext, 'a') as file:
            def m9_build_python_case_file():
                now = datetime.now()
                with open(gcp_system_log_file, 'a') as logfile:
                    logfile.write(str(now) + " --> Accessed Get projects list mode\n")
                    logfile.close()
                step_string_var="step_string"
                step_string="Step: Main menu: - 6 - Get a list of all projects"
                new_line=('\n')
                file.write(new_line+step_string_var+equals+quote+step_string+quote+new_line)
                file.write(print_string+left_bracket+quote+quote+right_bracket+new_line)
                file.write(print_string+left_bracket+quote+running+space+quote+plus+step_string_var+plus+quote+dots+quote+right_bracket+new_line)
                file.write(print_string+left_bracket+quote+'Listing all projects... '+quote+right_bracket+new_line+new_line)
                
                # Generate authentication validation code
                file.write(new_line + '# Authentication validation before gcloud command execution' + new_line)
                file.write('import subprocess' + new_line)
                file.write('def validate_auth():' + new_line)
                file.write('    try:' + new_line)
                file.write('        result = subprocess.run("gcloud config get-value project", shell=True, capture_output=True, text=True)' + new_line)
                file.write('        if result.returncode != 0:' + new_line)
                file.write('            return False' + new_line)
                file.write('        project = result.stdout.strip()' + new_line)
                file.write('        if not project or project == "(unset)":' + new_line)
                file.write('            return False' + new_line)
                file.write('        test_result = subprocess.run(f"gcloud projects describe {project} --format=\\\"value(projectId)\\\" --quiet", shell=True, capture_output=True, text=True)' + new_line)
                file.write('        return test_result.returncode == 0' + new_line)
                file.write('    except:' + new_line)
                file.write('        return False' + new_line)
                file.write(new_line + 'import sys' + new_line)
                file.write('sys.stdout.flush()' + new_line)
                file.write('if validate_auth():' + new_line)
                file.write('    # Add start delimiter with timestamp' + new_line)
                file.write('    print("=" * 60)' + new_line)
                file.write('    print("🚀 START COMMAND EXECUTION - " + datetime.now().strftime("%Y-%m-%d %H:%M:%S"))' + new_line)
                file.write('    print("Command: ' + gcloud_projects_list + '")' + new_line)
                file.write('    print("=" * 60)' + new_line)
                file.write('    # Capture command output and display it between delimiters' + new_line)
                file.write('    result = subprocess.run("' + gcloud_projects_list + '", shell=True, capture_output=True, text=True)' + new_line)
                file.write('    if result.stdout:' + new_line)
                file.write('        print(result.stdout.strip())' + new_line)
                file.write('    if result.stderr:' + new_line)
                file.write('        print(f"STDERR: {result.stderr.strip()}")' + new_line)
                file.write('    # Add end delimiter with timestamp' + new_line)
                file.write('    print("=" * 60)' + new_line)
                file.write('    print("✅ END COMMAND EXECUTION - " + datetime.now().strftime("%Y-%m-%d %H:%M:%S"))' + new_line)
                file.write('    print(f"Command completed with return code: {result.returncode}")' + new_line)
                file.write('    print("=" * 60)' + new_line)
                file.write('else:' + new_line)
                file.write('    print("❌ Authentication failed! Please authenticate using: gcloud auth login")' + new_line)
                file.write('    print("🚫 Command execution cancelled due to authentication failure")' + new_line)
                file.close()
                now = datetime.now()
                print('\nAdded '+step_string)
                with open(gcp_system_log_file, 'a') as logfile:
                    logfile.write(str(now) + " + Step added to script: List all projects\n")
                    logfile.close()
                now = datetime.now()
                with open(gcp_system_log_file, 'a') as logfile:
                    logfile.write(str(now) + " <-- Exited Get projects list mode\n")
                    logfile.close()
            m9_build_python_case_file()
        add_another_step_main_menu()
    if selection == '7':
        with open (gcp_scripts_dir+"/"+test_case_file_name+pyext, 'a') as file:
            def m10_build_python_case_file():
                now = datetime.now()
                with open(gcp_system_log_file, 'a') as logfile:
                    logfile.write(str(now) + " --> Accessed List organizations mode\n")
                    logfile.close()
                step_string_var="step_string"
                step_string="Step: Main menu: - 7 - Get a list of all organizations"
                new_line=('\n')
                file.write(new_line+step_string_var+equals+quote+step_string+quote+new_line)
                file.write(print_string+left_bracket+quote+quote+right_bracket+new_line)
                file.write(print_string+left_bracket+quote+running+space+quote+plus+step_string_var+plus+quote+dots+quote+right_bracket+new_line)
                file.write(print_string+left_bracket+quote+'Listing all organizations... '+quote+right_bracket+new_line+new_line)
                
                # Generate authentication validation code
                file.write(new_line + '# Authentication validation before gcloud command execution' + new_line)
                file.write('import subprocess' + new_line)
                file.write('def validate_auth():' + new_line)
                file.write('    try:' + new_line)
                file.write('        result = subprocess.run("gcloud config get-value project", shell=True, capture_output=True, text=True)' + new_line)
                file.write('        if result.returncode != 0:' + new_line)
                file.write('            return False' + new_line)
                file.write('        project = result.stdout.strip()' + new_line)
                file.write('        if not project or project == "(unset)":' + new_line)
                file.write('            return False' + new_line)
                file.write('        test_result = subprocess.run(f"gcloud projects describe {project} --format=\\\"value(projectId)\\\" --quiet", shell=True, capture_output=True, text=True)' + new_line)
                file.write('        return test_result.returncode == 0' + new_line)
                file.write('    except:' + new_line)
                file.write('        return False' + new_line)
                file.write(new_line + 'import sys' + new_line)
                file.write('sys.stdout.flush()' + new_line)
                file.write('if validate_auth():' + new_line)
                file.write('    # Add start delimiter with timestamp' + new_line)
                file.write('    print("=" * 60)' + new_line)
                file.write('    print("🚀 START COMMAND EXECUTION - " + datetime.now().strftime("%Y-%m-%d %H:%M:%S"))' + new_line)
                file.write('    print("Command: ' + gcloud_organizations_list + '")' + new_line)
                file.write('    print("=" * 60)' + new_line)
                file.write('    # Capture command output and display it between delimiters' + new_line)
                file.write('    result = subprocess.run("' + gcloud_organizations_list + '", shell=True, capture_output=True, text=True)' + new_line)
                file.write('    if result.stdout:' + new_line)
                file.write('        print(result.stdout.strip())' + new_line)
                file.write('    if result.stderr:' + new_line)
                file.write('        print(f"STDERR: {result.stderr.strip()}")' + new_line)
                file.write('    # Add end delimiter with timestamp' + new_line)
                file.write('    print("=" * 60)' + new_line)
                file.write('    print("✅ END COMMAND EXECUTION - " + datetime.now().strftime("%Y-%m-%d %H:%M:%S"))' + new_line)
                file.write('    print(f"Command completed with return code: {result.returncode}")' + new_line)
                file.write('    print("=" * 60)' + new_line)
                file.write('else:' + new_line)
                file.write('    print("❌ Authentication failed! Please authenticate using: gcloud auth login")' + new_line)
                file.write('    print("🚫 Command execution cancelled due to authentication failure")' + new_line)
                file.close()
                print('\nAdded '+step_string)
                now = datetime.now()
                with open(gcp_system_log_file, 'a') as logfile:
                    logfile.write(str(now) + " + Step added to script: List all organizations\n")
                    logfile.close()
                now = datetime.now()
                with open(gcp_system_log_file, 'a') as logfile:
                    logfile.write(str(now) + " <-- Exited List organizations mode\n")
                    logfile.close()
            m10_build_python_case_file()
        add_another_step_main_menu()
    if selection == 'b':
        test_case_module()
    else:
        input('\nInvalid option provided. Press enter to get back to the main menu.')
        with open(gcp_system_log_file, 'a') as logfile:
            logfile.write(str(now) + " ! - ERROR: Invalid option provided in menu \n")
            logfile.close()
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
    selection = input('\nPlease provide the action item you want to add to the test case.\nType a number or letter from the menu and press enter to operate: ')
    if selection == '1':
        with open(gcp_scripts_dir+"/"+test_case_file_name+pyext, 'a') as file:
            def c1_build_python_case_file():
                gcp_system_log_file = 'gcp_system_log.log'
                now = datetime.now()
                with open(gcp_system_log_file, 'a') as logfile:
                    logfile.write(str(now) + " --> Accessed List zones mode\n")
                    logfile.close()
                step_string_var = "step_string"
                step_string = "Step: Compute menu: - 1 - List zones"
                new_line = ('\n')
                file.write(new_line+step_string_var+equals+quote+step_string+quote+new_line)
                file.write(print_string+left_bracket+quote+quote+right_bracket+new_line)
                file.write(print_string+left_bracket+quote+running+space+quote+plus+step_string_var+plus+quote+dots+quote+right_bracket+new_line)
                file.write(print_string+left_bracket+quote+'Listing compute zones: '+quote+right_bracket+new_line)
                
                # Generate authentication validation code
                file.write(new_line + '# Authentication validation before gcloud command execution' + new_line)
                file.write('import subprocess' + new_line)
                file.write('def validate_auth():' + new_line)
                file.write('    try:' + new_line)
                file.write('        result = subprocess.run("gcloud config get-value project", shell=True, capture_output=True, text=True)' + new_line)
                file.write('        if result.returncode != 0:' + new_line)
                file.write('            return False' + new_line)
                file.write('        project = result.stdout.strip()' + new_line)
                file.write('        if not project or project == "(unset)":' + new_line)
                file.write('            return False' + new_line)
                file.write('        test_result = subprocess.run(f"gcloud projects describe {project} --format=\\\"value(projectId)\\\" --quiet", shell=True, capture_output=True, text=True)' + new_line)
                file.write('        return test_result.returncode == 0' + new_line)
                file.write('    except:' + new_line)
                file.write('        return False' + new_line)
                file.write(new_line + 'import sys' + new_line)
                file.write('sys.stdout.flush()' + new_line)
                file.write('if validate_auth():' + new_line)
                file.write('    # Add start delimiter with timestamp' + new_line)
                file.write('    print("=" * 60)' + new_line)
                file.write('    print("🚀 START COMMAND EXECUTION - " + datetime.now().strftime("%Y-%m-%d %H:%M:%S"))' + new_line)
                file.write('    print("Command: ' + gcloud_compute_list_zones + '")' + new_line)
                file.write('    print("=" * 60)' + new_line)
                file.write('    # Capture command output and display it between delimiters' + new_line)
                file.write('    result = subprocess.run("' + gcloud_compute_list_zones + '", shell=True, capture_output=True, text=True)' + new_line)
                file.write('    if result.stdout:' + new_line)
                file.write('        print(result.stdout.strip())' + new_line)
                file.write('    if result.stderr:' + new_line)
                file.write('        print(f"STDERR: {result.stderr.strip()}")' + new_line)
                file.write('    # Add end delimiter with timestamp' + new_line)
                file.write('    print("=" * 60)' + new_line)
                file.write('    print("✅ END COMMAND EXECUTION - " + datetime.now().strftime("%Y-%m-%d %H:%M:%S"))' + new_line)
                file.write('    print(f"Command completed with return code: {result.returncode}")' + new_line)
                file.write('    print("=" * 60)' + new_line)
                file.write('else:' + new_line)
                file.write('    print("❌ Authentication failed! Please authenticate using: gcloud auth login")' + new_line)
                file.write('    print("🚫 Command execution cancelled due to authentication failure")' + new_line)
                file.close()
                print('\nAdded ' + step_string)
                now = datetime.now()
                with open(gcp_system_log_file, 'a') as logfile:
                    logfile.write(str(now) + " + Step added to script: "+test_case_file_name+pyext+" - List compute zones\n")
                    logfile.close()
                now = datetime.now()
                with open(gcp_system_log_file, 'a') as logfile:
                    logfile.write(str(now) + " <-- Exited List zones mode\n")
                    logfile.close()
            c1_build_python_case_file()
        add_another_step_compute_menu()
    if selection == '2':
        with open(gcp_scripts_dir+"/"+test_case_file_name+pyext, 'a') as file:
            def c2_build_python_case_file():
                gcp_system_log_file = 'gcp_system_log.log'
                now = datetime.now()
                with open(gcp_system_log_file, 'a') as logfile:
                    logfile.write(str(now) + " --> Accessed Describe zone mode\n")
                    logfile.close()
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
                now = datetime.now()
                with open(gcp_system_log_file, 'a') as logfile:
                    logfile.write(str(now) + " + Step added to script: "+test_case_file_name+pyext+" - Describe zone: "+zone_to_describe+"\n")
                    logfile.close()
                now = datetime.now()
                with open(gcp_system_log_file, 'a') as logfile:
                    logfile.write(str(now) + " <-- Exited Describe zone mode\n")
                    logfile.close()
            c2_build_python_case_file()
        add_another_step_compute_menu()
    if selection == '3':
        with open(gcp_scripts_dir+"/"+test_case_file_name+pyext, 'a') as file:
            def c3_build_python_case_file():
                gcp_system_log_file = 'gcp_system_log.log'
                now = datetime.now()
                with open(gcp_system_log_file, 'a') as logfile:
                    logfile.write(str(now) + " --> Accessed List running vms mode\n")
                    logfile.close()
                step_string_var = "step_string"
                step_string = "Step: Compute menu: - 3 - List running vms - os-instances"
                new_line = ('\n')
                file.write(new_line+step_string_var+equals+quote+step_string+quote+new_line)
                file.write(print_string+left_bracket+quote+quote+right_bracket+new_line)
                file.write(print_string+left_bracket+quote+running+space+quote+plus+step_string_var+plus+quote+dots+quote+right_bracket+new_line)
                file.write(print_string+left_bracket+quote+'Listing running os instances: '+quote+right_bracket+new_line)
                
                # Generate authentication validation code
                file.write(new_line + '# Authentication validation before gcloud command execution' + new_line)
                file.write('import subprocess' + new_line)
                file.write('def validate_auth():' + new_line)
                file.write('    try:' + new_line)
                file.write('        result = subprocess.run("gcloud config get-value project", shell=True, capture_output=True, text=True)' + new_line)
                file.write('        if result.returncode != 0:' + new_line)
                file.write('            return False' + new_line)
                file.write('        project = result.stdout.strip()' + new_line)
                file.write('        if not project or project == "(unset)":' + new_line)
                file.write('            return False' + new_line)
                file.write('        test_result = subprocess.run(f"gcloud projects describe {project} --format=\\\"value(projectId)\\\" --quiet", shell=True, capture_output=True, text=True)' + new_line)
                file.write('        return test_result.returncode == 0' + new_line)
                file.write('    except:' + new_line)
                file.write('        return False' + new_line)
                file.write(new_line + 'import sys' + new_line)
                file.write('sys.stdout.flush()' + new_line)
                file.write('if validate_auth():' + new_line)
                file.write('    # Add start delimiter with timestamp' + new_line)
                file.write('    print("=" * 60)' + new_line)
                file.write('    print("🚀 START COMMAND EXECUTION - " + datetime.now().strftime("%Y-%m-%d %H:%M:%S"))' + new_line)
                file.write('    print("Command: ' + gcloud_compute_instances_os_inventory_list_instances + '")' + new_line)
                file.write('    print("=" * 60)' + new_line)
                file.write('    # Capture command output and display it between delimiters' + new_line)
                file.write('    result = subprocess.run("' + gcloud_compute_instances_os_inventory_list_instances + '", shell=True, capture_output=True, text=True)' + new_line)
                file.write('    if result.stdout:' + new_line)
                file.write('        print(result.stdout.strip())' + new_line)
                file.write('    if result.stderr:' + new_line)
                file.write('        print(f"STDERR: {result.stderr.strip()}")' + new_line)
                file.write('    # Add end delimiter with timestamp' + new_line)
                file.write('    print("=" * 60)' + new_line)
                file.write('    print("✅ END COMMAND EXECUTION - " + datetime.now().strftime("%Y-%m-%d %H:%M:%S"))' + new_line)
                file.write('    print(f"Command completed with return code: {result.returncode}")' + new_line)
                file.write('    print("=" * 60)' + new_line)
                file.write('else:' + new_line)
                file.write('    print("❌ Authentication failed! Please authenticate using: gcloud auth login")' + new_line)
                file.write('    print("🚫 Command execution cancelled due to authentication failure")' + new_line)
                file.close()
                print('\nAdded ' + step_string)
                now = datetime.now()
                with open(gcp_system_log_file, 'a') as logfile:
                    logfile.write(str(now) + " + Step added to script: "+test_case_file_name+pyext+" - List runnning vms - os instances\n")
                    logfile.close()
                now = datetime.now()
                with open(gcp_system_log_file, 'a') as logfile:
                    logfile.write(str(now) + " <-- Exited List running vms mode\n")
                    logfile.close()
            c3_build_python_case_file()
        add_another_step_compute_menu()
    if selection == '4':
        with open(gcp_scripts_dir+"/"+test_case_file_name+pyext, 'a') as file:
            def c4_build_python_case_file():
                gcp_system_log_file = 'gcp_system_log.log'
                now = datetime.now()
                with open(gcp_system_log_file, 'a') as logfile:
                    logfile.write(str(now) + " --> Accessed describe vm instance mode\n")
                    logfile.close()
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
                now = datetime.now()
                with open(gcp_system_log_file, 'a') as logfile:
                    logfile.write(str(now) + " + Step added to script: "+test_case_file_name+pyext+" - Describe vm instance\n")
                    logfile.close()
                now = datetime.now()
                with open(gcp_system_log_file, 'a') as logfile:
                    logfile.write(str(now) + " <-- Exited Describe vm instance mode\n")
                    logfile.close()
            c4_build_python_case_file()
        add_another_step_compute_menu()
    if selection == '5':
        with open(gcp_scripts_dir+"/"+test_case_file_name+pyext, 'a') as file:
            def c5_build_python_case_file():
                gcp_system_log_file = 'gcp_system_log.log'
                now = datetime.now()
                with open(gcp_system_log_file, 'a') as logfile:
                    logfile.write(str(now) + " --> Accessed Find vm instance mode\n")
                    logfile.close()
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
                now = datetime.now()
                with open(gcp_system_log_file, 'a') as logfile:
                    logfile.write(
                        str(now) + " + Step added to script: " + test_case_file_name + pyext + " - Find vm instance name: "+vm_instance_to_find+"\n")
                    logfile.close()
                now = datetime.now()
                with open(gcp_system_log_file, 'a') as logfile:
                    logfile.write(str(now) + " <-- Exited Find vm instance mode\n")
                    logfile.close()
            c5_build_python_case_file()
        add_another_step_compute_menu()
    if selection == '6':
        with open(gcp_scripts_dir+"/"+test_case_file_name+pyext, 'a') as file:
            def c6_build_python_case_file():
                gcp_system_log_file = 'gcp_system_log.log'
                now = datetime.now()
                with open(gcp_system_log_file, 'a') as logfile:
                    logfile.write(str(now) + " --> Accessed Find vm by image mode\n")
                    logfile.close()
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
                now = datetime.now()
                with open(gcp_system_log_file, 'a') as logfile:
                    logfile.write(
                        str(now) + " + Step added to script: " + test_case_file_name + pyext + " - Find vm by image name: "+vm_image_to_find+"\n")
                    logfile.close()
                now = datetime.now()
                with open(gcp_system_log_file, 'a') as logfile:
                    logfile.write(str(now) + " <-- Exited Find vm by image name mode\n")
                    logfile.close()
            c6_build_python_case_file()
        add_another_step_compute_menu()
    if selection == '7':
        with open(gcp_scripts_dir+"/"+test_case_file_name+pyext, 'a') as file:
            def c7_build_python_case_file():
                gcp_system_log_file = 'gcp_system_log.log'
                now = datetime.now()
                with open(gcp_system_log_file, 'a') as logfile:
                    logfile.write(str(now) + " --> Accessed List images mode\n")
                    logfile.close()
                step_string_var = "step_string"
                step_string = "Step: Compute menu: - 7 - List images"
                new_line = ('\n')
                file.write(new_line+step_string_var+equals+quote+step_string+quote+new_line)
                file.write(print_string+left_bracket+quote+quote+right_bracket+new_line)
                file.write(print_string+left_bracket+quote+running+space+quote+plus+step_string_var+plus+quote+dots+quote+right_bracket+new_line)
                file.write(print_string+left_bracket+quote+'Listing images: '+quote+right_bracket+new_line)
                
                # Generate authentication validation code
                file.write(new_line + '# Authentication validation before gcloud command execution' + new_line)
                file.write('import subprocess' + new_line)
                file.write('def validate_auth():' + new_line)
                file.write('    try:' + new_line)
                file.write('        result = subprocess.run("gcloud config get-value project", shell=True, capture_output=True, text=True)' + new_line)
                file.write('        if result.returncode != 0:' + new_line)
                file.write('            return False' + new_line)
                file.write('        project = result.stdout.strip()' + new_line)
                file.write('        if not project or project == "(unset)":' + new_line)
                file.write('            return False' + new_line)
                file.write('        test_result = subprocess.run(f"gcloud projects describe {project} --format=\\\"value(projectId)\\\" --quiet", shell=True, capture_output=True, text=True)' + new_line)
                file.write('        return test_result.returncode == 0' + new_line)
                file.write('    except:' + new_line)
                file.write('        return False' + new_line)
                file.write(new_line + 'import sys' + new_line)
                file.write('sys.stdout.flush()' + new_line)
                file.write('if validate_auth():' + new_line)
                file.write('    # Add start delimiter with timestamp' + new_line)
                file.write('    print("=" * 60)' + new_line)
                file.write('    print("🚀 START COMMAND EXECUTION - " + datetime.now().strftime("%Y-%m-%d %H:%M:%S"))' + new_line)
                file.write('    print("Command: ' + gcloud_compute_images_list + '")' + new_line)
                file.write('    print("=" * 60)' + new_line)
                file.write('    # Capture command output and display it between delimiters' + new_line)
                file.write('    result = subprocess.run("' + gcloud_compute_images_list + '", shell=True, capture_output=True, text=True)' + new_line)
                file.write('    if result.stdout:' + new_line)
                file.write('        print(result.stdout.strip())' + new_line)
                file.write('    if result.stderr:' + new_line)
                file.write('        print(f"STDERR: {result.stderr.strip()}")' + new_line)
                file.write('    # Add end delimiter with timestamp' + new_line)
                file.write('    print("=" * 60)' + new_line)
                file.write('    print("✅ END COMMAND EXECUTION - " + datetime.now().strftime("%Y-%m-%d %H:%M:%S"))' + new_line)
                file.write('    print(f"Command completed with return code: {result.returncode}")' + new_line)
                file.write('    print("=" * 60)' + new_line)
                file.write('else:' + new_line)
                file.write('    print("❌ Authentication failed! Please authenticate using: gcloud auth login")' + new_line)
                file.write('    print("🚫 Command execution cancelled due to authentication failure")' + new_line)
                file.close()
                print('\nAdded ' + step_string)
                now = datetime.now()
                with open(gcp_system_log_file, 'a') as logfile:
                    logfile.write(str(now) + " + Step added to script: List images\n")
                    logfile.close()
                now = datetime.now()
                with open(gcp_system_log_file, 'a') as logfile:
                    logfile.write(str(now) + " <-- Exited List images mode\n")
                    logfile.close()
            c7_build_python_case_file()
        add_another_step_compute_menu()
    if selection == '8':
        with open(gcp_scripts_dir+"/"+test_case_file_name+pyext, 'a') as file:
            def c8_build_python_case_file():
                gcp_system_log_file = 'gcp_system_log.log'
                now = datetime.now()
                with open(gcp_system_log_file, 'a') as logfile:
                    logfile.write(str(now) + " --> Accessed SSH into vm with hostname mode\n")
                    logfile.close()
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
                now = datetime.now()
                with open(gcp_system_log_file, 'a') as logfile:
                    logfile.write(str(now) + " + Step added to script: "+test_case_file_name+pyext+" - SSH into vm: "+ssh_to_vm+"\n")
                    logfile.close()
                now = datetime.now()
                with open(gcp_system_log_file, 'a') as logfile:
                    logfile.write(str(now) + " <-- Exited SSH into vm with hostname mode\n")
                    logfile.close()
            c8_build_python_case_file()
        add_another_step_compute_menu()
    if selection == '9':
        #CREATE MANY INSTANCES OF VMS
        with open(gcp_scripts_dir+"/"+test_case_file_name+pyext, 'a') as file:
            def c9_build_python_case_file():
                gcp_system_log_file = 'gcp_system_log.log'
                now = datetime.now()
                with open(gcp_system_log_file, 'a') as logfile:
                    logfile.write(str(now) + " --> Accessed Create vm instances mode\n")
                    logfile.close()
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
                    now = datetime.now()
                    with open(gcp_system_log_file, 'a') as logfile:
                        logfile.write(str(now) + " + Step added to script: Added vm instance: " + create_vm + " to script: "+test_case_file_name+pyext+"\n")
                        logfile.close()
                for vm_instance_created in vm_instances_list:
                    file.write(quote+vm_instance_created+quote)
            c9_build_python_case_file()
        file.close()
        def c9_2_build_python_case_file():
            step_string = "Step: Compute menu: - 9 - Create vm instance"
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
            rename_file = test_case_file_name_out + pyext
            new_filename = gcp_scripts_dir+"/"+test_case_file_name + pyext
            os.rename(rename_file, new_filename)
            print('\nAdded ' + step_string)
            gcp_system_log_file = 'gcp_system_log.log'
            now = datetime.now()
            with open(gcp_system_log_file, 'a') as logfile:
                logfile.write(str(now) + " <-- Exited Create vm instances mode\n")
                logfile.close()
        c9_2_build_python_case_file()
        add_another_step_compute_menu()
    if selection == '10':
        #DELETE MANY INSTANCES OF VMS
        with open(gcp_scripts_dir+"/"+test_case_file_name+pyext, 'a') as file:
            def c10_build_python_case_file():
                gcp_system_log_file = 'gcp_system_log.log'
                now = datetime.now()
                with open(gcp_system_log_file, 'a') as logfile:
                    logfile.write(str(now) + " --> Accessed Delete vm instance mode\n")
                    logfile.close()
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
                    now = datetime.now()
                    with open(gcp_system_log_file, 'a') as logfile:
                        logfile.write(str(now) + " + Step added to script: "+test_case_file_name+pyext+" - Delete vm instance: " + delete_vm_instance+"\n")
                        logfile.close()
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
            rename_file = test_case_file_name_out + pyext
            new_filename = gcp_scripts_dir+"/"+test_case_file_name + pyext
            os.rename(rename_file, new_filename)
            print('\nAdded ' + step_string)
            now = datetime.now()
            gcp_system_log_file = 'gcp_system_log.log'
            with open(gcp_system_log_file, 'a') as logfile:
                logfile.write(str(now) + " <-- Exited Delete vm instance mode\n")
                logfile.close()
        c10_2_build_python_case_file()
        add_another_step_compute_menu()
    if selection == '11':
        with open(gcp_scripts_dir+"/"+test_case_file_name+pyext, 'a') as file:
            def c11_build_python_case_file():
                gcp_system_log_file = 'gcp_system_log.log'
                now = datetime.now()
                with open(gcp_system_log_file, 'a') as logfile:
                    logfile.write(str(now) + " --> Accessed Create instance template mode\n")
                    logfile.close()
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
                now = datetime.now()
                with open(gcp_system_log_file, 'a') as logfile:
                    logfile.write(
                        str(now) + " + Step added to script: " + test_case_file_name + pyext + " - Create instance template: " + create_instance_template + "\n")
                    logfile.close()
                now = datetime.now()
                with open(gcp_system_log_file, 'a') as logfile:
                    logfile.write(str(now) + " <-- Exited Create instance template mode\n")
                    logfile.close()
            c11_build_python_case_file()
        add_another_step_compute_menu()
    if selection == '12':
        with open(gcp_scripts_dir+"/"+test_case_file_name+pyext, 'a') as file:
            def c12_build_python_case_file():
                gcp_system_log_file = 'gcp_system_log.log'
                now = datetime.now()
                with open(gcp_system_log_file, 'a') as logfile:
                    logfile.write(str(now) + " --> Accessed Delete instance template mode\n")
                    logfile.close()
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
                now = datetime.now()
                with open(gcp_system_log_file, 'a') as logfile:
                    logfile.write(
                        str(now) + " + Step added to script: " + test_case_file_name + pyext + " - Delete instance template: " + delete_instance_template + "\n")
                    logfile.close()
                now = datetime.now()
                with open(gcp_system_log_file, 'a') as logfile:
                    logfile.write(str(now) + " <-- Exited Delete instance template mode\n")
                    logfile.close()
            c12_build_python_case_file()
        add_another_step_compute_menu()
    if selection == '13':
        with open(gcp_scripts_dir+"/"+test_case_file_name+pyext, 'a') as file:
            def c13_build_python_case_file():
                gcp_system_log_file = 'gcp_system_log.log'
                now = datetime.now()
                with open(gcp_system_log_file, 'a') as logfile:
                    logfile.write(str(now) + " --> Accessed Find instance template mode\n")
                    logfile.close()
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
                now = datetime.now()
                with open(gcp_system_log_file, 'a') as logfile:
                    logfile.write(
                        str(now) + " + Step added to script: " + test_case_file_name + pyext + " - Find instance template: " + instance_template_to_find + "\n")
                    logfile.close()
                now = datetime.now()
                with open(gcp_system_log_file, 'a') as logfile:
                    logfile.write(str(now) + " <-- Exited Find instance template mode\n")
                    logfile.close()
            c13_build_python_case_file()
        add_another_step_compute_menu()
    if selection == '14':
        with open(gcp_scripts_dir+"/"+test_case_file_name+pyext, 'a') as file:
            def c14_build_python_case_file():
                gcp_system_log_file = 'gcp_system_log.log'
                now = datetime.now()
                with open(gcp_system_log_file, 'a') as logfile:
                    logfile.write(str(now) + " --> Accessed List instance template mode\n")
                    logfile.close()
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
                now = datetime.now()
                with open(gcp_system_log_file, 'a') as logfile:
                    logfile.write(str(now) + " + Step added to script: List instance templates\n")
                    logfile.close()
                now = datetime.now()
                with open(gcp_system_log_file, 'a') as logfile:
                    logfile.write(str(now) + " <-- Exited List instance template mode\n")
                    logfile.close()
            c14_build_python_case_file()
        add_another_step_compute_menu()
    if selection == '15':
        with open(gcp_scripts_dir+"/"+test_case_file_name+pyext, 'a') as file:
            def c15_build_python_case_file():
                gcp_system_log_file = 'gcp_system_log.log'
                now = datetime.now()
                with open(gcp_system_log_file, 'a') as logfile:
                    logfile.write(str(now) + " --> Accessed Describe instance template mode\n")
                    logfile.close()
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
                now = datetime.now()
                with open(gcp_system_log_file, 'a') as logfile:
                    logfile.write(str(now) + " + Step added to script: "+test_case_file_name+pyext+" - Describe instance template: "+instance_template_to_describe+"\n")
                    logfile.close()
                now = datetime.now()
                with open(gcp_system_log_file, 'a') as logfile:
                    logfile.write(str(now) + " <-- Exited Describe instance template mode\n")
                    logfile.close()
            c15_build_python_case_file()
        add_another_step_compute_menu()

def list_log_files():
    """List all test case log files"""
    create_logs_directory()
    
    try:
        log_files = [f for f in os.listdir(test_logs_dir) if f.endswith('.log')]
        if not log_files:
            print("📭 No log files found")
            return []
        
        log_files.sort(reverse=True)  # Sort by name (newest first due to timestamp format)
        
        print(f"📋 Found {len(log_files)} log file(s):")
        print("=" * 70)
        for i, log_file in enumerate(log_files, 1):
            # Parse timestamp and test name from filename
            try:
                timestamp_part, test_name_part = log_file.replace('.log', '').split('-', 1)
                formatted_time = timestamp_part.replace('_', ':').replace(':', ' ', 2).replace(' ', '/')
                print(f"{i:2d}. 📄 {log_file}")
                print(f"     🕐 Time: {formatted_time}")
                print(f"     🧪 Test: {test_name_part}")
                print()
            except ValueError:
                print(f"{i:2d}. 📄 {log_file}")
                print()
        
        return log_files
    except FileNotFoundError:
        print(f"📁 Logs directory not found: {test_logs_dir}")
        return []

def view_log_file(log_filename):
    """View contents of a specific log file using less"""
    log_path = os.path.join(test_logs_dir, log_filename)
    try:
        if not os.path.exists(log_path):
            print(f"❌ Log file not found: {log_filename}")
            return
            
        print(f"📄 Opening log file: {log_filename}")
        print("💡 Use 'q' to quit, arrow keys or space to navigate")
        input("⏎ Press enter to open with less...")
        
        # Use less to view the file (with fallback options)
        # Try less, then more, then cat as fallbacks
        pagers = ['less', 'more', 'cat']
        for pager in pagers:
            if os.system(f"which {pager} > /dev/null 2>&1") == 0:
                result = os.system(f"{pager} '{log_path}'")
                return
            
        # If no pager available, fall back to direct print
        result = 1
        
        if result != 0:
            print("❌ Error opening with less, showing content directly:")
            with open(log_path, 'r') as log_file:
                content = log_file.read()
                print("=" * 80)
                print(f"📄 LOG FILE: {log_filename}")
                print("=" * 80)
                print(content)
                print("=" * 80)
                
    except Exception as e:
        print(f"❌ Error viewing log file: {str(e)}")

def search_logs_with_regex():
    """Search log files using regex pattern"""
    create_logs_directory()
    
    print("🔍 REGEX SEARCH IN LOG FILES")
    print("=" * 50)
    
    pattern = input("Enter regex pattern to search for: ").strip()
    if not pattern:
        print("❌ No pattern provided")
        return
    
    search_option = input("Search in:\n1. All log files\n2. Specific log file\nEnter choice (1 or 2): ").strip()
    
    try:
        regex = re.compile(pattern, re.IGNORECASE)
        matches_found = False
        
        if search_option == "1":
            # Search all log files
            log_files = [f for f in os.listdir(test_logs_dir) if f.endswith('.log')]
            if not log_files:
                print("📭 No log files found")
                return
            
            print(f"\n🔍 Searching pattern '{pattern}' in {len(log_files)} log files...")
            print("=" * 70)
            
            for log_file in log_files:
                log_path = os.path.join(test_logs_dir, log_file)
                try:
                    with open(log_path, 'r') as f:
                        lines = f.readlines()
                        file_matches = []
                        
                        for line_num, line in enumerate(lines, 1):
                            if regex.search(line):
                                file_matches.append((line_num, line.strip()))
                        
                        if file_matches:
                            matches_found = True
                            print(f"\n📄 {log_file} ({len(file_matches)} matches):")
                            for line_num, line in file_matches:  # Show all matches
                                print(f"   {line_num:4d}: {line}")
                            
                except Exception as e:
                    print(f"❌ Error reading {log_file}: {str(e)}")
                    
        elif search_option == "2":
            # Search specific log file
            log_files = list_log_files()
            if not log_files:
                return
                
            file_choice = input(f"\nEnter log file name or number (1-{len(log_files)}): ").strip()
            
            if file_choice.isdigit():
                file_index = int(file_choice)
                if 1 <= file_index <= len(log_files):
                    selected_file = log_files[file_index - 1]
                else:
                    print(f"❌ Invalid selection. Choose 1-{len(log_files)}")
                    return
            else:
                selected_file = file_choice
                if selected_file not in log_files:
                    print(f"❌ File not found: {selected_file}")
                    return
            
            log_path = os.path.join(test_logs_dir, selected_file)
            try:
                with open(log_path, 'r') as f:
                    lines = f.readlines()
                    file_matches = []
                    
                    for line_num, line in enumerate(lines, 1):
                        if regex.search(line):
                            file_matches.append((line_num, line.strip()))
                    
                    if file_matches:
                        matches_found = True
                        print(f"\n📄 {selected_file} ({len(file_matches)} matches):")
                        print("=" * 60)
                        for line_num, line in file_matches:
                            print(f"{line_num:4d}: {line}")
                    else:
                        print(f"\n📄 {selected_file}: No matches found")
                        
            except Exception as e:
                print(f"❌ Error reading {selected_file}: {str(e)}")
        else:
            print("❌ Invalid option")
            return
            
        if not matches_found:
            print(f"\n🔍 No matches found for pattern: '{pattern}'")
        else:
            print(f"\n✅ Search completed for pattern: '{pattern}'")
            
    except re.error as e:
        print(f"❌ Invalid regex pattern: {str(e)}")
    except Exception as e:
        print(f"❌ Search error: {str(e)}")

def manage_test_logs():
    """Main log management menu"""
    gcp_system_log_file = 'gcp_system_log.log'
    now = datetime.now()
    with open(gcp_system_log_file, 'a') as logfile:
        logfile.write(str(now) + " --> Accessed MANAGE TEST LOGS mode\n")
        logfile.close()
    
    while True:
        print("\n" + "=" * 60)
        print("📋        TEST CASE LOG MANAGEMENT MENU")
        print("=" * 60)
        print("1 - 📋 List all test case log files")
        print("2 - 📄 View specific log file")
        print("3 - 🔍 Search logs with regex")
        print("4 - 🗑️  Delete log files")
        print("5 - 📊 Log statistics")
        print("b - 🔙 Back to test case module menu")
        
        choice = input("\nSelect an option: ").strip()
        
        if choice == "1":
            print("\n📋 LISTING TEST CASE LOG FILES")
            print("=" * 50)
            list_log_files()
            input("\n⏎ Press enter to continue...")
            
        elif choice == "2":
            print("\n📄 VIEW LOG FILE")
            print("=" * 30)
            log_files = list_log_files()
            if log_files:
                file_choice = input(f"\nEnter log file name or number (1-{len(log_files)}): ").strip()
                
                if file_choice.isdigit():
                    file_index = int(file_choice)
                    if 1 <= file_index <= len(log_files):
                        selected_file = log_files[file_index - 1]
                        view_log_file(selected_file)
                    else:
                        print(f"❌ Invalid selection. Choose 1-{len(log_files)}")
                else:
                    if file_choice in log_files:
                        view_log_file(file_choice)
                    else:
                        print(f"❌ File not found: {file_choice}")
            input("\n⏎ Press enter to continue...")
            
        elif choice == "3":
            search_logs_with_regex()
            input("\n⏎ Press enter to continue...")
            
        elif choice == "4":
            print("\n🗑️ DELETE LOG FILES")
            print("=" * 40)
            log_files = list_log_files()
            if log_files:
                delete_choice = input("\nDelete options:\n1. Delete specific file\n2. Delete all log files\nEnter choice (1 or 2): ").strip()
                
                if delete_choice == "1":
                    file_choice = input(f"\nEnter log file name or number (1-{len(log_files)}): ").strip()
                    
                    if file_choice.isdigit():
                        file_index = int(file_choice)
                        if 1 <= file_index <= len(log_files):
                            selected_file = log_files[file_index - 1]
                        else:
                            print(f"❌ Invalid selection")
                            continue
                    else:
                        selected_file = file_choice
                        if selected_file not in log_files:
                            print(f"❌ File not found: {selected_file}")
                            continue
                    
                    confirm = input(f"Are you sure you want to delete '{selected_file}'? (y/n): ").lower()
                    if confirm == 'y':
                        try:
                            os.remove(os.path.join(test_logs_dir, selected_file))
                            print(f"✅ Deleted: {selected_file}")
                        except Exception as e:
                            print(f"❌ Error deleting file: {str(e)}")
                    else:
                        print("❌ Deletion cancelled")
                        
                elif delete_choice == "2":
                    confirm = input(f"Are you sure you want to delete ALL {len(log_files)} log files? (y/n): ").lower()
                    if confirm == 'y':
                        deleted_count = 0
                        for log_file in log_files:
                            try:
                                os.remove(os.path.join(test_logs_dir, log_file))
                                deleted_count += 1
                            except Exception as e:
                                print(f"❌ Error deleting {log_file}: {str(e)}")
                        print(f"✅ Deleted {deleted_count} log files")
                    else:
                        print("❌ Deletion cancelled")
                else:
                    print("❌ Invalid option")
            input("\n⏎ Press enter to continue...")
            
        elif choice == "5":
            print("\n📊 LOG STATISTICS")
            print("=" * 40)
            create_logs_directory()
            try:
                log_files = [f for f in os.listdir(test_logs_dir) if f.endswith('.log')]
                if log_files:
                    total_size = sum(os.path.getsize(os.path.join(test_logs_dir, f)) for f in log_files)
                    print(f"📁 Directory: {test_logs_dir}")
                    print(f"📄 Total log files: {len(log_files)}")
                    print(f"💾 Total size: {total_size:,} bytes ({total_size/1024:.1f} KB)")
                    
                    # Show newest and oldest
                    log_files.sort()
                    if log_files:
                        print(f"🕐 Newest log: {log_files[-1]}")
                        print(f"🕐 Oldest log: {log_files[0]}")
                else:
                    print("📭 No log files found")
            except Exception as e:
                print(f"❌ Error getting statistics: {str(e)}")
            input("\n⏎ Press enter to continue...")
            
        elif choice.lower() == "b":
            now = datetime.now()
            with open(gcp_system_log_file, 'a') as logfile:
                logfile.write(str(now) + " <-- Exited MANAGE TEST LOGS mode\n")
                logfile.close()
            break
        else:
            print("❌ Invalid option. Please try again.")

def test_case_module():
    now = datetime.now()
    gcp_system_log_file = 'gcp_system_log.log'
    with open(gcp_system_log_file, 'a') as logfile:
        logfile.write(str(now) + " --> Accessed TEST CASE MODULE MENU\n")
        logfile.close()
def build_new_test_case():
        gcp_system_log_file = 'gcp_system_log.log'
        now = datetime.now()
        with open(gcp_system_log_file, 'a') as logfile:
            logfile.write(str(now) + " --> Accessed Create new script mode\n")
            logfile.close()
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
            file.write(import_os_module+new_line+import_sys_module+new_line+"import datetime"+new_line+"from datetime import datetime")
            file.close()
        print('\nTest case '+test_case_file_name+pyext+' was created and is empty.\n')
        now = datetime.now()
        with open(gcp_system_log_file, 'a') as logfile:
            logfile.write(str(now) + " + Created script: " + test_case_file_name+pyext+"\n")
            logfile.close()
        input("Press enter to continue: ")
        now = datetime.now()
        with open(gcp_system_log_file, 'a') as logfile:
            logfile.write(str(now) + " <-- Exited Create new script mode\n")
            logfile.close()
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

def create_logs_directory():
    """Create the test logs directory if it doesn't exist"""
    if not os.path.exists(test_logs_dir):
        os.makedirs(test_logs_dir)
        print(f"Created logs directory: {test_logs_dir}")

def get_timestamp():
    """Get timestamp in yyyy_mm_dd_hh_mm_ss format"""
    return datetime.now().strftime("%Y_%m_%d_%H_%M_%S")

def run_test_case_with_logging(script_path, test_name):
    """Run a test case, display output in real-time, and capture to log file"""
    
    # AUTHENTICATION CHECK - Validate before creating any log files
    print("🔐 Re-validating authentication before test execution...")
    is_authenticated, account, project = validate_gcloud_authentication()
    
    if not is_authenticated:
        print("❌ Authentication validation failed!")
        print("🚫 LOG FILE NOT CREATED - User not properly authenticated")
        print("💡 Please authenticate using Main Menu → 'l' → 'l' (login) or 'c' (set project)")
        print("⚠️ Test execution cancelled due to authentication failure")
        return False
    
    print(f"✅ Authentication validated - Account: {account}")
    if project:
        print(f"✅ Active project: {project}")
    else:
        print("⚠️ Warning: No active project set")
    
    create_logs_directory()
    timestamp = get_timestamp()
    log_filename = f"{timestamp}-{test_name}.log"
    log_filepath = os.path.join(test_logs_dir, log_filename)
    
    print(f"📝 Logging output to: {log_filepath}")
    print("🔄 Executing test case (output will be shown and logged)...")
    print("=" * 60)
    
    try:
        # Initialize log file with header
        with open(log_filepath, 'w') as log_file:
            log_file.write(f"=== Test Case Execution Log ===\n")
            log_file.write(f"Test Name: {test_name}\n")
            log_file.write(f"Script Path: {script_path}\n")
            log_file.write(f"Execution Time: {datetime.now()}\n")
            log_file.write(f"{'='*50}\n\n")
            log_file.write("STDOUT:\n")
            log_file.flush()
        
        # Execute the script with real-time output display and logging
        process = subprocess.Popen([sys.executable, script_path], 
                                 stdout=subprocess.PIPE, 
                                 stderr=subprocess.PIPE,
                                 universal_newlines=True)
        
        stdout_lines = []
        stderr_lines = []
        
        # Read stdout in real-time
        while True:
            output = process.stdout.readline()
            if output == '' and process.poll() is not None:
                break
            if output:
                print(output.strip())  # Display to user
                stdout_lines.append(output)
                # Append to log file immediately
                with open(log_filepath, 'a') as log_file:
                    log_file.write(output)
                    log_file.flush()
        
        # Get any remaining stderr
        stderr_output = process.stderr.read()
        if stderr_output:
            stderr_lines.append(stderr_output)
            print(f"STDERR: {stderr_output.strip()}")  # Show errors to user too
        
        # Wait for process to complete and get return code
        return_code = process.poll()
        
        # Append stderr and return code to log
        with open(log_filepath, 'a') as log_file:
            log_file.write(f"\nSTDERR:\n")
            log_file.write(stderr_output)
            log_file.write(f"\nReturn Code: {return_code}\n")
            log_file.write(f"Execution completed at: {datetime.now()}\n")
        
        print("=" * 60)
        if return_code == 0:
            print(f"✅ Test case executed successfully, logged to: {log_filename}")
        else:
            print(f"⚠️ Test case completed with errors (return code: {return_code}), logged to: {log_filename}")
            
        return return_code == 0
        
    except Exception as e:
        print(f"❌ Error executing test case: {str(e)}")
        with open(log_filepath, 'a') as log_file:
            log_file.write(f"\nEXECUTION ERROR: {str(e)}\n")
        return False

def run_test_cases():
        gcp_system_log_file = 'gcp_system_log.log'
        now = datetime.now()
        with open(gcp_system_log_file, 'a') as logfile:
            logfile.write(str(now) + " --> Accessed Run script mode\n")
            logfile.close()
        
        print('\n🚀 Run test case/s menu accessed\n')
        
        # AUTHENTICATION CHECK - Validate before running any test cases
        if not check_authentication_before_test_execution():
            return  # Authentication failed, function handles user direction
        
        print('*' * 70)
        print('    ENHANCED TEST CASE RUNNER WITH LISTING FUNCTIONALITY')
        print('*' * 70)
        print()
        
        # Enhanced functionality: Use the function from menu 5 (view_test_cases) to list available test cases first
        print("📋 AVAILABLE TEST CASES:")
        print("=" * 50)
        
        # Use the same logic as view_test_cases but adapted for inline display
        test_case_string_var = "_tst_k_s_"
        dir_path = os.path.dirname(os.path.realpath(__file__))
        available_test_cases = []
        
        print('🔍 Listing test cases in path: ' + dir_path + "/" + gcp_scripts_dir + '\n')
        
        try:
            for i, filename in enumerate(os.listdir(path=dir_path+"/"+gcp_scripts_dir), 1):
                if test_case_string_var in filename:
                    print(f"{i:2d}. 📄 {filename}")
                    available_test_cases.append(filename)
                    now = datetime.now()
                    with open(gcp_system_log_file, 'a') as logfile:
                        logfile.write(str(now) + " - Listing test case script - Found test case script: "+filename+" in path: "+gcp_scripts_dir+"\n")
                        logfile.close()
                    
            if not available_test_cases:
                print("📭 No test cases found with the pattern '_tst_k_s_'")
                print("💡 Create test cases using menu option 1 first")
                input('\n⏎ Press enter to get back to the test case module menu: ')
                test_case_module()
                return
                
            print(f"\n📊 Total available test cases: {len(available_test_cases)}")
            
        except FileNotFoundError:
            print(f"📁 Directory {gcp_scripts_dir} not found. Please create test cases first.")
            input('\n⏎ Press enter to get back to the test case module menu: ')
            test_case_module()
            return
        
        print("\n" + "=" * 60)
        print("🎯 TEST CASE EXECUTION OPTIONS:")
        print("=" * 60)
        print("📝 You can now:")
        print("   • Copy and paste the exact filename from the list above")
        print("   • Enter the number (e.g., '1', '2', '3') to run by index")
        print("   • Enter 'list' to refresh the list")
        print("   • Enter 'back' to return to test case module menu")
        print()
        
        while True:
            selection = input("👉 Enter your choice: ").strip()
            
            if selection.lower() == 'back':
                print("🔙 Returning to test case module menu...")
                test_case_module()
                return
            elif selection.lower() == 'list':
                print("🔄 Refreshing test case list...")
                run_test_cases()  # Recursive call to refresh the list
                return
            elif selection.isdigit():
                test_index = int(selection)
                if 1 <= test_index <= len(available_test_cases):
                    test_case_run = available_test_cases[test_index - 1]
                    print(f"\n🎯 Selected test case #{test_index}: {test_case_run}")
                    break
                else:
                    print(f"❌ Invalid selection. Please enter a number between 1 and {len(available_test_cases)}")
                    continue
            else:
                # Treat as filename (copy/paste functionality)
                test_case_run = selection
                if test_case_run in available_test_cases:
                    print(f"\n🎯 Selected test case: {test_case_run}")
                    break
                else:
                    print(f"❌ Test case '{test_case_run}' not found in available test cases.")
                    print("💡 Available test cases are listed above. Please copy and paste exactly or enter 'list' to refresh.")
                    continue
        
        # Execute the selected test case with logging
        print("=" * 60)
        print(f"🚀 Attempting to run test case: {test_case_run}...")
        print("=" * 40)
        
        # Extract test name from filename (remove path and extension)
        test_name = os.path.splitext(test_case_run)[0]
        script_full_path = os.path.abspath(os.path.join(gcp_scripts_dir, test_case_run))
        
        # Run with logging
        success = run_test_case_with_logging(script_full_path, test_name)
        
        print("=" * 40)
        if success:
            print(f"✅ Test case {test_case_run} executed successfully!")
            now = datetime.now()
            with open(gcp_system_log_file, 'a') as logfile:
                logfile.write(str(now) + ": ! Executed script: " +test_case_run+"\n")
                logfile.close()
            timestamp()
        else:
            # Check if this was an authentication failure (no log file created)
            expected_log_file = f"{get_timestamp()}-{test_name}.log"
            if not os.path.exists(os.path.join(test_logs_dir, expected_log_file)):
                print("⚠️ No log file was created due to authentication failure.")
                print("🔐 Please authenticate before running test cases.")
            else:
                print("💡 Check the log file for detailed error information.")
            
            now = datetime.now()
            with open(gcp_system_log_file, 'a') as logfile:
                logfile.write(str(now) + ": ! ERROR: Script execution failed: " +test_case_run+"\n")
                logfile.close()
        
        # Ask if user wants to run another test case
        print(f"\n{'='*60}")
        run_another = input("🔄 Would you like to run another test case? (y/n): ").strip().lower()
        if run_another == 'y':
            run_test_cases()  # Recursive call to run another test case
        else:
            print("🏁 Test case execution session completed.")
            input('\n⏎ Press enter to get back to the test case module menu: ')
            now = datetime.now()
            with open(gcp_system_log_file, 'a') as logfile:
                logfile.write(str(now) + " <-- Exited Run script mode\n")
                logfile.close()
            test_case_module()

def list_available_test_cases():
    """List all available test cases and return the list"""
    test_case_string_var = "_tst_k_s_"
    dir_path = os.path.dirname(os.path.realpath(__file__))
    available_test_cases = []
    
    try:
        print('🔍 Listing available test cases in path: ' + dir_path + "/" + gcp_scripts_dir + '\n')
        
        for i, filename in enumerate(os.listdir(path=dir_path+"/"+gcp_scripts_dir), 1):
            if test_case_string_var in filename:
                print(f"{i:2d}. 📄 {filename}")
                available_test_cases.append(filename)
                
        if not available_test_cases:
            print("📭 No test cases found with the pattern '_tst_k_s_'")
            print("💡 Create test cases using menu option 1 first")
            return []
            
        print(f"\n📊 Total available test cases: {len(available_test_cases)}")
        return available_test_cases
        
    except FileNotFoundError:
        print(f"📁 Directory {gcp_scripts_dir} not found. Please create test cases first.")
        return []

def view_test_cases():
    gcp_system_log_file = 'gcp_system_log.log'
    now = datetime.now()
    with open(gcp_system_log_file, 'a') as logfile:
        logfile.write(str(now) + " --> Accessed Show scripts mode\n")
        logfile.close()
    global check_file, dir_path, test_case_string_var
    test_case_string_var="_tst_k_s_"
    print('\nView test cases menu accessed')
    dir_path = os.path.dirname(os.path.realpath(__file__))
    check_file=os.path.isfile(test_case_string_var)
    print('\nListing test cases in path '+dir_path+"/"+gcp_scripts_dir+': \n')
    for i in os.listdir(path=dir_path+"/"+gcp_scripts_dir):
        if test_case_string_var in i:
            print(i)
            now = datetime.now()
            with open(gcp_system_log_file, 'a') as logfile:
                logfile.write(str(now) + " - Listing test case script - Found test case script: "+i+" in path: "+gcp_scripts_dir+"\n")
                logfile.close()
    input('\nPress enter to get back to the main menu: ')
    now = datetime.now()
    with open(gcp_system_log_file, 'a') as logfile:
        logfile.write(str(now) + " <-- Exited Show scripts mode\n")
        logfile.close()
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
        gcp_system_log_file = 'gcp_system_log.log'
        now = datetime.now()
        with open(gcp_system_log_file, 'a') as logfile:
            logfile.write(str(now) + " --> Accessed Read script steps mode\n")
            logfile.close()
        
        print('\n📋 Read test case steps menu accessed\n')
        print("=" * 60)
        print("     READ TEST CASE STEPS FROM FILE")
        print("=" * 60)
        print()
        
        # Show available test cases first
        available_test_cases = list_available_test_cases()
        
        if not available_test_cases:
            input('\n⏎ Press enter to get back to the test case module menu: ')
            test_case_module()
            return
            
        print("\n" + "=" * 60)
        print("📝 FILE SELECTION OPTIONS:")
        print("=" * 60)
        print("You can:")
        print("• Enter the exact filename from the list above")
        print("• Enter the number (e.g., '1', '2', '3') to select by index")
        print("• Enter 'back' to return to test case module menu")
        print()
        
        while True:
            file_choice = input("👉 Enter your choice: ").strip()
            
            if file_choice.lower() == 'back':
                test_case_module()
                return
            elif file_choice.isdigit():
                file_index = int(file_choice)
                if 1 <= file_index <= len(available_test_cases):
                    file_to_read = available_test_cases[file_index - 1]
                    break
                else:
                    print(f"❌ Invalid selection. Choose 1-{len(available_test_cases)}")
                    continue
            else:
                if file_choice in available_test_cases:
                    file_to_read = file_choice
                    break
                else:
                    print(f"❌ File '{file_choice}' not found in available test cases.")
                    print("💡 Use exact filename from the list or number selection")
                    continue
        
        string_to_read="Step:"
        print(f"\n📋 Listing test case steps for file: {file_to_read}")
        print("=" * 70)
        with open(gcp_scripts_dir+"/"+file_to_read, 'r') as filedata:     # Opening the given file in read-only mode
           for line in filedata:
                if string_to_read in line:
                    replace_string=line.replace("step_string='", '')
                    replace_string2=line.replace("'", "")
                    print(replace_string)
        filedata.close()
        input("\nPress enter to get back to the menu: ")
        now = datetime.now()
        with open(gcp_system_log_file, 'a') as logfile:
            logfile.write(
                str(now) + " - Listed test case scripts in path: "+gcp_scripts_dir+"\n")
            logfile.close()
        now = datetime.now()
        with open(gcp_system_log_file, 'a') as logfile:
            logfile.write(str(now) + " <-- Exited Read script steps mode\n")
            logfile.close()
        test_case_module()
    except:
        invalid_file_provided()

def read_code_from_script():
    try:
        gcp_system_log_file = 'gcp_system_log.log'
        now = datetime.now()
        with open(gcp_system_log_file, 'a') as logfile:
            logfile.write(str(now) + " --> Accessed Read script code mode\n")
            logfile.close()
        
        print('\n📄 Read test case code menu accessed\n')
        print("=" * 60)
        print("     VIEW ALL CODE IN TEST CASE FILE")
        print("=" * 60)
        print()
        
        # Show available test cases first
        available_test_cases = list_available_test_cases()
        
        if not available_test_cases:
            input('\n⏎ Press enter to get back to the test case module menu: ')
            test_case_module()
            return
            
        print("\n" + "=" * 60)
        print("📝 FILE SELECTION OPTIONS:")
        print("=" * 60)
        print("You can:")
        print("• Enter the exact filename from the list above")
        print("• Enter the number (e.g., '1', '2', '3') to select by index")
        print("• Enter 'back' to return to test case module menu")
        print()
        
        while True:
            file_choice = input("👉 Enter your choice: ").strip()
            
            if file_choice.lower() == 'back':
                test_case_module()
                return
            elif file_choice.isdigit():
                file_index = int(file_choice)
                if 1 <= file_index <= len(available_test_cases):
                    file_to_read = available_test_cases[file_index - 1]
                    break
                else:
                    print(f"❌ Invalid selection. Choose 1-{len(available_test_cases)}")
                    continue
            else:
                if file_choice in available_test_cases:
                    file_to_read = file_choice
                    break
                else:
                    print(f"❌ File '{file_choice}' not found in available test cases.")
                    print("💡 Use exact filename from the list or number selection")
                    continue
        
        print(f"\n📄 Viewing all code in file: {file_to_read}")
        print("=" * 70)
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
        test_case_module()
    except:
        invalid_file_provided()

def delete_cases():
    gcp_system_log_file = 'gcp_system_log.log'
    now = datetime.now()
    with open(gcp_system_log_file, 'a') as logfile:
        logfile.write(str(now) + " --> Accessed Script deletion mode\n")
        logfile.close()
    
    print('\n🗑️ Delete test case files menu accessed\n')
    print("=" * 60)
    print("     DELETE SPECIFIC TEST CASE FILES")
    print("=" * 60)
    print()
    
    # Show available test cases first
    available_test_cases = list_available_test_cases()
    
    if not available_test_cases:
        input('\n⏎ Press enter to get back to the test case module menu: ')
        test_case_module()
        return
        
    print("\n" + "=" * 60)
    print("🗑️ DELETION OPTIONS:")
    print("=" * 60)
    print("You can:")
    print("• Enter the exact filename(s) from the list above")
    print("• Enter number(s) (e.g., '1', '2 3', '1 5 7') to select by index")
    print("• Separate multiple selections with spaces")
    print("• Enter 'back' to return to test case module menu")
    print()
    print("⚠️ WARNING: This will permanently delete the selected test cases!")
    print()
    
    while True:
        delete_input = input("👉 Enter your choice: ").strip()
        
        if delete_input.lower() == 'back':
            test_case_module()
            return
            
        if not delete_input:
            print("❌ No selection provided. Please enter filename(s) or number(s).")
            continue
            
        cases_to_delete = []
        
        # Parse input - could be numbers or filenames
        for item in delete_input.split():
            if item.isdigit():
                file_index = int(item)
                if 1 <= file_index <= len(available_test_cases):
                    cases_to_delete.append(available_test_cases[file_index - 1])
                else:
                    print(f"❌ Invalid number: {item}. Choose 1-{len(available_test_cases)}")
                    cases_to_delete = []  # Reset on error
                    break
            else:
                if item in available_test_cases:
                    cases_to_delete.append(item)
                else:
                    print(f"❌ File '{item}' not found in available test cases.")
                    cases_to_delete = []  # Reset on error
                    break
        
        if not cases_to_delete:
            continue  # Try again
        
        # Show what will be deleted and confirm
        print(f"\n🗑️ Files selected for deletion:")
        for i, case in enumerate(cases_to_delete, 1):
            print(f"  {i}. {case}")
            
        confirm = input(f"\n⚠️ Are you sure you want to delete {len(cases_to_delete)} test case(s)? (y/n): ").strip().lower()
        
        if confirm == 'y':
            break
        else:
            print("❌ Deletion cancelled.")
            continue
    
    # Proceed with deletion
    print(f"\n🗑️ Deleting {len(cases_to_delete)} test case(s)...")
    print("=" * 50)
    
    deleted_count = 0
    for case in cases_to_delete:
        try:
            os.remove(gcp_scripts_dir+"/"+case)
            print(f'✅ Deleted: {case}')
            deleted_count += 1
            now = datetime.now()
            with open(gcp_system_log_file, 'a') as logfile:
                logfile.write(str(now) + f"- Deleted script : {case} from path: {gcp_scripts_dir}\n")
                logfile.close()
        except FileNotFoundError:
            print(f'❌ File not found: {case}')
        except Exception as e:
            print(f'❌ Error deleting {case}: {str(e)}')
            with open(gcp_system_log_file, 'a') as logfile:
                logfile.write(str(now) + f" - ERROR: Unable to delete {case}: {str(e)}\n")
                logfile.close()

    print("=" * 50)
    if deleted_count > 0:
        print(f'✅ Successfully deleted {deleted_count} test case(s)')
    else:
        print('❌ No files were deleted')
        
    input('\n⏎ Press enter to get back to the test case module menu: ')
    now = datetime.now()
    with open(gcp_system_log_file, 'a') as logfile:
        logfile.write(str(now) + " <-- Exited Script deletion mode\n")
        logfile.close()
    test_case_module()

def delete_all_test_cases():
    gcp_system_log_file = 'gcp_system_log.log'
    now = datetime.now()
    with open(gcp_system_log_file, 'a') as logfile:
        logfile.write(str(now) + " --> Accessed Delete ALL scripts mode\n")
        logfile.close()
    
    print('\n🗑️ Delete ALL test cases menu accessed\n')
    print("=" * 60)
    print("     DELETE ALL TEST CASE FILES")
    print("=" * 60)
    print()
    
    # Show available test cases first
    available_test_cases = list_available_test_cases()
    
    if not available_test_cases:
        input('\n⏎ Press enter to get back to the test case module menu: ')
        test_case_module()
        return
        
    print("\n" + "=" * 60)
    print("⚠️ ⚠️ ⚠️  DANGER - DELETE ALL TEST CASES  ⚠️ ⚠️ ⚠️")
    print("=" * 60)
    print(f"You are about to permanently delete ALL {len(available_test_cases)} test cases!")
    print("This action CANNOT be undone!")
    print()
    
    delete_all = input('🚨 Are you absolutely sure you want to delete ALL test cases? (type "DELETE ALL" to confirm): ').strip()
    
    if delete_all == 'DELETE ALL':
        print(f"\n🗑️ Deleting ALL {len(available_test_cases)} test cases...")
        print("=" * 50)
        
        deleted_count = 0
        for case in available_test_cases:
            try:
                os.remove(gcp_scripts_dir+"/"+case)
                print(f'✅ Deleted: {case}')
                deleted_count += 1
                now = datetime.now()
                with open(gcp_system_log_file, 'a') as logfile:
                    logfile.write(str(now) + f" - Deleted script file: {case} from path: {gcp_scripts_dir}\n")
                    logfile.close()
            except Exception as e:
                print(f'❌ Error deleting {case}: {str(e)}')

        print("=" * 50)
        print(f'✅ Successfully deleted {deleted_count} out of {len(available_test_cases)} test cases')
        input('\n⏎ Press enter to get back to the test case module menu: ')
        
    else:
        print('❌ Deletion cancelled - you must type "DELETE ALL" exactly to confirm.')
        input('\n⏎ Press enter to get back to the test case module menu: ')
        now = datetime.now()
        with open(gcp_system_log_file, 'a') as logfile:
            logfile.write(str(now) + " ! - Aborted the deletion of all scripts mode\n")
            logfile.close()
    
    now = datetime.now()
    with open(gcp_system_log_file, 'a') as logfile:
        logfile.write(str(now) + " <-- Exited Delete ALL scripts mode\n")
        logfile.close()
    test_case_module()


def test_case_module():
    now = datetime.now()
    gcp_system_log_file = 'gcp_system_log.log'
    with open(gcp_system_log_file, 'a') as logfile:
        logfile.write(str(now) + " --> Accessed TEST CASE MODULE MENU\n")
        logfile.close()
    print('\nMode T accessed.\n')
    print("*******************************************")
    print('          TEST CASE MODULE MENU           \n')
    print('1 - Build a new test case')
    print('2 - Run test case/s')
    print('3 - Delete test case file/s')
    print('4 - Delete all test case files')
    print('5 - View saved test cases')
    print('6 - Read test case steps from file')
    print('7 - Read code in a test case. Shows all file content')
    print('8 - 📋 Manage test case logs')
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
    if test_case_menu_selection == "7":
        read_code_from_script()
    if test_case_menu_selection == "8":
        manage_test_logs()
    if test_case_menu_selection == 'c':
        return_to_compute_menu()
    if test_case_menu_selection == 'b':
        now = datetime.now()
        with open(gcp_system_log_file, 'a') as logfile:
            logfile.write(str(now) + " <-- Exited TEST CASE MODULE MENU\n")
            logfile.close()
        return_to_main_menu()
    else:
        test_case_module()
