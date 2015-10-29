from django.test import TestCase
from academics.models import Student, AcademicYear, Teacher

# Create your tests here.
class StudentTestCase(TestCase):
    def setUp(self):
        Student.objects.create(first_name="Adam", last_name="Peacock", student_id="ST00001")
        Student.objects.create(first_name="Adam", last_name="Peacock", nickname="The Fixer", student_id="ST00002")
    
    def tearDown(self):
        Student.objects.all().delete()
    
    def test_nickname_format(self):
        student = Student.objects.get(student_id="ST00002")
        self.assertEqual(student.name, "Adam (The Fixer) Peacock")
    
    def test_nonickname_format(self):
        student = Student.objects.get(student_id="ST00001")        
        self.assertEqual(student.name, "Adam Peacock")

class TeacherTestCase(TestCase):
    def setUp(self):
        Teacher.objects.create(first_name="Adam", last_name="Peacock", teacher_id="T001")
    
    def tearDown(self):
        Teacher.objects.all().delete()
    
    def test_name_format(self):
        t = Teacher.objects.get(teacher_id="T001")
        
        self.assertEquals(t.name, "Adam Peacock")

class AcademicYearTestCase(TestCase):
    def checkEquals(self, year):
        currentYear = AcademicYear.objects.current()
        
        self.assertEqual(currentYear.year, year)
    
    def tearDown(self):
        AcademicYear.objects.all().delete()

class AcademicYearBasicTestCase(AcademicYearTestCase):
    def setUp(self):    
        AcademicYear.objects.create(year="2011-2012", current=False)
        AcademicYear.objects.create(year="2012-2013", current=False)
        AcademicYear.objects.create(year="2013-2014", current=False)
        AcademicYear.objects.create(year="2014-2015", current=True)
        
    def test_basic(self):
        self.checkEquals("2014-2015")

class AcademicYearOldOpenTestCase(AcademicYearTestCase):
    def setUp(self):    
        AcademicYear.objects.create(year="2011-2012", current=False)
        AcademicYear.objects.create(year="2012-2013", current=False)
        AcademicYear.objects.create(year="2013-2014", current=True)
        AcademicYear.objects.create(year="2014-2015", current=False)
    
    def test_basic(self):
        self.checkEquals("2013-2014")

class AcademicYearMultipleTestCase(AcademicYearTestCase):
    def setUp(self):
        AcademicYear.objects.create(year="2011-2012", current=False)
        AcademicYear.objects.create(year="2012-2013", current=True)
        AcademicYear.objects.create(year="2013-2014", current=True)
        AcademicYear.objects.create(year="2014-2015", current=False)
    
    def test_multiple_open(self):
        self.checkEquals("2013-2014")

class AcademicYearNoOpenTestCase(AcademicYearTestCase):
    def setUp(self):
        AcademicYear.objects.create(year="2011-2012", current=False)
        AcademicYear.objects.create(year="2012-2013", current=False)
        AcademicYear.objects.create(year="2013-2014", current=False)
        AcademicYear.objects.create(year="2014-2015", current=False)
    
    def test_no_open(self):
        self.checkEquals("2014-2015")
    
class AcademicYearNoObjectsTestCase(AcademicYearTestCase):
    def test_no_objects(self):
        thrown = False
    
        try:
            o = AcademicYear.objects.current()
        except AcademicYear.DoesNotExist:
            thrown = True
    
        self.assertEquals(thrown, True)
    