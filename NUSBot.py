import requests
import re
import Error as e

api_url = "https://api.nusmods.com/v2/2022-2023/modules/"
lessonTypesLst = {"REC": "Recitation", "LAB": "Laboratory", "LEC": "Lecture",
"SEM":"Seminar-Style Module Class", "TUT":"Tutorial","WS":"Workshop", "SEC":"Sectional Teaching"
, "TUT2":"Tutorial Type 2", "PLEC": "Packaged Lecture", "PTUT":"Packaged Tutorial"}

#Get request from API
def getModuleRequest(moduleCode): 
    url = api_url + moduleCode + ".json"
    response = requests.get(url).json()
    return response

#Get lesson timetable from JSON
def getModuleLessons(jsonresult):
    return jsonresult["semesterData"][0]["timetable"]

#Gets and formats all lesson timings into a list of tuples
def getLessonTiming(moduleCode, moduleLessons):
    result = []
    try:
        lessonsList = getModuleLessons(getModuleRequest(moduleCode))
        for lessonType, lessonCode in moduleLessons.items():
            lessonTime = [(moduleCode, lessonCode, lessonType, (x['day'], x['startTime'], x['endTime'])) for x in lessonsList if (x["lessonType"] == lessonTypesLst.get(lessonType) and x["classNo"] == lessonCode)]
            result.extend(lessonTime)
        return result
    except IndexError:
        return result

#Formats NUSMods link for processing
def getUserLessons(link):

    def getLessonList(lessonDetail):
        result = {}
        if lessonDetail == '':
            return result
        else:
            lessonList = lessonDetail.split(',')
            for lesson in lessonList:
                lessonType, lessonCode = lesson.split(":")
                result[lessonType] = lessonCode
            return result

    modList = (link.split("share?")[1]).split("&")
    result = {}
    for mod in modList:
        try:
            moduleCode, lessonDetail = mod.split("=")
            result[moduleCode] = getLessonList(lessonDetail)
        except:
            raise e.InvalidModError
    return result

#Accessors for lesson data representation (e.g (modCode, lessonCode, lessonType, (Day, startTime, endTime)))
def getModuleCode(lessonDetail):
    return lessonDetail[0]

def getLessonCode(lessonDetail):
    return lessonDetail[1]

def getLessonType(lessonDetail):
    return lessonDetail[2]

def getLessonTime(lessonDetail):
    return lessonDetail[3]

def getLessonDay(lessonTime):
    return lessonTime[0]

def getStartTime(lessonTime):
    return lessonTime[1]

def getEndTime(lessonTime):
    return lessonTime[2]