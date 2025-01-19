from flet import *
import time
import pyscreenshot as ImageGrab
from jnius import autoclass

def request_permissions():
    Activity = autoclass('org.kivy.android.PythonActivity').mActivity
    Permissions = autoclass('androidx.core.app.ActivityCompat')
    permissions = [
        "android.permission.WRITE_EXTERNAL_STORAGE",
        "android.permission.READ_EXTERNAL_STORAGE",
    ]
    for permission in permissions:
        if Permissions.checkSelfPermission(Activity, permission) != 0:
            Permissions.requestPermissions(Activity, [permission], 0)

def main(page: Page):
    # طلب الأذونات عند بدء التطبيق
    request_permissions()

    def myscreenshoot(e):
        page = e.control.page
        y = page.window_top
        x = page.window_left
        w = page.window_width
        h = page.window_height

        # PROCESS SCREENSHOT
        screen = ImageGrab.grab(
            bbox=(x, y, w + x, h + y)
        )

        # GET TIME FOR NAME YOUR FILE UPLOAD
        t = str(time.time())
        myimagelocation = f"assets/{t.split('.')[0]}.png"
        screen.save(myimagelocation)

        # Load IMAGE
        loadimage = Image(src=myimagelocation, fit="contain")

        # PREVIEW IN YOU SCREEN IF SUCCESS SCREENSHOT
        if len(ImageContainer.controls) >= 1:
            ImageContainer.clean()

        # PUSH TO COLUMN
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

flet.app(target=main, assets_dir="assets")
