import tkinter as tk
import ttkbootstrap as ttkb
from ttkbootstrap.constants import *
from ttkbootstrap.scrolled import ScrolledFrame
import create_config
import server
import client
import aes_crypt
import steg
import os
import threading


class Main_GUI(ttkb.Frame):

    def __init__(self, master) -> None:

        super().__init__(master, padding=(20,10))
        self.pack(fill=BOTH, expand=YES)
        self.conf_folder = os.path.join('data', 'configurations')
        self.key = "Default"
        
        self.config_section()
        # self.server_is_online = False
        # self.is_connected = False
        # sep = ttkb.Separator(self, bootstyle="default", orient=HORIZONTAL)
        # sep.pack(fill=X, padx=10, side=TOP)
        self.chat_section()


    def create_config_window(self) -> None:
        """ Creates a top level window that allows the user to 
            create configuration file """

        self.top = ttkb.Toplevel()
        self.top.title("Create Configuration")
        # self.top.resizable(False, False)
        create_config.Create_Config(self.top, self.conf_folder, self.update_conf_menu)


    def update_conf_menu(self) -> None:
        """ Updates the Config Menu items after Adding, Editing or Deleting the items """

        self.conf_items = self.get_conf_items()
        # print(self.conf_items)
        self.menu.destroy()
        self.menu = ttkb.Menu(self.conf_menu_btn)
        for x in self.conf_items:
            self.menu.add_radiobutton(label=x, variable=self.conf_item, command=self.config_menu_selected)

        self.conf_menu_btn['menu'] = self.menu
        self.top.destroy()


    def config_section(self) -> None:
        """ Shows Config Menu, and Create Config Button
            
            Might return frame"""

        frame = ttkb.Frame(self)
        frame.pack(pady=10)

        load_frame = ttkb.LabelFrame(frame, text="Load Configuration", padding=10, bootstyle="default")
        load_frame.pack(side=LEFT, padx=10)

        self.conf_menu_btn = ttkb.Menubutton(load_frame, text="Client_Default", width=30, bootstyle="dark")
        self.conf_menu_btn.pack(side=LEFT, padx=10)

        self.menu = ttkb.Menu(self.conf_menu_btn)
        self.conf_item = ttkb.StringVar(value="Client_Default")
        self.conf_items = self.get_conf_items()
        
        for x in self.conf_items:
            self.menu.add_radiobutton(label=x, variable=self.conf_item, command=self.config_menu_selected)

        self.conf_menu_btn['menu'] = self.menu

        load_btn = ttkb.Button(load_frame, text="Load", command=self.thread_load_configuration, bootstyle="dark")
        load_btn.pack(side=LEFT, padx=10)


        new_frame = ttkb.LabelFrame(frame, text="New Configuration", padding=10, bootstyle="default")
        new_frame.pack(side=LEFT, padx=10)

        new_btn = ttkb.Button(new_frame, text="Create New", bootstyle="dark", command=self.create_config_window)
        new_btn.pack(side=LEFT, padx=10)


    def chat_section(self) -> None:
        """ Shows the chat section including the converstion box, 
            message entry and send button
            
            Might return frame1 and frame2 """

        frame1 = tk.Frame(self, highlightbackground="gray", highlightthickness=1)     # uncomment just this
        frame1.pack(pady=(10,0))                                                      # two lines
        

        # frame1 = tk.Frame(self)
        # frame1.pack(pady=(10,0))
        
        # sep = ttkb.Separator(frame1, bootstyle="default", orient=HORIZONTAL)
        # sep.pack(fill=X, expand=True, padx=2)
        # sep1 = ttkb.Separator(frame1, bootstyle="default", orient=VERTICAL)
        # sep1.pack(fill=Y, padx=2, side=LEFT)

        self.convo_frame = ScrolledFrame(frame1, autohide=True, bootstyle="round", width=500, height=300)
        self.convo_frame.pack(fill=BOTH, expand=YES, side=LEFT)

        # adding space (fix method)
        for i in range(60):
            ttkb.Label(self.convo_frame, text="", font=('Helvetica', 10)).pack(side=TOP, padx=12, pady=2)


        # sep2 = ttkb.Separator(frame1, bootstyle="default", orient=VERTICAL)
        # sep2.pack(fill=Y, padx=2, side=LEFT)

        # sep3 = ttkb.Separator(frame1, bootstyle="default", orient=HORIZONTAL)
        # sep3.pack(fill=X, padx=10, side=BOTTOM)

        frame2 =  ttkb.Frame(self)
        frame2.pack(pady=10, side=BOTTOM)

        self.message_var = ttkb.StringVar()
        self.message_box = ttkb.Entry(frame2, width=70, textvariable=self.message_var)
        self.message_box.focus()
        self.message_box.bind('<Return>', self.send_message)
        self.message_box.pack(side=LEFT, padx=5)

        send_btn = ttkb.Button(frame2, text="Send", command=self.send_message)
        send_btn.pack(side=LEFT, padx=5)
        

    def config_menu_selected(self) -> None:
        """ Updates the Config Menu After user select an item and clicked Load """

        self.conf_menu_btn.configure(text=self.conf_item.get())
        # print(self.conf_item.get())

    def thread_load_configuration(self) -> None:
        self.listen_thread = threading.Thread(target=self.load_configuration).start()

    def load_configuration(self) -> None:
        """ Loads the Configuration data """

        with open(os.path.join(self.conf_folder, self.conf_item.get() + ".mtconf"), 'r') as f:           
            data = f.read()
            self.conf_name, self.username, self.ip, self.port, self.is_server, self.cover_path, self.stego_path = [i.split(" = ")[1] for i in data.split("\n")]
            self.port = int(self.port)
            self.is_server = True if self.is_server == "1" else False

            # print(self.conf_name)
            # print(self.username)
            # print(self.ip)
            # print(self.port)
            # print(self.is_server)
            # print(self.cover_path)
            # print(self.stego_path)

            if self.is_server:
                # print('server')
                self.serve = server.Server(self.ip, self.port)
                if self.serve.initiate_server():
                    # get username
                    
                    # encoded_username = self.encrypt_and_embed(self.username)
                    # self.serve.send(encoded_username)
                    # encoded_username2 = self.serve.client_handler()
                    # self.username2 = self.extract_and_decrypt()

                    self.username2 = "client"


                    # self.server_is_online = True
                    while True:
                        message = b""
                        while True:
                            tmp_message = self.serve.client_handler()
                            message += tmp_message
                            if len(tmp_message) < 1024:
                                break
                        if message:
                            with open(os.path.join(self.stego_path, 'res.png'), 'wb') as f:
                                f.write(message)
                            res_message = self.extract_and_decrypt()
                            if res_message == "quit":
                                break
                            # print(res_message)
                            self.push_message(self.username2, res_message)
                            self.message_box.focus()
            else:
                # print('client')
                self.client = client.Client(self.ip, self.port)
                if self.client.initiate_client():
                    # get username
                    
                    
                    # encoded_username2 = self.client.connection_handler()
                    # self.username2 = self.extract_and_decrypt()
                    # encoded_username = self.encrypt_and_embed(self.username)
                    # self.client.send(encoded_username)

                    self.username2 = "server"

                    while True:
                        message = b""
                        while True:
                            tmp_message =  self.client.connection_handler()
                            message += tmp_message
                            if len(tmp_message) < 1024:
                                break
                        if message:
                            with open(os.path.join(self.stego_path, 'res.png'), 'wb') as f:
                                f.write(message)
                            res_message = self.extract_and_decrypt()
                            if res_message == "quit":
                                break
                            # print(res_message)
                            self.push_message(self.username2, res_message)
                            self.message_box.focus()
            # self.message_box.config(state=NORMAL)

            # for line in lines:
                # print(line.split(" = ")[1])
        # print(self.conf_item.get())

    @staticmethod
    def get_conf_items() -> list:
        """ Gets menu items """

        conf_list = os.listdir(os.path.join('data', 'configurations'))
        conf_list = [conf.split(".mtconf")[0].title() for conf in conf_list]
        return conf_list
    

    # def send_message_v2(self, event=""):
    #     tk.Label(self.convo_frame, text=self.message_var.get(), bg="#ab23ff").pack(side=LEFT, padx=12, pady=2)
    #     self.message_box.delete(0, END)
    #     self.message_box.focus()
    #     print(self.message_var.get())

    def push_message(self, user, msg):

        f = ttkb.Frame(self.convo_frame, bootstyle="")
        f.pack(expand=True, fill=X)
        ttkb.Label(f, text=user + ":", font=('Helvetica', 10)).pack(side=LEFT, padx=(3, 0), pady=2)
        ttkb.Label(f, text=msg, font=('Helvetica', 10)).pack(side=LEFT, padx=(0, 12), pady=2)
        # self.message_box.delete(0, END)
        # self.message_box.focus()
        self.convo_frame.yview_scroll(200, 'units')

    def send_message(self, event=""):
        """ Sends message and adds the message to conversation box """

        message = self.message_var.get()
        if self.is_server:
            # print('serve_send')
            manipulated_message = self.encrypt_and_embed(message)
            self.serve.send(manipulated_message)
        else:
            # print('client_send')
            manipulated_message = self.encrypt_and_embed(message)
            self.client.send(manipulated_message)

        self.push_message(self.username, message)
        # f = ttkb.Frame(self.convo_frame, bootstyle="")
        # f.pack(expand=True, fill=X)
        # ttkb.Label(f, text=self.username + ":", font=('Helvetica', 10)).pack(side=LEFT, padx=(3, 0), pady=2)
        # ttkb.Label(f, text=self.message_var.get(), font=('Helvetica', 10)).pack(side=LEFT, padx=(0, 12), pady=2)
        self.message_box.delete(0, END)
        self.message_box.focus()
        # self.convo_frame.yview_scroll(200, 'units')
        # print(self.message_var.get())

        # f = ttkb.Frame(self.convo_frame, bootstyle="")
        # f.pack(expand=True, fill=X)
        # ttkb.Label(f, text=self.message_var.get()).pack(side=RIGHT, padx=12, pady=2)
        # self.message_box.delete(0, END)
        # # self.message_box.focus()
        # print(self.message_var.get())


        # f1 = ttkb.Frame(self.convo_frame, bootstyle="dark")
        # f1.pack(expand=True, fill=X)
        # tk.Label(f1, text=self.message_var.get(), bg="#ab23ff").pack(side=RIGHT, padx=12, pady=2)
        # self.message_box.delete(0, END)
        # self.message_box.focus()
        # print(self.message_var.get())

    def encrypt_and_embed(self, message: str) -> bytes:
        aes = aes_crypt.AES_Cipher(self.key)
        ciphertext = aes.encrypt(message.encode())
        stego_img = os.path.join(self.stego_path, 'res.png')
        lsb_steg = steg.Steg(os.path.join(self.cover_path, 'gfg.png'), stego_img)
        lsb_steg.embed(ciphertext)

        with open(stego_img, 'rb') as f:
            stego_img_b = f.read()

        return stego_img_b


    def extract_and_decrypt(self) -> str:
        stego_img = os.path.join(self.stego_path, 'res.png')
        lsb_steg = steg.Steg(stego=stego_img)
        ciphertext = lsb_steg.extract()
        aes = aes_crypt.AES_Cipher(self.key)
        message = aes.decrypt(ciphertext)
        return message.decode()
    

if __name__ == "__main__":
    app = ttkb.Window(title="Message Transmission", themename="superhero", resizable=(False,False))
    Main_GUI(app)
    app.mainloop()