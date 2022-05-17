#Importing things required by bSDD API
#import mybSDDV5_Main
from bSDDV5_Classes import TClassification, TCountry, TDomain, TPostman
import requests
import msal
import sys

#Importing things required by the GUI
#from Old.mainwindowOld2 import Ui_MainWindow
from mainwindow import Ui_MainWindow
from PyQt5 import QtWidgets, QtGui
from PyQt5 import QtCore

#Importing things required by JSON Tree Viewer GUI
import json
from collections import OrderedDict
import jsonTreeViewer

#Importing things required for saving xml files
from dict2xml import dict2xml

#Global object used to handle all API calls
bsdd = TPostman() 

#Class that defines the main window of the GUI
class mainWindow(QtWidgets.QMainWindow, Ui_MainWindow):

    def __init__(self, parent=None):
        super(mainWindow, self).__init__(parent=parent)
        self.setupUi(self)
        self.currentResponse=["","",""]

        #Initiate custom widgets not present in the .ui file template
        #self.renderCheckableComboBoxInTab(self.OpenSearch_CheckComboBoxHolder_widget, ["teste","teste"])
        self.renderJSONTreeViewerInGetDomainTab(dict())
        self.renderJSONTreeViewerInOpenSearchTab(dict())
        self.renderCheckableComboBoxInOpenSearchTab(["No information retrieved yet"])
        self.renderCheckableComboBoxInOpenSearchClassificationTab(["No information retrieved yet"]) 

        # "Connect to bSDD" panel
        self.connect_pushButton.clicked.connect(self.connectToBSDD)

        # "Check bSDD general information" panel
        self.checkLanguage_pushButton.clicked.connect(lambda: self.displayDataInTreeViewer(bsdd.Languages, "Showing available Languages in bSDD"))
        self.checkDomains_pushButton.clicked.connect(lambda: self.displayDataInTreeViewer(bsdd.Domains, "Showing available Domains in bSDD"))
        self.checkCountries_pushButton.clicked.connect(lambda: self.displayDataInTreeViewer(bsdd.Countries, "Showing available Countries in bSDD"))
        self.checkRefDocs_pushButton.clicked.connect(lambda: self.displayDataInTreeViewer(bsdd.ReferenceDocuments, "Showing available Reference Documents in bSDD"))
        self.checkUnits_pushButton.clicked.connect(lambda: self.displayDataInTreeViewer(bsdd.Units, "Showing available Units in bSDD"))

        # "Get a Domain" tab panel
        self.GetDomain_Search_pushButton.clicked.connect(lambda: self.searchButtonDomainTab())
        self.GetDomain_OpenInNewWindow_pushButton.clicked.connect(lambda: self.displayDataInTreeViewer(self.currentResponse[1], "Get a Domain query results"))
        self.GetDomain_SaveTo_pushButton.clicked.connect(lambda: self.saveDataDialog(self.currentResponse[1]))

        # "Open search in all bSDD"
        self.OpenSearch_Search_pushButton.clicked.connect(lambda: self.searchButtonOpenSearchTab())
    
    #Signal that is called when Search button on "Get a Domain" panel is clicked: it performs the querry specified
    def searchButtonDomainTab(self):
        if str(self.GetDomain_DomainURI_comboBox.currentText())=="" or str(self.GetDomain_DataStructure_comboBox.currentText())=="":
            #There are no inputs in the holders, so do nothing
            pass
        else:
            #Perform the search
            self.currentResponse=bsdd.get_Domain_Classes_Tree(self.GetDomain_DomainURI_comboBox.currentText(), str(self.GetDomain_DataStructure_comboBox.currentText()), False)
            #result=bsdd.GetDomainFromURI(self.GetDomain_DomainURI_comboBox.currentText())
            if self.currentResponse[2]==200:
                #200 is the HTML code for a successful query
                self.GetDomain_QuerryStatusResult_label.setText("Status code "+str(self.currentResponse[2])+": Success")
                self.GetDomain_QuerryStatusResult_label.setStyleSheet("background-color: #8CF585")
                self.renderJSONTreeViewerInGetDomainTab(self.currentResponse[1])
            else:
                self.GetDomain_QuerryStatusResult_label.setText("Status code unknown: Failure")
                self.GetDomain_QuerryStatusResult_label.setStyleSheet("background-color: #DE8C8C")
                self.renderJSONTreeViewerInGetDomainTab(dict())

    #Signal that is called when Search button on "Open search in all bSDD" panel is clicked: it performs the querry specified
    def searchButtonOpenSearchTab(self):
        if str(self.OpenSearch_SearchTextString_lineEdit.text())=="":
            #There are no inputs in the search string holder, so do nothing
            #TODO: implement an error message
            pass
        else:
            #Perform the search
            #get_Open_Search(self, _SearchText, _TypeFilter, _FilteringDomainUris, _SaveResult)
            filteringDomainUris=self.sub_widgetCheckableComboBoxInOpenSearchTab.currentData()
            self.currentResponse=bsdd.get_TextOpen_Search(str(self.OpenSearch_SearchTextString_lineEdit.text()), str(self.OpenSearch_Filter_comboBox.currentText()), filteringDomainUris, False)
            #result=bsdd.GetDomainFromURI(self.GetDomain_DomainURI_comboBox.currentText())
            if self.currentResponse[2]==200:
                #200 is the HTML code for a successful query
                self.GetDomain_QuerryStatusResult_label.setText("Status code "+str(self.currentResponse[2])+": Success")
                self.GetDomain_QuerryStatusResult_label.setStyleSheet("background-color: #8CF585")
                self.renderJSONTreeViewerInOpenSearchTab(self.currentResponse[1])
            else:
                self.GetDomain_QuerryStatusResult_label.setText("Status code unknown: Failure")
                self.GetDomain_QuerryStatusResult_label.setStyleSheet("background-color: #DE8C8C")
                self.renderJSONTreeViewerInOpenSearchTab(dict())

    #Render the JSON Tree Viewer in the Get Domain tab
    def renderJSONTreeViewerInGetDomainTab(self, dataToBeDisplayed):
        try:
            self.JSONlayoutGetDomain.removeWidget(self.sub_widgetJSONTreeViewerInGetDomainTab)
            #self.sub_widget.deleteLater()
            #self.sub_widget = None
            self.sub_widgetJSONTreeViewerInGetDomainTab = jsonTreeViewer.JsonView(dataToBeDisplayed, "",self.GetDomain_JSONViewerHolder_widget)
            self.JSONlayoutGetDomain.addWidget(self.sub_widgetJSONTreeViewerInGetDomainTab)
            self.sub_widgetJSONTreeViewerInGetDomainTab.show()
        except:
            self.JSONlayoutGetDomain = QtWidgets.QHBoxLayout(self.GetDomain_JSONViewerHolder_widget)
            self.JSONlayoutGetDomain.setContentsMargins(0, 0, 0, 0)
            self.sub_widgetJSONTreeViewerInGetDomainTab = jsonTreeViewer.JsonView(dataToBeDisplayed, "",self.GetDomain_JSONViewerHolder_widget)
            self.JSONlayoutGetDomain.addWidget(self.sub_widgetJSONTreeViewerInGetDomainTab)

    #Render the JSON Tree Viewer in the Get Domain tab
    def renderJSONTreeViewerInOpenSearchTab(self, dataToBeDisplayed):
        try:
            self.JSONlayoutOpenSearch.removeWidget(self.sub_widgetJSONTreeViewerInOpenSearchTab)
            #self.sub_widget.deleteLater()
            #self.sub_widget = None
            self.sub_widgetJSONTreeViewerInOpenSearchTab = jsonTreeViewer.JsonView(dataToBeDisplayed, "",self.OpenSearch_JSONViewerHolder_widget)
            self.JSONlayoutOpenSearch.addWidget(self.sub_widgetJSONTreeViewerInOpenSearchTab)
            self.sub_widgetJSONTreeViewerInOpenSearchTab.show()
        except:
            self.JSONlayoutOpenSearch = QtWidgets.QHBoxLayout(self.OpenSearch_JSONViewerHolder_widget)
            self.JSONlayoutOpenSearch.setContentsMargins(0, 0, 0, 0)
            self.sub_widgetJSONTreeViewerInOpenSearchTab = jsonTreeViewer.JsonView(dataToBeDisplayed, "",self.OpenSearch_JSONViewerHolder_widget)
            self.JSONlayoutOpenSearch.addWidget(self.sub_widgetJSONTreeViewerInOpenSearchTab)

    #Render the Checkable ComboBox in the OpenSearch tab
    def renderCheckableComboBoxInOpenSearchTab(self, dataToBeDisplayed):
        #dataToBeDisplayed: 1D list
        try:
            self.checkableOpenSearchlayout.removeWidget(self.sub_widgetCheckableComboBoxInOpenSearchTab)
            #self.sub_widget.deleteLater()
            #self.sub_widget = None
            self.sub_widgetCheckableComboBoxInOpenSearchTab = CheckableComboBox(self.OpenSearch_CheckComboBoxHolder_widget)
            self.checkableOpenSearchlayout.addWidget(self.sub_widgetCheckableComboBoxInOpenSearchTab)
            self.sub_widgetCheckableComboBoxInOpenSearchTab.addItems(dataToBeDisplayed)
            self.sub_widgetCheckableComboBoxInOpenSearchTab.show()
        except:
            self.checkableOpenSearchlayout = QtWidgets.QHBoxLayout(self.OpenSearch_CheckComboBoxHolder_widget)
            self.checkableOpenSearchlayout.setContentsMargins(0, 0, 0, 0)
            self.sub_widgetCheckableComboBoxInOpenSearchTab = CheckableComboBox(self.OpenSearch_CheckComboBoxHolder_widget)
            self.sub_widgetCheckableComboBoxInOpenSearchTab.addItems(dataToBeDisplayed)
            self.checkableOpenSearchlayout.addWidget(self.sub_widgetCheckableComboBoxInOpenSearchTab)
            self.sub_widgetCheckableComboBoxInOpenSearchTab.show()

    #Render the Checkable ComboBox in the OpenSearchClassification tab
    def renderCheckableComboBoxInOpenSearchClassificationTab(self, dataToBeDisplayed):
        #dataToBeDisplayed: 1D list
        try:
            self.checkableOpenSearchClassificationslayout.removeWidget(self.sub_widgetCheckableComboBoxInOpenSearchClassificationsTab)
            #self.sub_widget.deleteLater()
            #self.sub_widget = None
            self.sub_widgetCheckableComboBoxInOpenSearchClassificationsTab = CheckableComboBox(self.OpenSearchClassifications_CheckComboBoxHolder_widget)
            self.checkableOpenSearchClassificationslayout.addWidget(self.sub_widgetCheckableComboBoxInOpenSearchClassificationsTab)
            self.sub_widgetCheckableComboBoxInOpenSearchClassificationsTab.addItems(dataToBeDisplayed)
            self.sub_widgetCheckableComboBoxInOpenSearchClassificationsTab.show()
        except:
            self.checkableOpenSearchClassificationslayout = QtWidgets.QHBoxLayout(self.OpenSearchClassifications_CheckComboBoxHolder_widget)
            self.checkableOpenSearchClassificationslayout.setContentsMargins(0, 0, 0, 0)
            self.sub_widgetCheckableComboBoxInOpenSearchClassificationsTab = CheckableComboBox(self.OpenSearchClassifications_CheckComboBoxHolder_widget)
            self.sub_widgetCheckableComboBoxInOpenSearchClassificationsTab.addItems(dataToBeDisplayed)
            self.checkableOpenSearchClassificationslayout.addWidget(self.sub_widgetCheckableComboBoxInOpenSearchClassificationsTab)
            self.sub_widgetCheckableComboBoxInOpenSearchClassificationsTab.show()

    #Signal that is called when Connect Button is clicked: it allows login to bSDD server, so the RESTful API can be used
    def connectToBSDD(self):
        bsdd.Authorize() #login to bsdd api
        #TODO: If success (implement this verification), get all general information
        self.getGeneralInformation()
        #TODO: If success connection, unlock all search buttons. They must be locked at first

        #Populate all comboBoxes and fields with relevant information
        #GetDomain tab
        self.GetDomain_DomainURI_comboBox.addItems([item.namespaceUri for item in bsdd.Domains])
        self.GetDomain_DataStructure_comboBox.addItems(["true","false"])

        #OpenSearch tab
        self.renderCheckableComboBoxInOpenSearchTab([item.namespaceUri for item in bsdd.Domains])  
        self.OpenSearch_Filter_comboBox.addItems(["All","Properties","Classifications"])

        #GetClasificationDetails tab
        self.GetClassificationDetails_DomainURI_comboBox.addItems([item.namespaceUri for item in bsdd.Domains])
        self.GetClassificationDetails_DataStructure_comboBox.setMaxVisibleItems(5)
        self.GetClassificationDetails_DataStructure_comboBox.setMaxCount(len(bsdd.Languages))
        #TODO: Make fields screen adjustable, so the full item.name+"/"+item.isoCode can be shown here
        #self.GetClassificationDetails_DataStructure_comboBox.addItems([item.name+"/"+item.isoCode for item in bsdd.Languages])
        self.GetClassificationDetails_DataStructure_comboBox.addItems([item.isoCode for item in bsdd.Languages])

        #GetListMaterialDomain tab
        self.GetListMaterialDomain_DomainURI_comboBox.addItems([item.namespaceUri for item in bsdd.Domains])
        self.GetListMaterialDomain_DataStructure_comboBox.setMaxVisibleItems(5)
        self.GetListMaterialDomain_DataStructure_comboBox.setMaxCount(len(bsdd.Languages))
        #TODO: Make fields screen adjustable, so the full item.name+"/"+item.isoCode can be shown here
        #self.GetListMaterialDomain_DataStructure_comboBox.addItems([item.name+"/"+item.isoCode for item in bsdd.Languages])
        self.GetListMaterialDomain_DataStructure_comboBox.addItems([item.isoCode for item in bsdd.Languages])

        #GetMaterialDetails tab
        self.GetMaterialDetails_DataStructure_comboBox.setMaxVisibleItems(5)
        self.GetMaterialDetails_DataStructure_comboBox.setMaxCount(len(bsdd.Languages))
        #TODO: Make fields screen adjustable, so the full item.name+"/"+item.isoCode can be shown here
        #self.GetListMaterialDomain_DataStructure_comboBox.addItems([item.name+"/"+item.isoCode for item in bsdd.Languages])
        self.GetMaterialDetails_DataStructure_comboBox.addItems([item.isoCode for item in bsdd.Languages])
        self.GetMaterialDetails_DataStructure_comboBox_2.addItems(["true", "false"])

        #GetPropertyDetails tab
        self.GetPropertyDetails_DataStructure_comboBox.setMaxVisibleItems(5)
        self.GetPropertyDetails_DataStructure_comboBox.setMaxCount(len(bsdd.Languages))
        #TODO: Make fields screen adjustable, so the full item.name+"/"+item.isoCode can be shown here
        #self.GetListMaterialDomain_DataStructure_comboBox.addItems([item.name+"/"+item.isoCode for item in bsdd.Languages])
        self.GetPropertyDetails_DataStructure_comboBox.addItems([item.isoCode for item in bsdd.Languages])

        #GetPropertyValueDetails tab
        self.GetPropertyValueDetails_DataStructure_comboBox.setMaxVisibleItems(5)
        self.GetPropertyValueDetails_DataStructure_comboBox.setMaxCount(len(bsdd.Languages))
        #TODO: Make fields screen adjustable, so the full item.name+"/"+item.isoCode can be shown here
        #self.GetListMaterialDomain_DataStructure_comboBox.addItems([item.name+"/"+item.isoCode for item in bsdd.Languages])
        self.GetPropertyValueDetails_DataStructure_comboBox.addItems([item.isoCode for item in bsdd.Languages])

        #OpenSearchClassifications tab
        self.OpenSearchClassifications_Filter_comboBox.setMaxVisibleItems(5)
        self.OpenSearchClassifications_Filter_comboBox.setMaxCount(len(bsdd.Languages))
        #TODO: Make fields screen adjustable, so the full item.name+"/"+item.isoCode can be shown here
        #self.GetListMaterialDomain_DataStructure_comboBox.addItems([item.name+"/"+item.isoCode for item in bsdd.Languages])
        self.OpenSearchClassifications_Filter_comboBox.addItems([item.isoCode for item in bsdd.Languages])
        self.GetListMaterialDomain_DomainURI_comboBox.addItems([item.namespaceUri for item in bsdd.Domains])
        self.renderCheckableComboBoxInOpenSearchClassificationTab([item.namespaceUri for item in bsdd.Domains]) 






    #Signal that is called to get general information available on bSDD API
    def getGeneralInformation(self):
        bsdd.get_Countries(False)
        bsdd.get_Domains(False)
        bsdd.get_Languages(False)
        bsdd.get_ReferenceDocuments(False)
        bsdd.get_Units(False)
        print("Cheguei aqui")

    #Signal that is called to show a new window with the JSON Viewer Window
    def displayDataInTreeViewer(self, dataToBeViewed, dataDescriptionLabel):
        self.treeWin = JSONViewer(dataToBeViewed, dataDescriptionLabel)
        #Set initial JSON Tree Viewer window size
        wInitial=800
        hInitial=600
        self.treeWin.resize(wInitial,hInitial)
        self.treeWin.show()

    #Signal that is called when "Save to..." button is clicked
    def saveDataDialog(self, dataToBeSaved):
        selectSavePathDialog = saveDialog()
        saveFilePath = selectSavePathDialog.getSaveFilePath()
        if (not(saveFilePath=="")):
            #If the saveFilePath variable contains any valid path, proceed to save
            saveFile = open(saveFilePath, "w")
            saveFile = json.dump(dataToBeSaved, saveFile, indent = 1)

