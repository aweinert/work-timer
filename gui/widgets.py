from gi.repository import Gtk
import wrappers.contract as contract_wrappers
import wrappers.category as category_wrappers

import gobjects
import datetime

from gui.gobjects import GContract, GCategory

class Widget (object):
    def __init__(self, gui, builder):
        from . import Gui

        assert isinstance(gui, Gui)
        self._gui = gui
        
        assert isinstance(builder, Gtk.Builder)
        self._builder = builder

    def create_new(self):
        """Initializes a new object with default values and writes it to the database"""
        assert False
        
    def save_changes(self):
        """Writes the values set by the user to the currently selected object and writes it to the database"""
        assert False
        
    def delete_object(self):
        """Removes the currently selected object from the database"""
        assert False

class ContractWidget (Widget):
    def __init__(self, gui, builder):
        super(ContractWidget, self).__init__(gui, builder)
        
        self._gui = gui
        self._model = contract_wrappers.StoreWrapper()
        self._view = contract_wrappers.ViewWrapper(self._model, builder.get_object("contracts-view"))
        self._controller = contract_wrappers.ControlWrapper(builder, self._model)
        
        self._view._treeview.connect("cursor-changed", lambda x: self._contract_selected())

        # Fill the store with items from the database
        contract_list = gui._logic_controller.crud_controller.retrieve_all_contracts()
        contract_list = map(lambda x: gobjects.GContract(x), contract_list)
        for contract in contract_list:
            self._model.add(contract)
    
    def create_new(self):
        contract = self._gui._logic_controller.crud_controller.create_contract("", datetime.date.today(), datetime.date.today(), 0)
        gcontract = GContract(contract);
        self._model.add(gcontract)
    
    def save_changes(self):
        selected_gcontract = self._get_selected_contract()
        self._controller.update_contract(selected_gcontract)
        contract = selected_gcontract.get_contract()
        self._gui._logic_controller.crud_controller.update_contract(contract)
        self._model.update(selected_gcontract)
    
    def delete_object(self):
        gcontract = self._get_selected_contract()
        self._model.remove(gcontract)
        contract = gcontract.get_contract()
        self._gui._logic_controller.crud_controller.delete_contract(contract)
    
    def _contract_selected(self):
        selected_contract = self._get_selected_contract()
        self._controller.display_contract(selected_contract)
            
    def _get_selected_contract(self):
        return self._view.get_selected_contract()

class CategoryWidget (Widget):
    def __init__(self, gui, builder):
        super(CategoryWidget, self).__init__(gui, builder)

        self._gui = gui
        self._model = category_wrappers.StoreWrapper()
        self._view = category_wrappers.ViewWrapper(self._model, builder.get_object("categories-view"))
        self._controller = category_wrappers.ControlWrapper(builder, self._model)
        
        self._view._treeview.connect("cursor-changed", lambda x: self._category_selected())

        # Fill the store with items from the database
        category_list = gui._logic_controller.crud_controller.retrieve_all_categories()
        category_list = map(lambda x: gobjects.GCategory(x), category_list)
        for gcategory in category_list:
            self._model.add(gcategory)
    
    def create_new(self):
        category = self._gui._logic_controller.crud_controller.create_category("new_category")
        gcategory = GCategory(category);
        self._model.add(gcategory)
    
    def save_changes(self):
        selected_gcategory = self._get_selected_category()
        self._controller.update_category(selected_gcategory)
        category = selected_gcategory.get_category()
        self._gui._logic_controller.crud_controller.update_category(category)
        self._model.update(selected_gcategory)
    
    def delete_object(self):
        gcategory = self._get_selected_category()
        self._model.remove(gcategory)
        category = gcategory.get_category()
        self._gui._logic_controller.crud_controller.delete_category(category)
    
    def _category_selected(self):
        selected_category = self._get_selected_category()
        self._controller.display_category(selected_category)
        
    def _get_selected_category(self):
        return self._view.get_selected_category()

class ProjectWidget (Widget):
    def __init__(self, gui, builder):
        super(ProjectWidget, self).__init__(gui, builder)
    
    def create_new(self):
        pass
    
    def save_changes(self):
        pass
    
    def delete_object(self):
        pass

class WorktimeWidget (Widget):
    def __init__(self, gui, builder):
        super(WorktimeWidget, self).__init__(gui, builder)
    
    def create_new(self):
        pass
    
    def save_changes(self):
        pass
    
    def delete_object(self):
        pass