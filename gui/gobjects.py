from gi.repository import GObject
import domain

class GCategory(GObject.GObject):
    def __init__(self, category):
        super(GObject.GObject, self).__init__()
        assert isinstance(category, domain.Category)
        self._domain_category = category
        
    def get_category(self):
        return self._domain_category

class GContract(GObject.GObject):
    def __init__(self, contract):
        super(GObject.GObject, self).__init__()
        assert isinstance(contract, domain.Contract)
        self._domain_contract = contract
        
    def get_contract(self):
        return self._domain_contract

class GProject(GObject.GObject):
    def __init__(self, project):
        super(GObject.GObject, self).__init__()
        assert isinstance(project, domain.Project)
        self._domain_project = project
        
    def get_project(self):
        return self._domain_project
    
class GWorktime(GObject.GObject):
    def __init__(self, worktime):
        super(GObject.GObject, self).__init__()
        assert isinstance(worktime, domain.Worktime)
        self._domain_worktime = worktime
        
    def get_worktime(self):
        return self._domain_worktime