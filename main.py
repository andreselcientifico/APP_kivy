from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.window import Window
from kivy.clock import Clock
import kivy
import requests


kivy.require('2.2.1')
Window.size = (400, 700)
Window.keyboard_anim_args = {'d': 0.2, 't': 'in_out_expo'}
Window.softinput_mode = 'below_target'


class UI(ScreenManager):
    pass

class LoginAPP(MDApp):
    def build(self):
        self.theme_cls.theme_style_switch_animation = True
        self.theme_cls.theme_style_switch_animation_duration = 0.8
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Green"
        Builder.load_file("Style.kv")
        self.url = "https://applogin-ab9d0-default-rtdb.firebaseio.com/.json"
        self.key = 'BiU0NrlyXhDeLm6inII76LhUqewBrcqFRSxT4cvs'
        return UI()
    
    def login_data(self):
        login_screen = self.root.get_screen('loginApp')
        username = login_screen.ids.user.text
        password = login_screen.ids.password.text
        state = False
        data = requests.get(self.url, headers={'Authorization': self.key})

        for key, value in data.json().items():
            user_reg = value['user']
            password_reg = value['password']

            if username == user_reg:
                if password == password_reg:
                    state = True
                    login_screen.ids.welcome_label.text = f'Sup {username}!'
                    login_screen.ids.user.text = ""
                    login_screen.ids.password.text = ""
                else:
                    login_screen.ids.welcome_label.text = "Incorrect Password"
                    login_screen.ids.user.text = ""
                    login_screen.ids.password.text = ""
            else:
                login_screen.ids.welcome_label.text = "Incorrect Username"
                login_screen.ids.user.text = ""
                login_screen.ids.password.text = ""
        return state
    
    def register_data(self):
        state = 'incorrect data'

        login_screen = self.root.UI.get_screen('Register')
        username = login_screen.ids.user.text
        password = login_screen.ids.password.text
        password2 = login_screen.ids.password2.text

        data = requests.get(self.url, headers={'Authorization': self.key})

        if password != password2:
            state = 'passwords not match'
        elif len(username) < 4:
            state = 'username too short'
        elif password == password2 and len(username) >= 4:
            state = 'password too short'
        else:
            for key, value in data.json().items():
                user_reg = value['user']
                password_reg = value['password']

                if username == user_reg:
                    state = 'username already exists'
                    break
                else:
                    state = 'correct data'
                    data = {'user': username, 'password': password}
                    requests.patch(url = self.url, json= data)
                    login_screen.ids.welcome_label.text = 'Correct register'
        
        login_screen.ids.welcome_label.text = state
        login_screen.ids.user.text = ""
        login_screen.ids.password.text = ""
        login_screen.ids.password2.text = ""
        return state
         
    def on_start(self):
        Clock.schedule_once(self.login, 2)

    def login(self, *args):
        self.root.current = "login"

    def clear(self):
        login_screen = self.root.get_screen('login')
        login_screen.ids.welcome_label.text = "WELCOME"
        login_screen.ids.user.text = ""
        login_screen.ids.password.text = ""

    def switch_theme_style(self):
        self.theme_cls.primary_palette = (
            "Orange" if self.theme_cls.primary_palette == "Red" else "Red"
        )
        self.theme_cls.theme_style = (
            "Dark" if self.theme_cls.theme_style == "Light" else "Light"
        )
        login_screen = self.root.get_screen('login')

if __name__ == '__main__':
    LoginAPP().run()