from abc import ABC


class Page(ABC):

    def get_xml_object(self):
        raise NotImplementedError("get_xml_object(self) method must be implemented...")
    
    def destroy(self):
        del self
        
    def connect_builder(self):
        raise NotImplementedError("connect_builder(self, ....) method must be implemented")
    
    def connect_handler(self, controller=None):
        raise NotImplementedError("connect_handler(self, ....) method must be implemented")
    
    def get_name(self):
        raise NotImplementedError("get_name must be implemented")
    
    def get_icon(self):
        """
            Page should have an icon but if is missing minus will show in application

        """
        return None