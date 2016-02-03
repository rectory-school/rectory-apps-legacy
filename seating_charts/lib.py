from random import choice, random, sample

import time

from seating_charts import models

class GeneratorError(Exception):
    def __init__(self, s):
        super(GeneratorError, self).__init__()
        self.s = s
    def __str__(self):
        return "Table generation exception: %s" % self.s

class Table(object):
    def __init__(self, table, mealTime):
        self.id = table.id
        self.capacity = table.capacity - sum(sf.seats for sf in models.SeatFiller.objects.filter(table=table).filter(meal_time=mealTime))
        self.usedCapacity = 0
        self.students = set()

    def availableCapacity(self):
        return self.capacity - self.usedCapacity

    def addStudent(self, s):
        self.students.add(s)
        self.usedCapacity += 1

    def reset(self):
        self.students = set()
        self.usedCapacity = 0

    def passesAllRules(self):
        if not noDomination(self.students, 'ethnicity'):
            #We have an ethnic domination
            return False
            
        if not noSingleton(self.students, 'gender'):
            #We have a single boy or girl
            return False
        
        return True

class Student(object):
    def __init__(self, o):
        self.id = o.id
        self.first_name = o.first_name
        self.last_name = o.last_name
        self.gender = o.gender
        self.ethnicity = o.ethnicity and o.ethnicity.ethnicity
        self.boarder = o.enrollment.boarder
        self.grade = o.enrollment.grade.grade      

class SeatingChartGenerator(object):
    def __init__(self, students, tables, pinnedStudents):
        self.students = students
        self.tables = tables
        self.pinnedStudents = pinnedStudents
        
        self.running = True
        self.availableStudents = set(self.students)

    def generateTables(self):
        #Run 100 iterations before giving up
        for i in range(100):
            self.populateTables()
            recycled = self.recycleBadTables()
            self.populateTables()
            

    def populateTables(self):
        for student in self.pinnedStudents:
            if student in self.availableStudents:
                table = self.pinnedStudents[student]
                table.addStudent(student)
                self.availableStudents.remove(student)
        
        while self.availableStudents:
            table = sorted(self.tables, key=Table.availableCapacity)[-1]
            student = sample(self.availableStudents, 1)[0]
            table.addStudent(student)
            self.availableStudents.remove(student)


    def recycleBadTables(self):
        for t in self.tables:
            if not t.passesAllRules():
                self.availableStudents.update(t.students)
                t.reset()

    def reset(self):
        for t in self.tables:
            self.availableStudents.update(t.students())
            t.reset()

def makeSeatingChart(mealTime):
    tables = getTables(mealTime)

    sc = models.SeatingChart()
    sc.meal_time = mealTime
    sc.save()

    for t in tables:
        table = models.Table.objects.get(pk=t.id)
        for s in t.students:
            student = models.Student.objects.get(pk=s.id)

            assignment=models.TableAssignment()
            assignment.seating_chart = sc
            assignment.meal_time = mealTime
            assignment.table = table
            assignment.student = student
            assignment.save()

    return sc

def getTables(mealTime, max_processes=16):
    students = []
    tables = []
    studentLookup = {}
    tableLookup = {}
    
    for s in mealTime.allStudents():
        localStudent = Student(s)
        students.append(localStudent)
        studentLookup[s.id] = localStudent
        
    for t in mealTime.table_set.all():
        localTable = Table(t, mealTime)
        tables.append(localTable)
        tableLookup[t.id] = localTable
    
    pinnedStudents = {}
    
    for ps in models.PinnedStudent.objects.filter(meal_time=mealTime):
        try:
            localStudent = studentLookup[ps.student.id]
        except KeyError:
            raise GeneratorError("%s is pinned to table %s during %s, but that student is not participating in that meal time. Please check the student's grade/boarding status." % (ps.student.name, ps.table.description, mealTime.name))

        try:
            localTable = tableLookup[ps.table.id]
        except KeyError:
            raise GeneratorError("%s is pinned to table %s during %s, but that table is not available during that lunch period. Please check your settings." % (ps.student.name, ps.table.description, mealTime.name))

        pinnedStudents[localStudent] = localTable
        
    generator = SeatingChartGenerator(students, tables, pinnedStudents)
    generator.generateTables()
    
    return generator.tables


def noSingleton(students, attr):
    totalStudents = len(students)
    collection = getCollection(students, attr)
    
    #2/0, 1/1 or 0/2 are all OK non-singletons
    if totalStudents < 3:
        return True
        
    for v in collection.values():
        if v == 1:
            return False
            
    return True
    
def noDomination(students, attr, threshold=1):
    totalStudents = len(students)
    #You can't call it domination if there are only two of them...
    if totalStudents < 3:
        return True
    
    
    collection = getCollection(students, attr)
    for v in collection.values():
        ratio = v/totalStudents
        
        if ratio >= threshold:
            return False
            
    return True
    
def minimumDiversity(students, attr, minimumValue):
    #We can't have more diversity than there are students...
    minimumValue = min(students, minimumValue)
    
    #Make sure we have at least as many attributes as minimumCalue
    collection = getCollection(students, attr)
    return (len(collection) >= minimumValue)
    
def getCollection(students, attr):
    collection = {}

    for s in students:
        o = getattr(s, attr)
        
        if not o:
          continue
        
        if o not in collection:
            collection[o] = 0

        collection[o] += 1

    return collection
