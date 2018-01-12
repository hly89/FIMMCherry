import sys
from PyQt4 import QtCore, QtGui

class LineEdit(QtGui.QLineEdit):
    def __init__(self, parent=None):
        super(LineEdit, self).__init__(parent)

        self.setFocusPolicy(QtCore.Qt.StrongFocus)

        self.completer = QtGui.QCompleter(self)

        self.completer.setCompletionMode(QtGui.QCompleter.UnfilteredPopupCompletion)
        self.pFilterModel = QtGui.QSortFilterProxyModel(self)

        self.pFilterModel.setFilterCaseSensitivity(QtCore.Qt.CaseInsensitive)
        self.completer.setPopup(self.view())
        self.setCompleter(self.completer)

        self.textEdited[unicode].connect(self.pFilterModel.setFilterFixedString)

        self.setModelColumn(0)

    def setModel(self, model):
        self.pFilterModel.setSourceModel(model)
        self.completer.setModel(self.pFilterModel)

    def setModelColumn( self, column ):
        self.completer.setCompletionColumn(column)
        self.pFilterModel.setFilterKeyColumn(column)

    def view(self):
        return self.completer.popup()

    def index( self ):
        return self.currentIndex()



