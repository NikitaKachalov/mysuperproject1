#-*- coding: utf-8 -*-
#                                         --StarFight: Exodus--
#---Name----
#-SF:Exodus-
#
#--Version--
#----1.0----
#
#SF: Exodus contain of 5 main classes: 'Space_ship', 'Enemys_space_ship', 'Shooter', 'Score', 'Lives', 'Explosion', 'Lives'
#### This programm include 13 functions: 'Exodus', 'player_initialization', 8*'Enemy_call', 'random_choice_enemys',
#### 'init_Score', 'init_lives'-----------------------------------------------------------------------------------.
#### 9 main Global vars have been used: 'bullet_number', 'score', 'reg', 'warn', 'user_dies', 'test_var', 'list_of_lives',
#### 'counter', 'counter_main', '----------------------------------------------------------------------.
#### ------ packages: -livewires (games, color)
####                  -pygame
####                  -random
####                  -time
from livewires import games, color
import pygame
import random
import time
bullet_number = 0
score = 0
reg = 0
warn = False
user_dies = 0
test_var = False
list_of_lives = []
counter = 0
counter_main = 0
user_fall = False
switch = -1
switch_count= 0
g_score = None
boom = ["media/boom.bmp", "media/boom_1.bmp", "media/boom_2.bmp", "media/boom_3.bmp", "media/boom_4.bmp", "media/boom_5.bmp", "media/boom_6.bmp", "media/boom_7.bmp",]
#print(len(games.screen.get_all_objects())) --use it to check the length of Sprite in screen
#init main screen
def Exodus():
	games.init(screen_width = 1000, screen_height = 500, fps = 50)
	background_image = games.load_image("media/cn.jpg", transparent = False)
	games.screen.background = background_image
#class of user sprite and player model
class Space_ship(games.Sprite):
	shoot_count = 0
	shoot_pause = 0
	def update(self):
		global reg, warn, test_var
		self.limitation()
		self.controls()
		self.check_ol()
		#warning of losing live
		if warn == True:
			Enemy_shoot.is_collideable = False
			reg += 1
			if reg == 30:
				self.new_image = games.load_image("media/bgspeedship.png")
				self.image = self.new_image
			elif reg == 60:
				self.new_image = games.load_image("media/temp_ship.bmp")
				self.image = self.new_image
			elif reg == 90:
				self.new_image = games.load_image("media/bgspeedship.png")
				self.image = self.new_image
			elif reg == 120:
				self.new_image = games.load_image("media/temp_ship.bmp")
				self.image = self.new_image
			elif reg == 150:
				self.new_image = games.load_image("media/bgspeedship.png")
				self.image = self.new_image
				warn = False
				reg = 0
				test_var = False
				Enemy_shoot.is_collideable = True		
		#check for enemys
		self.list = games.screen.get_all_objects()
		if len(self.list) < 7 and warn == False and test_var == False:
			random_choice_enemys()
		if user_dies == 3 or len(list_of_lives) == 0:
			self.destroy()
			self.animation_main = Explosion(images = boom, x = self.x, y = self.y, repeat_interval = 5, n_repeats = 1, is_collideable = False)
			games.screen.add(self.animation_main)
			games.screen.clear()
			games.music.stop()
			self.game_over = Over(value = "Game Over", size = 100, color = color.white, x = games.screen.width / 2, y = games.screen.height / 2)
			self.user_total = games.Text(value = 'Your Score:' + str(score), size = 100, color = color.white, x = games.screen.width / 2, y = (games.screen.height / 2)+80, is_collideable = False)
			games.screen.add(self.game_over)
			games.screen.add(self.user_total)
	def limitation(self):
		if self.right > games.screen.width:
			self.x = 60
		elif self.left < 0:
			self.x = games.screen.width - 60
	def controls(self):
		global switch, switch_count
		switch_count += 1
		if games.keyboard.is_pressed(pygame.K_LEFT):
			self.x -= 5
		elif games.keyboard.is_pressed(pygame.K_RIGHT):
			self.x += 5       
		elif games.keyboard.is_pressed(pygame.K_DOWN):
			self.dx = 0
		if games.keyboard.is_pressed(pygame.K_SPACE) and warn == False and test_var == False:
			self.shoot_count += 1
			if self.shoot_count == 13:
				self.shoot()
				self.sound = init_Shoot_sound()
				self.sound.play()
				self.shoot_count = 0
		if games.keyboard.is_pressed(pygame.K_ESCAPE):
			games.screen.clear()
			games.screen.quit()
		if games.keyboard.is_pressed(pygame.K_TAB) and switch_count == 1:
			switch = -switch
		elif switch_count == 13:
			switch_count = 0
	def shoot(self):
		global bullet_number
		self.shoot_img = games.load_image("media/user_shoot.bmp")
		self.player_shoot = Shooter(image = self.shoot_img, x = self.x, y = self.top -10, dy = -2)
		games.screen.add(self.player_shoot)
		bullet_number += 1
	def check_ol(self):
		global warn
		for object in self.overlapping_sprites:
			object.register()
			self.registration()
	def registration(self):
		global reg, warn, user_dies, list_of_lives
		if reg == 0:
			self.new_image = games.load_image("media/temp_ship.bmp")
			self.image = self.new_image
		warn = True
		if test_var == False:
			user_dies += 1
			if len(list_of_lives) != 0:
				list_of_lives[0].image = self.new_image
				list_of_lives.remove(list_of_lives[0])
	def die(self):
		pass