class JSONViewer(QtWidgets.QMainWindow):
    def __init__(self, dataToBeShown, titleName, parent=None):
        super(JSONViewer, self).__init__() # Call the inherited classes __init__ method

        if str(type(dataToBeShown))=="<class 'list'>":
            #Check if dataToBeShown is a list. It will be a list if we are showing the results from getGeneralInformation method, which are retrieved as list of classes with attributes, so they have to be unpacked as lists to work with the JSON viewer.
            #TODO: perhaps we could harmonize how the data is store to avoid separate treatments: everything could be a dictionary. Depends on the use of the app, though.
            visualization=self.unpackClassAttributesForVisualization(dataToBeShown)
        else:
            #The other cases in which we are going to show data in a new window of JSONViewer will always pass data as dict() type, so unpacking is not needed
            visualization=dataToBeShown
        json_view = jsonTreeViewer.JsonView(visualization, titleName)
        self.setCentralWidget(json_view)
        self.setWindowTitle("JSON Viewer")

    def unpackClassAttributesForVisualization(self, classToBeUnpacked):
        unpackedList=[]
        for item in classToBeUnpacked:
            unpackedList.append(vars(item))
        return unpackedList

    def viewJSONPackage (self, dataToBeShown):
        visualization=self.unpackClassAttributesForVisualization(dataToBeShown)
        self.json_viewer = jsonTreeViewer.JsonViewer(visualization)
        self.json_viewer.show()
