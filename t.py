from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.image import Image
from kivy.uix.scatterlayout import ScatterPlaneLayout
from kivy.graphics import Color, Ellipse, Rectangle, Scale
from kivy.config import Config

Config.set("input", "mouse", "mouse, disable_multitouch")

import json

with open('json/tree.json') as data_file:
    tree = json.load(data_file)

class PaperWidget(ScatterPlaneLayout):

    def __init__(self, **kwargs):
        super(PaperWidget, self).__init__(**kwargs)

        self.touch_offset = None
        self.scale_count = 0

        self.groups = {}
        self.nodes = {}

        for key, value in tree['groups'].items():
            self.groups[key] = {'pos': (value['x'], value['y']*-1), 'r': 10}

        for value in tree['nodes']:
            icon = value['icon'].split('/')
            stone_type = 'Base'
            size = (64, 64)
            offset = (32, 32)
            if value['ks']:
                stone_type = 'Keystone'
                offset = (64, 64)
                size = (128, 128)
            if value['m']:
                stone_type = 'Master'
                offset = (128, 128)
                size = (256, 256)
            if value['not']:
                stone_type = 'Notable'
                offset = (64, 64)
                size = (128, 128)


            if value['o'] == 0:
                pos = self.groups[str(value['g'])]['pos']

                self.nodes[value['id']] = {
                    'g': value['g'],
                    'pos': pos,
                    'r': 10,
                    'icon': icon[-1],
                    'stone_type': stone_type,
                    'offset': offset,
                    'size': size
                }


        for key, value in self.nodes.items():
            node = Image(source='downloaded/'+value['icon'])
            node.size = value['size']
            node.center = value['pos']

            self.add_widget(node)
            '''
            self.groups[key]['node'] = avg.CircleNode(color="FFffFF", fillcolor='777777', fillopacity=1,
                        strokewidth=1, pos=value['pos'], r=value['r'], parent=self.paper)
            '''
           # num = avg.WordsNode(text=str(value['g']), parent=node)

    def on_touch_down(self, touch):

        scale = [
            1.0, 0.5, 0.25, 0.1, 0.05
        ]
        scale = scale[:-1] + scale[::-1]
        scale = scale[:-1]

        if self.collide_point(*touch.pos):
            touch.grab(self)
            x_o, y_o = touch.pos
            x_p, y_p = self.pos
            self.touch_offset = (x_o-x_p, y_o-y_p)
            # do whatever else here

        if touch.button == 'scrollup':
            self.scale_count += 1
            scalar = scale[self.scale_count % len(scale)]
            self.scale = scalar

        if touch.button == 'scrolldown':
            self.scale_count -= 1
            scalar = scale[self.scale_count % len(scale)]
            self.scale = scalar

    def on_touch_move(self, touch):
        if touch.grab_current is self:
            x_o, y_o = self.touch_offset
            self.pos = (touch.x - x_o, touch.y - y_o)

    def on_touch_up(self, touch):

        if touch.grab_current is self:
            touch.ungrab(self)
            #self.touch_origin = self.pos
            # and finish up here


class PathfinderApp(App):

    def build(self):
        self.root = root = PaperWidget()
        #root.bind(size=self._update_rect, pos=self._update_rect)

        with root.canvas.before:
            Color(0, 1, 0, 1)  # green; colors range from 0-1 not 0-255
            self.rect = Rectangle(size=(100, 100), pos=root.pos)
        return root

    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos


if __name__ == '__main__':
    PathfinderApp().run()