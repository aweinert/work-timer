import controllers
import datetime

# Constants
SCREEN_WIDTH = 80

def print_horizontal_line(width = SCREEN_WIDTH):
    print "-" * width
    
def print_title():
    print_horizontal_line()
    print "Worktime Bookeeping".capitalize().center(SCREEN_WIDTH)
    print_horizontal_line()
    print ""
    
def create_controller(default_path = "work.db"):
    path = raw_input("Please enter path to database (" + default_path + "): ")
    
    if path == "":
        path = default_path
        
    return controllers.PersistenceController(path)

def show_menu():
    configuration = {
         1: { "description": "Start Work", "function": start_work},
         2: { "description": "Stop Work", "function": stop_work},
         3: { "description": "Enter new Contract", "function": enter_contract},
         4: { "description": "Enter new Project", "function": enter_project},
         5: { "description": "Enter new Category", "function": enter_category},
         6: { "description": "Show Info", "function": show_info}
       }
    default_choice = 1
    
    for i in configuration.keys():
        print "(" + str(i) + ") " + configuration[i]["description"]
        
    print ""
    
    choice = raw_input("Please choose an option (" + str(default_choice) + "): ")

    if choice == "":
        choice = str(default_choice)
        
    return configuration[int(choice)]["function"]
    
def start_work(controller):
    project = choose_domain_object("Please choose a project", controller.retrieve_all_projects)
    category = choose_domain_object("Please choose a category", controller.retrieve_all_categories)
    description = raw_input("Please enter a short description: ")
    start_time = datetime.datetime.now()
    
    controller.create_worktime(project, category, start_time, None, description)

def stop_work(controller):
    worktimes = controller.retrieve_all_worktimes()
    running_worktimes = filter(lambda time: time.end == None, worktimes)
    
    for time in running_worktimes:
        time.end = datetime.datetime.now()
        controller.update_worktime(time)

def enter_contract(controller):
    pass

def enter_project(controller):
    pass

def enter_category(controller):
    pass

def show_info(controller):
    pass

def choose_domain_object(query_string, getter_function):
    domain_objects = getter_function()
    
    index = 1
    for obj in domain_objects:
        print "(" + str(index) + ") " + str(obj)
        index += 1
        
    print ""
    
    choice = raw_input(query_string + " (1): ")
    
    if choice == "":
        choice = "1"
        
    return domain_objects[int(choice) - 1]
        
def main():
    print_title()
    controller = create_controller()
    function = show_menu()
    function(controller)