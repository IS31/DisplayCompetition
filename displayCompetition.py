import os

class DisplayCompetition(object):
    submissionsDir = 'submissions'

    groups2Bots = {}
    
    def __init__(self):
        self.initGroups2Bots()

    def initGroups2Bots(self):
        for d in os.listdir(self.submissionsDir):
            f = open(self.submissionsDir + '/' + d + '/bot.txt', 'r')
            self.groups2Bots[d] = f.readline()
        
dc = DisplayCompetition()
