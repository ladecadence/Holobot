import os
import requests
import text
import colorlines
import invaders
import plasma
from PIL import Image, ImageOps


class HolobotLEDS:
    def __init__(self, url):
        self.url = url

    def upload_bmp(self, filename):
        bmp_file = open(filename, "rb")
        upload_url = self.url + "/upload"
        test_response = requests.post(upload_url, files = {"file": bmp_file})
        if test_response.ok:
            print("Upload completed successfully!")
            print(test_response.text)
        else:
            print("Something went wrong!")

    def show_stripes(self, time=None, width=None, steps=None, step_delay=None, color=None):
        url = self.url + "/stripes?"

        if time:
            url += "t=" + str(time) + "&"
        if width:
            url += "w=" + str(width) + "&"
        if steps:
            url += "s=" + str(steps) + "&"
        if step_delay:
            url += "d=" + str(step_delay) + "&"
        if color:
            url += "r=" + str(color[0]) + "&g=" + str(color[1]) + "&b=" + str(color[2])

        print(url)
        response = requests.get(url)
        if response.ok:
            print("Stripes OK!")
            print(response.text)
        else:
            print("Something went wrong!")

    def show_picture(self, delay=None, filename=None):
        url = self.url + "/picture?"

        if delay:
            url += "d=" + str(delay) + "&"

        if filename:
            url += "f=" + str(filename) + "&"

        response = requests.get(url)
        if response.ok:
            print("Picture OK!")
            print(response.text)
        else:
            print("Something went wrong!")

    def test(self):
        url = self.url + "/test"

        response = requests.get(url)
        if response.ok:
            print("LED Test OK!")
            print(response.text)
        else:
            print("Something went wrong!")

    def status(self):
        url = self.url + "/status"

        response = requests.get(url)
        if response.ok:
            print("Test OK!")
            status = response.text.splitlines()[0]
            message = response.text.splitlines()[1]
            return ((status, message))
        else:
            print("Something went wrong!")
            return (("255", "Problem communicating with LEDs"))

    def set_brightness(self, brightness=100):
        url = self.url + "/brightness"
        url += "?b=" + str(brightness)

        response = requests.get(url)
        if response.ok:
            print("Brightness OK!")
            print(response.text)
        else:
            print("Something went wrong!")

    def get_battery(self):
        url = self.url +  "/battery"

        response = requests.get(url)
        if response.ok:
            battery = response.text.strip()
            return battery
        else:
            print ("Problem reading battery")
            return 0

    def picture_info(self, picture):
        im = Image.open(picture)
        width, height = im.size
        return (width, height)

    def transform_picture(self, picture, pictureout, rotation, mirror):
            im = Image.open(picture)
            im = im.rotate(90*rotation, expand=True)
            if mirror :
                im = ImageOps.mirror(im)
            im.save(pictureout)


if __name__ == "__main__":
    holo = HolobotLEDS("http://holobot-leds.local")

    #text.gen_text(144, "¿Qué es industria?, dices mientras clavas\nen mi pupila tu pupila azul.\n¿Qué es industria? ¿Y tú me lo preguntas?\nIndustria... eres tú.", (255, 128, 0), 'img/text.bmp')
    #gen_text(62, "ola ke ase", (100, 100, 0), 'img/text.bmp')
    #show_stripes(time=5000, width=2, steps=3, step_delay=500, color=(255, 255, 255))
    #text.gen_banner(144, "MOLOBOT", (255, 0, 255), 'img/banner.bmp')
    #plasma.gen_plasmachars(200, 144, 'img/plasma.bmp', full=False)
    #invaders.gen_invaders(5, 5, 144, 200, 'img/invaders.bmp')
    #colorlines.gen_colorlines(200, 144, 15, 0.02, 'img/lines.bmp')

    #holo.upload_bmp('img/banner.bmp')
    #holo.upload_bmp('img/invaders.bmp')
    #holo.upload_bmp('img/test.bmp')
    #holo.upload_bmp("img/text.bmp")
    #holo.upload_bmp("img/plasma.bmp")
    #holo.upload_bmp("img/plantas1.bmp")
    holo.upload_bmp("../img/img.bmp")

    #holo.show_picture(delay=10, filename="banner.bmp")

