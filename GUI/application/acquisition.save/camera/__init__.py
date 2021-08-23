#!/usr/bin/env python3

import PySpin as spin


class NodeMap:

    def __init__(self, nodemap):
        self.nodemap = nodemap

    def __getitem__(self, k):
        node = self.nodemap.GetNode(k)
        t = node.GetPrincipalInterfaceType()
        return {spin.intfIString: NodeEnum,
                spin.intfIInteger: NodeInt,
                spin.intfIFloat: NodeFloat,
                spin.intfIBoolean: NodeBool,
                spin.intfIEnumeration: NodeEnum,
                spin.intfICommand: NodeCmd
                }[t](node)


class Node:
    pass


class NodeEnum(Node):

    def __init__(self, node):
        self.node = spin.CEnumerationPtr(node)

    @property
    def content(self):
        return {e.GetName() for e in self.node.GetEntries()}

    @property
    def value(self):
        return self.node.GetCurrentEntry().GetName()

    @value.setter
    def value(self, v):
        entry = self.node.GetEntryByName(v)
        if entry is None:
            raise KeyError(v)
        v = entry.GetValue()
        self.node.SetIntValue(v)


class NodeCmd(Node):

    def __init__(self, node):
        self.node = spin.CCommandPtr(node)

    def exec(self):
        self.node.Execute()


class NodeFloat(Node):

    def __init__(self, node):
        self.node = spin.CFloatPtr(node)

    @property
    def min(self):
        return self.node.GetMin()

    @property
    def max(self):
        return self.node.GetMax()

    @property
    def value(self):
        return self.node.GetValue()

    @value.setter
    def value(self, v):
        if not self.min <= v <= self.max:
            raise ValueError(f'{v} out of bounds ({self.min} to {self.max})')
        self.node.SetValue(v)


class NodeBool(Node):

    def __init__(self, node):
        self.node = spin.CBooleanPtr(node)

    @property
    def value(self):
        return self.node.GetValue()

    @value.setter
    def value(self, v):
        self.node.SetValue(bool(v))


class NodeInt(Node):

    def __init__(self, node):
        self.node = spin.CIntegerPtr(node)

    @property
    def min(self):
        return self.node.GetMin()

    @property
    def max(self):
        return self.node.GetMax()

    @property
    def value(self):
        return self.node.GetValue()

    @value.setter
    def value(self, v):
        if not self.min <= v <= self.max:
            raise ValueError(f'{v} out of bounds ({self.min} to {self.max})')
        self.node.SetValue(v)


class NodeStr(Node):

    def __init__(self, node):
        self.node = spin.CEnumerationPtr(node)

    @property
    def value(self):
        return self.node.GetValue()

    @value.setter
    def value(self, v):
        self.node.SetValue(v)


class Camera:

    def __init__(self, index=0):
        self.sys = spin.System.GetInstance()
        self.camera_list = self.sys.GetCameras()
        self.camera = self.camera_list.GetByIndex(index)
        self.camera.Init()
        self.nodemap = NodeMap(self.camera.GetNodeMap())
        self.s_nodemap = NodeMap(self.camera.GetTLStreamNodeMap())
        self.d_nodemap = NodeMap(self.camera.GetTLDeviceNodeMap)

    def __getitem__(self, v):
        try:
            return self.nodemap[v]
        except AttributeError:
            try:
                return self.s_nodemap[v]
            except AttributeError:
                return self.d_nodemap[v]

    def BeginAcquisition(self):
        self.camera.BeginAcquisition()

    def EndAcquisition(self):
        self.camera.EndAcquisition()

    def Init(self):
        self.camera.Init()

    def DeInit(self):
        self.camera.DeInit()

    def Delete(self):
        del self.camera
        del self.nodemap
        del self.s_nodemap
        del self.d_nodemap

    def GetNextImage(self):
        return self.camera.GetNextImage()

    def Clear_cam_list(self):
        self.camera_list.Clear()

    def ReleaseInstance(self):
        self.sys.ReleaseInstance()

    def __del__(self):
        self.DeInit()
        self.Clear_cam_list()
        self.Delete()
        self.ReleaseInstance()


#    def AcquisitionStatus(self):
#        return self.camera.AcquisitionStatus()


#    def __del__(self):
#        self.release()

#        self.camera.EndAcquisition()
#        self.camera.DeInit()
#        del self.camera
#        self.sys.ReleaseInstance()