#class of Enemys
class Enemy_space_ship_0(games.Sprite):
	tries = 0
	shoot_count = 0
	counter = 0	   
	def update(self):
		global counter, counter_main, bullet_number
		#self.counter += 1
		#print(counter) 
		#print(counter_main) -- подсчет цикла, переменная, которая изменяется вместе с fps
		if self.top > games.screen.height:
			self.destroy()
			random_choice_enemys()
		if switch == -1:
			if self.tries == 0:
				self.on_shooting = random.choice([True, False])
				if self.dy == 3:
					self.on_shooting = False
				self.tries += 1
			if self.on_shooting == True:
				self.strike()
	def die(self):
		global score, g_score, reg, boom
		score += 1
		if score != 1:
			if score <= 10:
				g_score.value = g_score.value.replace(g_score.value[len(g_score.value)-1], str(score))
			elif score > 10 and score <= 100:
				g_score.value = g_score.value[:len(g_score.value)-2] + str(score)
			elif score > 100 and score <=999:
				g_score.value = g_score.value[:len(g_score.value)-3] + str(score)
			elif score > 1000 and score <=9999:
				g_score.value = g_score.value[:len(g_score.value)-4] + str(score)
			elif score > 10000 and score <=99999:
				g_score.value = g_score.value[:len(g_score.value)-5] + str(score)
		else:
			g_score.value += str(score)
		self.destroy()
		self.animation_main = Explosion(images = boom, x = self.x, y = self.y, repeat_interval = 5, n_repeats = 1, is_collideable = False)
		games.screen.add(self.animation_main)
		self.sound = init_Shoot_sound_1()
		self.sound.play()
		if reg == 0 or reg == 90:
			random_choice_enemys()
	def register(self):
		global reg, warn, test_var, enemy_mas
		if warn == False:
			self.destroy()
			self.animation_main = Explosion(images = boom, x = self.x, y = self.y, repeat_interval = 5, n_repeats = 1, is_collideable = False)
			games.screen.add(self.animation_main)
			self.sound = init_Shoot_sound_1()
			self.sound.play() 
		else:
			test_var = True
		if reg == 0 or reg == 150:
			random_choice_enemys()
	def strike(self):
		global bullet_number
		if self.shoot_count != 250:
			self.shoot_count += 1
		else:
			self.shoot_count = 0
		if self.shoot_count == 13:
			self.shoot()
			bullet_number += 1
			self.sound_2 = init_Shoot_sound_2()
			self.sound_2.play()
		elif self.shoot_count == 26:
			self.shoot()
			bullet_number += 1
			self.sound_2 = init_Shoot_sound_2()
			self.sound_2.play()
		elif self.shoot_count == 39:
			self.shoot()
			bullet_number += 1
			self.sound_2 = init_Shoot_sound_2()
			self.sound_2.play()
		elif self.shoot_count == 52:
			self.shoot()
			bullet_number += 1
			self.sound_2 = init_Shoot_sound_2()
			self.sound_2.play()
		elif self.shoot_count == 65:
			self.shoot()
			bullet_number += 1
			self.sound_2 = init_Shoot_sound_2()
			self.sound_2.play()
	def shoot(self):
		self.shoot_img = games.load_image("media/enemy_shoot.bmp")
		if self.dy == 1:
			self.speed_b = 4
		elif self.dy == 2:
			self.speed_b = 8
		elif self.dy == 3: 
			self.speed_b = 12
		self.enemy_shoot = Enemy_shoot(image = self.shoot_img, x = self.x, y = self.bottom + 8, dy = self.speed_b)
		games.screen.add(self.enemy_shoot)
