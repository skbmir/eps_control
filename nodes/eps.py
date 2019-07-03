import re
import time
import serial
import threading

class EPS():
    '''
    '''
    def __init__(self, port, baud_rate, 
                 steering_rate, telemetry_period,
                 max_angle, max_steer, middle_steer):
        '''
        '''
        self.__port = port
        self.__baud_rate = baud_rate
        self.__client = serial.Serial(self.__port, self.__baud_rate)
        self._steering_rate = steering_rate
        self._telemetry_period = telemetry_period
        self._angle = 0

        self.__can_sync = threading.Event()
        
        self.__MAX_ANGLE = 32
        self.__MAX_STEER = 2000
        self.__MIDDLE_STEER = 1000
        self.__STEER_DELTA = self.__MAX_STEER - self.__MIDDLE_STEER

        self._stop = False
        self.__allow_send_param_msg = True

        self.__control_sync_thread = threading.Thread(target=self.__ctrl_sync_worker)
        self.__param_sync_thread = threading.Thread(target=self.__param_sync_worker)

        self.__SYNC_CTRL_MSG = 'SEND_PACKET=2C0A8782000000020000000004\r\n'
        self.__SYNC_PARAM_MSG = 'SEND_PACKET=2C098782000000000000000000\r\n'
        self.__CONTROL_MSG = 'SEND_PACKET=2C088782000000000000000000\r\n'
        self.__REG_CTRL_1_MSG_HEAD = 'SEND_PACKET=2C208782'
        self.__REG_CTRL_1_MSG_TAIL = '0000000008\r\n'

    def __ctrl_sync_worker(self):
        '''
        '''
        while not self._stop:
            self.__client.write(self.__SYNC_CTRL_MSG)
            time.sleep(0.01)
            self.__can_sync.set()
            time.sleep(0.04)

    def __param_sync_worker(self):
        '''
        '''
        while not self._stop:
            self.__can_sync.wait()
            self.__client.write(self.__SYNC_PARAM_MSG)
            self.__can_sync.clear()
            time.sleep(self._telemetry_period)

    def __connect(self):
        '''
        '''
        self.__client.open()

        self.__client.write('DISABLE INFO MESSAGE\r\n')
        self.__client.write('BAUDRATE_CAN=0003D090\r\n')
        self.__client.write('DISABLE PASSIVE MODE\r\n')
        self.__client.write('DISABLE BIN MODE\r\n')
        self.__client.write('ENABLE CAN RXTX\r\n')
        
        self.__client.write(self.__CONTROL_MSG)

    def start(self):
        '''
        '''
        self.__connect()

        self.__control_sync_thread.start()
        self.__param_sync_thread.start()

    def stop(self):
        '''
        '''
        self._stop = True

        self.__control_sync_thread.join()
        self.__param_sync_thread.join()

    def set_steering_angle(self, angle):
        '''
        '''
        if angle < -1.0:
            angle = -1.0
        elif angle > 1.0:
            angle = 1.0
        
        angle = angle * self.__MAX_ANGLE
        steer_cmd = int((angle * self.__STEER_DELTA) / self.__MAX_ANGLE + self.__MIDDLE_STEER)

        cmd = self.__REG_CTRL_1_MSG_HEAD
        cmd += format(self._steering_rate, '04x')
        cmd += format(steer_cmd, '04x')
        cmd += self.__REG_CTRL_1_MSG_TAIL
        self.__client.write(cmd)
