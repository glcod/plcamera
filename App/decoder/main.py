from kivymd.app import MDApp
from kivymd.toast import toast

from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.utils import platform
from kivy.core.window import Window

from plyer import storagepath
import time
from libs.uix.decode_barcode import read_barcodes
#from libs.uix.permissions.access import check_permission, ask_permission

Builder.load_string('''
#:import win kivy.core.window
<CameraClick>:
    orientation: 'vertical'

    Camera:
        id: camera
        resolution:(1920,1080) #Window.size
        play: True
        allow_stretch: True
        size: dp(500), dp(500)
        canvas.before:
            PushMatrix
            Rotate:
                angle: -90
                origin: self.center
        canvas.after:
            PopMatrix

    MDIconButton:
        icon: "camera-iris"
        elevation_normal: 14
        user_font_size: "48sp"
        pos_hint: {"center_x": .5, "center_y": .13}
        on_release: root.capture()

''')


class CameraClick(BoxLayout):
    
    def capture(self):
        '''
        Function to capture the images and give them the names
        according to their captured time and date.
        '''
        IMAGE_PATH = str(storagepath.get_pictures_dir())
        #IMAGE_PATH = "C:\\Users\\Jain\\Desktop\\Decoder\\kamera"
        camera = self.ids['camera']
        timestr = time.strftime("%Y%m%d_%H%M%S")
        #camera.export_to_png("IMG_{}.png".format(timestr))
        filename = '{0}/IMG_{1}.jpeg'.format(IMAGE_PATH, timestr)
        camera.export_to_png(filename)
        print(filename)
        print("Captured")
        toast(read_barcodes(filename))


class TestCamera(MDApp):
    
    
    def build(self):
        return CameraClick()


TestCamera().run()
