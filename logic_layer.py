import persistence_layer
import datetime

class _AnalysisController:
    def __init__(self, persistence_controller):
        self._persistence_controller = persistence_controller
        
    def get_time_worked_to_today(self, contract):
        return self.get_hours_worked(contract, datetime.date.today())

    def get_time_to_work_to_today(self, contract):
        return self.get_hours_to_work(contract, datetime.date.today())
        
    def get_hours_worked(self, contract, date):
        """Returns the time in hours that actually was invested in the given
        contract from its beginning to the given date"""
        worktimes = self._persistence_controller.retrieve_all_worktimes()
        
        time_worked = 0
        for worktime in filter(lambda x: x.project.contract == contract, worktimes):
            if worktime.end.date() <= date:
                worktime_duration = worktime.get_duration()
                time_worked += (worktime_duration.days * 24 + float(worktime_duration.seconds) / (60.0 * 60.0 * 24.0))
                
        return time_worked
    
    def get_hours_to_work(self, contract, date):
        """Gets the time in hours that should have been worked for the given
        contract up to the given day."""
        start_date = contract.start
        
        WORK_DAYS_PER_WEEK = 5
        hours_per_day = contract.hours / WORK_DAYS_PER_WEEK
        
        if date <= contract.end:
            end_date = date
        else:
            end_date = contract.end
            
        hours_to_work = 0
        # There should be a way to specify a timedelta of one day directly...
        ONE_DAY_TIMEDELTA = datetime.date(1,1,2) - datetime.date(1,1,1)
        current_date = start_date
        
        while current_date <= end_date:
            # Exclude weekends, i.e., the fifth and sixth day of the week
            if current_date.weekday() <> 5 and current_date.weekday() <> 6:
                hours_to_work += hours_per_day

            current_date += ONE_DAY_TIMEDELTA
        
        return hours_to_work

class _CrudController:
    def __init__(self, persistence_controller):
        self._persistence_controller = persistence_controller

    def create_contract(self, name, start, end, hours):
        return self._persistence_controller.create_contract(name, start, end, hours)
    
    def retrieve_all_contracts(self):
        return self._persistence_controller.retrieve_all_contracts()
    
    def retrieve_contract_by_id(self, contract_id):
        return self._persistence_controller.retrieve_contract_by_id(contract_id)
    
    def update_contract(self, contract):
        self._persistence_controller.update_contract(contract)
    
    def delete_contract(self, contract):
        self._persistence_controller.delete_contract(contract)

    # CRUD-interface for projects
    def create_project(self, name, contract):
        return self._persistence_controller.create_project(name, contract)
    
    def retrieve_all_projects(self):
        return self._persistence_controller.retrieve_all_projects()
    
    def retrieve_project_by_id(self, project_id):
        return self._persistence_controller.retrieve_project_by_id(project_id)
    
    def update_project(self, project):
        self._persistence_controller.update_project(project)
    
    def delete_project(self, project):
        self._persistence_controller.delete_project(project)

    # CRUD-interface for categories
    def create_category(self, name):
        return self._persistence_controller.create_category(name)
    
    def retrieve_all_categories(self):
        return self._persistence_controller.retrieve_all_categories()
    
    def retrieve_category_by_id(self, category_id):
        return self._persistence_controller.retrieve_category_by_id(category_id)
    
    def update_category(self, category):
        self._persistence_controller.update_category(category)
    
    def delete_category(self, category):
        self._persistence_controller.delete_category(category)
    
    # CRUD-interface for times
    def create_worktime(self, project, category, start, end, description):
        return self._persistence_controller.create_worktime(project, category, start, end, description)
    
    def retrieve_all_worktimes(self):
        return self._persistence_controller.retrieve_all_worktimes()
    
    def retrieve_worktime_by_id(self, worktime_id):
        return self._persistence_controller.retrieve_worktime_by_id(worktime_id)
    
    def update_worktime(self, worktime):
        self._persistence_controller.update_worktime(worktime)
    
    def delete_worktime(self, worktime):
        self._persistence_controller.delete_worktime(worktime)

class LogicController:
    def __init__(self, db_path = "work.db"):
        self._persistence_controller = persistence_layer.PersistenceController(db_path)
        self.crud_controller = _CrudController(self._persistence_controller)
        self.analysis_controller = _AnalysisController(self._persistence_controller)