#user/player init
def player_initialization():
	space_ship_image = games.load_image("media/bgspeedship.png")
	user_ship = Space_ship(image = space_ship_image, x = games.screen.width/2, y = games.screen.height - 60, dx = 0, dy = 0)
	games.screen.add(user_ship)
#list of varieties of Enemys
def Enemy_call():
	enemy_fighter_image_0 = games.load_image("media/heavyfreighter.png")
	x_position = random.randint(55, games.screen.width - 55)
	y_position = 0
	speed = random.randint(1,3)
	enemy = Enemy_space_ship_0(image = enemy_fighter_image_0, x = x_position, y = y_position, dy = speed, dx = 0)
	games.screen.add(enemy)
def Enemy_call_1():
	enemy_fighter_image_0 = games.load_image("media/medfighter.png")
	x_position = random.randint(55, games.screen.width - 55)
	y_position = 0
	speed = random.randint(1,3)
	enemy = Enemy_space_ship_0(image = enemy_fighter_image_0, x = x_position, y = y_position, dy = speed, dx = 0)
	games.screen.add(enemy)
def Enemy_call_2():
	enemy_fighter_image_0 = games.load_image("media/medfrighter.png")
	x_position = random.randint(55, games.screen.width - 55)
	y_position = 0
	speed = random.randint(1,3)
	enemy = Enemy_space_ship_0(image = enemy_fighter_image_0, x = x_position, y = y_position, dy = speed, dx = 0)
	games.screen.add(enemy)
def Enemy_call_3():
	enemy_fighter_image_0 = games.load_image("media/bgbattleship.png")
	x_position = random.randint(55, games.screen.width - 55)
	y_position = 0
	speed = random.randint(1,3)
	enemy = Enemy_space_ship_0(image = enemy_fighter_image_0, x = x_position, y = y_position, dy = speed, dx = 0)
	games.screen.add(enemy)
def Enemy_call_4():
	enemy_fighter_image_0 = games.load_image("media/smallfreighterspr.png")
	x_position = random.randint(55, games.screen.width - 55)
	y_position = 0
	speed = random.randint(1,3)
	enemy = Enemy_space_ship_0(image = enemy_fighter_image_0, x = x_position, y = y_position, dy = speed, dx = 0)
	games.screen.add(enemy)
def Enemy_call_5():
	enemy_fighter_image_0 = games.load_image("media/speedship.png")
	x_position = random.randint(55, games.screen.width - 55)
	y_position = 0
	speed = random.randint(1,3)
	enemy = Enemy_space_ship_0(image = enemy_fighter_image_0, x = x_position, y = y_position, dy = speed, dx = 0)
	games.screen.add(enemy)
def Enemy_call_6():
	enemy_fighter_image_0 = games.load_image("media/spshipspr1.png")
	x_position = random.randint(55, games.screen.width - 55)
	y_position = 0
	speed = random.randint(1,3)
	enemy = Enemy_space_ship_0(image = enemy_fighter_image_0, x = x_position, y = y_position, dy = speed, dx = 0)
	games.screen.add(enemy)
def Enemy_call_7():
	enemy_fighter_image_0 = games.load_image("media/xspr5.png")
	x_position = random.randint(55, games.screen.width - 55)
	y_position = 0
	speed = random.randint(1,3)
	enemy = Enemy_space_ship_0(image = enemy_fighter_image_0, x = x_position, y = y_position, dy = speed, dx = 0)
	games.screen.add(enemy)
#choice of Enemy
def random_choice_enemys():
	choice = random.randint(0, 7)
	if choice == 0:
		Enemy_call()
	elif choice == 1:
		Enemy_call_1()
	elif choice == 2:
		Enemy_call_2()
	elif choice == 3:
		Enemy_call_3()
	elif choice == 4:
		Enemy_call_4()
	elif choice == 5:
		Enemy_call_5()
	elif choice == 6:
		Enemy_call_6()
	elif choice == 7:
		Enemy_call_7()
#amount of user/player kills
class Score(games.Text):
	def update(self):
		pass
	def die(self):
		pass
def init_Score():
	game_score = Score(value = "Score:", size = 25, color = color.white, x = 40, y = 15, is_collideable = False)
	games.screen.add(game_score)
	return game_score
