class Group:
    def __init__(self, group_id):
        self.group_id = group_id
        self.users = {}
        self.freeDayAndTime = {"Monday": [], "Tuesday": [], "Wednesday": [], "Thursday": [], "Friday": []}
        self.allLessonsDayAndTime = {"Monday": ([],[]), "Tuesday": ([],[]),
        "Wednesday": ([],[]), "Thursday": ([],[]), "Friday": ([],[])}
        
    #Accessor for group id
    def getGroupID(self):
        return self.group_id
    
    #Add new user to group
    def add_user(self, student):
        if student.getStudentID() not in self.users:
            self.users[student.getStudentID()] = student
            self.calculateFreeTime()

    #Calculate free time based on all lessons
    def calculateFreeTime(self):

        def getStartLst(lessonTime):
            return lessonTime[0]

        def getEndLst(lessonTime):
            return lessonTime[1]

        def calculateDayFreeTime(startTime, endTime):
            startTime.sort()
            endTime.sort()
            freeTimeResult = []
            firstLesson = min(startTime)
            lastLesson = max(endTime)

            #free time from start of day to first lesson
            if firstLesson > '0800':
                freeTimeResult.append(('0800', firstLesson))
            #free time from last lesson to end of day
            if lastLesson < '2000':
                freeTimeResult.append((lastLesson, '2000'))
                
            def isOutOfRangeBreak():
                return j == len(endTime) or i == len(startTime)
            
            i, j = 0, -1
            while True:

                j += 1
                if isOutOfRangeBreak():
                    break 

                while startTime[i] <= endTime[j]:
                    i += 1
                    if isOutOfRangeBreak():
                        break 

                while True:
                    j += 1
                    if isOutOfRangeBreak():
                        break 
                    if (endTime[j] > startTime[i]) and (endTime[j-1] != startTime[i]):
                        freeTimeResult.append((endTime[j-1], startTime[i]))
                    if endTime[j] >= startTime[i]:
                        break
                    
                if isOutOfRangeBreak():
                    break 

            return freeTimeResult

        for day in self.allLessonsDayAndTime:
            self.freeDayAndTime[day] = []
            start = getStartLst(self.allLessonsDayAndTime[day])
            end = getEndLst(self.allLessonsDayAndTime[day])
            self.freeDayAndTime[day] = calculateDayFreeTime(start, end)
            self.freeDayAndTime[day].sort(key=lambda x:x[0])

    #Recalculates group free time everytime a user updates his/her modlink
    def recalculateFreeTime(self):
        self.freeDayAndTime = {"Monday": [], "Tuesday": [], "Wednesday": [], "Thursday": [], "Friday": []}
        self.allLessonsDayAndTime = {"Monday": ([],[]), "Tuesday": ([],[]),
        "Wednesday": ([],[]), "Thursday": ([],[]), "Friday": ([],[])}
        for user in self.users:
            self.users[user].updateLessons()
        self.calculateFreeTime()
    
    #Returns out list of available times
    def showFreeTime(self):

        def getStartTime(result):
            return result[0]

        def getEndTime(result):
            return result[1]
        message = 'These free timings are available!\n'
        for day in self.freeDayAndTime:
            message += f"{day}:\n"
            if self.freeDayAndTime[day]:
                for time in self.freeDayAndTime[day]:
                    if time:
                        message += f"{getStartTime(time)}h to {getEndTime(time)}h\n"
            else:
                message += "No free timings\n"
            message += '\n'
        return message  