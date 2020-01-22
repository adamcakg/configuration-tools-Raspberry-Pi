from abc import ABC, abstractmethod

class Page(ABC):
    
    def next(self, controller=None):
        raise NotImplementedError("next(self) method must be implemented...")
    
    def back(self, controller=None):
        raise NotImplementedError("back(self) method must be implemented...")

    def get_xml_object(self):
        raise NotImplementedError("get_xml_object(self) method must be implemented...")
    
    def destroy(self):
        raise NotImplementedError("destroy(self) method must be implemented...")
    
    def connect_handler(self, controller=None):
        raise NotImplementedError("connect_handler(self, ....) method must be implemented")

    def execute(self):
        raise NotImplementedError("execute(self) method must be implemented")