class saveDialog(QtWidgets.QWidget):
    #Save file dialog taken from https://pythonspot.com/pyqt5-file-dialog/
    def __init__(self):
        super().__init__()
        self.title = 'PyQt5 file dialogs - pythonspot.com'
        self.left = 10
        self.top = 10
        self.width = 320
        self.height = 240
        self.selectedFilePath = self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        options = QtWidgets.QFileDialog.Options()
        #options |= QtWidgets.QFileDialog.DontUseNativeDialog
        selectedFilePath, _ = QtWidgets.QFileDialog.getSaveFileName(self,"QFileDialog.getSaveFileName()","","JSON Files (*.json)", options=options)
        return selectedFilePath   
    def getSaveFilePath(self):
        return self.selectedFilePath
class CheckableComboBox(QtWidgets.QComboBox):
    #Obtained from https://gis.stackexchange.com/questions/350148/qcombobox-multiple-selection-pyqt5
    # Subclass Delegate to increase item height
    class Delegate(QtWidgets.QStyledItemDelegate):
        def sizeHint(self, option, index):
            size = super().sizeHint(option, index)
            size.setHeight(20)
            return size

    def __init__(self, parent=None):
        super(CheckableComboBox, self).__init__(parent=None)

        # Make the combo editable to set a custom text, but readonly
        self.setEditable(True)
        self.lineEdit().setReadOnly(True)
        # Make the lineedit the same color as QPushButton
        palette = QtWidgets.qApp.palette()
        palette.setBrush(QtGui.QPalette.Base, palette.button())
        self.lineEdit().setPalette(palette)

        # Use custom delegate
        self.setItemDelegate(CheckableComboBox.Delegate())

        # Update the text when an item is toggled
        self.model().dataChanged.connect(self.updateText)

        # Hide and show popup when clicking the line edit
        self.lineEdit().installEventFilter(self)
        self.closeOnLineEditClick = False

        # Prevent popup from closing when clicking on an item
        self.view().viewport().installEventFilter(self)

    def resizeEvent(self, event):
        # Recompute text to elide as needed
        self.updateText()
        super().resizeEvent(event)

    def eventFilter(self, object, event):

        if object == self.lineEdit():
            if event.type() == QtCore.QEvent.MouseButtonRelease:
                if self.closeOnLineEditClick:
                    self.hidePopup()
                else:
                    self.showPopup()
                return True
            return False

        if object == self.view().viewport():
            if event.type() == QtCore.QEvent.MouseButtonRelease:
                index = self.view().indexAt(event.pos())
                item = self.model().item(index.row())

                if item.checkState() == QtCore.Qt.Checked:
                    item.setCheckState(QtCore.Qt.Unchecked)
                else:
                    item.setCheckState(QtCore.Qt.Checked)
                return True
        return False

    def showPopup(self):
        super().showPopup()
        # When the popup is displayed, a click on the lineedit should close it
        self.closeOnLineEditClick = True

    def hidePopup(self):
        super().hidePopup()
        # Used to prevent immediate reopening when clicking on the lineEdit
        self.startTimer(100)
        # Refresh the display text when closing
        self.updateText()

    def timerEvent(self, event):
        # After timeout, kill timer, and reenable click on line edit
        self.killTimer(event.timerId())
        self.closeOnLineEditClick = False

    def updateText(self):
        texts = []
        for i in range(self.model().rowCount()):
            if self.model().item(i).checkState() == QtCore.Qt.Checked:
                texts.append(self.model().item(i).text())
        text = ", ".join(texts)

        # Compute elided text (with "...")
        metrics = QtGui.QFontMetrics(self.lineEdit().font())
        elidedText = metrics.elidedText(text, QtCore.Qt.ElideRight, self.lineEdit().width())
        self.lineEdit().setText(elidedText)

    def addItem(self, text, data=None):
        item = QtGui.QStandardItem()
        item.setText(text)
        if data is None:
            item.setData(text)
        else:
            item.setData(data)
        item.setFlags(QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsUserCheckable)
        item.setData(QtCore.Qt.Unchecked, QtCore.Qt.CheckStateRole)
        self.model().appendRow(item)

    def addItems(self, texts, datalist=None):
        for i, text in enumerate(texts):
            try:
                data = datalist[i]
            except (TypeError, IndexError):
                data = None
            self.addItem(text, data)

    def currentData(self):
        # Return the list of selected items data
        res = []
        for i in range(self.model().rowCount()):
            if self.model().item(i).checkState() == QtCore.Qt.Checked:
                res.append(self.model().item(i).data())
        return res

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    mainWin = mainWindow()
    mainWin.show()
    sys.exit(app.exec_())