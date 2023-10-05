#!/usr/bin/env python3

import pygame_tools as pgt
from pygame_tools import Point
import pygame

class MainMenu(pgt.MenuScreen):
	def __init__(self):
		pygame.init()
		real_size = Point(600, 600)
		size = real_size // 2
		super().__init__(pygame.display.set_mode(real_size), real_size, size)
		self.font = pygame.font.SysFont(pygame.font.get_default_font(), 20)
		self.buttons = [
			pgt.Button(CPUSelectMenu(self).run, '1 Player', (33, 150, 100, 50), self.font, border_size = 2),
			pgt.Button(PyongGame(self).run, '2 Players', (167, 150, 100, 50), self.font, border_size = 2),
		]
		self.title_font = pygame.font.SysFont(pygame.font.get_default_font(), 60)
		self.title = self.title_font.render('PYONG', False, 'white')

	def update(self):
		super().update()
		self.screen.blit(self.title, (self.window_size.x // 2 - self.title.get_width() / 2, 70))

class CPUSelectMenu(pgt.MenuScreen):
	def __init__(self, parent: MainMenu):
		super().__init__(parent.screen, parent.real_window_size, parent.window_size, parent.frame_rate)
		self.font = parent.font
		self.game = PyongGame(self)

class PyongGame(pgt.GameScreen):
	def __init__(self, parent: pgt.MenuScreen):
		super().__init__(parent.screen, parent.real_window_size, parent.window_size, parent.frame_rate)
		self.font = parent.font

def main():
	'''Driver Code'''
	MainMenu().run()

if __name__ == '__main__':
	main()
