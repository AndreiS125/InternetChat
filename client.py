from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
import socket, struct

from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from threading import Thread
import time

from kivy.uix.recycleboxlayout import RecycleBoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.textinput import TextInput


class MyApp(App):
    socket = socket.socket()
    conected = False

    def recv(self, conn):
        size = struct.unpack("<I", conn.recv(4))[0]

        return conn.recv(size).decode("utf-8")

    def send(self,conn, text):
        size = struct.pack("<I", len(text.encode('utf-8')))
        print(size)
        text = text.encode("utf-8")

        print(size)
        conn.send(size)
        conn.send(text)

    def update(self, inst):
        self.answ = self.recv(self.socket)
        print(self.answ)
        self.textcontainer.add_widget(Label(text="", color=(1, 0, 0, 1)))
        self.textcontainer.add_widget(Label(text=self.answ, color=(1, 0, 0, 1)))



            ##pass

    def sth(self):

        while not self.conected:
            try:
                self.socket.connect(("127.0.0.1", 9090))
                self.conected = True
                print("Horray")
            except:
                pass



    def confirm(self, inst):
        self.send(self.socket, self.entr.text)
        self.textcontainer.add_widget(Label(text=self.entr.text, color=(0.1, 0.9, 0.3, 1), halign="right", size_hint = (1, 0.1)))

        self.textcontainer.add_widget(Label(text="", color=(1, 0, 0, 1)))
        self.entr.text=""
    def regist(self, inst):
        self.send(self.socket, self.reg.text)
        self.container.clear_widgets()

        self.textcontainer = GridLayout(cols=2, spacing=30, size_hint_y=None, padding=[0, 15, 0, 0])
        self.textcontainer.bind(minimum_height=self.textcontainer.setter('height'))

        self.c = ScrollView(size_hint=(1, 1))
        self.c.add_widget(self.textcontainer)
        self.updater = Button(text="Update", background_color=(0.7, 0, 0.8, 1), size_hint=(0.1, 0.1))
        self.updater.bind(on_press=self.update)
        self.entr = TextInput(_hint_text='Введите текст...', multiline=True)
        self.container.add_widget(self.c)
        self.container.add_widget(self.updater)

        self.container2 = BoxLayout(orientation="horizontal", size_hint=(1, 0.1))
        self.btn = Button(text="Send", background_color=(0.7, 0, 0.8, 1), size_hint=(0.1, 1))
        self.btn.bind(on_press=self.confirm)
        self.container2.add_widget(self.entr)
        self.container2.add_widget(self.btn)
        self.container.add_widget(self.container2)
    def build(self):
        self.thread = Thread(target=self.sth)
        self.thread.start()
        self.reg = TextInput(_hint_text='Введите логин...', multiline=True)
        self.logen = Button(text="Send login", background_color=(0.7, 0, 0.8, 1), size_hint=(0.1, 0.1))
        self.logen.bind(on_press=self.regist)

        self.container = BoxLayout(orientation="vertical")

        self.container.add_widget(self.reg)
        self.container.add_widget(self.logen)
        return self.container


if __name__ == "__main__":
    MyApp().run()
