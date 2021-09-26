import mido 
import random
import collections
import base64
import parameters

def read_patches(name, count):
    ms = [] 
    with mido.open_input() as inport:
        for msg in inport:
            print(msg.type)
            if (msg.type == 'sysex'):
                ms.append(msg)
                print(msg)
            if (len(ms) >= count):
                 break

    mido.write_syx_file(name, ms)

# read_patches("increment.syx", 30)

messages = mido.read_syx_file('patch.syx')


def print_message(message):
    print(message)

def display_patches(messages):
    messages = [m.data for m in messages]

    l = len(messages[0])
    for i in range(1,l):
        d = [m[i] for m in messages]
        c = collections.Counter(d)
        top = c.most_common(1)[0][0]
        order = [cm[0] for cm in c.most_common()]

        for m in messages:
            print('0123456789ABCDEF'[m[i]//16], end='')
            print('0123456789ABCDEF'[m[i]%16], end=' ')
        print('   ', end = '')

        uniques = len(c)
        pairs = len(set([(m[i], m[i-1]) for m in messages]))
        prev = len(set( [m[i-1] for m in messages]))
        print(pairs-uniques,',',pairs-prev, end = '    ')

        for m in messages:
            if (m[i] == top):
              print(' ',end='')
            elif len(order) > 9:
              print('#', end='')
            else:
              print(order.index(m[i]), end='')
        print()

def display_bytes(messages, bytes):
    messages = [m.data for m in messages]

    l = len(messages[0])
    for i in range(1,l):
        d = [m[i] for m in messages]
        c = collections.Counter(d)
        top = c.most_common(1)[0][0]
        order = [cm[0] for cm in c.most_common()]

        for m in messages:
            print('0123456789ABCDEF'[m[i]//16], end='')
            print('0123456789ABCDEF'[m[i]%16], end=' ')
        print(i, end = ' ')
        print('   ', end = '')   
        print(bytes[i])

def init_patch():
    with mido.open_output() as outport:
    #     outport.send(d)
        for m in parameters.all_messages.values():
            m.send(outport, m.default)


def fetch_current(inport, outport):
    outport.send(mido.Message.from_bytes([0xF0, 0, 0x20, 0x29, 0x01, 0x11, 0x01, 0x33, 0x40, 0, 0, 0, 0, 0, 0xF7]))
    m = inport.receive()
    while m.type != 'sysex':
        m = inport.receive()
    return m


def listen():
    with mido.open_input() as inport:
        for msg in inport:
            print(msg)

def search_params():
    init_patch()
    sysex = []
    bytes = [""] * 600
    with mido.open_output() as outport:
        outport.callback = print_message
        with mido.open_input() as inport:
            msg = fetch_current(inport, outport)
            last = msg

            for key in list(parameters.all_messages.keys()):
                print("Checking " + key)
                m = parameters.all_messages[key]
                for i in range(m.val_min, m.val_max)[:3]:
                    m.send(outport,  i)
                    msg = fetch_current(inport, outport)
                    for b in range(len(msg.data)):
                        if msg.data[b] != last.data[b]:
                            if bytes[b] != "" and bytes[b] != key:
                                print("Conflict at byte " + str(b) + " between " + bytes[b] + " and " + key )   
                            bytes[b] = key
                m.send(outport,  m.default)
                last = fetch_current(inport, outport)

    display_bytes(messages, bytes)           

listen()
search_params()

def print_changed_bytes():
    last = []
    with mido.open_input() as inport:
        for msg in inport:
                if msg.type == 'sysex':
                    if last == None:
                        last = msg.data
                    for i in range(len(last)):
                        if last[i] != msg.data[i]:
                            print(i)
                    last = msg.data
                else: print(msg)

# inport  = mido.open_input()
# outport = mido.open_output()
# o1c = parameters.parameters["Oscillator 1 Coarse"]



a = messages[random.randrange(len(messages))].data
b = a
while b == a:
    b = messages[random.randrange(len(messages))].data

d = list(a)
for i in range(len(d)):
    if bool(random.getrandbits(1)):
        d[i] = b[i]



d = mido.Message('sysex', data=d)

with mido.open_output() as outport:
    outport.send(d)