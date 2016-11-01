from selectwindow import SelectWindow
import pickle
import cv2
import glob
import numpy as np

class WindowHandler:
	def __init__(self, wName, dir_path):
		self.wName = wName
		self.dir_path = dir_path
		self.img_idx = 0
		

		self.windows = []
		
		self.newWindow = False

		self.ix = self.iy = 0
		self.activeWindow = None

		self.load_dir()
		if len(self.image_list):
			self._load_image(self.image_list[self.img_idx])
			

	def load_dir(self):
		self.image_list = glob.glob(self.dir_path + '*.jpg')

	def load_img(self, idx):
		if len(self.image_list) > idx:
			if (len(self.windows) > 0): #if any windows drawn, save them.
				self.dump_windows_to_file()
				self.windows = []
			self.img_idx = idx
			self._load_image(self.image_list[self.img_idx])


	def _load_image(self, img_fname):
		self.img_fname = img_fname
		self.true_img = cv2.imread(self.img_fname)
		self.targ_img = np.copy(self.true_img)
		self.buffer_img = np.zeros(self.true_img.shape[0:2], dtype = bool)
		self.windows = self.load_image_data()
		self.init_cvWindow()

	def load_image_data(self):
		print(self.generate_data_fname())
		self.data_fname = glob.glob(self.generate_data_fname())
		if len(self.data_fname) == 0:
			return []
		return self.load_windows_from_file(self.data_fname[0])

	def load_windows_from_file(self, fname):
		windows_list = []
		with open(fname, 'rb') as file:
			while(True): #Isso ta gambioso, ver um jeito de melhorar depois.
				try:
					data = pickle.load(file)
					w = SelectWindow(self.buffer_img, self.true_img, self.targ_img)
					w.set_coords(data['ix'], data['iy'], data['fx'], data['fy'])
					w.set_tag(data['tag'])
					windows_list.append(w)
				except:
					break
		print(len(windows_list))
		return windows_list





	def brute_force_search(self, x, y):
		for i,w in enumerate(self.windows):
			if w.within(x,y):
				return i
		return -1


	def find_window(self, x, y):
		if not len(self.windows):
			return -1

		return self.brute_force_search(x,y)

	def generate_data_fname(self):
		return self.img_fname.split('.')[-2] + '.data'

	def dump_windows_to_file(self):
		with open(self.generate_data_fname(), 'w') as file:
			for w in self.windows:
				pickle.dump(w.get_window_data(),file)


	def init_cvWindow(self):
		cv2.namedWindow(self.wName)
		cv2.setMouseCallback(self.wName, self.onMouseCB)
		sw = SelectWindow(self.buffer_img, self.true_img, self.targ_img)
		
		cv2.imshow(self.wName, self.targ_img)
		if len(self.windows):
			self.refresh_windows()
		self.onKeyPressed()

	def refresh_windows(self):
		for aw in self.windows:
			aw.draw_finished()
			aw.draw_buffer_only()


		

	def onMouseCB(self,event,x,y,flags,params):

		if event == cv2.EVENT_LBUTTONDOWN:

			w = self.find_window(x,y)
			if w < 0:
				self.newWindow = True
				self.activeWindow = SelectWindow(self.buffer_img, self.true_img, self.targ_img)
				self.activeWindow.set_coords(x,y,x,y)
				self.activeWindow.draw_finished()
				self.windows.append(self.activeWindow)

			else:
				self.activeWindow = self.windows[w]
				self.activeWindow.draw_finished()
				self.ix = x
				self.iy = y
				self.activeWindow.moving = True



		if event == cv2.EVENT_MOUSEMOVE:
			if self.newWindow:
				self.activeWindow.draw_on_move(x,y)
				cv2.imshow(self.wName, self.targ_img)

			if self.activeWindow and self.activeWindow.moving:
				self.activeWindow.remove_window()
				delta_x = x - self.ix
				delta_y = y - self.iy
				self.activeWindow.move_window(delta_x,delta_y)
				self.activeWindow.draw_finished()
				self.ix = x
				self.iy = y
				cv2.imshow(self.wName, self.targ_img)

		if event == cv2.EVENT_LBUTTONUP:
			self.activeWindow.moving = False
			self.newWindow = False
			self.activeWindow.draw_buffer_only()
			
	
	def onKeyPressed(self):
		while True:
			cv2.imshow(self.wName,self.targ_img)
			k = cv2.waitKey() % 256
			print('key: ' + str(k))
			if k == 120:
				break
			if k == 49 or k == 50:
				self.activeWindow.color = np.array([0, 200, 0], np.uint8) if k == 49 else np.array([0, 0, 255], np.uint8)
				self.activeWindow.tag = 1 if k == 49 else 2
				self.activeWindow.draw_finished()
				self.activeWindow.draw_buffer_only()
			if k == 114:
				self.refresh_windows()
			if k == 27:
				if self.activeWindow:
					self.activeWindow.draw_finished()
					self.activeWindow.draw_finished()
					self.windows.remove(self.activeWindow)
					self.activeWindow = self.windows[-1] if len(self.windows) else None
			if k == 113 or k == 119: # 'q' or 'w'
				if k == 119:
					self.load_img(self.img_idx+1)
					break
				else:
					self.load_img(self.img_idx-1)
					break
			if k == 111:
				self.dump_windows_to_file()


