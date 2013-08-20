import persistence_layer
import datetime
import dateutil

# Constants
SCREEN_WIDTH = 80

def print_horizontal_line(width = SCREEN_WIDTH):
    print "-" * width
    
def print_title():
    print_horizontal_line()
    print "Worktime Bookkeeping".capitalize().center(SCREEN_WIDTH)
    print_horizontal_line()
    print ""
    
def create_controller(default_path = "work.db"):
    path = raw_input("Please enter path to database (" + default_path + "): ")
    
    if path == "":
        path = default_path
        
    return persistence_layer.PersistenceController(path)

def show_menu():
    configuration = {
         1: { "description": "Start Work", "function": start_work},
         2: { "description": "Stop Work", "function": stop_work},
         3: { "description": "Enter Time", "function": enter_work},
         4: { "description": "Enter new Contract", "function": enter_contract},
         5: { "description": "Enter new Project", "function": enter_project},
         6: { "description": "Enter new Category", "function": enter_category},
         7: { "description": "Show Info", "function": show_info}
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
        
def enter_work(controller):
    project = choose_domain_object("Please choose a project", controller.retrieve_all_projects)
    category = choose_domain_object("Please choose a category", controller.retrieve_all_categories)
    description = raw_input("Please enter a short description: ")
    
    start_date = dateutil.parser.parse(raw_input("Please enter the start date of the work: ")).date()
    start_time = dateutil.parser.parse(raw_input("Please enter the start time of the work: ")).time()
    start = datetime.datetime(start_date.year, start_date.month, start_date.day, start_time.hour, start_time.minute, start_time.second, start_time.microsecond)
    
    end_date_string = raw_input("Please enter the end date of the work (" + str(start_date) + "): ")
    if end_date_string == "":
        end_date = start_date
    else:
        end_date = dateutil.parser.parse(end_date_string).date()

    end_time = dateutil.parser.parse(raw_input("Please enter the end time of the work: ")).time()

    end = datetime.datetime(end_date.year, end_date.month, end_date.day, end_time.hour, end_time.minute, end_time.second, end_time.microsecond)
    
    controller.create_worktime(project, category, start, end, description)

def enter_contract(controller):
    name = raw_input("Please enter name of new contract: ")
    start = dateutil.parser.parse(raw_input("Please enter first day of new contract: ")).date()
    end = dateutil.parser.parse(raw_input("Please enter last day of new contract: ")).date()
    hours = int(raw_input("Please enter hours per week: "))
    
    controller.create_contract(name, start, end, hours)

def enter_project(controller):
    contract = choose_domain_object("Please choose a contract for this project", controller.retrieve_all_contracts)
    name = raw_input("Please enter a name for this project: ")
    
    controller.create_project(name, contract)

def enter_category(controller):
    name = raw_input("Please enter name of category: ")
    
    controller.create_category(name)

def show_info(controller):
    # TODO: Implement
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