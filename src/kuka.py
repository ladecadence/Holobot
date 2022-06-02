from py_openshowvar import openshowvar
import random
import json

class Kuka:
    STATUS_OK = 104
    MOV_HOME = "100"

    def __init__(self, ip, port):
        # load movements
        try:
            f = open('movements.json',)
            self.movements = json.load(f)
        except :
            print("Can't open movements data")

        try:
            self.connected = False
            self.client = openshowvar(ip, port)
            if self.client.can_connect:
                self.connected = True
        except:
            print("Can't connect to robot")

    def status(self):
        status = int(self.client.read('EXT_ALIVE', debug=False))
        return status

    def move(self, number):
        self.client.write('EXT_ACTION', number, debug=False)

    def home(self):
        self.client.write('EXT_ACTION', self.MOV_HOME, debug=False)

    def is_moving(self):
        moving = int(self.client.read('EXT_STATUS', debug=True))
        return not not moving

    def get_movement(self, mov_id):
        return self.movements[mov_id]

    def get_random_movement(self):
        mov = random.randrange(len(self.movements))
        return self.movements[mov]

if __name__ == "__main__":
    kuka = Kuka("192.168.10.45", 7000)
    print(kuka.status())
