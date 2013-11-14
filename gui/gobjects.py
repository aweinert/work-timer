from gi.repository import GObject
import domain

class GCategory(GObject.GObject):
    def __init__(self, category):
        super(GObject.GObject, self).__init__()
        assert isinstance(category, domain.Category)
        self._domain_category = category
        
    def get_category(self):
        return self._domain_category
    
    def __eq__(self, other):
        if isinstance(other, GCategory):
            return self._domain_category == other._domain_category
        
        return NotImplemented

class GContract(GObject.GObject):
    def __init__(self, contract):
        super(GObject.GObject, self).__init__()
        assert isinstance(contract, domain.Contract)
        self._domain_contract = contract
        
    def get_contract(self):
        return self._domain_contract

    def __eq__(self, other):
        if isinstance(other, GContract):
            return self._domain_contract == other._domain_contract
        
        return NotImplemented

class GProject(GObject.GObject):
    def __init__(self, project):
        super(GObject.GObject, self).__init__()
        assert isinstance(project, domain.Project)
        self._domain_project = project
        
    def get_project(self):
        return self._domain_project

    def __eq__(self, other):
        if isinstance(other, GProject):
            return self._domain_project == other._domain_project
        
        return NotImplemented
    
class GWorktime(GObject.GObject):
    def __init__(self, worktime):
        super(GObject.GObject, self).__init__()
        assert isinstance(worktime, domain.Worktime)
        self._domain_worktime = worktime
        
    def get_worktime(self):
        return self._domain_worktime

    def __eq__(self, other):
        if isinstance(other, GWorktime):
            return self._domain_worktime == other._domain_worktime
        
        return NotImplemented