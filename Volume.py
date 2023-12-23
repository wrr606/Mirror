from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

#傳入數字，會將音量調整為該數字(換算百分比)
def set_volume(new_volume):
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(
        IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    volume = cast(interface, POINTER(IAudioEndpointVolume))
    volume.SetMasterVolumeLevelScalar(new_volume, None)

"""
pip install pycaw

from Volume import set_volume

set_volume(0.5)
這樣就會設定音量為 50%
"""