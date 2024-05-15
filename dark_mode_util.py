# https://youtu.be/4Gi1sKKn_Ts?si=ZdAX5KIP_Y-kwQ_S

import ctypes as ct
def dark_title_bar(window):
    """
    MORE INFO:
    https://docs.microsoft.com/en-us/windows/win32/api/dwmapi/ne-dwmapi-dwmwindowattribute
    """
    window.update()
    DWMWA_USE_IMMERSIVE_DARK_MODE = 20
    set_window_attribute = ct.windll.dwmapi.DwmSetWindowAttribute
    get_parent = ct.windll.user32.GetParent
    hwnd = get_parent(window.winfo_id())
    rendering_policy = DWMWA_USE_IMMERSIVE_DARK_MODE
    value = 2
    value = ct.c_int(value)
    set_window_attribute(hwnd, rendering_policy, ct.byref(value), ct.sizeof(value))

# def set_dark_menubar(window):
#     """
#     Sets the menubar background to dark mode.
#     """
#     window.update()
#     DWMWA_USE_IMMERSIVE_DARK_MODE = 20
#     set_window_attribute = ct.windll.dwmapi.DwmSetWindowAttribute
#     get_parent = ct.windll.user32.GetParent
#     hwnd = get_parent(window.winfo_id())
#     rendering_policy = DWMWA_USE_IMMERSIVE_DARK_MODE
#     value = 2  # 0 for light, 1 for dark, 2 for system default (dark)
#     value = ct.c_int(value)
#     set_window_attribute(hwnd, rendering_policy, ct.byref(value), ct.sizeof(value))
