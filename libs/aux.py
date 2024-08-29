# Ancillary scripts for cloning existing AVI objects



# Display a menu from a given List and returns the selected option key
def display_menu_from_list (options, menu_title):  
    """
    Display a menu from a list of options and return the selected option.

    :param options: List of option descriptions.
    :param menu_title: String with Menu Title
    :return: The selected option (string) or None if the choice is invalid.
    """
    if not options:
        print("No options available.")
        return None

    print("\033[1m"+menu_title+"\033[0m")
    print("\033[1m--------------------------------------------------\033[0m")
    for index, option in enumerate(options, start=1):
        print(f"{index}. {option}")
    
    try:
        choice = int(input("Enter the number corresponding to your choice: "))
        if 1 <= choice <= len(options):
            return options[choice - 1]
        else:
            print("Invalid choice. Please select a valid option.")
            return None
    except ValueError:
        print("Invalid input. Please enter a number.")
        return None


    


