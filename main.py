import sqlite3
from kivy.app import App
from kivy.config import Config
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.lang import Builder
from kivy.properties import ObjectProperty
from kivy.uix.screenmanager import ScreenManager, Screen

"""Config.set(
	'kivy',
	'keyboard_mode',
	'systemanddock'
)"""


class FirstPage(Screen):
	pass


class NextPage(Screen):
	pass


class InterData(Screen):
	pass


class InterId(Screen):
	id_card = ObjectProperty(None)
	inter_id_box = ObjectProperty(None)

	def inter_id(self):

		id_card = str(self.id_card.text)
		db = sqlite3.connect('db/db.sqlite3')
		cursor = db.cursor()

		cursor.execute("SELECT id_card FROM fields_range WHERE id_card = ?", [id_card])

		if cursor.fetchall():
			return self.data()

		else:
			invalidForm()

		cursor.close()
		db.close()

	def data(self):

		print(self.id_card.text)


class SelectTree(Screen):
	pass


class LoginPage(Screen):

	login = ObjectProperty(None)
	passw = ObjectProperty(None)

	def sing_in(self):

		login = str(self.login.text)
		passw = str(self.passw.text)

		db = sqlite3.connect('db/db.sqlite3')
		cursor = db.cursor()

		cursor.execute("SELECT username, password FROM auth_user WHERE username = ? AND password = ?", [
			login,
			passw
		])

		if cursor.fetchall():
			sm.current = 'first_page'

		else:
			invalidLogin()

		cursor.close()
		db.close()


class WindowStart(ScreenManager):
	pass


def invalidLogin():
	pop = Popup(
		title='Неверный пароль',
		content=Label(text='Проверьте пароль\nи попробуте снова'),
		size_hint=(None, None), size=(200, 200)
	)
	pop.open()


def invalidForm():
	pop = Popup(
		title='Нет информации',
		content=Label(text='Нет информации\nв базе данных!'),
		size_hint=(None, None), size=(200, 200)
	)
	pop.open()


sm = WindowStart()

kv = Builder.load_file('kv/my.kv')


screens = [
	LoginPage(name='login'),
	FirstPage(name='first_page'),
	InterId(name='inter_id'),
	SelectTree(name='select_tree'),
	InterData(name='inter_data'),
	NextPage(name='next_page')
]

for screen in screens:
	sm.add_widget(screen)

sm.current = 'login'


class MyApp(App):
	title = 'AppAgro'

	def build(self):
		return sm


if __name__ == '__main__':
	MyApp().run()
