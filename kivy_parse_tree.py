__author__ = 'Nycidian'

# !/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
from math import sin, cos, pi
import json
from pprint import pprint


import kivy
kivy.require('1.9.0') # replace with your current kivy version !

from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput

with open('json/tree.json') as data_file:
    tree = json.load(data_file)

class LoginScreen(GridLayout):

    def __init__(self, **kwargs):
        super(LoginScreen, self).__init__(**kwargs)
        self.cols = 2
        self.add_widget(Label(text='User Name'))
        self.username = TextInput(multiline=False)
        self.add_widget(self.username)
        self.add_widget(Label(text='password'))
        self.password = TextInput(password=True, multiline=False)
        self.add_widget(self.password)

class PoePathFinder(App):

    def __init__(self, *args, **kwargs):
        super(self.__class__, self).__init__(*args, **kwargs)
        self.groups = {}
        self.nodes = {}

    def build(self):
        return LoginScreen()


    def onInit(self):
        self.paper = avg.DivNode(pos=(800, 500), width=1600, height=1000, parent=self)

        for key, value in tree['groups'].iteritems():
            self.groups[key] = {'pos': (value['x'], value['y']), 'r': 10}

        for value in tree['nodes']:
            icon = value['icon'].split('/')
            stone_type = 'Base'
            size = (64*self.image_scale, 64*self.image_scale)
            offset = (-32*self.image_scale, -32*self.image_scale)
            if value['ks']:
                stone_type = 'Keystone'
                offset = (-64*self.image_scale, -64*self.image_scale)
                size = (128*self.image_scale, 128*self.image_scale)
            if value['m']:
                stone_type = 'Master'
                offset = (-128*self.image_scale, -128*self.image_scale)
                size = (256*self.image_scale, 256*self.image_scale)
            if value['not']:
                stone_type = 'Notable'
                offset = (-64*self.image_scale, -64*self.image_scale)
                size = (128*self.image_scale, 128*self.image_scale)


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


        for key, value in self.nodes.iteritems():
            node = avg.DivNode(pos=value['pos'], width=25, height=25, parent=self.paper)
            self.nodes[key]['node'] = avg.ImageNode(href='downloaded/'+value['icon'], pos=value['offset'], size=value['size'], parent=node)

            '''
            self.groups[key]['node'] = avg.CircleNode(color="FFffFF", fillcolor='777777', fillopacity=1,
                        strokewidth=1, pos=value['pos'], r=value['r'], parent=self.paper)
            '''
            num = avg.WordsNode(text=str(value['g']), parent=node)


        """
        for key, value in nodes.iteritems():
            value['store'] = avg.CircleNode(color="FFffFF", fillcolor='777777', fillopacity=1, strokewidth=1,
                                            pos=value['pos'], r=10, parent=self, id=key)f
            value['clicked'] = False
            value['store'].subscribe(avg.Node.CURSOR_DOWN, self.onDown)

            for n in value['linked']:
                lines[frozenset([key, n])] = {
                    'store': None,
                    'cords': [value['pos'], nodes[n]['pos']]
                }

        for key, value in lines.iteritems():
            value['store'] = avg.LineNode(color="ff7777", strokewidth=1, pos1=value['cords'][0], pos2=value['cords'][1],
                                 parent=self)
        """
        self.subscribe(avg.Node.CURSOR_DOWN, self.middleMouse)

        self.printbutton = avg.CircleNode(color="FF00FF", fillcolor = 'FF0000', fillopacity=1, strokewidth=1, pos=(30, 30), r=25, parent=self)
        self.printbutton.subscribe(avg.Node.CURSOR_DOWN, self.printThis)




    def middleMouse(self, event):
        if event.button == 3:
            print(event.button)
        print(event.button)
        if event.button == 4:
            print('up')
            print(self.paper.x)
            self.paper.height=50
        if event.button == 5:
            print('down')

    def printThis(self, event):
        print(2*cos(2*pi/8), 2*sin(2*pi/8))




if __name__ == '__main__':
    PoePathFinder().run()