import time
from tkinter import *
import tkinter as tk
import numpy as np
from PIL import Image, ImageTk

#쥐 월드!
class MouseWorld():
    def __init__(self):
        self.window = tk.Tk()

        # 쥐 월드 제작
        self.pixel_size = 80         # 픽셀 크기
        self.mouse_world_height = 5  # 쥐 월드 높이
        self.mouse_world_width = 5   # 쥐 월드 너비
        self.mouse_world_height_pixel = self.pixel_size * self.mouse_world_height
        self.mouse_world_width_pixel = self.pixel_size * self.mouse_world_width

        # 캔버스에 그리드 월드를 가져 옴
        self.canvas = tk.Canvas(self.window, background="forest green",\
                                width=self.mouse_world_width_pixel,\
                                height=self.mouse_world_height_pixel)

        self.action_space = ['up', 'down', 'left', 'right']   # 쥐가 할 수 있는 액션
        self.num_actions = len(self.action_space)             # 쥐가 할 수 있는 액션의 수
        self.window.geometry(str(self.mouse_world_width_pixel) + \
                             "x" + str(self.mouse_world_height_pixel))

        # Grid 영역 나눠주기 (row_num)
        for row_num in range(self.mouse_world_height):
            self.canvas.create_line(0, self.pixel_size * row_num,\
                                    self.mouse_world_width_pixel,\
                                    self.pixel_size * row_num, fill="dark green")

        # Grid 영역 나눠주기 (col_num)
        for col_num in range(self.mouse_world_width):
            self.canvas.create_line(self.pixel_size * col_num, 0,\
                                    self.pixel_size * col_num,\
                                    self.mouse_world_height_pixel, fill="dark green")

        # 생쥐 출발 지점 및 쥐 소환
        self.origin = np.array([20, 20])
        self.mouse = self.load_image(image_name="./mouse.jpg", location=[0, 0])

        # 함정 소환
        self.fire_position = [[1, 4], [3, 2]]
        self.fire_1 = self.make_trap_goal(self.fire_position[0], "fire", 1)
        self.fire_2 = self.make_trap_goal(self.fire_position[1], "fire", 2)

        # 도착 지점 소환
        self.goal_position = [[3, 3]]
        self.goal_1 = self.make_trap_goal(self.goal_position[0], "goal", 1)

        self.canvas.pack()

    # trap이나 goal을 만들어주는 함수
    def make_trap_goal(self, position, name, num):
        move_right = self.pixel_size * position[0]
        move_down = self.pixel_size * position[1]
        trap_goal_center = self.origin + np.array([move_right, move_down])

        if name == "fire":
            vars()["fire"+str(num)] = self.canvas.create_rectangle(
                trap_goal_center[0] - 0, trap_goal_center[1] - 0,
                trap_goal_center[0] + 0, trap_goal_center[1] + 0,
                fill='red')
            return vars()["fire"+str(num)]

        elif name == "goal":
            vars()["goal"+str(num)] = self.canvas.create_rectangle(
                trap_goal_center[0] - 0, trap_goal_center[1] - 0,
                trap_goal_center[0] + 0, trap_goal_center[1] + 0,
                fill='lightblue')
            return vars()["goal"+str(num)]

        elif name == "forest":
            vars()["goal"+str(num)] = self.canvas.create_rectangle(
                trap_goal_center[0] - 15, trap_goal_center[1] - 15,
                trap_goal_center[0] + 15, trap_goal_center[1] + 15,
                fill='green')
            return vars()["forest"+str(num)]

    #이미지 로드용 함수
    def load_image(self, image_name="./mouse.jpg", location=[0, 0], size=[60, 20], anchor=tk.SW):
        load = Image.open(image_name).resize((size[0], size[1]))
        photo = ImageTk.PhotoImage(load)
        loaded_img = self.canvas.create_image(location[0], location[1], anchor=anchor, image=photo)
        label = Label(image=photo)
        label.image = photo
        return loaded_img

    # 게임 리셋 함수
    def reset(self):
        self.window.update()
        time.sleep(0.05)
        self.canvas.delete(self.mouse)
        self.origin = np.array([20, 20])

        # 각 사물 배치 시키기
        self.board = self.load_image(image_name="./board.jpg", location=[200, 200], \
                                       size=[self.pixel_size * self.mouse_world_height,\
                                             self.pixel_size * self.mouse_world_width],\
                                             anchor=tk.CENTER)

        self.grass_1 = self.load_image(image_name="./grass.jpg", location=[90, 80])
        self.grass_2 = self.load_image(image_name="./grass.jpg", location=[170, 80])
        self.grass_3 = self.load_image(image_name="./grass.jpg", location=[170, 230])
        self.grass_4 = self.load_image(image_name="./grass.jpg", location=[90, 310])
        self.grass_5 = self.load_image(image_name="./grass.jpg", location=[250, 390])
        self.grass_6 = self.load_image(image_name="./grass.jpg", location=[330, 310])
        self.grass_7 = self.load_image(image_name="./grass.jpg", location=[410, 470])

        self.trap_jpg_1 = self.load_image(image_name="./trap.jpg",\
                                       location=[self.pixel_size * self.fire_position[0][0] + self.pixel_size//2,\
                                                 self.pixel_size * self.fire_position[0][1] + self.pixel_size//2],\
                                       size=[self.pixel_size * 3//5, self.pixel_size * 3//5], anchor=tk.CENTER)

        self.trap_jpg_2 = self.load_image(image_name="./trap.jpg",\
                                       location=[self.pixel_size * self.fire_position[1][0] + self.pixel_size//2,\
                                                 self.pixel_size * self.fire_position[1][1] + self.pixel_size//2],\
                                       size=[self.pixel_size * 3//5, self.pixel_size * 3//5], anchor=tk.CENTER)

        self.cheese_jpg = self.load_image(image_name="./cheese.jpg",\
                                         location=[self.pixel_size * self.goal_position[0][0] + self.pixel_size//2,\
                                                   self.pixel_size * self.goal_position[0][1] + self.pixel_size//2],\
                                         size=[self.pixel_size * 3//5, self.pixel_size * 3//5], anchor=tk.CENTER)

        self.mouse = self.load_image(image_name="./mouse.jpg", location=[self.pixel_size // 2, self.pixel_size // 2],\
                                     size=[self.pixel_size  * 3//5, self.pixel_size  * 3//5], anchor=tk.CENTER)

        s = self.canvas.coords(self.mouse)

        return self.origin

    # 생쥐의 이동 함수
    def step(self, action):
        s = self.canvas.coords(self.mouse)
        strans = [s[0]-20, s[1]-20]

        base_action = np.array([0, 0])
        if action == 0:   # up
            if strans[1] > self.pixel_size:
                base_action[1] -= self.pixel_size
        elif action == 1:   # down
            if strans[1] < (self.mouse_world_height - 1) * self.pixel_size:
                base_action[1] += self.pixel_size
        elif action == 2:   # right
            if strans[0] < (self.mouse_world_width - 1) * self.pixel_size:
                base_action[0] += self.pixel_size
        elif action == 3:   # left
            if strans[0] > self.pixel_size:
                base_action[0] -= self.pixel_size

        self.canvas.move(self.mouse, base_action[0], base_action[1])
        s_ = self.canvas.coords(self.mouse)  # next state
        s_trans = [s_[0]-20, s_[1]-20]

        # reward function
        if s_trans == self.return_mid(self.goal_1):
            reward = 1
            done = True
        elif s_trans in [self.return_mid(self.fire_1), self.return_mid(self.fire_2)]:
            reward = -1
            done = True
        else:
            reward = 0
            done = False
        return s_trans, reward, done

    # 중간 지점 리턴 함수
    def return_mid(self, rect_name):
        temp_position = self.canvas.coords(rect_name)
        return [(temp_position[0] + temp_position[2])/2,\
                (temp_position[1] + temp_position[3])/2]

    # 랜더링 함수
    def render(self):
        time.sleep(0.05)
        self.window.update()

if __name__ == "__main__":
    ENV = MouseWorld()
    ENV.window.mainloop()
