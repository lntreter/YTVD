from kivy.app import App
from kivy.uix.widget import Widget
from kivy.lang import Builder
from kivy.animation import Animation
from kivy.core.window import Window
from kivy.properties import ObjectProperty
from kivy.uix.textinput import TextInput
from kivy.config import Config
from kivy.uix.image import Image
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.image import AsyncImage
from pytube import YouTube
from pytube.cli import on_progress
import threading, os, sys
from kivy.resources import resource_add_path, resource_find

#--------------------------------------------

Builder.load_string('''
#:kivy 2.0

<Button>
    text: "1.Kat"
    background_color: (.75, 0, 0, 1.0)
    font_size: 16
    size_hint: .35, .15

<MyLayout>

    FloatLayout:
        orientation: "vertical"
        size: root.width, root.height
        canvas:
            Color:
                rgba: .827, .827, .827, 1.0
            Rectangle:
                pos: self.pos
                size: self.size

        Label:
            id: my_label
            bold: True
            text: "YouTube Video İndirici"
            color: .392,0,0,1 #
            font_size: 32
            size_hint: .3, .3
            pos_hint: {"center_x": 0.5,"center_y": 0.84}
        
        Label:
            id: author
            bold: True
            text: "by Intreter"
            color: .392,0,0,1 #
            font_size: 14
            size_hint: .3, .3
            pos_hint: {"center_x": 0.9,"center_y": 0.1}

        Label:
            id: my_label2
            text: "Video İsmi: "
            color: .392,0,0,1 #
            font_size: 18
            size_hint: .3, .3
            pos_hint: {"center_x": 0.5,"center_y": 0.74}

        ProgressBar:
            id: prog
            min: 0
            max: 100
            value: 0
            size_hint: .7, .2
            pos_hint: {"center_x": 0.5,"center_y": 0.68}

        TextInput:
            id: link
            hint_text:'                                      Video Linki'
            size_hint: .5, .3
            pos_hint: {"center_x": 0.5,"center_y": 0.5}

        AsyncImage:
            id: img_tn
            source: 'yt.png'
            size_hint: .27, .15
            pos_hint: {"center_x": 0.68,"center_y": 0.23}

        Button:
            text: "Bir YT video linki girip butona bas!"
            pos_hint: {"center_x": 0.38,"center_y": 0.23}
            on_press: root.animate_press(self)
            on_release: 
                root.animate_release(self)
                root.thread()



''')

Config.window_icon = 'icon.png'

class MyLayout(Widget):
    def animate_press(self,widget,*args):
        animate = Animation(
            duration = .001)

        animate += Animation(
            size_hint = (.335,.135),
            color = (.7,0,0,1),
            duration = .03,)

        # Start the Animation
        animate.start(widget)

    def animate_release(self,widget,*args):
        animate = Animation(
            duration = .001)

        animate += Animation(
            size_hint = (.35,.15),
            color = (1,1,1,1),
            duration = .03,)

        # Start the Animation
        animate.start(widget)

    def b(self,stream,chunk:bytes,bytes_remaining):
        val = 0
        total_size = stream.filesize
        bytes_downloaded = total_size - bytes_remaining
        percentage_of_completion = (bytes_downloaded/total_size)*100
        inc = int(percentage_of_completion)
        while val < inc:
            val += 1
            self.ids.prog.value = val

    def download(self):
        self.ids.my_label.text = "İndiriliyor..."
        url = self.ids.link.text
        try:
            yt = YouTube(url, on_progress_callback=self.b)
        except:
            self.ids.my_label.text = "Hata"
            return
        self.ids.my_label2.text = "Başlık: " + yt.title
        try:
            self.ids.img_tn.source = yt.thumbnail_url
        except KeyError:
            self.ids.img_tn.source = "noimage.png"
        stream = yt.streams.get_highest_resolution()
        variable = 0
        while stream.download():
            variable += 2
            self.ids.prog.value = variable
            if variable == 100 or variable > 100:
                break
        if variable != 100:
            variable = 100
        self.ids.my_label.text = "İndirildi!"

    def thread(self):
        thread=threading.Thread(target=self.download)
        thread.start()

class YTVDApp(App):
    def build(self):
        self.icon = 'icon1.png'
        return MyLayout()

if __name__ == "__main__":
    if hasattr(sys, '_MEIPASS'):
        resource_add_path(os.path.join(sys._MEIPASS))
    YTVDApp().run()