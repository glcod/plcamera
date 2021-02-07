from kivymd.app import MDApp
from kivymd.toast import toast
from kivymd.uix.button import MDIconButton

from kivy.lang import Builder
from kivy.core.window import Window

import os
from plyer import camera, storagepath
from jnius import autoclass, cast
from permissions.access import check_permission, ask_permission 
import android.activity
import android
from plyer.platforms.android import activity

#Window.size = (300,500)

KV = """
Screen:
    BoxLayout:
        orientation:'vertical'
        MDToolbar:
            title: 'Kampy'
            elevation:10

        Widget:

        FloatLayout:
            MDIconButton:
                icon: "camera-iris"
                elevation_normal: 14
                user_font_size: "48sp"
                pos_hint: {"center_x": .5, "center_y": .13}
                on_release: app.take_shot()

"""

class KampyApp(MDApp):
    IMAGE_PATH = str(storagepath.get_pictures_dir())
    
    def request_kampy_permission(self):
        ask_permission("android.permission.WRITE_EXTERNAL_STORAGE")
        ask_permission("android.permission.CAMERA")
        

    def check_kampy_permission(self):
        if check_permission("android.permission.WRITE_EXTERNAL_STORAGE") and check_permission("android.permission.CAMERA"):
            pass
        else:
            request_kampy_permission()
            
    def take_shot(self, *args):
        self.time = datetime.now().strftime("%Y%m%d_%H%M%S%f")
        filename = '{0}/IMG_{1}.jpg'.format(IMAGE_PATH, self.time)
        try:
            camera.take_picture(filename=filename, on_complete=self.complete_callback)
        except NotImplementedError:
            self.camera_status = 'Camera is not implemented for your platform'

    def complete_callback(self, filename):
        try:
            Intent = autoclass('android.content.Intent')
            PythonActivity = autoclass('org.kivy.android.PythonActivity')
            Uri = autoclass('android.net.Uri')
            context = PythonActivity.mActivity
            intent = Intent()
            uri = 'file://{0}'.format(filename)
            intent.setAction(Intent.ACTION_MEDIA_SCANNER_SCAN_FILE)
            intent.setData(Uri.parse(uri))
            context.sendBroadcast(intent)
            im = Image.open(filename)
            im.thumbnail(Window.size)
            outfile = '{0}/IMG_{1}.jpg'.format(THUMBNAIL_PATH, self.time)
            im.save(outfile, "JPEG")
        except Exception as e:
            Logger.error(str(e))
            self.error = str(e)
        return False
    
    def __init__(self):
        check_kampy_permission()
        
    def build(self):
        self.theme_cls.primary_palette = "Blue"
        self.theme_cls.primary_hue = "900"
        self.theme_cls.accent_palette = "Red"
        self.theme_cls.accent_hue = "A700"
        self.theme_cls.theme_style = "Light"
        return Builder.load_string(KV)
         

    def change_theme(self):
        if self.theme_cls.theme_style == "Light":
            self.theme_cls.theme_style = "Dark"
        else:
            self.theme_cls.theme_style = "Dark"

if __name__ == "__main__":
    KampyApp().run()  
