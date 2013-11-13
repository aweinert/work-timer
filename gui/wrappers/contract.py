from gi.repository import Gtk
from gui.gobjects import GContract

import datetime

    
class ContractStoreWrapper:
    
    OBJECT_COLUMN = 0
    NAME_COLUMN = 1
    FROM_COLUMN = 2
    TO_COLUMN = 3
    HOURS_COLUMN = 4
    
    def __init__(self):
        self._list_store = Gtk.ListStore(GContract, str, str, str, int)
        
    def add(self, obj):
        assert isinstance(obj, GContract)
        contract = obj.get_contract()
        self._list_store.append([obj, contract.name, str(contract.start), str(contract.end), contract.hours])
        
    def remove(self, obj):
        iterator = self._list_store.get_iter_first()
        
        removed = False
        while iterator <> None and removed == False:
            if self._list_store[iterator][self.OBJECT_COLUMN] is obj:
                self._list_store.remove(iterator)
                removed = True

            iterator = self._list_store.iter_next(iterator)
            
    def update(self, gcontract):
        assert isinstance(gcontract, GContract)
        
        iterator = self._list_store.get_iter_first()
        
        found = False
        while iterator <> None and found == False:
            if self._list_store[iterator][self.OBJECT_COLUMN] is gcontract:
                found = True
            else:
                iterator = self._list_store.iter_next(iterator)
                
        self._list_store.set(iterator, self.NAME_COLUMN, gcontract.get_contract().name)
        self._list_store.set(iterator, self.FROM_COLUMN, str(gcontract.get_contract().start))
        self._list_store.set(iterator, self.TO_COLUMN, str(gcontract.get_contract().end))
        self._list_store.set(iterator, self.HOURS_COLUMN, gcontract.get_contract().hours)

    def get_model(self):
        return self._list_store
    
class ContractViewWrapper:

    def __init__(self, model, treeview):
        self._treeview = treeview
        self._model = model.get_model()
        
        self._treeview.set_model(self._model)
        self._treeview.append_column(Gtk.TreeViewColumn("name", Gtk.CellRendererText(), text=ContractStoreWrapper.NAME_COLUMN))
        self._treeview.append_column(Gtk.TreeViewColumn("start date", Gtk.CellRendererText(), text=ContractStoreWrapper.FROM_COLUMN))
        self._treeview.append_column(Gtk.TreeViewColumn("end date", Gtk.CellRendererText(), text=ContractStoreWrapper.TO_COLUMN))
        self._treeview.append_column(Gtk.TreeViewColumn("hours per week", Gtk.CellRendererText(), text=ContractStoreWrapper.HOURS_COLUMN))
        
    def get_selected_contract(self):
        model, iterator = self._treeview.get_selection().get_selected()
        assert model is self._model
        return model[iterator][ContractStoreWrapper.OBJECT_COLUMN]
        
class ContractControlWrapper:
    
    def __init__(self, builder, model):
        self._model = model
        self._name_entry = builder.get_object("contracts-name-entry")
        self._hours_button = builder.get_object("contracts-hours-button")
        self._start_calendar = builder.get_object("contracts-start-calendar")
        self._end_calendar = builder.get_object("contracts-end-calendar")
        
        self._hours_button.get_adjustment().set_lower(0)
        self._hours_button.get_adjustment().set_upper(168)
        self._hours_button.get_adjustment().set_step_increment(1)
        self._hours_button.get_adjustment().set_page_increment(10)
        
    def update_contract(self, gcontract):
        contract = gcontract.get_contract()
        contract.name = self._name_entry.get_text()
        contract.hours = self._hours_button.get_value_as_int()
        start_year, start_month, start_day = self._start_calendar.get_date()
        contract.start = datetime.date(start_year, start_month + 1, start_day)
        end_year, end_month, end_day = self._end_calendar.get_date()
        contract.end = datetime.date(end_year, end_month + 1, end_day)
        
    def display_contract(self, gcontract):
        contract = gcontract.get_contract()
        self._name_entry.set_text(contract.name)
        self._hours_button.set_value(contract.hours)
        self._start_calendar.select_month(contract.start.month - 1, contract.start.year)
        self._start_calendar.select_day(contract.start.day)
        self._end_calendar.select_month(contract.end.month - 1, contract.end.year)
        self._end_calendar.select_day(contract.end.day)