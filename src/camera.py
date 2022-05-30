import gphoto2 as gp
from datetime import datetime

class Camera:
    # CANON EOS 1200D
    APERTURE_4      = "4"
    APERTURE_4_5    = "4.5"
    APERTURE_5      = "5"
    APERTURE_5_6    = "5.6"
    APERTURE_6_3    = "6.3"
    APERTURE_7_1    = "7.1"
    APERTURE_8      = "8"
    APERTURE_9      = "9"
    APERTURE_10     = "10"
    APERTURE_11     = "11"
    APERTURE_13     = "13"
    APERTURE_14     = "14"
    APERTURE_16     = "16"
    APERTURE_18     = "18"
    APERTURE_20     = "20"
    APERTURE_22     = "22"
    APERTURE_25     = "25"

    SHUTTER_30      = "30"
    SHUTTER_25      = "25"
    SHUTTER_20      = "20"
    SHUTTER_15      = "15"
    SHUTTER_13      = "13"
    SHUTTER_10_3    = "10.3"
    SHUTTER_8       = "8"
    SHUTTER_6_3     = "6.3"
    SHUTTER_5       = "5"
    SHUTTER_4       = "4"
    SHUTTER_3_2     = "3.2"
    SHUTTER_2_5     = "2.5"
    SHUTTER_2       = "2"
    SHUTTER_1_6     = "1.6"
    SHUTTER_1_3     = "1_3"
    SHUTTER_1       = "1"
    SHUTTER_0_8     = "0.8"
    SHUTTER_0_6     = "0.6"
    SHUTTER_0_5     = "0.5"
    SHUTTER_0_4     = "0.4"
    SHUTTER_0_3     = "0.3"
    SHUTTER_1_4TH   = "1/4"
    SHUTTER_1_5TH   = "1/5"
    SHUTTER_1_6TH   = "1/6"
    SHUTTER_1_8TH   = "1/8"
    SHUTTER_1_10TH  = "1/10"
    SHUTTER_1_13TH  = "1/13"
    SHUTTER_1_15TH  = "1/15"
    SHUTTER_1_20TH  = "1/20"
    SHUTTER_1_25TH  = "1/25"
    SHUTTER_1_40TH  = "1/40"
    SHUTTER_1_50TH  = "1/50"
    SHUTTER_1_60TH  = "1/60"
    SHUTTER_1_80TH  = "1/80"
    SHUTTER_1_100TH  = "1/100"
    SHUTTER_1_125TH  = "1/125"
    SHUTTER_1_160TH  = "1/160"
    SHUTTER_1_200TH  = "1/200"
    SHUTTER_1_250TH  = "1/250"
    SHUTTER_1_320TH  = "1/320"
    SHUTTER_1_400TH  = "1/400"
    SHUTTER_1_500TH  = "1/500"
    SHUTTER_1_640TH  = "1/640"
    SHUTTER_1_800TH  = "1/800"
    SHUTTER_1_1000TH  = "1/1000"
    SHUTTER_1_1250TH  = "1/1250"
    SHUTTER_1_1600TH  = "1/1600"
    SHUTTER_1_2000TH  = "1/2000"
    SHUTTER_1_2500TH  = "1/2500"
    SHUTTER_1_3200TH  = "1/3200"
    SHUTTER_1_4000TH  = "1/4000"

    ISO_AUTO = "AUTO"
    ISO_100 = "100"
    ISO_200 = "200"
    ISO_400 = "400"
    ISO_800 = "800"
    ISO_1600 = "1600"
    ISO_3200 = "3200"
    ISO_6400 = "6400"

    apertures = {4 : "4", 4.5 : "4.5", 5 : "5", 5.6 : "5.6", 6.3 : "6.3", 7.1 : "7.1", \
                8 : "8", 9 : "9", 10 : "10", 11 : "11", 13 : "13", 14 : "14", \
                16 : "16", 18 : "18", 20 : "20", 22 : "22", 25 : "25", }

    shutters = {5 : "5", 8 : "8", 10.3 : "10.3", 13 : "13", 15 : "15", 20 : "20", \
               25 : "25", 30 : "30", }

    def __init__(self, file_path):
        self.camera = gp.Camera()
        self.camera.init()
        self.config = self.camera.get_config()
        self.path = file_path

    def set_aperture(self, apert):
        OK, aperture = gp.gp_widget_get_child_by_name(self.config, 'aperture')
        if OK >= gp.GP_OK:
            aperture.set_value(apert)
            self.camera.set_config(self.config)
            return True
        else:
            return False

    def set_shutter_speed(self, speed):
        OK, shutter_speed = gp.gp_widget_get_child_by_name(self.config, 'shutterspeed')
        if OK >= gp.GP_OK:
            shutter_speed.set_value(speed)
            self.camera.set_config(self.config)
            return True
        else:
            return False

    def set_iso(self, value):
        OK, iso = gp.gp_widget_get_child_by_name(self.config, 'iso')
        if OK >= gp.GP_OK:
            iso.set_value(value)
            self.camera.set_config(self.config)
            return True
        else:
            return False

    def take_picture(self):
        file_path = self.camera.capture(gp.GP_CAPTURE_IMAGE)
        camera_file = self.camera.file_get(file_path.folder, file_path.name, gp.GP_FILE_TYPE_NORMAL)
        pic_name = datetime.now().strftime("holobot_pic_%Y%m%d_%H%M%S.jpg")
        camera_file.save(self.path + pic_name)
        camera_file.save(self.path + "last.jpg")

    def get_longer_shutter(self, duration):
        # try to find a long enough exposure time
        for shutter in self.shutters.items():
            if shutter[0] >= duration:
                return shutter[0]
        # no one? return longer
        return 20

    def __del__(self):
        self.camera.exit()

if __name__ == "__main__":
    cam = Camera("/home/zako/Imáxenes/")
    cam.set_aperture(cam.APERTURE_25)
    cam.set_shutter_speed(cam.SHUTTER_8)
    cam.set_iso(cam.ISO_100)
    cam.take_picture()

    
