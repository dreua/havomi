from dataclasses import dataclass
import mido
import mido.backends.rtmidi

from havomi.device import DeviceChannel
from havomi.target import Target
from havomi.scribble import scribble

@dataclass
class Channel:
    cid: int
    name: str
    level: int
    color: str
    dev_binding: DeviceChannel
    target: Target

    def update_scribble(self):
        return scribble(self.cid, color=self.color, top=self.name, bottom=self.level, inv_bot=True)

    def update_fader(self):
        d = self.dev_binding
        c = d.find_control("fader")
        if c.feedback:
            kwargs = {
                c.midi_id_field: c.midi_id,
                c.midi_value_field: self.level
            }
            return mido.Message(c.midi_type,**kwargs)

    def update_level(self):
        d = self.dev_binding
        c = d.find_control("level")
        if c.feedback:
            kwargs = {
                c.midi_id_field: c.midi_id,
                c.midi_value_field: self.level
            }
            return mido.Message(c.midi_type,**kwargs)

    def change_color(self, inc):
        colors = ["black","white","red","green","yellow","blue","cyan","magenta"]
        cur_index = colors.index(self.color)
        new_index = (cur_index+inc)%8
        self.color = colors[new_index]

    def set_level_from_float(self, value):
        prelim_level = 127*value
        self.level = int(prelim_level) if prelim_level >= 0 else 0

    def get_level_from_target(self):
        self.set_level_from_float(self.target.session.SimpleAudioVolume.GetMasterVolume())

    def update_target_volume(self):
        self.target.session.SimpleAudioVolume.SetMasterVolume(self.level/127, None)
