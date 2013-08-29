import logic_layer
import datetime
import dateutil

class _Screen:
    def __init__(self, width = 80):
        self._width = width

    # Output functions
    def print_unformatted(self, message):
        print message

    def print_horizontal_line(self, width = None):
        if width == None:
            width = self._width
            
        self.print_unformatted("-" * width)
        
    def print_blank_line(self):
        self.print_unformatted("")
        
    def print_centered(self, message):
        self.print_unformatted(message.center(self._width, " "))
        
    def print_title(self, title):
        self.print_horizontal_line()
        self.print_centered(title)
        self.print_horizontal_line()
        self.print_blank_line()
    
    def display_menu(self, menu_items):
        # Start index at 1 for human readability
        index = 1
        for item in menu_items:
            self.print_unformatted("(" + str(index) + ") " + str(item))
            index += 1
        
    # Input functions
    def read_string(self, prompt, default_value = ""):
        return_value = raw_input(prompt)
        
        if return_value == "":
            return_value = default_value
            
        return return_value
    
    def read_integer(self, prompt, default_value = None):
        input_string = raw_input(prompt)
        
        if input_string == "":
            return_value = default_value
        else:
            return_value = int(input_string)
            
        return return_value
        
class CommandlineInterface:
    def __init__(self):
        self._screen = _Screen()
        self._logic_controller = self._create_controller()

    def _create_controller(self, default_path = "work.db"):
        path = self._screen.read_string("Please enter path to database (" + default_path + "): ", "")
        
        if path == "":
            path = default_path
            
        return logic_layer.LogicController(path)

    def run(self):
        self._screen.print_title("Worktime Bookkeping".capitalize())
        function = self._main_menu()
        function()

    def _main_menu(self):
        configuration = {
             1: { "description": "Start Work", "function": self._start_work},
             2: { "description": "Stop Work", "function": self._stop_work},
             3: { "description": "Enter Time", "function": self._enter_work},
             4: { "description": "Enter new Contract", "function": self._enter_contract},
             5: { "description": "Enter new Project", "function": self._enter_project},
             6: { "description": "Enter new Category", "function": self._enter_category},
             7: { "description": "Show Info", "function": self._show_info},
             8: { "description": "End Program", "function": self._end_program}
           }
        
        self._screen.display_menu(map(lambda x: configuration[x]["description"], configuration.keys()))
        default_choice = 8
        
        choice = self._screen.read_integer("Please choose an option: ", default_choice)
    
        return configuration[int(choice)]["function"]
    
    def _start_work(self):
        project = self._choose_domain_object("Please choose a project", self._persistence_controller.retrieve_all_projects)
        category = self._choose_domain_object("Please choose a category", self._persistence_controller.retrieve_all_categories)
        description = self._screen.read_string("Please enter a short description: ")
        start_time = datetime.datetime.now()
    
        self._logic_controller.crud_controller.create_worktime(project, category, start_time, None, description)

    def _stop_work(self):
        worktimes = self._logic_controller.crud_controller.retrieve_all_worktimes()
        running_worktimes = filter(lambda time: time.end == None, worktimes)
        
        for time in running_worktimes:
            time.end = datetime.datetime.now()
            self._logic_controller.crud_controller.update_worktime(time)
        
    def _enter_work(self):
        project = self._choose_domain_object("Please choose a project", self._logic_controller.crud_controller.retrieve_all_projects)
        category = self._choose_domain_object("Please choose a category", self._logic_controller.crud_controller.retrieve_all_categories)
        description = self._screen.read_string("Please enter a short description: ")
        
        start_date = dateutil.parser.parse(self._screen.read_string("Please enter the start date of the work: ")).date()
        start_time = dateutil.parser.parse(self._screen.read_string("Please enter the start time of the work: ")).time()
        start = datetime.datetime(start_date.year, start_date.month, start_date.day, start_time.hour, start_time.minute, start_time.second, start_time.microsecond)
        
        end_date_string = self._screen.read_string("Please enter the end date of the work (" + str(start_date) + "): ")
        if end_date_string == "":
            end_date = start_date
        else:
            end_date = dateutil.parser.parse(end_date_string).date()
    
        end_time = dateutil.parser.parse(self._screen.read_string("Please enter the end time of the work: ")).time()
    
        end = datetime.datetime(end_date.year, end_date.month, end_date.day, end_time.hour, end_time.minute, end_time.second, end_time.microsecond)
        
        self._logic_controller.crud_controller.create_worktime(project, category, start, end, description)

    def _enter_contract(self):
        name = self._screen.read_string("Please enter name of new contract: ")
        start = dateutil.parser.parse(self._screen.read_string("Please enter first day of new contract: ")).date()
        end = dateutil.parser.parse(self._screen.read_string("Please enter last day of new contract: ")).date()
        hours = int(self._screen.read_string("Please enter hours per week: "))
    
        self._logic_controller.crud_controller.create_contract(name, start, end, hours)

    def _enter_project(self):
        contract = self._choose_domain_object("Please choose a contract for this project", self._logic_controller.crud_controller.retrieve_all_contracts)
        name = self._screen.read_string("Please enter a name for this project: ")
        
        self._logic_controller.crud_controller.create_project(name, contract)

    def _enter_category(self):
        name = self._screen.read_string("Please enter name of category: ")
        
        self._logic_controller.crud_controller.create_category(name)

    def _show_info(self):
        for contract in self._logic_controller.crud_controller.retrieve_all_contracts():
            aim = round(self._logic_controller.analysis_controller.get_time_to_work_to_today(contract), 1)
            actual = round(self._logic_controller.analysis_controller.get_time_worked_to_today(contract), 1)

            self._screen.print_unformatted(contract.name + ": ")
            self._screen.print_unformatted("\tTo work:    " + str(aim) + "h")
            self._screen.print_unformatted("\tWorked:     " + str(actual) + "h")
            self._screen.print_unformatted("\tDifference: " + str(actual - aim) + "h")
    
    def _end_program(self):
        # Simply do nothing
        pass

    def _choose_domain_object(self, query_string, getter_function):
        domain_objects = getter_function()
        
        index = 1
        for obj in domain_objects:
            print "(" + str(index) + ") " + str(obj)
            index += 1
            
        print ""
        
        choice = self._screen.read_string(query_string + " (1): ")
        
        print ""
        
        if choice == "":
            choice = "1"
            
        return domain_objects[int(choice) - 1]
        