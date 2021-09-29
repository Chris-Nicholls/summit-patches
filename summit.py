import mido 
import random
import collections
import parameters
import pprint
from byte_mapping import byte_mapping

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

messages = mido.read_syx_file('all.syx')


def get_patch_name(patch_bytes):
    n = patch_bytes[15: 31]
    cs = [chr(x) for x in n]
    return ''.join(cs)

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
    byte_mapping = {}
    with mido.open_output() as outport:
        outport.callback = print_message
        with mido.open_input() as inport:
            msg = fetch_current(inport, outport)
            last = msg

            for key in list(parameters.all_messages.keys()):
                print("Checking " + key)
                m = parameters.all_messages[key]
                found = False
                for i in range(m.val_min, m.val_max + 1)[:3]:
                    m.send(outport,  i)
                    msg = fetch_current(inport, outport)
                    for b in range(len(msg.data)):
                        if msg.data[b] != last.data[b]:
                            if bytes[b] != "" and bytes[b] != key:
                                print("Conflict at byte " + str(b) + " between " + bytes[b] + " and " + key )   
                            bytes[b] = key
                            byte_mapping[key] = b
                            found = True
                if not found:
                    print("Could not find byte for parameter " + key)
                m.send(outport,  m.default)
                last = fetch_current(inport, outport)

    display_bytes(messages, bytes)    
    pprint.pprint(byte_mapping)


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


# print_changed_bytes()
# search_params()

def send_random_patch():
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


def mix_patches(patch_a_bytes, patch_b_bytes):
    out = [x for x in patch_a_bytes]
    for group in parameters.patch_groups:
        b = random.getrandbits(1)
        pick = patch_a_bytes if b else patch_b_bytes
        # print(group + " " + str(b))
        for param in parameters.patch_groups[group]:
            byte_index = byte_mapping[param]
            out[byte_index]=pick[byte_index]
    return out


def send_mixed_patch(messages):
    messages = [m.data for m in messages]
    a = messages[random.randrange(len(messages))]
    # a = messages[0]
    b = a
    while b == a:
        b = messages[random.randrange(len(messages))]

    print(get_patch_name(a) + " " + get_patch_name(b))

    d = mix_patches(a,b)

    d = mido.Message('sysex', data=d)

    with mido.open_output() as outport:
        outport.send(d)

def fetch_all_patches():
    ms = []
    with mido.open_output() as outport:
        with mido.open_input() as inport:
            for bank in [1,2,3,4]:
                for patch in range(128):
                    outport.send(mido.Message('control_change', channel=0, control=32, value=bank))
                    outport.send(mido.Message('program_change', channel=0, program=patch))
                    msg = fetch_current(inport, outport)
                    if not get_patch_name(msg.data).startswith("Init Patch"):
                        print(get_patch_name(msg.data))
                        ms.append(msg)

    mido.write_syx_file("all.syx", ms)


# fetch_all_patches()
# print(len(messages))
# for m in messages:
#     print(get_patch_name(m.data))
def wait_for_animate(inport):
    for msg in inport:
        if msg.type == 'control_change' and msg.control in [114,115] and msg.value == 127:
            return


# listen()
with mido.open_input() as inport:
    while True:
        send_mixed_patch(messages)
        wait_for_animate(inport)