#Sprite and model of bullets
class Shooter(games.Sprite):	
	def update(self):
		global bullet_number
		self.check_ol()
		#use it to monitor the position of sprite: print(self.get_position())
		if self.y == 0:
			self.destroy()
			bullet_number -= 1
	def check_ol(self):
		global bullet_number
		for object in self.overlapping_sprites:
			object.die()
			bullet_number -= 1
			self.destroy()
	def die(self):
		pass
	def register(self):
		pass
class Enemy_shoot(games.Sprite):
	def update(self):
		global bullet_number
		self.lim = self.get_y()
		if self.y == 500 or self.lim > 500:
			self.destroy()
			bullet_number -= 1
	def register(self):
		pass
	def die(self):
		pass
class Lives(games.Sprite):
	def die(self):
		pass
	def register(self):
		pass
	def registration(self):
		pass
def init_lives():
	global list_of_lives
	live_image = games.load_image("media/live.bmp")
	live = Lives(image = live_image, x = 900, y = 20, is_collideable = False)
	live_1 = Lives(image = live_image, x = 930, y = 20, is_collideable = False)
	live_2 = Lives(image = live_image, x = 960, y = 20, is_collideable = False)
	games.screen.add(live)
	games.screen.add(live_1)
	games.screen.add(live_2)
	list_of_lives.append(live)
	list_of_lives.append(live_1)
	list_of_lives.append(live_2)
class Explosion(games.Animation):
	def die(self):
		pass
	def register(self):
		pass
	def registration(self):
		pass
def init_Shoot_sound():
	Shooter_sound = games.load_sound("media/shoot_s.wav")
	return Shooter_sound
def init_Shoot_sound_1():
	Shooter_sound = games.load_sound("media/boom.wav")
	return Shooter_sound
def init_Shoot_sound_2():
	Shooter_sound = games.load_sound("media/enemy.wav")
	return Shooter_sound
class Over(games.Text):
	over_start = False
	over_timer = 0
	def update(self):
		self.over_timer += 1
		if self.over_timer == 300:
			self.destroy()
			games.screen.clear()
			games.screen.quit()	
	def check_ol(self):
	    pass
	def register(self):
	    pass
	def die(self):
		pass
class Start(games.Question):
	def update(self):
		if games.keyboard.is_pressed(pygame.K_SPACE):
			self.destroy()
			games.screen.clear()
			main_part()
def init_start():
	game_start = Start(value = "Press 'Space' to play", size = 40, color = color.gray, x = games.screen.width / 2, y = (games.screen.height / 2)-170, responses = ())
	games.screen.add(game_start)
	g_name = games.Text(value = 'StarFight: Exodus',size = 80, color = color.gray, x = games.screen.width / 2, y = (games.screen.height / 2)-220)
	games.screen.add(g_name)
	g_description = games.Text(value = 'Buttons:',size = 25, color = color.gray, x = 40, y = (games.screen.height / 2)+150)
	games.screen.add(g_description)
	g_description = games.Text(value = '[Space]-Shoot',size = 25, color = color.gray, x = 75, y = (games.screen.height / 2)+165)
	games.screen.add(g_description)
	g_description = games.Text(value = '[Esc]-Exit',size = 25, color = color.gray, x = 58, y = (games.screen.height / 2)+182)
	games.screen.add(g_description)
	g_description = games.Text(value = '[<-/->]-Left/Right move',size = 25, color = color.gray, x = 110, y = (games.screen.height / 2)+198)
	games.screen.add(g_description)
	g_description = games.Text(value = '[Tab]-Light mode',size = 25, color = color.gray, x = 87, y = (games.screen.height / 2)+214)
	games.screen.add(g_description)
	#return game_start
def main_part():
	global g_score
	#Score, the amount of enemy`s destroys
	background_image = games.load_image("media/bk.jpg", transparent = False)
	games.screen.background = background_image
	g_score = init_Score()
	#initialization of player and creating the model or Sprite of player
	#m_s()
	player_initialization()
	#call enemys
	random_choice_enemys()
	init_lives()
	#display light mode
	init_mode_show()

	games.music.load('media/space walk.ogg')
	games.music.play(-1)

class Mode(games.Text):
	def update(self):
		if switch == -1:
			self.value = "Light mode: off"
		elif switch == 1:
			self.value = "Light mode: on"
def init_mode_show():
	disp_mode = Mode(value = "Light mode: off", size = 20, color = color.white, x = 930, y = 45, is_collideable = False)
	games.screen.add(disp_mode)

if __name__ == '__main__':
	#Class game Screen 
	Exodus()
	#calling  visible for user part of programm!
	init_start()
	#Calling the main part after pressing of 'Space' Button
	games.screen.mainloop()