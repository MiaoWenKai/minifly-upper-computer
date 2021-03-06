from pywifi import const, PyWiFi, Profile
import time


# wifi类
class wifi(object):
    def __init__(self):
        self.wifi = PyWiFi()  # 创建一个无线对象
        self.interfaces = self.wifi.interfaces()  # 获取无线网卡接口
        self.iface = self.interfaces[0]  # 获取第一个无线网卡接口
        self.minifly_find = 0

    # 扫描周围wifi
    def scan_wifi(self):
        self.iface.scan()  # 扫描周围wifi
        time.sleep(1)  # 不缓冲显示不出来
        result = self.iface.scan_results()  # 获取扫描结果，wifi可能会有重复
        has = []  # 初始化已扫描到的wifi
        wifi_list = []  # 初始化扫描结果
        for i in result:
            if i not in has:  # 若has中没有该wifi，则
                has.append(i)  # 添加到has列表
                if i.signal > -90:  # 信号强度<-90的wifi几乎连不上
                    wifi_list.append((i.ssid, i.signal))  # 添加到wifi列表
                    # print('wifi信号强度：{0}，名称：{1}。'.format(i.signal, i.ssid))  # 输出wifi名称
                if i.ssid == "MiniFly":
                    self.minifly_find = 1
                    print('wifi信号强度：{0}，名称：{1}。'.format(i.signal, i.ssid))  # 输出wifi名称
        return sorted(wifi_list, key=lambda x: x[1], reverse=True)  # 按信号强度由高到低排序

    # 连接wifi
    def connect_wifi(self, wifi_name):
        # self.iface.disconnect()  # 断开无线网卡连接
        # time.sleep(1)  # 缓冲1秒
        profile_info = Profile()  # wifi配置文件
        profile_info.ssid = wifi_name  # wifi名称
        profile_info.auth = const.AUTH_ALG_OPEN  # 需要密码
        self.iface.connect(profile_info)  # 连接
        # 检查是否连接成功
        sec = 0  # 秒数计时变量
        while self.iface.status() != const.IFACE_CONNECTED:
            print(f"正在建立连接……连接用时：{sec}s")
            sec += 0.1
            time.sleep(0.1)
        print('=' * 50)
        print('视频链路连接成功！')
        print('=' * 50)
        return True

    # 断开无线网卡已连接状态
    def disconnect_wifi(self):
        self.iface.disconnect()
        if self.iface.status() in [const.IFACE_DISCONNECTED, const.IFACE_INACTIVE]:
            print('无线网卡：%s 已断开。' % self.iface.name())
        else:
            print('无线网卡：%s 未断开。' % self.iface.name())


# 连接摄像头wifi
def camera_connect(wifi_name):
    counter = 0
    while wifi_name.minifly_find == 0:
        print(f"正在扫描wifi...扫描用时{counter}s")
        counter += 1
        wifi_name.scan_wifi()  # 扫描周围wifi
    print("已搜索到MiniFly")
    wifi_name.connect_wifi("MiniFly")
    # time.sleep(3)  # 等待3秒后，才能接收到图像


# 检查wifi连接情况
def check_connection(wifi_name):
    if wifi_name.iface.status() in [const.IFACE_DISCONNECTED, const.IFACE_INACTIVE]:
        print("连接中断！尝试重连中......")
        wifi_name.connect_wifi("MiniFly")


if __name__ == '__main__':
    WIFI = wifi()  # 实例化wifi类
    camera_connect(WIFI)
    while True:
        check_connection(WIFI)
        time.sleep(0.1)
