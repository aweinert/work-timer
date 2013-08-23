import persistence_layer

class AnalysisController:
    def __init__(self, persistence_controller):
        self._persistence_controller = persistence_controller

class CrudController:
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
        self.crud_controller = CrudController(self._persistence_controller)
        self.analysis_controller = AnalysisController(self._persistence_controller)