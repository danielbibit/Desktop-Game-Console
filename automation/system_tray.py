import wx.adv
import os

TRAY_TOOLTIP = 'System Tray Demo'
TRAY_ICON = 'assets/tray_icon.png'

def create_menu_item(menu, label, func):
    item = wx.MenuItem(menu, -1, label)
    menu.Bind(wx.EVT_MENU, func, id=item.GetId())
    menu.AppendItem(item)
    return item

class TaskBarIcon(wx.adv.TaskBarIcon):
    def __init__(self, frame, event_engine):
        self.frame = frame

        self.event_engine = event_engine

        super(TaskBarIcon, self).__init__()
        icon = wx.Icon(wx.Bitmap(TRAY_ICON, wx.BITMAP_TYPE_ANY))

        self.SetIcon(icon,TRAY_TOOLTIP)
        self.Bind(wx.adv.EVT_TASKBAR_LEFT_DOWN, self.on_left_down)

    def CreatePopupMenu(self):
        menu = wx.Menu()

        create_menu_item(menu, 'Launch Playnite', self.on_launch)

        menu.AppendSeparator()

        create_menu_item(menu, 'Exit', self.on_exit)

        return menu

    def set_icon(self, path):
        icon = wx.Icon(wx.Bitmap(path))
        self.SetIcon(icon, TRAY_TOOLTIP)

    def on_left_down(self, event):
        print ('Tray icon was left-clicked.')

    def on_launch(self, event):
        print('Launching through tray icon')
        self.event_engine.new_event('0x410')

    def on_exit(self, event):
        wx.CallAfter(self.Destroy)
        self.frame.Close()
        os._exit(1)

class WxApp(wx.App):
    def __init__(self, event_engine):
        self.event_engine = event_engine
        wx.App.__init__(self, redirect=False)

    def OnInit(self):
        frame=wx.Frame(None)
        self.SetTopWindow(frame)
        TaskBarIcon(frame, self.event_engine)

        return True
