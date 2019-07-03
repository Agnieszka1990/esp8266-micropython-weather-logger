# import webrepl_setup   # 1madc777

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


# MEASUREMENTS {

import dht
import machine
import utime

d = dht.DHT11(machine.Pin(5))  # D1
p = machine.Pin(4, machine.Pin.OUT)
brzeczyk = machine.PWM(machine.Pin(0))

log = list()


def pomiar():
    brzeczyk.freq(500)
    brzeczyk.duty(512)
    p.on()
    d.measure()
    lt = {'temperatura': d.temperature(), 'wilgotnosc': d.humidity()}
    log.append(lt)
    print(lt)
    # utime.sleep_ms(250)
    p.off()
    brzeczyk.deinit()


t = machine.Timer(-1)
t.init(period=int(30 * 1000), mode=machine.Timer.PERIODIC, callback=lambda f: pomiar())

# } # MEASUREMENTS
