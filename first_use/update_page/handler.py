
class Handler:
    def __init__(self, builder, controller=None):
        self.builder = builder
        
# ADDING CONTROLLER TO HANDLER
# ----------------------------------------------------------------------------------------------------------------------        
    def add_controller(self, controller):
        self.controller = controller

    def next(self,button=None):
        self.controller.next()

    def back(self,button):
        self.controller.back()
        
    def update_button_pressed(self, button):
        self.controller.execute()
        
    def update(self):
        print('updating')
        import os
        os.system('echo {} | apt update'.format('yes'))
        os.system('echo {} | apt upgrade'.format('yes'))
        print('apt updated')
        os.system('echo {} | sudo apt dist-upgrade'.format('yes'))
        print('upgraded')
        os.system('sudo apt-get update')
        print('apt-get updated')
        
    def thread_function(self):
        self.update()
        
    def create_modal(self):
        print('modal function')
        dialog = self.builder.get_object('update_dialog')
        dialog.set_attached_to(self.builder.get_object('update_page'))
        dialog.set_destroy_with_parent(True)
        dialog.set_modal(True)
        dialog.show_all()
        print('modal displayed')
        
    def delete_modal(self):
        dialog = self.builder.get_object('update_dialog')
        dialog.destroy()
        self.next()
        
                     