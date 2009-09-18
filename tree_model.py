# -*- coding: utf-8 -*-
# Created By: Virgil Dupras
# Created On: 2009-09-14
# $Id$
# Copyright 2009 Hardcoded Software (http://www.hardcoded.net)
# 
# This software is licensed under the "BSD" License as described in the "LICENSE" file, 
# which should be included with this package. The terms are also available at 
# http://www.hardcoded.net/licenses/bsd_license

from PyQt4.QtCore import Qt, QAbstractItemModel, QModelIndex

class NodeContainer(object):
    def __init__(self):
        self._subnodes = None
        self._ref2node = {}
    
    def _createNode(self, ref, row):
        # This returns a TreeNode instance from ref
        raise NotImplementedError()
    
    def _getChildren(self):
        # This returns a list of ref instances, not TreeNode instances
        raise NotImplementedError()
    
    @property
    def subnodes(self):
        if self._subnodes is None:
            children = self._getChildren()
            self._subnodes = []
            for index, child in enumerate(children):
                if child in self._ref2node:
                    node = self._ref2node[child]
                    node.row = index
                else:
                    node = self._createNode(child, index)
                    self._ref2node[child] = node
                self._subnodes.append(node)
        return self._subnodes
    

class TreeNode(NodeContainer):
    def __init__(self, model, parent, row):
        NodeContainer.__init__(self)
        self.model = model
        self.parent = parent
        self.row = row
    
    @property
    def index(self):
        return self.model.createIndex(self.row, 0, self)
    

class TreeModel(QAbstractItemModel, NodeContainer):
    def __init__(self):
        QAbstractItemModel.__init__(self)
        NodeContainer.__init__(self)
    
    def index(self, row, column, parent):
        if not self.subnodes:
            return QModelIndex()
        node = parent.internalPointer() if parent.isValid() else self
        return self.createIndex(row, column, node.subnodes[row])
    
    def parent(self, index):
        if not index.isValid():
            return QModelIndex()
        node = index.internalPointer()
        if node.parent is None:
            return QModelIndex()
        else:
            return self.createIndex(node.parent.row, 0, node.parent)
    
    def reset(self):
        self._subnodes = None
        self._ref2node = {}
        QAbstractItemModel.reset(self)
    
    def rowCount(self, parent):
        node = parent.internalPointer() if parent.isValid() else self
        return len(node.subnodes)
    
