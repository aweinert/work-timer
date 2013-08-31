from gi.repository import Gtk

class Gui:
    CREATE_CONTRACT_XML_PATH= "guixml/create_contract.xml"

    def __init__(self):
        self._builder = Gtk.Builder()
        self._builder.add_from_file(Gui.CREATE_CONTRACT_XML_PATH)
        
    def run(self):
        contract_window_name = "create_contract_window"
        contract_window = self._builder.get_object(contract_window_name)
        contract_window.show()
        Gtk.main()