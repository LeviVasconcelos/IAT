import numpy as np

def abs_range(a,b):
	return range(a,b+1) if a < b else range(a,b-1,-1)

class SelectWindow:
	def __init__(self, buffer_img, true_img, targ_img):
		self.iy = self.ix = self.fy = self.fx = 0
		self.moving = False
		self.selected = False
		self.tag = 0
		self.class_dict = {0:np.array([255,0,0], np.uint8), 1:np.array([0,255,0], np.uint8), 2:np.array([0,0,255], np.uint8)}
		self.color = np.array([255,0,0], np.uint8) #blue
		self.buffer_img = buffer_img
		self.true_img = true_img
		self.targ_img = targ_img

	def set_coords(self, x, y, fx, fy):
		self.ix = x
		self.iy = y
		self.fx = fx
		self.fy = fy

	def update_window(self, fx, fy):
		self.fx = fx
		self.fy = fy

	def within(self, x, y):
		if x >= self.ix and x <= self.fx and y >= self.iy and y <= self.fy:
			return True
		return False

	def get_sizes(self):
		width = abs(self.ix - self.fx)
		height = abs(self.iy - self.fy)
		return (width,height)

	def move_window(self, delta_x, delta_y):
		self.ix += delta_x
		self.iy += delta_y
		self.fx += delta_x
		self.fy += delta_y

	def set_tag(self, tag):
		self.tag = tag
		self.color = self.class_dict[self.tag]

	def draw_on_move(self, x, y):
		(w,h) = self.get_sizes()
		width = abs(x - self.ix) - w
		height = abs(y - self.iy) - h
		x_offset = 1 if x - self.ix >= 0 else -1
		y_offset = 1 if y - self.iy >= 0 else -1

		#horizontal:
		if y != self.fy:
			self.draw(x, y + (0 if height >= 0 else y_offset), self.ix , self.fy + (y_offset if height >= 0 else 0))
		#vertical
		if x != self.fx:
			self.draw(x + (0 if width >= 0 else x_offset), y, self.fx + (x_offset if width >= 0 else 0), self.iy)
		#intersection
		if x != self.fx and y != self.fy:
			self.draw(x + (0 if width >= 0 else x_offset) , y + (0 if height >= 0 else y_offset), self.fx + (x_offset if width >= 0 else 0), self.fy + (y_offset if height >= 0 else 0))

		self.update_window(x,y)


	def remove_window(self):
		self.draw(self.ix, self.iy, self.fx, self.fy)

	def draw_finished(self):
		self.draw(self.ix, self.iy, self.fx, self.fy)

	def get_color(self, pColor):
		c = [max(pColor[i],self.color[i]) for i in range(0,3)]
		return np.matrix(c, np.uint8)

	def draw_buffer_only(self):
		for i in abs_range(self.iy, self.fy):
			for j in abs_range(self.ix, self.fx):
				self.buffer_img[i,j] = self.buffer_img[i,j] ^ 1

	def draw(self, ix, iy, fx, fy):
		for i in abs_range(iy, fy):
			for j in abs_range(ix, fx):
				self.buffer_img[i,j] = self.buffer_img[i,j] ^ 1
				self.targ_img[i,j] = self.get_color(self.true_img[i,j]) if self.buffer_img[i,j] else self.true_img[i,j]

	def get_window_data(self):
		rect = {'ix':self.ix, 'iy':self.iy, 'fx':self.fx, 'fy':self.fy, 'tag':self.tag}
		return rect


