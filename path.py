__author__ = 'Nycidian'

# !/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
from libavg import app, avg
from tree import nodes

lines = {}
sys.setrecursionlimit(15000)

class MainDiv(app.MainDiv):

    def onInit(self):

        self.chosenNodes = set()
        #self.clickSave=None
        self.nodes = nodes
        self.settings.set("app_resolution", "%dx%d" % (1000, 10000))
        '''
        #self.toggleTouchVisualization()
        self.node = avg.CircleNode(color="FF00FF", fillcolor = 'FFFF00', fillopacity=1, strokewidth=1, pos=(30, 30), r=25, parent=self)
        #self.node = avg.ImageNode(href="art/node_blank.png", pos=(10,30), parent=self)
        self.line = avg.LineNode(color="FF00FF", strokewidth=1, pos1=(30, 30), pos2=(500, 30), parent=self)
        #(href="art/node_blank.png", pos=(10,30), parent=self)
        self.node.subscribe(avg.Node.CURSOR_DOWN, self.onDown)
        '''
        for key, value in nodes.iteritems():
            value['store'] = avg.CircleNode(color="FFffFF", fillcolor='777777', fillopacity=1, strokewidth=1,
                                            pos=value['pos'], r=10, parent=self, id=key)
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
        self.printbutton = avg.CircleNode(color="FF00FF", fillcolor = 'FF0000', fillopacity=1, strokewidth=1, pos=(450, 30), r=25, parent=self)
        #self.printbutton.subscribe(avg.Node.CURSOR_DOWN, self.printThis)
        self.printbutton.subscribe(avg.Node.CURSOR_DOWN, self.checkPath)


    def onDown(self, event):

        if not nodes[event.node.id]['clicked']:
            event.node.fillcolor = 'FFFFFF'
            nodes[event.node.id]['clicked'] = True
            self.chosenNodes.add(event.node.id)

        else:
            event.node.fillcolor = '777777'
            self.chosenNodes.remove(event.node.id)
            nodes[event.node.id]['clicked'] = False


    def checkPath(self, event):

        def pathRecursive(node_origin, node_end, past, path_list):

            for branch in nodes[node_origin]['linked']:
                # branch doubles back end
                if branch in past:
                    continue

                pass_past = [n for n in past] + [branch]

                if branch == node_end:
                    path_list.append(pass_past)
                    continue
                else:
                    pathRecursive(branch, node_end, pass_past, path_list)

        def pathCombine(alpha_dict, omega_dict, key_length, chosenNodes, stored):

            def reduceCompundSet(s):
                ret = set()
                for fs in s:
                    for n in fs:
                        ret.add(n)
                return ret


            new_dict = {}
            key_length += 1
            chosen_set = set(chosenNodes)

            alpha_dict = {key: value for key, value in alpha_dict.iteritems()}
            omega_dict = {key: value for key, value in omega_dict.iteritems()}
            for key_alpha, path_object_alpha in alpha_dict.iteritems():
                for key_omega, path_object_omega in omega_dict.iteritems():
                    Kalpha, Komega, alpha, omega = list(key_alpha), list(key_omega), list(path_object_alpha), list(path_object_omega)
                    new_key = frozenset(Kalpha+Komega)
                    new_path = set(alpha+omega)
                    if len(new_key) == key_length:
                        new_dict[new_key] = new_path

                    if chosen_set.issubset(reduceCompundSet(new_path)) and len(set(Kalpha)& set(Komega)) > 0:
                        stored.append(new_path)


            return new_dict, key_length, stored

        # --------------------------------------------------------------------------------------------------
        if event.button == 1:
            node_sets = {}
            frozen_sets = set()

            for begin in self.chosenNodes:
                for end in self.chosenNodes:
                    if begin != end:
                        frozen_sets.add(frozenset([begin, end]))

            for frozen_set in frozen_sets:
                begin, end = frozen_set
                path_list = []
                pathRecursive(begin, end, [begin], path_list)
                min_line = []
                for line in path_list:
                    this_line = []
                    last = None
                    for node in line:
                        if last is not None:
                            this_line.append(frozenset([last, node]))

                        last = node
                    min_line.append(this_line)

                min_path = min_line[0]
                for path in min_line:

                    if len(path) < len(min_path):
                        min_path = path

                node_sets[frozen_set] = min_path

            key_length = 2
            target_key_length = len(self.chosenNodes)
            new_node_sets = {key: value for key, value in node_sets.iteritems()}
            stored_list = []
            while key_length < target_key_length:

                new_node_sets, key_length, stored_list = pathCombine(node_sets, new_node_sets, key_length, self.chosenNodes, stored_list)

            min_path = None

            for path in stored_list:

                if min_path is None:
                    min_path = path
                else:
                    if len(min_path) > len(path):
                        min_path = path

            for line in min_path:

                lines[line]['store'].color = 'ffffff'
                lines[line]['store'].strokewidth = 3


        # --------------------------------------------------------------------------------------------------
        if event.button == 2:
            for key, value in lines.iteritems():
                lines[key]['store'].color = 'ff7777'
                lines[key]['store'].strokewidth = 1

app.App().run(MainDiv(), app_resolution='500x540')