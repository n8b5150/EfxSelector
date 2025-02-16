from machine import Pin
import uasyncio as asyncio
from primitives import Pushbutton, Switch
import time, os, json
#from . import m_excl, m_pre, m_toggle, io_def

#onboard led on/off
led = Pin(25, Pin.OUT)
led.value(0)

#define led/relay control
l_ready = Pin(22, Pin.OUT) #29
l_bypass = Pin(1, Pin.OUT) #2
l_tuner = Pin(2, Pin.OUT) #4
l_loop1 = Pin(3, Pin.OUT) #5
l_loop2 = Pin(4, Pin.OUT) #6
l_loop3 = Pin(5, Pin.OUT) #7
l_loop4 = Pin(6, Pin.OUT) #9

#led/relay initial states
l_ready.value(0)
l_bypass.value(0)
l_tuner.value(0)
l_loop1.value(0)
l_loop2.value(0)
l_loop3.value(0)
l_loop4.value(0)

#define footswitches
b_bypass = Pushbutton(Pin(7, Pin.IN, Pin.PULL_UP), suppress=True) #10
b_tuner = Pushbutton(Pin(8, Pin.IN, Pin.PULL_UP), suppress=True) #11
b_loop1 = Pushbutton(Pin(9, Pin.IN, Pin.PULL_UP), suppress=True) #12
b_loop2 = Pushbutton(Pin(10, Pin.IN, Pin.PULL_UP), suppress=True) #14
b_loop3 = Pushbutton(Pin(11, Pin.IN, Pin.PULL_UP), suppress=True) #15
b_loop4 = Pushbutton(Pin(12, Pin.IN, Pin.PULL_UP), suppress=True) #16

#define toggle/exclusive/preset
l_toggle = Pin(16, Pin.OUT) #21
l_excl = Pin(17, Pin.OUT) #22
l_pre = Pin(18, Pin.OUT) #24
sw_toggle = Switch(Pin(13, Pin.IN, Pin.PULL_UP)) #17
sw_excl = Switch(Pin(14, Pin.IN, Pin.PULL_UP)) #19
sw_pre = Switch(Pin(15, Pin.IN, Pin.PULL_UP)) #20

#used to activate transistor to close mode switch ground
init_delay = Pin(0, Pin.OUT) #1
init_delay.value(0)
print(init_delay.value())

#define led blink function
def blink():
    l_toggle.value(0)
    led.value(0)
    time.sleep(0.125)
    l_toggle.value(1)
    led.value(1)
    time.sleep(0.125)
    l_toggle.value(0)
    led.value(0)
    time.sleep(0.125)
    l_toggle.value(1)
    led.value(1)
    
    
#define function to read/create preset file
def get_preset(file):
    try:
        with open(file) as fd:
            return json.load(fd)

    except OSError:
        with open(file, "w") as fd:
            pre = {
                "l_loop1": 0,
                "l_loop2": 0,
                "l_loop3": 0,
                "l_loop4": 0
            }
            json.dump(pre, fd)
            return pre

#define preset class
class Preset:
    def __init__(self, p):
        self.pre = p

preset1 = get_preset("preset1.json")
preset2 = get_preset("preset2.json")
preset3 = get_preset("preset3.json")
preset4 = get_preset("preset4.json")
last_state = get_preset("last_state.json")
print("preset 1: ", preset1)
print("preset 2: ", preset2)
print("preset 3: ", preset3)
print("preset 4: ", preset4)
print("last state = ", last_state)

#define save preset function
async def save_pre(file):
    if Pin(13).value() == 0:
        global preset1, preset2, preset3, preset4
        #get loop status and save to preset object
        pre = {
        "l_loop1": l_loop1.value(),
        "l_loop2": l_loop2.value(),
        "l_loop3": l_loop3.value(),
        "l_loop4": l_loop4.value()
        }
        #send file name and preset object to write_preset
        with open(file, "w") as fd:
            json.dump(pre, fd)
            print("preset saved to: ", file)
        blink()
        preset1 = get_preset("preset1.json")
        preset2 = get_preset("preset2.json")
        preset3 = get_preset("preset3.json")
        preset4 = get_preset("preset4.json")
        await asyncio.sleep(1)

#define save state function
async def save_state(file):
    #get loop status and save to preset object
    st = {
    "l_loop1": l_loop1.value(),
    "l_loop2": l_loop2.value(),
    "l_loop3": l_loop3.value(),
    "l_loop4": l_loop4.value()
    }
    #send file name and preset object to write_preset
    with open(file, "w") as fd:
        json.dump(st, fd)
        print("state saved to: ", file)
    await asyncio.sleep(0.1)

