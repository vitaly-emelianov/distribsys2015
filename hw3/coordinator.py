from view import View


class Coordinator:
    """Coordinator server class."""

    def __init__(self, deadPings=10):
        self.deadPings = deadPings
        self.times = dict()
        self.freeServers = set()
        self.garbageServers = set()
        self.view = View()
        self.masterAcked = False
        self.viewChanged = False

    def ping(self, number, name):
        self.times[name] = self.deadPings
        if name not in {self.view.master, self.view.backup}:
            self.freeServers.add(name)
        if self.view.master == None:
            self.changeMaster()
        if name == self.view.master:
            if number == 0:
                self.masterAcked = True
                self.freeServers.add(self.view.master)
                self.changeMaster()
            if number == self.view.number:
                self.masterAcked = True
        if name == self.view.backup and number == 0 and self.masterAcked:
            self.viewChanged = True
        if self.times[self.view.master] == 0 and self.masterAcked:
            self.garbageServers.add(self.view.master)
            self.changeMaster()
        if self.view.backup == None:
            self.changeBackup()
        if self.view.backup != None and self.times[self.view.backup] == 0:
            self.garbageServers.add(self.view.backup)
            self.changeBackup()

        if self.viewChanged:
            self.view.number += 1
            self.masterAcked = False
            self.viewChanged = False
            for server in self.garbageServers:
                del self.times[server]
            self.garbageServers = set()
        return self.view

    def changeMaster(self):
        if self.view.backup == None and self.freeServers:
            self.view.master = self.freeServers.pop()
            self.viewChanged = True
        elif self.view.backup != None:
            self.view.master = self.view.backup
            self.viewChanged = True
            self.changeBackup()

    def changeBackup(self):
        if self.freeServers:
            self.view.backup = self.freeServers.pop()
            self.viewChanged = True
        else:
            if self.view.backup != None:
                self.view.backup = None
                self.viewChanged = True

    def master(self):
        return self.view.master

    def tick(self):
        for name in self.times.keys():
            if self.times[name] > 0:
                self.times[name] -= 1
            if name in self.freeServers and self.times[name] == 0:
                self.freeServers.remove(name)
                del self.times[name]
