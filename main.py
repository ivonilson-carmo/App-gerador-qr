from kivymd.app import MDApp
from kivymd.toast import toast

from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import StringProperty
from kivy.core.window import Window
from kivy.clock import Clock

from datetime import datetime
from pyqrcode import create
import os.path, sys

FOLDER_SAVE_QR = '/sdcard/GeradorQR/'

if sys.platform == 'win32':
	FOLDER_SAVE_QR = 'GeradorRQR/'
	Window.size = (400, 620)

class Inicial(Screen):
	global FOLDER_SAVE_QR
	""" Tela Inicial do App """
	
	def gera_codigo(self):
		"""" Função que gera codigo qr e salva o codigo em png """
		
		texto = self.ids.palavra.text
		self.qr = create(texto)

		date = datetime.now().strftime('%Y%m%d-%H%M')
		self.nome_arquivo = f'{FOLDER_SAVE_QR}geradorqr-{date}.png'
		
		sufixo = 1
		while os.path.exists(self.nome_arquivo):
			size_name = len(f'{FOLDER_SAVE_QR}geradorqr-{date}')
			
			self.nome_arquivo = f'{self.nome_arquivo[:size_name]}({sufixo}).png' # adciona sufixo (num)
			sufixo += 1
		
		self.saveImg()
	
	def saveImg(self):
		# salva arquivo
		self.qr.png(self.nome_arquivo, scale=16)
		
		# adciona box com img do qrcode
		self.ids.content.add_widget(ExibeCodigo(cod=self.nome_arquivo))
		
		# exibe toast avisando que o arquivo foi salvo
		toast(f'Imagem salva: {self.nome_arquivo[:-4]}')
		
		# limpa o texto do input
		self.ids.palavra.text = ''


class ExibeCodigo(BoxLayout):
	""" Box que contém codigo qr """
	def __init__(self, cod, **kwargs):
		super(ExibeCodigo, self).__init__()
		self.ids.image.source = cod
	
	def close(self):
		""" Remove esse box da tela """
		self.parent.remove_widget(self)


class Main(MDApp):
	def __init__(self, **kwargs):
		super(Main, self).__init__()
		global FOLDER_SAVE_QR
		# verifica se não existe a pasta 'GeradorQR'
		if not os.path.exists(FOLDER_SAVE_QR):
			os.path.os.mkdir(FOLDER_SAVE_QR)
		
	def build(self):
		self.theme_cls.primary_palette = 'Purple'
		self.theme_cls.accent_palette = 'Yellow'
		gerenciador = ScreenManager ()
		
		for tela in [Inicial()]:
			gerenciador.add_widget(tela)
		
		return gerenciador

if __name__ == '__main__':
	Main().run()
