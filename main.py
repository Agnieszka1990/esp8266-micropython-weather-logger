# import webrepl_setup

# Micropython | Board
# 0|D3
# 2|D4 (also Led1 but inverse)
# 4|D2
# 5|D1
# 9|SD2
# 10|SD3
# 12|D6
# 13|D7
# 14|D5
# 15|D8
# 16|D0 (also Led2 but inverse)

import gc

gc.collect()
gc.mem_free()

# NETWORK STATUS {

import network
import utime

sta_if = network.WLAN(network.STA_IF)
sta_if.active(True)
networks = sta_if.scan()
networks.sort(key=lambda x: -x[3])
# sta_if.connect("<AP_name>", "<password>") # Connect to an AP
ap_if = network.WLAN(network.AP_IF)
# ap_if.active(False)


print("Available networks")
for i in networks:
    print(i)

utime.sleep(2)
print("Connected to WiFI = {}".format(sta_if.isconnected()))  # Check for successful connection
print("sta_if.ifconfig() = {}".format(sta_if.ifconfig()))
print("ap_if.ifconfig() = {}".format(ap_if.ifconfig()))

# } # NETWORK STATUS


# MEASUREMENTS {

import dht
import machine
import ntptime

ntptime.settime()
timeoffset = 2  # TODO: determine time zone automatically.

d = dht.DHT11(machine.Pin(5))  # D1
p = machine.Pin(4, machine.Pin.OUT)
brzeczyk = machine.PWM(machine.Pin(0))
rtc = machine.RTC()

log = list()


def pomiar():
    brzeczyk.freq(500)
    brzeczyk.duty(512)
    p.on()
    d.measure()
    tt = rtc.datetime()
    tstring = "{}.{:02d}.{:02d} {:02d}:{:02d}:{:02d}".format(tt[0], tt[1], tt[2], tt[4] + timeoffset, tt[5], tt[6])
    lt = {'czas': tstring, 'temperatura': d.temperature(), 'wilgotnosc': d.humidity()}
    log.append(lt)
    print(lt)
    # utime.sleep_ms(250)
    p.off()
    brzeczyk.deinit()
    gc.collect()
    print("gc.mem_free() = {}".format(gc.mem_free()))


t = machine.Timer(-1)
t.init(period=int(30 * 1000), mode=machine.Timer.PERIODIC, callback=lambda f: pomiar())

# } # MEASUREMENTS
