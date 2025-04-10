import tkinter as tk
import ttkbootstrap as ttkb
from ttkbootstrap.constants import *
import os

class Create_Config(ttkb.Frame):
    def __init__(self, master, conf_folder, update_conf_menu):
        super().__init__(master, padding=(20,10))
        self.pack(fill=BOTH, expand=YES)

        self.conf_folder = conf_folder
        self.update_conf_menu = update_conf_menu

        # Form variables
        self.conf_name = ttkb.StringVar(value="")
        self.username = ttkb.StringVar(value="")
        self.ip = ttkb.StringVar(value="")
        self.port = ttkb.IntVar(value=4444)
        self.is_server = ttkb.IntVar(value=0)
        self.cover_path = ttkb.StringVar(value="")
        self.stego_path = ttkb.StringVar(value="")

        hdr_txt = "Please enter configuration information" 
        self.hdr_frame = ttkb.LabelFrame(master=self, text=hdr_txt, padding=10, width=400)
        self.hdr_frame.pack(fill=X, pady=10)

        self.create_form_entry("File Name", self.conf_name)
        self.create_form_entry("Username", self.username)
        self.create_form_entry("IP", self.ip)
        self.create_form_entry("Port", self.port)
        self.create_form_entry("Is Server", self.is_server)
        self.create_form_entry("Cover Path", self.cover_path)
        self.create_form_entry("Stego Path", self.stego_path)
        self.create_buttonbox()

    def create_form_entry(self, label, variable):
        container = ttkb.Frame(self.hdr_frame)
        container.pack(fill=X, expand=YES, pady=5)

        lbl = ttkb.Label(master=container, text=label.title(), width=10)
        lbl.pack(side=LEFT, padx=5)

        ent = ttkb.Entry(master=container, textvariable=variable, width=30)
        ent.pack(side=LEFT, padx=5, fill=X, expand=YES)

    def create_buttonbox(self):
        container = ttkb.Frame(self)
        container.pack(fill=X, expand=YES, pady=(15, 10))

        sub_btn = ttkb.Button(container, text="Save", command=self.on_submit, bootstyle="success", width=6)
        sub_btn.pack(side=RIGHT, padx=5)
        sub_btn.focus_set()

        cnl_btn = ttkb.Button(container, text="Cancel", command=self.on_cancel, bootstyle="danger", width=6)
        cnl_btn.pack(side=RIGHT, padx=5)

    def on_submit(self):

        if self.conf_name.get() and self.username.get() and self.ip.get() and self.port.get() and self.cover_path.get() and self.stego_path.get():
            if not ("client" in self.conf_name.get().lower() or "server" in self.conf_name.get()):
                if self.is_server.get() == 1:
                    exten = "Server_"
                else:
                    exten = "Client_"
                conf_name = exten + self.conf_name.get().title()

            data = "NAME = " + conf_name
            data += "\nUSERNAME = " + self.username.get()
            data += "\nIP = " + self.ip.get()
            data += "\nPORT = " + str(self.port.get())
            data += "\nIS_SERVER = " + str(self.is_server.get())
            data += "\nCOVER_PATH = " + self.cover_path.get()
            data += "\nSTEGO_PATH = " + self.stego_path.get()

            with open(os.path.join(self.conf_folder, conf_name.lower() + ".mtconf"), 'w') as f:
                f.write(data)
            
            self.update_conf_menu()

        # return self.name.get(), self.address.get(), self.phone.get()

    def on_cancel(self):
        self.update_conf_menu()
        # self.destroy()


if __name__ == "__main__":
    top = ttkb.Toplevel()
    top.title("Configuration")
    # top.config(width=400)
    Create_Config(top, "data/configurations", "abc")
    
    # top.geometry("400x400")
    top.mainloop()