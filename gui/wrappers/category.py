from gi.repository import Gtk
from gui.gobjects import GCategory

class StoreWrapper:
    
    OBJECT_COLUMN = 0
    NAME_COLUMN = 1
    
    def __init__(self):
        self._list_store = Gtk.ListStore(GCategory, str)
        
    def add(self, gcategory):
        assert isinstance(gcategory, GCategory)
        category = gcategory.get_category()
        self._list_store.append([gcategory, category.name])
        
    def remove(self, gcategory):
        assert isinstance(gcategory, GCategory)
        
        iterator = self._list_store.get_iter_first()
        
        removed = False
        while iterator <> None and removed == False:
            if self._list_store[iterator][self.OBJECT_COLUMN] is gcategory:
                self._list_store.remove(iterator)
                removed = True

            iterator = self._list_store.iter_next(iterator)

    def update(self, gcategory):
        assert isinstance(gcategory, GCategory)
        
        iterator = self._list_store.get_iter_first()
        
        found = False
        while iterator <> None and found == False:
            if self._list_store[iterator][self.OBJECT_COLUMN] is gcategory:
                found = True
            else:
                iterator = self._list_store.iter_next(iterator)
                
        self._list_store.set(iterator, self.NAME_COLUMN, gcategory.get_category().name)
        
    def get_model(self):
        return self._list_store

class ViewWrapper:

    def __init__(self, model, treeview):
        self._treeview = treeview
        self._model = model.get_model()
        
        self._treeview.set_model(self._model)
        self._treeview.append_column(Gtk.TreeViewColumn("name", Gtk.CellRendererText(), text=StoreWrapper.NAME_COLUMN))
        
    def get_selected_category(self):
        model, iterator = self._treeview.get_selection().get_selected()
        assert model is self._model
        return model[iterator][StoreWrapper.OBJECT_COLUMN]

class ControlWrapper:
    
    def __init__(self, builder, model):
        self._model = model
        self._name_entry = builder.get_object("categories-name-entry")
        
    def update_category(self, gcategory):
        category = gcategory.get_category()
        category.name = self._name_entry.get_text()
        
    def display_category(self, gcategory):
        category = gcategory.get_category()
        self._name_entry.set_text(category.name)