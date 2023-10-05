#!/usr/bin/env python3

import sys
import pygame
import pygame_tools as pgt
from pygame_tools import Point
from enum import Enum

class Player2Type(Enum):
	HUMAN = 1
	EASY_CPU = 2
	HARD_CPU = 3

class MainMenu(pgt.MenuScreen):
	def __init__(self):
		pygame.init()
		real_size = Point(600, 600)
		size = real_size // 2
		super().__init__(pygame.display.set_mode(real_size), real_size, size)
		self.font_path = 'assets/PublicPixel.ttf'
		self.font = pygame.font.Font(self.font_path, 10)
		self.title_font = pygame.font.Font(self.font_path, 50)
		self.buttons = [
			pgt.Button(CPUSelectMenu(self).run, '1 Player', (33, 150, 100, 50), self.font, border_size = 2, antialias = False),
			pgt.Button(PyongGame(self, Player2Type.HUMAN).run, '2 Players', (167, 150, 100, 50), self.font, border_size = 2, antialias = False),
			pgt.Button(sys.exit, 'Exit', (120, 220, 60, 30), self.font, border_size = 2, antialias = False),
		]
		self.title = self.title_font.render('PYONG', False, 'white')

	def update(self):
		super().update()
		self.screen.blit(self.title, (self.window_size.x // 2 - self.title.get_width() / 2, 70))

class CPUSelectMenu(pgt.MenuScreen):
	def __init__(self, parent: MainMenu):
		print(parent.screen)
		super().__init__(parent.real_screen, parent.real_window_size, parent.window_size, parent.frame_rate)
		self.font = parent.font
		self.buttons = [
			pgt.Button(PyongGame(self, Player2Type.EASY_CPU).run, 'Easy', (33, 150, 100, 50), self.font, border_size = 2, antialias = False),
			pgt.Button(PyongGame(self, Player2Type.HARD_CPU).run, 'Hard', (167, 150, 100, 50), self.font, border_size = 2, antialias = False),
			pgt.Button(self.stop, 'Back', (10, 10, 50, 30), self.font, border_size = 2, antialias = False)
		]
		self.title_font = pygame.font.Font(parent.font_path, 18)
		self.title = self.title_font.render('CPU Difficulty', False, 'white')

	def stop(self):
		self.running = False

	def update(self):
		super().update()
		self.screen.blit(self.title, (self.window_size.x // 2 - self.title.get_width() / 2, 100))

class PyongGame(pgt.GameScreen):
	def __init__(self, parent: pgt.MenuScreen, player2_type: Player2Type):
		super().__init__(parent.real_screen, parent.real_window_size, parent.window_size, parent.frame_rate)
		self.font = parent.font
		self.player2_type = player2_type
		self.paddle_size = Point(5, 50)
		self.player1_paddle_pos = Point(3, 0)
		self.player2_paddle_pos = Point(self.window_size.x - self.paddle_size.x - 3, 0)
		ball_size = Point(6, 6)
		self.ball_rect = pygame.Rect(*(self.window_size // 2 - ball_size // 2), *ball_size)
		self.score = [0, 0]


	def draw_paddle(self, position: Point):
		pygame.draw.rect(self.screen, 'white', (position, self.paddle_size))

	def draw_ball(self):
		pygame.draw.rect(self.screen, 'white', self.ball_rect)

	def draw_score(self):
		p1_score = self.font.render(str(self.score[0]), False, 'white')
		p2_score = self.font.render(str(self.score[1]), False, 'white')
		self.screen.blit(p1_score, (self.window_size.x // 2 - p1_score.get_width() // 2 - 15, 3))
		self.screen.blit(p2_score, (self.window_size.x // 2 - p2_score.get_width() // 2 + 15, 3))

	def update(self):
		self.screen.fill('black')
		self.draw_paddle(self.player1_paddle_pos)
		self.draw_paddle(self.player2_paddle_pos)
		self.draw_ball()
		self.draw_score()

def main():
	'''Driver Code'''
	MainMenu().run()

if __name__ == '__main__':
	main()
