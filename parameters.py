import mido
import time

class NRPN:
    def __init__(self, cc1, cc2, val_min, val_max, default_val):
        self.cc1 = cc1
        self.cc2 = cc2
        self.val_min = val_min
        self.val_max = val_max
        self.default = default_val


    def send(self, port, value):
        port.send(mido.Message.from_bytes([0xb0, 99, self.cc1]))
        port.send(mido.Message.from_bytes([0xb0, 98, self.cc2]))
        port.send(mido.Message.from_bytes([0xb0, 6, value]))


class CC:
    def __init__(self, cc1, val_min, val_max, default_val):
        self.cc1 = cc1
        self.val_min = val_min
        self.val_max = val_max
        self.default = default_val

    def send(self, port, value):
        port.send(mido.Message.from_bytes([0xb0, self.cc1, value]))

class CC_Pair:
        def __init__(self, cc1, cc2, val_min, val_max, default_val):
            self.cc1 = cc1
            self.cc2 = cc2
            self.val_min = val_min
            self.val_max = val_max
            self.default = default_val

        def send(self, port, value):
            m1 = mido.Message.from_bytes([0xb0, self.cc1, value // 2 ])
            m2 = mido.Message.from_bytes([0xb0, self.cc2, (value % 2) * 127])
            port.send(m1)
            port.send(m2)


parameters = {
    "Patch Category": NRPN(cc1=0, cc2=0, val_min=0, val_max=14, default_val=0),
    "Patch Genre": NRPN(cc1=0, cc2=1, val_min=0, val_max=9, default_val=0),
    "Voice Mode": NRPN(cc1=0, cc2=2, val_min=0, val_max=4, default_val=3),
    "Voice Unison": NRPN(cc1=0, cc2=3, val_min=0, val_max=4, default_val=0),
    "Voice Unison Detune": NRPN(cc1=0, cc2=4, val_min=0, val_max=127, default_val=25),
    "Voice Unison Spread": NRPN(cc1=0, cc2=5, val_min=0, val_max=127, default_val=0),
    "Voice Keyboard Octave": NRPN(cc1=0, cc2=6, val_min=61, val_max=67, default_val=64),
    "Glide Time": CC(cc1=5, val_min=0, val_max=127, default_val=0),
    "Voice Pre-Glide": NRPN(cc1=0, cc2=7, val_min=52, val_max=76, default_val=64),
    "Glide On": CC(cc1=35, val_min=0, val_max=1, default_val=0),
    "Osc Common Diverge": NRPN(cc1=0, cc2=9, val_min=0, val_max=127, default_val=0),
    "Osc Common Drift": NRPN(cc1=0, cc2=10, val_min=0, val_max=127, default_val=0),
    "Osc Common Noise LPF": NRPN(cc1=0, cc2=11, val_min=0, val_max=127, default_val=127),
    "Osc Common Noise HPF": NRPN(cc1=0, cc2=12, val_min=0, val_max=127, default_val=127),
    "Osc Common Key Sync": NRPN(cc1=0, cc2=13, val_min=0, val_max=1, default_val=0),
    "Oscillator 1 Range": CC(cc1=3, val_min=63, val_max=66, default_val=64),
    "Oscillator 1 Coarse": CC_Pair(cc1=14, cc2=46, val_min=1, val_max=255, default_val=128),
    "Oscillator 1 Fine": CC_Pair(cc1=15, cc2=47, val_min=28, val_max=228, default_val=128), # Note: this doesn't get picked up correctly, but should map to byte 64,65
    "Oscillator 1 ModEnv2 > Pitch": CC(cc1=9, val_min=1, val_max=127, default_val=64),
    "Oscillator 1 LFO2 > Pitch": CC_Pair(cc1=16, cc2=48, val_min=1, val_max=255, default_val=128),
    "Oscillator 1 Wave": NRPN(cc1=0, cc2=14, val_min=0, val_max=4, default_val=2),
    "Oscillator 1 Wave More": NRPN(cc1=0, cc2=15, val_min=4, val_max=63, default_val=0),
    "Oscillator 1 Shape Source": NRPN(cc1=0, cc2=16, val_min=0, val_max=2, default_val=0),
    "Oscillator 1 Manual Shape": CC(cc1=12, val_min=0, val_max=127, default_val=64),
    "Oscillator 1 ModEnv1 > Shape": CC(cc1=119, val_min=0, val_max=127, default_val=64),
    "Oscillator 1 LFO1 > Shape": CC(cc1=33, val_min=1, val_max=127, default_val=64),
    "Oscillator 1 Vsync": CC(cc1=34, val_min=0, val_max=127, default_val=0),
    "Oscillator 1 Saw Density": NRPN(cc1=0, cc2=17, val_min=0, val_max=127, default_val=0),
    "Oscillator 1 Saw Density Detune": NRPN(cc1=0, cc2=18, val_min=0, val_max=127, default_val=0),
    "Oscillator 1 Fixed Note": NRPN(cc1=0, cc2=19, val_min=0, val_max=88, default_val=0),
    "Oscillator 1 Bend Range": NRPN(cc1=0, cc2=20, val_min=40, val_max=88, default_val=76),
    "Oscillator 2 Range": CC(cc1=37, val_min=63, val_max=66, default_val=64),
    "Oscillator 2 Coarse": CC_Pair(cc1=17, cc2=49, val_min=0, val_max=255, default_val=128),
    "Oscillator 2 Fine": CC_Pair(cc1=18, cc2=50, val_min=28, val_max=228, default_val=128), # Note: this doesn't get picked up correctly, but should map to byte 85,86
    "Oscillator 2 ModEnv2 > Pitch": CC(cc1=38, val_min=1, val_max=127, default_val=64),
    "Oscillator 2 LFO2 > Pitch": CC_Pair(cc1=19, cc2=51, val_min=1, val_max=255, default_val=64),
    "Oscillator 2 Wave": NRPN(cc1=0, cc2=23, val_min=0, val_max=4, default_val=2),
    "Oscillator 2 Wave More": NRPN(cc1=0, cc2=24, val_min=4, val_max=63, default_val=0),
    "Oscillator 2 Shape Source": NRPN(cc1=0, cc2=25, val_min=0, val_max=2, default_val=0),
    "Oscillator 2 Manual Shape": CC(cc1=39, val_min=0, val_max=127, default_val=64),
    "Oscillator 2 ModEnv1 > Shape": CC(cc1=40, val_min=0, val_max=127, default_val=64),
    "Oscillator 2 LFO1 > Shape": CC(cc1=41, val_min=1, val_max=127, default_val=64),
    "Oscillator 2 Vsync": CC(cc1=42, val_min=0, val_max=127, default_val=0),
    "Oscillator 2 Saw Density": NRPN(cc1=0, cc2=26, val_min=0, val_max=127, default_val=0),
    "Oscillator 2 Saw Density Detune": NRPN(cc1=0, cc2=27, val_min=0, val_max=127, default_val=0),
    "Oscillator 2 Fixed Note": NRPN(cc1=0, cc2=28, val_min=0, val_max=88, default_val=0),
    "Oscillator 2 Bend Range": NRPN(cc1=0, cc2=29, val_min=40, val_max=88, default_val=76),
    "Oscillator 3 Range": CC(cc1=65, val_min=63, val_max=66, default_val=64),
    "Oscillator 3 Coarse": CC_Pair(cc1=20, cc2=52, val_min=0, val_max=255, default_val=128),
    "Oscillator 3 Fine": CC_Pair(cc1=21, cc2=53, val_min=28, val_max=228, default_val=128), # Note: this doesn't get picked up correctly, but should map to byte 106,107
    "Oscillator 3 ModEnv2 > Pitch": CC(cc1=43, val_min=1, val_max=127, default_val=64),
    "Oscillator 3 LFO2 > Pitch": CC_Pair(cc1=22, cc2=54, val_min=1, val_max=255, default_val=128),
    "Oscillator 3 Wave": NRPN(cc1=0, cc2=32, val_min=0, val_max=4, default_val=0),
    "Oscillator 3 Wave More": NRPN(cc1=0, cc2=33, val_min=4, val_max=63, default_val=2),
    "Oscillator 3 Shape Source": NRPN(cc1=0, cc2=34, val_min=0, val_max=2, default_val=0),
    "Oscillator 3 Manual Shape": CC(cc1=71, val_min=0, val_max=127, default_val=64),
    "Oscillator 3 ModEnv1 > Shape": CC(cc1=72, val_min=0, val_max=127, default_val=64),
    "Oscillator 3 LFO1 > Shape": CC(cc1=73, val_min=1, val_max=127, default_val=64),
    "Oscillator 3 Vsync": CC(cc1=44, val_min=0, val_max=127, default_val=0),
    "Oscillator 3 Saw Density": NRPN(cc1=0, cc2=35, val_min=0, val_max=127, default_val=0),
    "Oscillator 3 Saw Density Detune": NRPN(cc1=0, cc2=36, val_min=0, val_max=127, default_val=0),
    "Oscillator 3 Fixed Note": NRPN(cc1=0, cc2=37, val_min=0, val_max=88, default_val=0),
    "Oscillator 3 Bend Range": NRPN(cc1=0, cc2=38, val_min=40, val_max=88, default_val=76),
    "Mixer Osc1": CC_Pair(cc1=23, cc2=55, val_min=0, val_max=255, default_val=255),
    "Mixer Osc2": CC_Pair(cc1=24, cc2=56, val_min=0, val_max=255, default_val=0),
    "Mixer Osc3": CC_Pair(cc1=25, cc2=57, val_min=0, val_max=255, default_val=0),
    "Ring 1*2 Level": CC_Pair(cc1=26, cc2=58, val_min=0, val_max=255, default_val=0),
    "Noise Level": CC_Pair(cc1=27, cc2=59, val_min=0, val_max=255, default_val=0),
    "Mixer Patch Level": NRPN(cc1=0, cc2=41, val_min=0, val_max=127, default_val=64),
    "Mixer VCA gain": NRPN(cc1=0, cc2=42, val_min=0, val_max=127, default_val=127),
    "Mixer Dry Level": NRPN(cc1=0, cc2=43, val_min=0, val_max=127, default_val=127),
    "Mixer Wet Level": NRPN(cc1=0, cc2=44, val_min=0, val_max=127, default_val=127),
    "Filter Overdrive": CC(cc1=80, val_min=0, val_max=127, default_val=0),
    "Filter Post Drive": CC(cc1=36, val_min=0, val_max=127, default_val=0),
    "Filter Slope": NRPN(cc1=0, cc2=45, val_min=0, val_max=1, default_val=1),
    "Filter Shape": NRPN(cc1=0, cc2=46, val_min=0, val_max=2, default_val=0),
    "Filter Dual Shape": NRPN(cc1=25, cc2=9, val_min=0, val_max=8, default_val=0),
    "Filter Freq Seperation": NRPN(cc1=25, cc2=10, val_min=0, val_max=127, default_val=64),
    "Filter Key Tracking": CC(cc1=75, val_min=0, val_max=127, default_val=127),
    "Filter Resonance": CC(cc1=79, val_min=0, val_max=127, default_val=0),
    "Filter Frequency": CC_Pair(cc1=29, cc2=61, val_min=0, val_max=255, default_val=255),
    "LFO1 > Filter": CC_Pair(cc1=28, cc2=60, val_min=1, val_max=255, default_val=128),
    "Osc3 > Filter": CC(cc1=76, val_min=0, val_max=127, default_val=0),
    "Filter Env Select": NRPN(cc1=0, cc2=47, val_min=0, val_max=1, default_val=0),
    "AmpEnv > Filter": CC(cc1=77, val_min=1, val_max=127, default_val=64),
    "ModEnv1 > Filter": CC(cc1=78, val_min=1, val_max=127, default_val=64),
    "Filter Divergence": NRPN(cc1=0, cc2=48, val_min=0, val_max=127, default_val=0),
    "Amp Envelope Attack": CC(cc1=86, val_min=0, val_max=127, default_val=0),
    "Amp Envelope Decay": CC(cc1=87, val_min=0, val_max=127, default_val=90),
    "Amp Envelope Sustain": CC(cc1=88, val_min=0, val_max=127, default_val=127),
    "Amp Envelope Release": CC(cc1=89, val_min=0, val_max=127, default_val=40),
    "Amp Envelope Velocity": NRPN(cc1=0, cc2=55, val_min=0, val_max=127, default_val=64),
    "Amp Envelope Trigger": NRPN(cc1=0, cc2=56, val_min=0, val_max=1, default_val=0),
    "Amp Envelope Delay": NRPN(cc1=25, cc2=30, val_min=0, val_max=127, default_val=0),
    "Amp Envelope HoldTime": NRPN(cc1=0, cc2=57, val_min=0, val_max=127, default_val=0),
    "Amp Envelope Repeats": NRPN(cc1=0, cc2=58, val_min=0, val_max=127, default_val=0),
    "Amp Envelope Loop": NRPN(cc1=25, cc2=27, val_min=0, val_max=1, default_val=0),
    "Mod Envelope Select": NRPN(cc1=0, cc2=59, val_min=0, val_max=1, default_val=0),
    "Mod Envelope 1 Attack": CC(cc1=90, val_min=0, val_max=127, default_val=0),
    "Mod Envelope 1 Decay": CC(cc1=91, val_min=0, val_max=127, default_val=75),
    "Mod Envelope 1 Sustain": CC(cc1=92, val_min=0, val_max=127, default_val=35),
    "Mod Envelope 1 Release": CC(cc1=93, val_min=0, val_max=127, default_val=45),
    "Mod Envelope 1 Velocity": NRPN(cc1=0, cc2=60, val_min=0, val_max=127, default_val=64),
    "Mod Envelope 1 Trigger": NRPN(cc1=0, cc2=61, val_min=0, val_max=1, default_val=0),
    "Mod Envelope 1 Delay": NRPN(cc1=25, cc2=31, val_min=0, val_max=127, default_val=0),
    "Mod Envelope 1 HoldTime": NRPN(cc1=0, cc2=62, val_min=0, val_max=127, default_val=0),
    "Mod Envelope 1 Repeats": NRPN(cc1=0, cc2=63, val_min=0, val_max=127, default_val=0),
    "Mod Envelope 1 Loop": NRPN(cc1=25, cc2=28, val_min=0, val_max=1, default_val=0),
    "Mod Envelope 2 Attack": CC(cc1=94, val_min=0, val_max=127, default_val=0),
    "Mod Envelope 2 Decay": CC(cc1=95, val_min=0, val_max=127, default_val=75),
    "Mod Envelope 2 Sustain": CC(cc1=117, val_min=0, val_max=127, default_val=35),
    "Mod Envelope 2 Release": CC(cc1=103, val_min=0, val_max=127, default_val=45),
    "Mod Envelope 2 Velocity": NRPN(cc1=0, cc2=64, val_min=0, val_max=127, default_val=64),
    "Mod Envelope 2 Trigger": NRPN(cc1=0, cc2=65, val_min=0, val_max=1, default_val=0),
    "Mod Envelope 2 Delay": NRPN(cc1=25, cc2=32, val_min=0, val_max=127, default_val=0),
    "Mod Envelope 2 HoldTime": NRPN(cc1=0, cc2=66, val_min=0, val_max=127, default_val=0),
    "Mod Envelope 2 Repeats": NRPN(cc1=0, cc2=67, val_min=0, val_max=127, default_val=0),
    "Mod Envelope 2 Loop": NRPN(cc1=25, cc2=29, val_min=0, val_max=1, default_val=0),
    "LFO 1 Range": NRPN(cc1=0, cc2=68, val_min=0, val_max=2, default_val=0),
    "LFO 1 Rate": CC_Pair(cc1=30, cc2=62, val_min=0, val_max=255, default_val=128),
    "LFO 1 Sync Rate": CC(cc1=81, val_min=0, val_max=34, default_val=16),
    "LFO 1 Wave": NRPN(cc1=0, cc2=69, val_min=0, val_max=3, default_val=0),
    "LFO 1 Phase": NRPN(cc1=0, cc2=70, val_min=0, val_max=120, default_val=0),
    "LFO 1 Slew": NRPN(cc1=0, cc2=71, val_min=0, val_max=127, default_val=0),
    "LFO 1 Fade Time": CC(cc1=82, val_min=0, val_max=127, default_val=0),
    "LFO 1 Fade In/Out": NRPN(cc1=0, cc2=72, val_min=0, val_max=3, default_val=0),
    "LFO 1 Fade Sync": NRPN(cc1=0, cc2=73, val_min=0, val_max=2, default_val=0),
    "LFO 1 Mono Trigger": NRPN(cc1=0, cc2=74, val_min=0, val_max=1, default_val=0),
    "LFO 1 One Shot": NRPN(cc1=0, cc2=75, val_min=0, val_max=1, default_val=0),
    "LFO 1 Common": NRPN(cc1=0, cc2=76, val_min=0, val_max=1, default_val=0),
    "LFO 2 Range": CC(cc1=83, val_min=0, val_max=2, default_val=0),
    "LFO 2 Rate": CC_Pair(cc1=31, cc2=63, val_min=0, val_max=255, default_val=128),
    "LFO 2 Sync Rate": CC(cc1=84, val_min=0, val_max=34, default_val=0),
    "LFO 2 Wave": NRPN(cc1=0, cc2=78, val_min=0, val_max=3, default_val=0),
    "LFO 2 Phase": NRPN(cc1=0, cc2=79, val_min=0, val_max=120, default_val=0),
    "LFO 2 Slew": NRPN(cc1=0, cc2=80, val_min=0, val_max=127, default_val=0),
    "LFO 2 Fade Time": CC(cc1=85, val_min=0, val_max=127, default_val=0),
    "LFO 2 Fade In/Out": NRPN(cc1=0, cc2=81, val_min=0, val_max=3, default_val=0),
    "LFO 1 Fade Sync": NRPN(cc1=0, cc2=82, val_min=0, val_max=1, default_val=0),
    "LFO 2 One Shot": NRPN(cc1=0, cc2=84, val_min=0, val_max=1, default_val=0),
    "LFO 2 Common": NRPN(cc1=0, cc2=85, val_min=0, val_max=1, default_val=0),
    "Distortion level": CC(cc1=104, val_min=0, val_max=127, default_val=0),
    "Effects Master Bypass": NRPN(cc1=0, cc2=88, val_min=0, val_max=1, default_val=0),
    "Effects Routing": NRPN(cc1=0, cc2=89, val_min=0, val_max=6, default_val=0),
    "Delay Level": CC(cc1=108, val_min=0, val_max=127, default_val=0),
    "Delay Time": CC(cc1=109, val_min=0, val_max=127, default_val=64),
    "Delay Width": NRPN(cc1=0, cc2=92, val_min=0, val_max=127, default_val=64),
    "Delay Sync": NRPN(cc1=0, cc2=93, val_min=0, val_max=1, default_val=0),
    "Delay Sync Time": NRPN(cc1=0, cc2=94, val_min=0, val_max=18, default_val=0),
    "Delay Feedback": CC(cc1=110, val_min=0, val_max=127, default_val=64),
    "Delay LP Damp": NRPN(cc1=0, cc2=95, val_min=0, val_max=127, default_val=85),
    "Delay HP Damp": NRPN(cc1=0, cc2=96, val_min=0, val_max=127, default_val=0),
    "Delay Slew Rate": NRPN(cc1=0, cc2=97, val_min=0, val_max=127, default_val=32),
    "Reverb Level": CC(cc1=112, val_min=0, val_max=127, default_val=0),
    "Reverb Type": NRPN(cc1=0, cc2=101, val_min=0, val_max=2, default_val=2),
    "Reverb Time": CC(cc1=113, val_min=0, val_max=127, default_val=90),
    "Reverb Damping LP": NRPN(cc1=0, cc2=102, val_min=0, val_max=127, default_val=50),
    "Reverb Damping HP": NRPN(cc1=0, cc2=103, val_min=0, val_max=127, default_val=1),
    "Reverb Size": NRPN(cc1=0, cc2=104, val_min=0, val_max=127, default_val=64),
    "Reverb Mod": NRPN(cc1=0, cc2=105, val_min=0, val_max=127, default_val=64),
    "Reverb Mod Rate": NRPN(cc1=0, cc2=106, val_min=0, val_max=127, default_val=4),
    "Reverb Low Pass": NRPN(cc1=0, cc2=107, val_min=0, val_max=127, default_val=74),
    "Reverb High Pass": NRPN(cc1=0, cc2=108, val_min=0, val_max=127, default_val=0),
    "Reverb Pre Delay": NRPN(cc1=0, cc2=109, val_min=0, val_max=127, default_val=40),
    "Chorus Level": CC(cc1=105, val_min=0, val_max=127, default_val=0),
    "Chorus Type": NRPN(cc1=0, cc2=111, val_min=0, val_max=2, default_val=2),
    "Chorus Rate": CC(cc1=118, val_min=0, val_max=127, default_val=20),
    "Chorus Mod Depth": NRPN(cc1=0, cc2=112, val_min=0, val_max=127, default_val=0),
    "Chorus Feedback": CC(cc1=107, val_min=0, val_max=127, default_val=64),
    "Chorus LP": NRPN(cc1=0, cc2=113, val_min=0, val_max=127, default_val=90),
    "Chorus HP": NRPN(cc1=0, cc2=114, val_min=0, val_max=127, default_val=2),
    "Arp/Clock Sync Rate": NRPN(cc1=0, cc2=116, val_min=0, val_max=18, default_val=16),
    "Arp/Clock Type": NRPN(cc1=0, cc2=117, val_min=0, val_max=6, default_val=0),
    "Arp/Clock Rhythm": NRPN(cc1=0, cc2=118, val_min=0, val_max=32, default_val=0),
    "Arp/Clock Octave": NRPN(cc1=0, cc2=119, val_min=0, val_max=5, default_val=1),
    "Arp/Clock Gate": CC(cc1=116, val_min=0, val_max=127, default_val=64),
    "Arp/Clock Swing": NRPN(cc1=0, cc2=120, val_min=20, val_max=80, default_val=50),
    "Arp/Clock On": NRPN(cc1=0, cc2=121, val_min=0, val_max=1, default_val=0),
    "Arp/Clock Key Latch": NRPN(cc1=0, cc2=122, val_min=0, val_max=1, default_val=0),
    "Arp/Clock Key Sync": NRPN(cc1=0, cc2=123, val_min=0, val_max=1, default_val=0) ,
    "Arp Velocity Mode": NRPN(cc1=0, cc2=124, val_min=0, val_max=1, default_val=0) ,
    "Clock Source": NRPN(cc1=64, cc2=6, val_min=0, val_max=4, default_val=0) ,
    "Animate 1 Hold": CC(cc1=114, val_min=0, val_max=1, default_val=0),
    "Animate 2 Hold": CC(cc1=115, val_min=0, val_max=1, default_val=0),
    "LFO 3/4 Select": NRPN(cc1=25, cc2=24, val_min=0, val_max=1, default_val=0),
    "LFO 3 Shape": NRPN(cc1=25, cc2=0, val_min=0, val_max=3, default_val=10),
    "LFO 3 Rate": NRPN(cc1=25, cc2=1, val_min=0, val_max=127, default_val=10),
    "LFO 3 Sync Rate": NRPN(cc1=25, cc2=2, val_min=0, val_max=34, default_val=10),
    "LFO 4 Shape": NRPN(cc1=25, cc2=3, val_min=0, val_max=3, default_val=10),
    "LFO 4 Rate": NRPN(cc1=25, cc2=4, val_min=0, val_max=127, default_val=10),
    "LFO 4 Sync Rate": NRPN(cc1=25, cc2=5, val_min=0, val_max=34, default_val=10),
    "Tuning Table": NRPN(cc1=25, cc2=6, val_min=0, val_max=16, default_val=0),
    "Voice Audio Input": NRPN(cc1=25, cc2=11, val_min=0, val_max=2, default_val=10),
    "FM 3>1 Source": NRPN(cc1=25, cc2=12, val_min=0, val_max=2, default_val=0),
    "FM 3>1 Manual": NRPN(cc1=25, cc2=13, val_min=0, val_max=127, default_val=0),
    "FM 3>1 Mod Env 2": NRPN(cc1=25, cc2=14, val_min=0, val_max=127, default_val=0),
    "FM 3>1 LFO 2": NRPN(cc1=25, cc2=15, val_min=0, val_max=127, default_val=0),
    "FM 1>2 Source": NRPN(cc1=25, cc2=16, val_min=0, val_max=2, default_val=0),
    "FM 1>2 Manual": NRPN(cc1=25, cc2=17, val_min=0, val_max=127, default_val=0),
    "FM 1>2 Mod Env 2": NRPN(cc1=25, cc2=18, val_min=0, val_max=127, default_val=0),
    "FM 1>2 LFO 2": NRPN(cc1=25, cc2=19, val_min=0, val_max=127, default_val=0),
    "FM 2>3 Source": NRPN(cc1=25, cc2=20, val_min=0, val_max=2, default_val=0),
    "FM 2>3 Manual": NRPN(cc1=25, cc2=21, val_min=0, val_max=127, default_val=0),
    "FM 2>3 Mod Env 2": NRPN(cc1=25, cc2=22, val_min=0, val_max=127, default_val=0),
    "FM 2>3 LFO 2": NRPN(cc1=25, cc2=23, val_min=0, val_max=127, default_val=0),
}

# unknown non-zero bytes: 250, 369,  386, 387, 395,410-429
# unknown nrpn: 



mod_matrix = {"Mod Matrix Selection": NRPN(cc1=0, cc2=125, val_min=0, val_max=15, default_val=0)}
for i in range(16):
    mod_matrix["Mod matrix " + str(i) + " Source 1"] = NRPN(cc1=i+1, cc2=0, val_min=0, val_max=16, default_val=0)
    mod_matrix["Mod matrix " + str(i) + " Source 2"] = NRPN(cc1=i+1, cc2=1, val_min=0, val_max=16, default_val=0)
    mod_matrix["Mod matrix " + str(i) + " Depth"] = NRPN(cc1=i+1, cc2=2, val_min=0, val_max=127, default_val=64)
    mod_matrix["Mod matrix " + str(i) + " Destination"] = NRPN(cc1=i+1, cc2=3, val_min=0, val_max=36, default_val=0)


fx_mod_matrix = {}
for i in range(4):
    fx_mod_matrix["FX Mod matrix " + str(i) + " Source 1"] = NRPN(cc1=i+17, cc2=0, val_min=0, val_max=15, default_val=0)
    fx_mod_matrix["FX Mod matrix " + str(i) + " Source 2"] = NRPN(cc1=i+17, cc2=1, val_min=0, val_max=15, default_val=0)
    fx_mod_matrix["FX Mod matrix " + str(i) + " Depth"] = NRPN(cc1=i+17, cc2=2, val_min=0, val_max=127, default_val=64)
    fx_mod_matrix["FX Mod matrix " + str(i) + " Destination"] = NRPN(cc1=i+17, cc2=3, val_min=0, val_max=11, default_val=0)


all_messages = {**parameters, **mod_matrix , **fx_mod_matrix}


'''
Mixing FM and Pitch from two patches might often be bad
same with waveform/wave shape 
Want to avoid mixing FM source with random: wave shape, pitch mod if the envelope is non-zero
if FM A>B is non zero, then group:
   A Pitch 
   A Wave
   (A Mod)
   B Pitch
'''

patch_groups = {
    "Osc1 Pitch": [
        "Oscillator 1 Range",
        "Oscillator 1 Coarse",
        "Oscillator 1 Fine",
    ],

    "Osc2 Pitch" : [         
        "Oscillator 2 Range",
        "Oscillator 2 Coarse",
        "Oscillator 2 Fine",
    ],

    "Osc3 Pitch": [
        "Oscillator 3 Range",
        "Oscillator 3 Coarse",
        "Oscillator 3 Fine",
    ],

    "FM" : [
        "FM 3>1 Source",
        "FM 3>1 Manual",
        "FM 3>1 Mod Env 2",
        "FM 3>1 LFO 2",
        "FM 1>2 Source",
        "FM 1>2 Manual",
        "FM 1>2 Mod Env 2",
        "FM 1>2 LFO 2",
        "FM 2>3 Source",
        "FM 2>3 Manual",
        "FM 2>3 Mod Env 2",
        "FM 2>3 LFO 2",
    ],

    "Osc1 Wave": [ 
        "Oscillator 1 Wave",
        "Oscillator 1 Wave More",
        "Oscillator 1 Shape Source",
        "Oscillator 1 Manual Shape",
        "Oscillator 1 Vsync",
        "Oscillator 1 Saw Density",
        "Oscillator 1 Saw Density Detune",
        "Oscillator 1 Fixed Note",
        "Oscillator 1 Bend Range",
        "Mixer Osc1",
    ],

    "Osc1 Mod": [
        "Oscillator 1 ModEnv2 > Pitch",
        "Oscillator 1 LFO2 > Pitch",
        "Oscillator 1 ModEnv1 > Shape",
        "Oscillator 1 LFO1 > Shape",
    ],

    "Osc2 Wave" : [
        "Oscillator 2 Wave",
        "Oscillator 2 Wave More",
        "Oscillator 2 Shape Source",
        "Oscillator 2 Manual Shape",
        "Oscillator 2 Vsync",
        "Oscillator 2 Saw Density",
        "Oscillator 2 Saw Density Detune",
        "Oscillator 2 Fixed Note",
        "Oscillator 2 Bend Range",
        "Mixer Osc2",
    ],

    "Osc2 Mod":[
        "Oscillator 2 ModEnv1 > Shape",
        "Oscillator 2 LFO1 > Shape",
        "Oscillator 2 ModEnv2 > Pitch",
        "Oscillator 2 LFO2 > Pitch",
    ],

    "Osc3 Wave" : [
        "Oscillator 3 Wave",
        "Oscillator 3 Wave More",
        "Oscillator 3 Shape Source",
        "Oscillator 3 Manual Shape",
        "Oscillator 3 Vsync",
        "Oscillator 3 Saw Density",
        "Oscillator 3 Saw Density Detune",
        "Oscillator 3 Fixed Note",
        "Oscillator 3 Bend Range",
        "Mixer Osc3",
    ],

    "Osc3 Mod" : [
        "Oscillator 3 ModEnv2 > Pitch",
        "Oscillator 3 LFO2 > Pitch",
        "Oscillator 3 ModEnv1 > Shape",
        "Oscillator 3 LFO1 > Shape"
    ],

    "Ring": ["Ring 1*2 Level"],

    "Voice" : [
        "Patch Category",
        "Patch Genre",
        "Voice Mode",
        "Voice Unison",
        "Voice Unison Detune",
        "Voice Unison Spread",
        "Voice Keyboard Octave",
        "Glide Time",
        "Voice Pre-Glide",
        "Glide On",
        "Osc Common Diverge",
        "Osc Common Drift",
        "Osc Common Key Sync",
    ],

    "Noise" : [
        "Osc Common Noise LPF",
        "Osc Common Noise HPF",
        "Noise Level",
    ],

    "Gain": [
        "Mixer Patch Level",
        "Mixer VCA gain",
        "Filter Overdrive",
        "Filter Post Drive",
        "Distortion level",
    ],

    "Filter" : [
        "Filter Slope",
        "Filter Shape",
        "Filter Dual Shape",
        "Filter Freq Seperation",
        "Filter Key Tracking",
        "Filter Resonance",
        "Filter Frequency",
        "Filter Divergence",
    ],

    "Filter Mod": [
        "LFO1 > Filter",
        "Osc3 > Filter",
        "Filter Env Select",
        "AmpEnv > Filter",
        "ModEnv1 > Filter",
    ],

    "Amp Envelope": [
        "Amp Envelope Attack",
        "Amp Envelope Decay",
        "Amp Envelope Sustain",
        "Amp Envelope Release",
        "Amp Envelope Velocity",
        "Amp Envelope Trigger",
        "Amp Envelope Delay",
        "Amp Envelope HoldTime",
        "Amp Envelope Repeats",
        "Amp Envelope Loop",
    ],

    "Mod Envelope 1" : [
        "Mod Envelope 1 Attack",
        "Mod Envelope 1 Decay",
        "Mod Envelope 1 Sustain",
        "Mod Envelope 1 Release",
        "Mod Envelope 1 Velocity",
        "Mod Envelope 1 Trigger",
        "Mod Envelope 1 Delay",
        "Mod Envelope 1 HoldTime",
        "Mod Envelope 1 Repeats",
        "Mod Envelope 1 Loop",
    ],

    "Mod Envelope 2" : [
        "Mod Envelope 2 Attack",
        "Mod Envelope 2 Decay",
        "Mod Envelope 2 Sustain",
        "Mod Envelope 2 Release",
        "Mod Envelope 2 Velocity",
        "Mod Envelope 2 Trigger",
        "Mod Envelope 2 Delay",
        "Mod Envelope 2 HoldTime",
        "Mod Envelope 2 Repeats",
        "Mod Envelope 2 Loop",
    ],

    "LFO 1" : [
        "LFO 1 Range",
        "LFO 1 Rate",
        "LFO 1 Sync Rate",
        "LFO 1 Wave",
        "LFO 1 Phase",
        "LFO 1 Slew",
        "LFO 1 Fade Time",
        "LFO 1 Fade In/Out",
        "LFO 1 Fade Sync",
        "LFO 1 Mono Trigger",
        "LFO 1 One Shot",
        "LFO 1 Common",
    ],

    "LFO 2": [
        "LFO 2 Range",
        "LFO 2 Rate",
        "LFO 2 Sync Rate",
        "LFO 2 Wave",
        "LFO 2 Phase",
        "LFO 2 Slew",
        "LFO 2 Fade Time",
        "LFO 2 Fade In/Out",
        "LFO 1 Fade Sync",
        "LFO 2 One Shot",
        "LFO 2 Common",
    ],

    "FX" : [
        "Mixer Dry Level",
        "Mixer Wet Level",
        "Effects Master Bypass",
        "Effects Routing",
    ],

    "Delay":[
        "Delay Level",
        "Delay Time",
        "Delay Width",
        "Delay Sync",
        "Delay Sync Time",
        "Delay Feedback",
        "Delay LP Damp",
        "Delay HP Damp",
        "Delay Slew Rate",
    ],

    "Reverb" : [
        "Reverb Level",
        "Reverb Type",
        "Reverb Time",
        "Reverb Damping LP",
        "Reverb Damping HP",
        "Reverb Size",
        "Reverb Mod",
        "Reverb Mod Rate",
        "Reverb Low Pass",
        "Reverb High Pass",
        "Reverb Pre Delay"
    ],

    "Chorus" : [
        "Chorus Level",
        "Chorus Type",
        "Chorus Rate",
        "Chorus Mod Depth",
        "Chorus Feedback",
        "Chorus LP",
        "Chorus HP",
    ],

    "Arp" : [
        "Arp/Clock Sync Rate",
        "Arp/Clock Type",
        "Arp/Clock Rhythm",
        "Arp/Clock Octave",
        "Arp/Clock Gate",
        "Arp/Clock Swing",
        "Arp/Clock On",
        "Arp/Clock Key Latch",
        "Arp/Clock Key Sync",
        "Arp Velocity Mode",
    ],

    "LFO3" : [
        "LFO 3 Shape",
        "LFO 3 Rate",
        "LFO 3 Sync Rate",
    ],

    "LFO 4" : [
        "LFO 4 Shape",
        "LFO 4 Rate",
        "LFO 4 Sync Rate",
    ]
}