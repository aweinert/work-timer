from gi.repository import Gtk

import gobjects
import widgets
import wrappers
from gui.gobjects import GContract

class Gui:
    
    """Main GUI-class, takes care of initializing and running the GUI"""

    _type_per_site = {0 : gobjects.GContract,
                      1 : gobjects.GProject,
                      2 : gobjects.GCategory,
                      3 : gobjects.GWorktime }
    
    def __init__(self, logic_controller):
        """Initializes a new instance of GUI
        
        logic_controller --- The logic controller used for queries and changes to the database"""
        
        self._logic_controller = logic_controller
        builder = Gtk.Builder()
        builder.add_from_file("gui/gui.glade")

        self._widgets_per_type = {gobjects.GContract : widgets.ContractWidget(self, builder),
                                  gobjects.GProject : widgets.ProjectWidget(self, builder),
                                  gobjects.GCategory : widgets.CategoryWidget(self, builder),
                                  gobjects.GWorktime : widgets.WorktimeWidget(self, builder) }
        

        self._notebook = wrappers.NotebookWrapper(builder.get_object("main-notebook"))
        
        builder.get_object("main-window").connect("destroy", lambda x: self.shutdown_gui())
        builder.get_object("quit-button").connect("clicked", lambda x: self.shutdown_gui())
        builder.get_object("new-button").connect("clicked", lambda x: self._new_button_clicked())
        builder.get_object("save-button").connect("clicked", lambda x: self._save_button_clicked())
        builder.get_object("delete-button").connect("clicked", lambda x: self._delete_button_clicked())

        builder.get_object("main-window").show()
        
    def run(self):
        """Displays the GUI and hands over control to the GTK main loop. Returns nothing."""
        Gtk.main()
    
    def shutdown_gui(self):
        """Shuts down the GUI and stops the GTK main loop. Returns nothing.
        
        Before shutting down, a message is displayed that asks the user to save
        unsaved data, if there is any"""
        Gtk.main_quit()
        
    def _new_button_clicked(self):
        """Makes the currently selected widget create a new object"""
        current_widget = self._get_selected_widget()
        current_widget.create_new()
    
    def _save_button_clicked(self):
        """Makes the currently selected widget save the changed data"""
        current_widget = self._get_selected_widget()
        current_widget.save_changes()
        
    def _delete_button_clicked(self):
        """Makes the currently selected widget save the changed data"""
        current_widget = self._get_selected_widget()
        current_widget.delete_object()
    
    def _get_selected_widget(self):
        """Returns the widget whose page is currently selected by the user"""
        widget_type = self._type_per_site[self._notebook.get_active_page()]
        return self._widgets_per_type[widget_type]