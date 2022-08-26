from Group import Group
from Student import Student
import pickle

modlink1 = "https://nusmods.com/timetable/sem-1/share?CFG1002=&CS1231S=TUT:05A,LEC:1&CS2030S=LEC:1,REC:01,LAB:16A&IS1108=TUT:22,LEC:1&MA1521=LEC:1,TUT:15&UTC1102C=SEM:2"
modlink2 = "https://nusmods.com/timetable/sem-1/share?CS1101S=TUT:03C,LEC:1,REC:16A&CS1231S=TUT:02C,LEC:1&IS1108=TUT:24,LEC:1&MA1521=LEC:1,TUT:13&UTW1001C=SEC:2"
modlink3 = "https://nusmods.com/timetable/sem-1/share?CS2030S=LEC:1,REC:03,LAB:16A&GEA1000=TUT:E14&GESS1036=SEC:A1&HSI1000=LAB:2,WS:E5,LEC:1&MA1301=TUT:11,LEC:1"
modlink4 = "https://nusmods.com/timetable/sem-1/share?BT1101=TUT:07,LAB:10A,LEC:1&CS1010S=TUT:06A,REC:04,LEC:1V&GEX1007=LEC:1&IS1108=TUT:22,LEC:2&MA2001=TUT:23,LEC:2,LAB:8"
modlink5 = "https://nusmods.com/timetable/sem-1/share?BT1101=TUT:01,LAB:10A,LEC:1&CS1010S=TUT:10A,LEC:1,REC:15&IS1108=TUT:22,LEC:3&MA2001=TUT:23,LAB:7,LEC:2&UTW1001F=SEC:1"
modlink6 = "https://nusmods.com/timetable/sem-1/share?ACC1701=TUT:V17,LEC:V1&BPM1701=SEC:A1&BPM1702=SEC:A1&BPM1705=SEC:A3&BSP1702=SEC:A7&GEA1000=TUT:D13&MKT1705B=SEC:B4&MNO2706=SEC:A2&STR1000=SEC:A1"
newGroup = Group('Test')
groups = {'123':newGroup}
newStudent = Student(modlink1, newGroup, "Jared", '12345')
newStudent2 = Student(modlink2, newGroup, "Ryann", '123456')
newStudent3 = Student(modlink3, newGroup, "Rick", '123')
newStudent4 = Student(modlink4, newGroup, "Pris", '123')
newStudent5 = Student(modlink5, newGroup, "Zhang Yue", '123')
newStudent6 = Student(modlink6, newGroup, "Sarah", '12345')
newGroup.calculateFreeTime()

print(groups['123'].freeDayAndTime)
with open('modFriendsTest.pkl', 'wb') as f:
    pickle.dump(groups, f)
        
with open('modFriendsTest.pkl', 'rb') as f:
    loaded_dict = pickle.load(f)

print(loaded_dict['123'].freeDayAndTime)