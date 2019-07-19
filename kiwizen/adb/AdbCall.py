
import time
import os
import re
from IPython import embed


class Device:
    def __init__(self, sn=None, wireless=False):
        # serial number or other identifier of connected device
        self.sn = None
        devices = self.get_device_identifier()
        if not devices:
            raise EnvironmentError(
                "设备未连接， 请检查：\n\t1）USB调试模式是否开启；\n\t2）手机驱动是否安装成功，可下载手机助手之类的软件进行安装")
        else:
            if sn is not None and sn in devices:
                self.sn = sn
            else:
                devices_no = len(devices)
                if devices_no == 1:
                    self.sn = devices[0]
                else:
                    print("There are %s devices connected:" % devices_no)
                    for i, device in enumerate(devices, 1):
                        print("[%s] %s" % (i, device))
                    in_no = -1
                    while in_no <= 0 or in_no > devices_no:
                        choice = input("Please input the No of device:")
                        try:
                            in_no = int(choice)
                        except:
                            continue
                    self.sn = devices[in_no-1]
        print("Connect device serial number: %s" % self.sn)

        info = self.get_device_info()
        print(info)
        self.width = info['screen_width']
        self.height = info['screen_height']
        if wireless:
            if info.get("ip", ''):
                self.sn = '%s:5555' % info['ip']
                # start wireless mode
                print(self.adb_command("adb tcpip 5555"))
                time.sleep(2)
                self.adb_command("adb connect %s" % info['ip'])
                if self.sn in self.get_device_identifier():
                    print(
                        "Wireless connection built, device ip:%s, \nPlease unplug phone USB connetion with PC.\n\n" % info['ip'])
                else:
                    raise ValueError("Wireless connection failed")

    def get_device_identifier(self):
        devices_info = self.adb_command("adb devices")
        print(devices_info)
        devices = re.findall("\n([\w\d.:]+)\s+device", devices_info)
        return devices

    def adb_command(self, command, wait=0.5):
        if self.sn:
            l = command.split()
            l.insert(1, "-s %s" % self.sn)
            command = " ".join(l)
        time.sleep(wait)
        return os.popen(command).read()

    def press_key(self, key_code, wait=0.5):
        return self.adb_command('adb shell input keyevent %s' % key_code, wait)

    def get_device_info(self):
        info = {}
        # screen size
        wh = self.adb_command("adb shell wm size")
        wh = re.search(".*?(\d+)x(\d+)", wh)
        if wh:
            wh = wh.groups()
            info["screen_width"], info["screen_height"] = [int(e) for e in wh]
        # ip addr
        s = self.adb_command("adb shell ifconfig wlan0")
        ips = re.findall(".*addr:(\d{1,3}.\d{1,3}.\d{1,3}.\d{1,3}).*", s)
        if ips:
            info['ip'] = ips[0]
        return info

    def screen_on(self, wait=0.5):
        # 点亮屏幕
        return self.adb_command("adb shell input keyevent 224", wait)

    def screen_off(self):
        # 熄灭屏幕
        return self.adb_command("adb shell input keyevent 223")

    def tap(self, x, y, wait=0.5):
        # 点击屏幕
        return self.adb_command(
            'adb shell input tap %s %s' % (x, y), wait=wait)

    def swipe(self, x0, y0, x1, y1, duration=300, wait=0.5):
        # 滑动屏幕
        return self.adb_command(
            'adb shell input swipe %s %s %s %s %s' % (x0, y0, x1, y1, round(duration)), wait)

    def swipe_up(self, wait=0.5):
        return self.swipe(self.width / 2, int(self.height * 0.8), self.width // 2, int(self.height * 0.2), duration=500, wait=wait)

    def input(self, text, wait=0.5):
        # 在输入框中输入，要先聚焦到输入框
        return self.adb_command("adb shell input text %s" % text, wait)

    def start_app(self, name="wechat", wait=0.5):
        if name == "wechat":
            self.adb_command(
                "adb shell am start -n com.tencent.mm/.ui.LauncherUI", wait)
        else:
            raise ValueError("Unknow app %s" % name)

    def call_number(self, phone_no="10010", **kwargs):
        # number是个列表，直接在这里天上你想要骚扰的号码即可
        # 直接一个for循环，循环号码
        times = kwargs.get("times", 1)
        for i in range(times):
            if isinstance(phone_no, list):
                phone = phone_no[i % len(phone_no)]
            elif isinstance(phone_no, str):
                phone = phone_no
            else:
                break
            print("%s/%s call to number %s" % (i+1, times, phone))
            # 使用adb打电话
            self.adb_command(
                'adb shell am start -a android.intent.action.CALL -d tel:%s' % phone)
            if kwargs.get("hands_free", False):
                self.adb_command(
                    'adb shell input tap %s %s ' % (858, 1737))
            self.press_key("HOME")
            # 这里的sleep时间基本就是你想让通话保持的时间了
            time.sleep(10)
            # 挂断电话
            end = self.adb_command('adb shell input keyevent 6')  # code6是挂断
            time.sleep(3)


if __name__ == '__main__':
    phone_no = ["1862"]
    D = Device(wireless=True)
    D.screen_on()
    D.call_number(phone_no, times=200, hands_free=True)
    # D.swipe_up(wait=1)
    # D.input("123456789", wait=2)  # 开屏密码
    # # D.call_number(phone_no, times=52, hands_free=True)
    # D.start_app("wechat", wait=2)
    # D.tap(822, 1870, wait=1)  # 应用锁页面，使用密码 按钮位置
    # D.input("1991")  # 应用程序密码
    # D.tap(822, 164, wait=1)
    # D.tap(989, 1254, wait=1)  # hide input method
    # D.input("gezi531337", wait=2)
    # D.press_key("ENTER")
    # D.tap(419, 439, wait=2) # go to chat
    # D.tap(392, 1852, wait=2) # tap input box
    # D.tap(989, 1254, wait=1)  # hide input method
    # D.input("hell", wait=1)
    # D.tap(1016, 1848, wait=1) # send
    embed()
