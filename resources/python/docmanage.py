import rocket
import freeablo
import freeablo_input
from collections import namedtuple

class DocManager(object):

    def __init__(self):
        test = None
        try:
            test = manager
        except Exception:
            pass

        if test:
            raise Exception("DocManager is a singleton, access the one instance via docmanage.manager")

        context = rocket.contexts['default']

        self.guiWasClicked = False
        self.docs = {}
        self.paused = False
        self.pauseHiddenDocs = []
        self.pauseHandle = context.LoadDocument('resources/gui/pausemenu.rml')

    def showDoc(self, docpath):
        handle = self.docs[docpath]
        handle["doc"].Show()
        handle["visible"] = True

    def hideDoc(self, docpath):
        handle = self.docs[docpath]
        handle["doc"].Hide()
        handle["visible"] = False

    def toggleDoc(self, docpath):
        if self.docs[docpath]["visible"]:
            self.hideDoc(docpath)
        else:
            self.showDoc(docpath)

    def loadDoc(self, docpath):
        context = rocket.contexts['default']
        newHandle = {"doc": context.LoadDocument(docpath), "visible": False}
        self.docs[docpath] = newHandle

    def pause(self):
        for docpath in self.docs:
            handle = self.docs[docpath]
            if handle["visible"]:
                self.toggleDoc(docpath)
                self.pauseHiddenDocs.append(docpath)

        self.paused = True
        self.pauseHandle.Show()
        freeablo.pause()

    def unpause(self):
        self.pauseHandle.Hide()

        for docpath in self.pauseHiddenDocs:
            self.toggleDoc(docpath)

        self.pauseHiddenDocs = []

        self.paused = False
        freeablo.unpause()

    def togglePause(self):
        if self.paused:
            self.unpause()
        else:
            self.pause()

    def onKeyDown(self, event):
        if event.parameters['key_identifier'] == rocket.key_identifier.ESCAPE:
            self.togglePause()

    def bodyClicked(self):
        # librocket generates click events in reverse hierarchical order, so
        # if there is an element inside body and that is clicked, we get an event for
        # that first, then for body. We can use this to find when body is clicked
        # outside the inner element by tracking the inner elements clicked status,
        # as has been done here. When the background (ie, body) is clicked, we send
        # a signal to the engine that this click was not on the gui, so it is for
        # the engine to process. resources/gui/base.rml takes care of the case where
        # the click occurs outside the boundaries of any currently visible rml documents
        if not self.guiWasClicked:
            freeablo_input.baseClicked()

        self.guiWasClicked = False

    def guiClicked(self):
        self.guiWasClicked = True


def init():
    global manager
    manager = DocManager()

