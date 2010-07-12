# Created By: Virgil Dupras
# Created On: 2009-05-09
# Copyright 2010 Hardcoded Software (http://www.hardcoded.net)
# 
# This software is licensed under the "BSD" License as described in the "LICENSE" file, 
# which should be included with this package. The terms are also available at 
# http://www.hardcoded.net/licenses/bsd_license

from __future__ import unicode_literals

from PyQt4.QtCore import SIGNAL, Qt, QUrl, QCoreApplication
from PyQt4.QtGui import QDialog, QMessageBox, QDesktopServices

from hscommon.reg import InvalidCodeError

from .ui.reg_submit_dialog_ui import Ui_RegSubmitDialog

class RegSubmitDialog(QDialog, Ui_RegSubmitDialog):
    def __init__(self, parent, validate_func):
        flags = Qt.CustomizeWindowHint | Qt.WindowTitleHint | Qt.WindowSystemMenuHint
        QDialog.__init__(self, parent, flags)
        self._setupUi()
        self.validate_func = validate_func
        
        self.connect(self.submitButton, SIGNAL('clicked()'), self.submitClicked)
        self.connect(self.purchaseButton, SIGNAL('clicked()'), self.purchaseClicked)
    
    def _setupUi(self):
        self.setupUi(self)
        # Stuff that can't be setup in the Designer
        appname = unicode(QCoreApplication.instance().applicationName())
        prompt = unicode(self.promptLabel.text())
        prompt = prompt.replace('$appname', appname)
        self.promptLabel.setText(prompt)
    
    #--- Events
    def purchaseClicked(self):
        url = QUrl('http://www.hardcoded.net/purchase.htm')
        QDesktopServices.openUrl(url)
    
    def submitClicked(self):
        code = unicode(self.codeEdit.text())
        email = unicode(self.emailEdit.text())
        title = "Registration"
        try:
            self.validate_func(code, email)
            msg = "This code is valid. Thanks!"
            QMessageBox.information(self, title, msg)
            self.accept()
        except InvalidCodeError as e:
            msg = unicode(e)
            QMessageBox.warning(self, title, msg)
    
