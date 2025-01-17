#!/usr/bin/env python3

__author__ = "Ashwin Nanjappa"

# GUI viewer to view JSON data as tree.
# Ubuntu packages needed:
# python3-pyqt5

# Std
import argparse
import collections
import json
import sys

# External
from PyQt5 import QtCore
from PyQt5 import QtGui
from PyQt5 import QtWidgets
import pathlib

class TextToTreeItem:

    def __init__(self):
        self.text_list = []
        self.titem_list = []

    def append(self, text_list, titem):
        for text in text_list:
            self.text_list.append(text)
            self.titem_list.append(titem)

    # Return model indices that match string
    def find(self, find_str):

        titem_list = []
        for i, s in enumerate(self.text_list):
            if find_str in s:
                titem_list.append(self.titem_list[i])
                #print("The search ", find_str, " was in ",s) #debugging, later comment this
            #else: #debugging, later comment this   
                #print("The search ", find_str, " was not in ",s) #debugging, later comment this   
        return titem_list


class JsonView(QtWidgets.QWidget):

    def __init__(self, fpath, titleName, parent=None):
        super(JsonView, self).__init__(parent=parent)

        self.find_box = None
        self.tree_widget = None
        self.text_to_titem = TextToTreeItem()
        self.find_str = ""
        self.found_titem_list = []
        self.found_idx = 0

        #jfile = open(fpath)
        #jdata = json.load(jfile, object_pairs_hook=collections.OrderedDict)
        jdata = fpath

        # Find UI

        find_layout = self.make_find_ui()

        # Tree

        self.tree_widget = QtWidgets.QTreeWidget()
        self.tree_widget.setAnimated(True)

        current_directory = str(pathlib.Path(__file__).parent.absolute())
        pathVline = current_directory.replace("\\", "/") + '/icon/vline.png'
        pathbranchmore = current_directory.replace("\\", "/") + '/icon/branch-more.png'
        pathbranchend = current_directory.replace("\\", "/") + '/icon/branch-end.png'
        pathbranchclosed = current_directory.replace("\\", "/") + '/icon/branch-closed.png'
        pathbranchopen = current_directory.replace("\\", "/") + '/icon/branch-open.png'

        self.tree_widget.setStyleSheet("""
        QTreeView::branch:has-siblings:!adjoins-item {
            border-image: url("""+pathVline+""") 0;
        }

        QTreeView::branch:has-siblings:adjoins-item {
            border-image: url("""+pathbranchmore+""") 0;
        }

        QTreeView::branch:!has-children:!has-siblings:adjoins-item {
            border-image: url("""+pathbranchend+""") 0;
        }

        QTreeView::branch:has-children:!has-siblings:closed,
        QTreeView::branch:closed:has-children:has-siblings {
                border-image: none;
                image: url("""+pathbranchclosed+""");
        }

        QTreeView::branch:open:has-children:!has-siblings,
        QTreeView::branch:open:has-children:has-siblings  {
                border-image: none;
                image: url("""+pathbranchopen+""");
        }
        """)

        self.tree_widget.setHeaderLabels(["Key", "Value"])
        self.tree_widget.header().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)

        root_item = QtWidgets.QTreeWidgetItem(["Root"])
        self.recurse_jdata(jdata, root_item)
        self.tree_widget.addTopLevelItem(root_item)

        # Add table to layout
        layout = QtWidgets.QHBoxLayout()
        layout.addWidget(self.tree_widget)

        # Group box

        gbox = QtWidgets.QGroupBox(titleName)
        gbox.setLayout(layout)

        #Remove borders
        gbox.setFlat(True)

        layout2 = QtWidgets.QVBoxLayout()
        layout2.addLayout(find_layout)
        layout2.addWidget(gbox)
        self.setLayout(layout2)

    def make_find_ui(self):

        # Text box
        self.find_box = QtWidgets.QLineEdit()
        self.find_box.returnPressed.connect(self.find_button_clicked)
        self.find_box.setPlaceholderText("Insert string here. Case sensitive")

        # Find Button
        find_button = QtWidgets.QPushButton("Find")
        find_button.clicked.connect(self.find_button_clicked)

        # Search Label
        search_label = QtWidgets.QLabel("Look for entry")

        layout = QtWidgets.QHBoxLayout()
        layout.addWidget(search_label)
        layout.addWidget(self.find_box)
        layout.addWidget(find_button)

        return layout

    def find_button_clicked(self):

        find_str = self.find_box.text()

        # Very common for use to click Find on empty string
        if find_str == "":
            return

        # New search string
        if find_str != self.find_str:
            self.find_str = find_str
            self.found_titem_list = self.text_to_titem.find(self.find_str)
            self.found_idx = 0
        
        item_num = len(self.found_titem_list)
        if item_num == 0: # Handle if nothing culd be found
            #TODO: A message may be sent to the user
            pass
        else:
            self.tree_widget.setCurrentItem(self.found_titem_list[self.found_idx])
            self.found_idx = (self.found_idx + 1) % item_num

    def recurse_jdata(self, jdata, tree_widget):

        if isinstance(jdata, dict):
            for key, val in jdata.items():
                self.tree_add_row(key, val, tree_widget)
        elif isinstance(jdata, list):
            for i, val in enumerate(jdata):
                key = str(i)
                self.tree_add_row(key, val, tree_widget)
        else:
            print("The data that you are trying to see is not structured in the correct way!")

    def tree_add_row(self, key, val, tree_widget):

        text_list = []

        if isinstance(val, dict) or isinstance(val, list):
            text_list.append(key)
            row_item = QtWidgets.QTreeWidgetItem([key])
            self.recurse_jdata(val, row_item)
        else:
            text_list.append(key)
            text_list.append(str(val))
            row_item = QtWidgets.QTreeWidgetItem([key, str(val)])

        tree_widget.addChild(row_item)
        self.text_to_titem.append(text_list, row_item)


class JsonViewer(QtWidgets.QMainWindow):

    def __init__(self, fpath):
        super(JsonViewer, self).__init__()

        json_view = JsonView(fpath, "teste")

        self.setCentralWidget(json_view)
        self.setWindowTitle("JSON Viewer")
        #Resize window
        self.show()

    def keyPressEvent(self, e):
        if e.key() == QtCore.Qt.Key_Escape:
            self.close()


if "__main__" == __name__:
    qt_app = QtWidgets.QApplication(sys.argv)
    fpath=r"D:\Documentos\OneDrive\Renan\Engenharia Civil\UMinho\01-REV@CONSTRUCTION\bSDD_API\Python\qtPracticing\json-viewer-master\sample.json"
    json_viewer = JsonViewer(fpath)
    sys.exit(qt_app.exec_())
