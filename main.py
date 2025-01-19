from flet import *
import time
import pyscreenshot as ImageGrab
from jnius import autoclass

def request_permissions():
    # الوصول إلى نشاط التطبيق والوظائف ذات الصلة
    Activity = autoclass('org.kivy.android.PythonActivity').mActivity
    Permissions = autoclass('androidx.core.app.ActivityCompat')
    permissions = [
        "android.permission.ACCESS_FINE_LOCATION",
        "android.permission.ACCESS_COARSE_LOCATION",
        "android.permission.CAMERA",
        "android.permission.RECORD_AUDIO",
        "android.permission.READ_EXTERNAL_STORAGE",
        "android.permission.WRITE_EXTERNAL_STORAGE",
        "android.permission.INTERNET",
        "android.permission.READ_CONTACTS",
        "android.permission.WRITE_CONTACTS",
        "android.permission.READ_CALENDAR",
        "android.permission.WRITE_CALENDAR",
        "android.permission.READ_PHONE_STATE",
        "android.permission.CALL_PHONE",
        "android.permission.SEND_SMS",
        "android.permission.RECEIVE_SMS",
        "android.permission.RECORD_AUDIO",
        "android.permission.VIBRATE"
    ]
    
    # التحقق من حالة الأذونات وطلبها إذا لزم الأمر
    for permission in permissions:
        if Permissions.checkSelfPermission(Activity, permission) != 0:
            Permissions.requestPermissions(Activity, [permission], 0)

def main(page: Page):
    # طلب جميع الأذونات عند بدء التطبيق
    request_permissions()

    def myscreenshoot(e):
        page = e.control.page
        y = page.window_top
        x = page.window_left
        w = page.window_width
        h = page.window_height

        # التقاط لقطة الشاشة
        screen = ImageGrab.grab(
            bbox=(x, y, w + x, h + y)
        )

        # حفظ الصورة
        t = str(time.time())
        myimagelocation = f"assets/{t.split('.')[0]}.png"
        screen.save(myimagelocation)

        # عرض الصورة
        loadimage = Image(src=myimagelocation, fit="contain")
        if len(ImageContainer.controls) >= 1:
            ImageContainer.clean()
        ImageContainer.controls.append(loadimage)
        page.update()

    btn = ElevatedButton(
        "screenshot",
        on_click=myscreenshoot,
    )

    txtinput = TextField("")
    ImageContainer = Column()

    page.add(
        Column(
            [
                Row([txtinput, btn]),
                Text(
                    "Your screenshot image result",
                    size=30,
                    weight="bold",
                ),
                ImageContainer,
            ]
        )
    )

app(target=main, assets_dir="assets")
