import hashlib
from typing import DefaultDict
import win32gui, win32process
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
import psutil
from collections import namedtuple

AppDef = namedtuple("AppDef", ["name", "color", "sessions"])

def get_active_window_session():
    hwnd = win32gui.GetForegroundWindow()
    tid, current_pid = win32process.GetWindowThreadProcessId(hwnd)
    process_name = psutil.Process(current_pid).name()
    sessions = AudioUtilities.GetAllSessions()
    for session in sessions:
        if session.Process and session.Process.name() == process_name:
            return session

def get_master_volume_session():
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    return cast(interface, POINTER(IAudioEndpointVolume))

def find_audio_sessions(target, session_list):
    if target is None:
        return None
    
    for i,s in enumerate(session_list):
        if target.session.InstanceIdentifier is None:
            if s.InstanceIdentifier is None:
                return i
        elif s.InstanceIdentifier == target.session.InstanceIdentifier:
            return i
    
    return None

def construct_color_from_hash(name):
    colors = ["red","green","yellow","blue","cyan","magenta"]
    name_to_int = int(hashlib.md5(name.encode('utf-8')).hexdigest(),16)
    return colors[name_to_int%len(colors)]

def get_active_window_app_def():
    hwnd = win32gui.GetForegroundWindow()
    tid, current_pid = win32process.GetWindowThreadProcessId(hwnd)
    process_name = psutil.Process(current_pid).name()
    sessions = AudioUtilities.GetAllSessions()
    app_sessions = []
    for session in sessions:
        if session.Process and session.Process.name() == process_name:
            app_sessions.append(session)
    color = construct_color_from_hash(process_name)

    return AppDef(process_name, color, app_sessions)

def get_applications_and_sessions():
    sessions = AudioUtilities.GetAllSessions()
    app_sessions = DefaultDict(list)

    apps = {}
    for session in sessions:
        name = session.Process.name() if session.Process else "Sys"
        app_sessions[name].append(session)
    
    for name,sessions in app_sessions.items():
        color = construct_color_from_hash(name) if name != "Sys" else "white"
        apps[name] = AppDef(name, color, sessions)
    
    apps["Master"] = AppDef("Master", "white", [get_master_volume_session()])

    return apps
