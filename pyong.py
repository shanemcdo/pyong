#!/usr/bin/env python3

import sys
import pygame
import pygame_tools as pgt
from pygame_tools import Point
from pygame.locals import *
from enum import Enum
from math import sin, cos

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
	PADDLE_SPEED = 2
	BALL_SPEED = 5
	BOUNCE_ANGLE = 1.047198 # 60 deg

	def __init__(self, parent: pgt.MenuScreen, player2_type: Player2Type):
		super().__init__(parent.real_screen, parent.real_window_size, parent.window_size, 60)
		self.font = parent.font
		self.player2_type = player2_type
		self.paddle_size = Point(5, 50)
		self.paddle_x = 0
		self.player1_paddle_rect = Rect(0, 0, *self.paddle_size)
		self.player2_paddle_rect = Rect(0, 0, *self.paddle_size)
		self.ball_rect = pygame.Rect(0, 0, 6, 6)
		self.reset_ball_and_paddles()
		self.score = [0, 0]
		self.ball_trajectory_end_y = None

	def reset_ball_and_paddles(self):
		self.ball_rect.center = self.window_size // 2
		self.ball_velocity = Point(self.BALL_SPEED, 0)
		self.player1_paddle_rect.left = 0
		self.player2_paddle_rect.right = self.window_size.x
		self.player1_paddle_rect.centery = self.player2_paddle_rect.centery = self.window_size.y // 2


	def draw_paddle(self, position: Point):
		pygame.draw.rect(self.screen, 'white', (position, self.paddle_size))

	def draw_ball(self):
		pygame.draw.rect(self.screen, 'white', self.ball_rect)

	def draw_score(self):
		p1_score = self.font.render(str(self.score[0]), False, 'white')
		p2_score = self.font.render(str(self.score[1]), False, 'white')
		self.screen.blit(p1_score, (self.window_size.x // 2 - p1_score.get_width() // 2 - 15, 3))
		self.screen.blit(p2_score, (self.window_size.x // 2 - p2_score.get_width() // 2 + 15, 3))

	def player1_move(self):
		keys = pygame.key.get_pressed()
		if keys[K_w]:
			self.player1_paddle_rect.y -= self.PADDLE_SPEED
			if self.player1_paddle_rect.top < 0:
				self.player1_paddle_rect.top = 0
		if keys[K_s]:
			self.player1_paddle_rect.y += self.PADDLE_SPEED
			if self.player1_paddle_rect.bottom > self.window_size.y:
				self.player1_paddle_rect.bottom = self.window_size.y

	def player2_move(self):
		keys = pygame.key.get_pressed()
		match self.player2_type:
			case Player2Type.HUMAN:
				if keys[K_UP]:
					self.player2_paddle_rect.y -= self.PADDLE_SPEED
					if self.player2_paddle_rect.top < 0:
						self.player2_paddle_rect.top = 0
				if keys[K_DOWN]:
					self.player2_paddle_rect.y += self.PADDLE_SPEED
					if self.player2_paddle_rect.bottom > self.window_size.y:
						self.player2_paddle_rect.bottom = self.window_size.y
			case Player2Type.EASY_CPU:
				# TODO make this medium and limit range on easy
				if self.player2_paddle_rect.centery < self.ball_rect.centery:
					self.player2_paddle_rect.centery += self.PADDLE_SPEED
				elif self.player2_paddle_rect.centery > self.ball_rect.centery:
					self.player2_paddle_rect.centery -= self.PADDLE_SPEED
			case Player2Type.HARD_CPU:
				if self.ball_velocity.x > 0:
					if self.ball_trajectory_end_y is None:
						self.ball_trajectory_end_y = self.calculate_ball_trajectory()
					goal_point = self.ball_trajectory_end_y
				else:
					self.ball_trajectory_end_y = None
					goal_point = self.window_size.y // 2
				if self.player2_paddle_rect.centery > goal_point:
					self.player2_paddle_rect.centery -= self.PADDLE_SPEED
				elif self.player2_paddle_rect.centery < goal_point:
					self.player2_paddle_rect.centery += self.PADDLE_SPEED

	def calculate_ball_trajectory(self):
		'''
		returns the final y position of the ball after traveling
		'''
		ball_rect = self.ball_rect.copy()
		ball_vel = Point(*self.ball_velocity)
		while ball_rect.centerx >= 0 and ball_rect.centerx < self.window_size.x:
			self.bounce_ball_vertical(ball_rect, ball_vel)
		return ball_rect.centery

	def bounce_ball_vertical(self, ball_rect, ball_vel):
		ball_rect.topleft += ball_vel
		if ball_rect.top < 0:
			ball_vel.y *= -1
			ball_rect.top *= -1
		elif ball_rect.bottom >= self.window_size.y:
			ball_rect.bottom = self.window_size.y - (ball_rect.bottom - self.window_size.y)
			ball_vel.y *= -1

	def update_ball(self):
		self.bounce_ball_vertical(self.ball_rect, self.ball_velocity)
		if self.ball_rect.left < 0:
			self.score[1] += 1
			self.reset_ball_and_paddles()
		elif self.ball_rect.right >= self.window_size.y:
			self.score[0] += 1
			self.reset_ball_and_paddles()
		collide_player1 = self.player1_paddle_rect.colliderect(self.ball_rect)
		collide_player2 = self.player2_paddle_rect.colliderect(self.ball_rect)
		if collide_player1 or collide_player2:
			# https://gamedev.stackexchange.com/questions/4253/in-pong-how-do-you-calculate-the-balls-direction-when-it-bounces-off-the-paddl
			paddle_center_y = self.player1_paddle_rect.centery if collide_player1 else self.player2_paddle_rect.centery
			bounce_angle = (paddle_center_y - self.ball_rect.centery) / ( self.paddle_size.y / 2) * self.BOUNCE_ANGLE
			self.ball_velocity.x = self.BALL_SPEED * cos(bounce_angle)
			self.ball_velocity.y = self.BALL_SPEED * sin(bounce_angle)
			if collide_player2:
				self.ball_velocity.x *= -1
				self.ball_rect.right = self.player2_paddle_rect.left
			else:
				self.ball_rect.left = self.player1_paddle_rect.right


	def update(self):
		self.screen.fill('black')
		self.draw_paddle(self.player1_paddle_rect.topleft)
		self.draw_paddle(self.player2_paddle_rect.topleft)
		self.draw_ball()
		self.draw_score()
		self.player1_move()
		self.player2_move()
		self.update_ball()

def main():
	'''Driver Code'''
	MainMenu().run()

if __name__ == '__main__':
	main()
