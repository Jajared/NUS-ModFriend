import NUSBot as nus
import Error as e

class Student:
    def __init__(self, modlink, group, username, userID):
        self.modlink = modlink
        self.linkChanged = False
        self.actionQueue = []
        self.username = username
        self.userID = userID
        self.group = group
        self.classList = nus.getUserLessons(self.modlink)
        self.lessonSum = self.lessonSummary(nus.getUserLessons(modlink))
        self.registerLesson(self.lessonSum)
        self.group.add_user(self)

    def addAction(self, action):
        self.actionQueue.append(action)

    def getNextAction(self):
        if self.actionQueue:
            return self.actionQueue[0]
        else:
            raise e.InvalidActionError

    def completeAction(self):
        self.actionQueue.pop(0)

    def changeLink(self, newLink):
        self.modlink = newLink
        self.linkChanged = True
    
    def updateLessons(self):
        if self.linkChanged:
            self.lessonSum = self.lessonSummary(nus.getUserLessons(self.modlink))
        self.registerLesson(self.lessonSum)
        self.linkChanged = False

    def getStudentID(self):
        return self.userID

    def lessonSummary(self, result):
        lessonsLst = []
        for module in result:
            lessonsLst.extend(nus.getLessonTiming(module, result[module]))
        return lessonsLst
    
    def registerLesson(self, all_lessons):
        for lesson in all_lessons:
            lessonTime = nus.getLessonTime(lesson)
            day = nus.getLessonDay(lessonTime)
            if day in ["Saturday", 'Sunday']:
                continue
            start = nus.getStartTime(lessonTime)
            end = nus.getEndTime(lessonTime)
            self.group.allLessonsDayAndTime[day][0].append(start)
            self.group.allLessonsDayAndTime[day][1].append(end)