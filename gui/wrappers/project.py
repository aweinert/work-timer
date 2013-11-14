from gi.repository import Gtk
from gui.gobjects import GProject
from gui.gobjects import GContract

class StoreWrapper:
    
    OBJECT_COLUMN = 0
    NAME_COLUMN = 1
    CONTRACT_COLUMN = 2
    CONTRACT_NAME_COLUMN = 3
    
    def __init__(self):
        self._list_store = Gtk.ListStore(GProject, str, GContract, str)
        
    def add(self, obj):
        assert isinstance(obj, GProject)
        project = obj.get_project()
        to_append = [obj, project.name]
        if project.contract <> None:
            to_append.append(GContract(project.contract))
            to_append.append(project.contract.name)
        else:
            to_append.append(None)
            to_append.append("no_contract")

        self._list_store.append(to_append)
        
    def remove(self, obj):
        iterator = self._list_store.get_iter_first()
        
        removed = False
        while iterator <> None and removed == False:
            if self._list_store[iterator][self.OBJECT_COLUMN] is obj:
                self._list_store.remove(iterator)
                removed = True

            iterator = self._list_store.iter_next(iterator)
            
    def update(self, gproject):
        assert isinstance(gproject, GProject)
        
        iterator = self._list_store.get_iter_first()
        
        found = False
        while iterator <> None and found == False:
            if self._list_store[iterator][self.OBJECT_COLUMN] is gproject:
                found = True
            else:
                iterator = self._list_store.iter_next(iterator)
                
        self._list_store.set(iterator, self.NAME_COLUMN, gproject.get_project().name)
        if gproject.get_project().contract <> None:
            self._list_store.set(iterator, self.CONTRACT_COLUMN, GContract(gproject.get_project().contract))
            self._list_store.set(iterator, self.CONTRACT_NAME_COLUMN, gproject.get_project().contract.name)
        else:
            self._list_store.set(iterator, self.CONTRACT_COLUMN, None)
            self._list_store.set(iterator, self.CONTRACT_NAME_COLUMN, "no_contract")

    def get_model(self):
        return self._list_store
    
class ViewWrapper:

    def __init__(self, model, treeview):
        self._treeview = treeview
        self._model = model.get_model()
        
        self._treeview.set_model(self._model)
        self._treeview.append_column(Gtk.TreeViewColumn("name", Gtk.CellRendererText(), text=StoreWrapper.NAME_COLUMN))
        self._treeview.append_column(Gtk.TreeViewColumn("contract", Gtk.CellRendererText(), text=StoreWrapper.CONTRACT_NAME_COLUMN))
        
    def get_selected_project(self):
        model, iterator = self._treeview.get_selection().get_selected()
        assert model is self._model
        return model[iterator][StoreWrapper.OBJECT_COLUMN]
        
class ControlWrapper:
    
    def __init__(self, builder, model, stores):
        self._model = model
        self._contract_store = stores[GContract]
        self._name_entry = builder.get_object("projects-name-entry")
        self._contract_box = builder.get_object("projects-contract-box")
        
        self._contract_box.set_model(self._contract_store.get_model())
        renderer = Gtk.CellRendererText()
        self._contract_box.pack_start(renderer, True)
        self._contract_box.add_attribute(renderer, "text", self._contract_store.NAME_COLUMN)
        
    def update_project(self, gproject):
        project = gproject.get_project()
        project.name = self._name_entry.get_text()
        project.contract = self._contract_store.get_model()[self._contract_box.get_active_iter()][self._contract_store.OBJECT_COLUMN].get_contract()
        
    def display_project(self, gproject):
        project = gproject.get_project()
        self._name_entry.set_text(project.name)
        
        if project.contract == None:
            self._contract_box.set_active(-1)
        else:
            found = False
            iterator = self._contract_store.get_model().get_iter_first()
            gcontract = GContract(project.contract)
            while found == False and iterator <> None:
                current_row = self._contract_store.get_model()[iterator]
                current_gcontract = current_row[self._contract_store.OBJECT_COLUMN]
                if current_gcontract == gcontract:
                    found = True
                else:
                    iterator = self._contract_store.get_model().iter_next(iterator)
                    
            self._contract_box.set_active_iter(iterator)