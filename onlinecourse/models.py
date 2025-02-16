import sys
from django.utils.timezone import now
try:
    from django.db import models
except Exception:
    print("There was an error loading django modules. Do you have django installed?")
    sys.exit()

from django.conf import settings
import uuid


# Instructor model
class Instructor(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    full_time = models.BooleanField(default=True)
    total_learners = models.IntegerField(default=0)

    def __str__(self):
        return self.user.username


# Learner model
class Learner(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    STUDENT = 'student'
    DEVELOPER = 'developer'
    DATA_SCIENTIST = 'data_scientist'
    DATABASE_ADMIN = 'dba'
    OCCUPATION_CHOICES = [
        (STUDENT, 'Student'),
        (DEVELOPER, 'Developer'),
        (DATA_SCIENTIST, 'Data Scientist'),
        (DATABASE_ADMIN, 'Database Admin')
    ]
    occupation = models.CharField(
        null=False,
        max_length=20,
        choices=OCCUPATION_CHOICES,
        default=STUDENT
    )
    social_link = models.URLField(max_length=200)

    def __str__(self):
        return self.user.username + "," + \
               self.occupation

# Course model
class Course(models.Model):
    name = models.CharField(null=False, max_length=30, default='online course')
    image = models.ImageField(upload_to='course_images/')
    description = models.CharField(max_length=1000)
    pub_date = models.DateField(null=True)
    instructors = models.ManyToManyField(Instructor)
    users = models.ManyToManyField(settings.AUTH_USER_MODEL, through='Enrollment')
    total_enrollment = models.IntegerField(default=0)
    is_enrolled = False
    def __str__(self):
        return "Name: " + self.name + "," + \
               "Description: " + self.description

# Lesson model
class Lesson(models.Model):
    title = models.CharField(max_length=200, default="title")
    order = models.IntegerField(default=0)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    content = models.TextField()

# <HINT> Create a Question Model with:
    # Used to persist question content for a course
    # Has a One-To-Many (or Many-To-Many if you want to reuse questions) relationship with course
    # Has a grade point for each question
    # Has question content
    # Other fields and methods you would like to design
class Question(models.Model):
    A = 'A'
    B ='B'
    C ='C'
    D= 'D'
    Choices = [(A , 'A'), (B, 'B'),(C, 'C'), (D, 'D') ]
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    text = models.TextField(max_length=500, default="question is...", null=False)
    grade = models.CharField(default=A, null=True, max_length=1)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    correct_ans = models.CharField(choices=Choices, default=A, null=False, max_length=10)

    # <HINT> A sample model method to calculate if learner get the score of the question
    def is_get_score(self, selected_ids):
        all_answers = self.choice_set.filter(is_correct=True).count()
        selected_correct = self.choice_set.filter(is_correct=True, id__in=selected_ids).count()
        if all_answers == selected_correct:
           return True
        else:
           return False

# Enrollment model
# <HINT> Once a user enrolled a class, an enrollment entry should be created between the user and course
# And we could use the enrollment to track information such as exam submissions
class Enrollment(models.Model):
    AUDIT = 'audit'
    HONOR = 'honor'
    BETA = 'BETA'
    COURSE_MODES = [
        (AUDIT, 'Audit'),
        (HONOR, 'Honor'),
        (BETA, 'BETA')
    ]
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    date_enrolled = models.DateField(auto_now=True)
    mode = models.CharField(max_length=50, choices=COURSE_MODES, default=AUDIT)
    rating = models.FloatField(default=5.0)

class Choice(models.Model):
    # Used to persist choice content for a question
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(null=False, max_length=500)
    correct = models.BooleanField()
    # Choice content
    A ='A'
    B ='B'
    C ='C'
    D= 'D'
    Choices = [(A , 'A'), (B, 'B'),(C, 'C'), (D, 'D') ]
    answer = models.CharField(max_length=500, choices=Choices, default=A)
    def is_correct(self, answer):
        correct_ans = Question.correct_ans
        if  answer == correct_ans:
           return True
        else:
           return False

# <HINT> The submission model
# One enrollment could have multiple submission
# One submission could have multiple choices
# One choice could belong to multiple submissions
class Submission(models.Model):
    enrollment = models.ForeignKey(Enrollment, on_delete=models.PROTECT)
    choices = models.ManyToManyField(Choice)
    user = models.ManyToManyField(Learner)
    course =  models.ManyToManyField(Course)
    #total = 
    # Other fields and methods you would like to design