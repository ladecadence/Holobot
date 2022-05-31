import config
import holobotleds
import camera
import kuka
import tkinter as tk
from tkinter import ttk
from tkinter.colorchooser import askcolor
from PIL import ImageTk,Image
import liblo
import time
import random
import threading
import http.server
import socketserver
import os

class Holobot(tk.Frame):

    def __init__(self, master=None):
        # tk init
        super().__init__(master)
        self.master = master
        self.master.geometry("600x920")
        self.master.protocol("WM_DELETE_WINDOW", self.on_exit)
        self.pack(fill='both', expand=True)
        # variables
        self.color = (255, 255, 255)
        self.time = tk.IntVar()
        self.shutter = 8
        self.brightness = 100
        self.auto = False
        # threads
        self.server_thread = None
        self.handler = http.server.SimpleHTTPRequestHandler

        # init submodules
        try:
            # holobot related
            self.config = config.options
            self.leds = holobotleds.HolobotLEDS(self.config["url_leds"])
            self.kuka = kuka.Kuka(self.config["ip_robot"], self.config["port_robot"])
            #self.camera = camera.Camera(self.config["image_path"])
        except TimeoutError:
            pass
        try:
            self.vis = liblo.Address(self.config["ip_vis"], self.config["port_vis"])
        except liblo.AddressError as err:
            print(err)
            sys.exit()

        # init GUI
        self.create_widgets()

    # tk rgb to hex notation
    def convert_rgb(self, rgb):
        return "#%02x%02x%02x" % rgb

    # web server
    def start_server(self):
        '''Start a simple webserver serving image path to share camera images'''
        os.chdir(self.config["image_path"])
        self.httpd = http.server.HTTPServer(('', self.config["http_server_port"]), self.handler)
        self.httpd.serve_forever()

    # move slider only through shutter values
    def valuecheck_shutter(self, value):
        newvalue = min(camera.Camera.shutters.keys(), key=lambda x:abs(x-float(value)))
        self.shutter_scale.set(newvalue)
        self.shutter = newvalue

    # Status related
    def get_status_robot(self):
        if self.kuka.connected:
            if self.kuka.status() == self.kuka.STATUS_OK:
                return "OK"
            else:
                return "BAD STATUS"
        else:
            return "NOT CONNECTED"

    def get_status_leds(self):
        status = self.leds.status()
        return "" + status[0] + " : " + status[1]


    # LED related
    def test_leds(self):
        self.leds.test()

    def set_brightness(self, value):
        if not self.auto:
            self.brightness = self.brightness_scale.get()
            print("brillo! " + str(self.brightness))
            self.leds.set_brightness(self.brightness)

    def test_lines(self):
        self.kuka.move("1")
        while self.kuka.is_moving():
            time.sleep(0.25)
        self.leds.show_stripes(time=self.time.get() * 1000, width=10, steps=5, step_delay=500, color=self.color)
        self.kuka.move("101")

    def test_all(self):
        self.camera.set_aperture(self.camera.APERTURE_25)
        self.camera.set_shutter_speed(str(self.shutter))
        self.camera.set_iso(self.camera.ISO_100)

        self.leds.show_stripes(time=(self.time.get() * 1000), width=10, steps=5, step_delay=500, color=self.color)
        self.camera.take_picture()
        self.after(2000, self.reload_img)

    def test_all_img(self):
        #self.camera.set_aperture(self.camera.APERTURE_25)
        #self.camera.set_shutter_speed(str(self.shutter))
        #self.camera.set_iso(self.camera.ISO_100)

        self.leds.show_picture(delay=35, filename="img.bmp")
        #self.camera.take_picture()
        self.after(2000, self.reload_img)

    # GUI and threads
    def create_widgets(self):
        self.robot_status_label = tk.Label(self)
        self.robot_status_label["text"] = "Robot status = " + str(self.get_status_robot())
        self.robot_status_label.pack(padx=20, pady=10, fill='x')

        self.leds_status_label = tk.Label(self)
        self.leds_status_label["text"] = "LEDs status = " #+ self.get_status_leds()
        self.leds_status_label.pack(padx=20, pady=10, fill='x')

        self.robot_test_leds_button = tk.Button(self)
        self.robot_test_leds_button["text"] = "Test LEDs"
        self.robot_test_leds_button["command"] = self.test_leds
        self.robot_test_leds_button.pack(padx=10, pady=5, fill='x')

        self.robot_test_lines_button = tk.Button(self)
        self.robot_test_lines_button["text"] = "Test Lines"
        self.robot_test_lines_button["command"] = self.test_lines
        self.robot_test_lines_button.pack(padx=10, pady=5, fill='x')

        self.robot_test_all_button = tk.Button(self)
        self.robot_test_all_button["text"] = "Test All"
        self.robot_test_all_button["command"] = self.test_all
        self.robot_test_all_button.pack(padx=10, pady=5, fill='x')

        self.robot_test_all_img_button = tk.Button(self)
        self.robot_test_all_img_button["text"] = "Test All + Image"
        self.robot_test_all_img_button["command"] = self.test_all_img
        self.robot_test_all_img_button.pack(padx=10, pady=5, fill='x')

        self.robot_color_button = tk.Button(self)
        self.robot_color_button["text"] = "COLOR"
        self.robot_color_button.configure(bg = "black",  fg = self.convert_rgb(self.color))
        self.robot_color_button["command"] = self.change_color
        self.robot_color_button.pack(padx=10, pady=5, fill='x')

        self.brightness_scale = tk.Scale(self, variable = self.brightness, orient=tk.HORIZONTAL, from_=0, to=255, label="Brightness")
        self.brightness_scale.bind("<ButtonRelease-1>", self.set_brightness)
        self.brightness_scale.pack(padx=10, pady=10, fill='x')
        self.brightness_scale.set(100)

        self.time_scale = tk.Scale(self, variable = self.time, orient=tk.HORIZONTAL, from_=1, to=30, label="Time")
        self.time_scale.pack(padx=10, pady=10, fill='x')
        self.time_scale.set(8)

        self.shutter_scale = tk.Scale(self, variable = self.shutter, orient=tk.HORIZONTAL, from_=5, to=30, label="Shutter", command=self.valuecheck_shutter)
        self.shutter_scale.pack(padx=10, pady=10, fill='x')

        self.last_img = Image.open(self.config["image_path"] + "last.jpg")
        self.last_img = self.last_img.resize((400, 300), Image.Resampling.LANCZOS)
        self.last_img = ImageTk.PhotoImage(self.last_img)

        self.img_label = tk.Label(self, image = self.last_img)
        self.img_label.image = self.last_img
        self.img_label.pack(padx=10, pady=10)

        self.auto_button = tk.Button(self)
        self.auto_button["text"] = "AUTO MODE"
        self.auto_button["command"] = self.change_auto
        self.auto_button.configure(bg = "red4",  fg = "white")
        self.auto_button.pack(padx=10, pady=5, fill='x')

        self.statusbar = ttk.Label(self, text="", relief=tk.SUNKEN, anchor=tk.W)
        self.statusbar.pack(side='bottom', fill="x", expand=True)
        self.statusbar["text"] = "READY"

        # server thread
        self.server_thread = threading.Thread(name='http_server',
                          target=self.start_server)
        self.server_thread.setDaemon(True)
        self.server_thread.start()

    def debug(self, msg):
        self.statusbar["text"] = msg

    def reload_img(self):
        self.last_img = Image.open(self.config["image_path"] + "last.jpg")
        self.last_img = self.last_img.resize((400, 300), Image.Resampling.LANCZOS)
        self.last_img = ImageTk.PhotoImage(self.last_img)

        #self.img_label = tk.Label(self, image = self.last_img)
        self.img_label.config(image=self.last_img)

    def change_color(self):
        colors = askcolor(title="Color Chooser")
        #print(colors)
        self.color = colors[0]
        self.robot_color_button.configure(bg = "black",  fg = self.convert_rgb(self.color))

    def blink_auto(self):
        if self.auto:
            if self.auto_button["fg"] == "white":
                self.auto_button["fg"] = "black"
                self.auto_button["bg"] = "red"
            else:
                self.auto_button["fg"] = "white"
                self.auto_button["bg"] = "red4"
            self.after(1000, self.blink_auto)

    def get_random_color(self):
        # avoid very dark colors
        r = random.randint(50, 200)
        g = random.randint(50, 200)
        b = random.randint(50, 200)

        return (r, g, b)

    def launch_random_animation(self, duration, rot, mirror):
        # one in several is a picture
        rnd = random.randint(1, 5)
        if rnd == 1 or rnd == 2:
            # get picture width
            width, height= self.leds.picture_info(self.config["picture_path"] + self.config["picture_name"])
            # rotate it
            self.leds.transform_picture(self.config["picture_path"] + self.config["picture_name"], \
                                     self.config["picture_path"] + self.config["temp_picture_name"],
                                     rot, mirror)
            # upload it
            self.debug("Uploading picture: " + self.config["temp_picture_name"] + "...")
            self.leds.upload_bmp(self.config["picture_path"] + self.config["temp_picture_name"])
            # calculate time
            duration = (duration * 1000) - 500 # (ms)
            time.sleep(0.25)
            self.leds.show_picture(delay=int(duration//width), filename=self.config["temp_picture_name"])

        else:
        # lines
            w = random.randint(1, 20)
            c = self.get_random_color()
            s = random.randint(1, 5)
            d = random.randint(100, 1000)
            self.leds.show_stripes(time=duration * 1000, width=w, steps=s, step_delay=d, color=c)

    # AUTO mode
    def change_auto(self):
        self.auto = not self.auto
        if self.auto:
            # disable manual controls TODO
            self.robot_test_leds_button["state"] = "disabled"
            self.robot_test_lines_button["state"] = "disabled"
            self.robot_test_all_button["state"] = "disabled"
            self.robot_test_all_img_button["state"] = "disabled"
            self.robot_color_button["state"] = "disabled"
            self.brightness_scale.configure(state = "disabled", takefocus=0)
            pass
            # launch auto mode in a new thread
            self.blink_auto()
            self.auto_thread = threading.Thread(target = self.auto_mode)
            self.auto_thread.start()
            pass
        else:
            # enable controls TODO
            self.robot_test_leds_button["state"] = "normal"
            self.robot_test_lines_button["state"] = "normal"
            self.robot_test_all_button["state"] = "normal"
            self.robot_test_all_img_button["state"] = "normal"
            self.robot_color_button["state"] = "normal"
            self.brightness_scale.configure(state = "normal", takefocus=1)
            pass

    def auto_mode(self):
        while (self.auto):
            # get a random movement
            mov = self.kuka.get_random_movement()
            # configure camera
            shutter = self.camera.get_longer_shutter(mov["duration"])
            print("Shutter: " + str(shutter))
            self.camera.set_aperture(self.camera.APERTURE_25)
            self.camera.set_shutter_speed(str(shutter))
            self.camera.set_iso(self.camera.ISO_100)

            # move to starting point
            self.debug("Moving to origin: " + mov["startpos"])
            self.kuka.move(mov["startpos"])
            while (self.kuka.is_moving() and self.auto):
                time.sleep(0.25)

            # ok, now call the movement, LED animation and trigger camera,
            self.launch_random_animation(mov["duration"], mov["rot"], mov["mirror"])
            # camera blocks, so launch it in a thread
            cam_th = threading.Thread(target = self.camera.take_picture)

            #self.camera.take_picture()
            cam_th.start()
            self.debug("Movement: " + mov["name"])
            self.kuka.move(mov["id"])
            while (self.kuka.is_moving() and self.auto):
                time.sleep(0.25)
            # wait for camera to finish
            cam_th.join()

            # return home
            self.debug("Homing...")
            self.kuka.home()

    def on_exit(self):
        self.auto=False
        self.master.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    root.title("Holobot")
    root.iconphoto(False, tk.PhotoImage(file='../holobot.png'))
    holo = Holobot(master = root)
    holo.mainloop()

 
