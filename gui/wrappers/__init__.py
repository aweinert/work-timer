class NotebookWrapper:
    def __init__(self, gtk_notebook):
        """Initializes an instance of NotebookWrapper.
        
        gtk_notebook --- The Gtk.Notebook to be wrapped"""
        self._notebook = gtk_notebook
        
    def get_active_page(self):
        return self._notebook.get_current_page()