from ..Qt import QtCore, QtGui, QtWidgets


class CmdInput(QtWidgets.QLineEdit):
    
    sigExecuteCmd = QtCore.Signal(object)
    
    def __init__(self, parent):
        QtWidgets.QLineEdit.__init__(self, parent)
        self.ps1 = ">>> "
        self.ps2 = "... "
        self.history = [""]
        self.ptr = 0
        font = QtGui.QFont("monospace")
        font.setStyleHint(QtGui.QFont.StyleHint.TypeWriter, QtGui.QFont.StyleStrategy.PreferAntialias)
        self.setFont(font)
        self.setMultiline(False)
    
    def setMultiline(self, ml):
        if ml:
            self.setPlaceholderText(self.ps2)
        else:
            self.setPlaceholderText(self.ps1)

    def keyPressEvent(self, ev):
        if ev.key() == QtCore.Qt.Key.Key_Up:
            if self.ptr < len(self.history) - 1:
                self.setHistory(self.ptr+1)
                ev.accept()
                return
        elif ev.key() ==  QtCore.Qt.Key.Key_Down:
            if self.ptr > 0:
                self.setHistory(self.ptr-1)
                ev.accept()
                return
        elif ev.key() in (QtCore.Qt.Key.Key_Return, QtCore.Qt.Key.Key_Enter):
            self.execCmd()
        else:
            super().keyPressEvent(ev)
            self.history[0] = self.text()
        
    def execCmd(self):
        cmd = self.text()
        if len(self.history) == 1 or cmd != self.history[1]:
            self.history.insert(1, cmd)
        self.history[0] = ""
        self.setHistory(0)
        self.sigExecuteCmd.emit(cmd)
        
    def setHistory(self, num):
        self.ptr = num
        self.setText(self.history[self.ptr])
