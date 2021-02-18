from kivy.utils import platform
import datetime
import os


def is_android():
    return platform == 'android'


def check_camera_permission():
    """
    Android runtime `CAMERA` permission check.
    """
    if not is_android():
        return True
    from android.permissions import Permission, check_permission
    permission = Permission.CAMERA
    return check_permission(permission)


def check_request_camera_permission(callback=None):
    """
    Android runtime `CAMERA` permission check & request.
    """
    had_permission = check_camera_permission()
    if not had_permission:
        from android.permissions import Permission, request_permissions
        permissions = [Permission.CAMERA]
        request_permissions(permissions, callback)
    return had_permission

class CameraClick(BoxLayout):
    directory = ObjectProperty(None)
    _previous_orientation = None
    __events__ = ('on_picture_taken', 'on_camera_ready')

    def __init__(self, **kwargs):
        Builder.load_file(os.path.join(ROOT, "xcamera.kv"))
        super().__init__(**kwargs)

    def _on_index(self, *largs):
        """
        Overrides `kivy.uix.camera.Camera._on_index()` to make sure
        `camera.open()` is not called unless Android `CAMERA` permission is
        granted, refs #5.
        """
        @mainthread
        def on_permissions_callback(permissions, grant_results):
            """
            On camera permission callback calls parent `_on_index()` method.
            """
            if all(grant_results):
                self._on_index_dispatch(*largs)
        if check_request_camera_permission(callback=on_permissions_callback):
            self._on_index_dispatch(*largs)

    def _on_index_dispatch(self, *largs):
        super()._on_index(*largs)
        self.dispatch('on_camera_ready')

    
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
