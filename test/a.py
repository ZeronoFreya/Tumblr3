import win32con, win32api, win32gui
import ctypes, ctypes.wintypes

FindWindow = ctypes.windll.user32.FindWindowW
SendMessage = ctypes.windll.user32.SendMessageW

class COPYDATASTRUCT(ctypes.Structure):
    _fields_ = [
        ('dwData', ctypes.wintypes.LPARAM),
        ('cbData', ctypes.wintypes.DWORD),
        ('lpData', ctypes.c_char_p)
        #formally lpData is c_void_p, but we do it this way for convenience
]

PCOPYDATASTRUCT = ctypes.POINTER(COPYDATASTRUCT)

# hwnd = FindWindow(None, "ZhornSoftwareStickiesMain")
# cds = COPYDATASTRUCT()
# cds.dwData = 0
# str = b'api do register'
# cds.cbData = ctypes.sizeof(ctypes.create_string_buffer(str))
# cds.lpData = ctypes.c_char_p(str)

class Listener:

    def __init__(self):
        print('jh')
        message_map = {
            win32con.WM_COPYDATA: self.OnCopyData
        }
        wc = win32gui.WNDCLASS()
        wc.lpfnWndProc = message_map
        wc.lpszClassName = 'MyWindowClass'
        hinst = wc.hInstance = win32api.GetModuleHandle(None)
        classAtom = win32gui.RegisterClass(wc)
        self.hwnd = win32gui.CreateWindow (
            classAtom,
            "win32gui test",
            0,
            0, 
            0,
            win32con.CW_USEDEFAULT, 
            win32con.CW_USEDEFAULT,
            0, 
            0,
            hinst, 
            None
        )
        self.register()

    def register(self):
        hwnd = FindWindow(None, "ZhornSoftwareStickiesMain")
        cds = COPYDATASTRUCT()
        cds.dwData = 0
        str = b'api do register'
        cds.cbData = ctypes.sizeof(ctypes.create_string_buffer(str))
        cds.lpData = ctypes.c_char_p(str)
        SendMessage(hwnd, win32con.WM_COPYDATA, self.hwnd, ctypes.byref(cds))

    def OnCopyData(self, hwnd, msg, wparam, lparam):
        print(hwnd)
        print(msg)
        print(wparam)
        print(lparam)
        pCDS = ctypes.cast(lparam, PCOPYDATASTRUCT)
        print(pCDS.contents.dwData)
        print(pCDS.contents.cbData)
        print(ctypes.wstring_at(pCDS.contents.lpData))
        # print(pCDS.contents.lpData.decode("ascii", "ignore"))
        return 1

l = Listener()
win32gui.PumpMessages()