def reading_steps_from_file():
    try:
        file_to_read=input('Provide file name to read: ')
        string_to_read="Step:"
        with open(file_to_read, 'r') as filedata:     # Opening the given file in read-only mode
           for line in filedata:
                if string_to_read in line:
                    replace_string=line.replace("step_string='", '')
                    replace_string2=line.replace("'", "")
                    print(replace_string)
        filedata.close()
    except:
        def invalid_file_provided():
            invalid_input=input('\nInvalid filename provided. Retry? y/n: ')
            if invalid_input == "y":
                reading_steps_from_file()
            if invalid_input == "n":
                print("Redirecting to menu")
            else:
                print("\nPlease type either 'y' or 'n'")
                invalid_file_provided()
        invalid_file_provided()
reading_steps_from_file()