#def set toggle function
def set_toggle(relay):
    print (relay, relay.value())
    relay.toggle()
    #test save last state
    await save_state("last_state.json")
    print (relay, relay.value())
    
#def set excl function
def set_excl(a, b, c, d):
    l_loop1.value(a)
    l_loop2.value(b)
    l_loop3.value(c)
    l_loop4.value(d)
    #test save last state
    await save_state("last_state.json")
    print(a, b, c, d, l_loop1.value(), l_loop2.value(), l_loop3.value(), l_loop4.value())

#def set pre function
def set_pre(pre_num):
    l_loop1.value(pre_num['l_loop1'])
    l_loop2.value(pre_num['l_loop2'])
    l_loop3.value(pre_num['l_loop3'])
    l_loop4.value(pre_num['l_loop4'])
    #test save last state
    await save_state("last_state.json")
    print(pre_num['l_loop1'], pre_num['l_loop2'], pre_num['l_loop3'], pre_num['l_loop4'])
    print(l_loop1.value(), l_loop2.value(), l_loop3.value(), l_loop4.value())

#def set last function
def set_last(pre_num):
    l_loop1.value(pre_num['l_loop1'])
    l_loop2.value(pre_num['l_loop2'])
    l_loop3.value(pre_num['l_loop3'])
    l_loop4.value(pre_num['l_loop4'])
    print("last", pre_num['l_loop1'], pre_num['l_loop2'], pre_num['l_loop3'], pre_num['l_loop4'])
    print("last", l_loop1.value(), l_loop2.value(), l_loop3.value(), l_loop4.value())

#define toggle mode function
async def m_toggle():
    print(l_toggle.value(), l_excl.value(), l_pre.value())
    print ("entering toggle")
    l_toggle.value(1)
    l_excl.value(0)
    l_pre.value(0)
    print(l_toggle.value(), l_excl.value(), l_pre.value())
    b_loop1.release_func(set_toggle, (l_loop1,))
    b_loop2.release_func(set_toggle, (l_loop2,))
    b_loop3.release_func(set_toggle, (l_loop3,))
    b_loop4.release_func(set_toggle, (l_loop4,))
    
    #b_bypass.long_func(-func-, (l_bypass,))
    #b_tuner.long_func(-func-, (l_tuner,))
    b_loop1.long_func(save_pre, ("preset1.json",))
    b_loop2.long_func(save_pre, ("preset2.json",))
    b_loop3.long_func(save_pre, ("preset3.json",))
    b_loop4.long_func(save_pre, ("preset4.json",))
    #await sw_toggle.open_func(print, ("leaving toggle",))
        
#define excl mode function
async def m_excl():
    print(l_toggle.value(), l_excl.value(), l_pre.value())
    print("entering excl")
    l_toggle.value(0)
    l_excl.value(1)
    l_pre.value(0)
    print(l_toggle.value(), l_excl.value(), l_pre.value())
    b_loop1.release_func(set_excl, (1, 0, 0, 0,))
    b_loop2.release_func(set_excl, (0, 1, 0, 0,))
    b_loop3.release_func(set_excl, (0, 0, 1, 0,))
    b_loop4.release_func(set_excl, (0, 0, 0, 1,))
    #await sw_excl.open_func(print, ("leaving excl",))

#define pre mode function
async def m_pre():
    print(l_toggle.value(), l_excl.value(), l_pre.value())
    print("entering pre")
    l_toggle.value(0)
    l_excl.value(0)
    l_pre.value(1)
    print(l_toggle.value(), l_excl.value(), l_pre.value())
    b_loop1.release_func(set_pre, (preset1,))
    b_loop2.release_func(set_pre, (preset2,))
    b_loop3.release_func(set_pre, (preset3,))
    b_loop4.release_func(set_pre, (preset4,))
    #await sw_pre.open_func(print, ("leaving pre",))


#define app function
async def app():
#     await set_init_mode()
    b_bypass.release_func(set_toggle, (l_bypass,))
    b_tuner.release_func(set_toggle, (l_tuner,))
    sw_toggle.close_func(m_toggle, ())
    sw_excl.close_func(m_excl, ())
    sw_pre.close_func(m_pre, ())
    await asyncio.sleep(0.5)
    init_delay.value(1) #switches on a transistor to ground sw_ rotary switch
    l_ready.value(1)
    led.value(1)
    set_last(last_state)
    while True:
        await asyncio.sleep(60)



asyncio.run(app())