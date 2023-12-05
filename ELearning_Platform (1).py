#!/usr/bin/env python
# coding: utf-8

# In[1]:


##### -*- coding: utf-8 -*-

import json
from pathlib import Path
import smtplib
from abc import ABC, abstractmethod
from email.mime.text import MIMEText

# models.py
class UserProfile:
    def __init__(self, username, BU_ID='', email=''):
        """
        Initialize a user profile with username, BU_ID, and email.
        """
        self.username = username
        self.BU_ID = BU_ID
        self.email = email
        self.courses_taught = []  # List of courses taught by the user
        self.achievement_badges = set()  # Set of achievement badges earned
        self.quiz_attempts = []  # List of quiz attempts by the user
        self.badges = []  # List of badges earned
        self.progress = CourseProgress(user=self, course=None)  # User's course progress

    def __str__(self):
        """
        Return the username when the object is converted to a string.
        """
        return self.username


class CourseProgress:
    def __init__(self, user, course):
        """
        Initialize course progress for a user with associated user and course.
        """
        self.user = user
        self.course = course
        self.modules_completed = set()  # Set of completed modules
        self.video_lessons_watched = set()  # Set of watched video lessons
        self.quizzes_completed = set()  # Set of completed quizzes
        self.score = 0  # Current score
        self.course_rating = None  # Course rating by the user

    def complete_module(self, module):
        """
        Mark a module as completed and update the score.
        """
        if module not in self.modules_completed:
            self.modules_completed.add(module)
            self.score += 10
            print(f"{self.user.username} completed module: {module.title}")
            print(f"Current score: {self.score}")
            return True
        else:
            print(f"{self.user.username} has already completed module: {module.title}")
            return False

    def watch_video_lesson(self, video_lesson):
        """
        Mark a video lesson as watched by the user.
        """
        self.video_lessons_watched.add(video_lesson)
        print(f"{self.user.username} watched video lesson: {video_lesson.title}")

    def complete_quiz(self, quiz):
        """
        Mark a quiz as completed and update the score.
        """
        if quiz not in self.quizzes_completed:
            self.quizzes_completed.add(quiz)
            self.score += 20
            print(f"{self.user.username} completed quiz: {quiz.title}")
            print(f"Current score: {self.score}")
            return True
        else:
            print(f"{self.user.username} has already completed quiz: {quiz.title}")
            return False

    def set_course_rating(self, rating):
        """
        Set the course rating within the range of 1 to 5.
        """
        if 1 <= rating <= 5:
            self.course_rating = rating
            print(f"{self.user.username} rated the course '{self.course.title}' with {rating}/5.")
        else:
            print("Invalid rating. Please enter a number between 1 and 5.")



class ObservableCourse:
    def __init__(self, title, description, author):
        """
        Initializes an ObservableCourse object.

        Args:
        - title (str): Title of the course.
        - description (str): Description of the course.
        - author (str): Author or creator of the course.
        """
        self.title = title
        self.description = description
        self.author = author
        self._observers = set()

    def add_observer(self, observer):
        """
        Adds an observer to the course.

        Args:
        - observer: An object observing the course.
        """
        self._observers.add(observer)

    def remove_observer(self, observer):
        """
        Removes an observer from the course.

        Args:
        - observer: An object observing the course.
        """
        self._observers.remove(observer)

    def notify_observers(self, content):
        """
        Notifies all observers about the new content posted.

        Args:
        - content (str): Content to be notified to the observers.
        """
        for observer in self._observers:
            observer.update(content, self)


class Course(ObservableCourse):
    def __init__(self, title, description, author):
        """
        Initializes a Course object, inheriting from ObservableCourse.

        Args:
        - title (str): Title of the course.
        - description (str): Description of the course.
        - author (str): Author or creator of the course.
        """
        super().__init__(title, description, author)
        self.modules = []
        self.video_lessons = []
        self.quizzes = []
        self.author = author
        self.students = []

    def add_module(self, module):
        """
        Adds a module to the course.

        Args:
        - module (Module): Module object to be added.
        """
        self.modules.append(module)

    def add_video_lesson(self, video_lesson):
        """
        Adds a video lesson to the course.

        Args:
        - video_lesson (VideoLesson): VideoLesson object to be added.
        """
        self.video_lessons.append(video_lesson)

    def add_quiz(self, quiz):
        """
        Adds a quiz to the course.

        Args:
        - quiz (Quiz): Quiz object to be added.
        """
        self.quizzes.append(quiz)

    def post_content(self, content):
        """
        Posts content to the course and notifies observers.

        Args:
        - content (str): Content to be posted.
        """
        print(f"Content posted: {content}")
        self.notify_observers(content)

    def get_students(self):
        """
        Retrieves the list of students enrolled in the course.

        Returns:
        - list: List of students enrolled in the course.
        """
        return self.students


class Module:
    def __init__(self, title, content):
        """
        Initializes a Module object.

        Args:
        - title (str): Title of the module.
        - content (str): Content of the module.
        """
        self.title = title
        self.content = content


class VideoLesson:
    def __init__(self, title, video_url):
        """
        Initializes a VideoLesson object.

        Args:
        - title (str): Title of the video lesson.
        - video_url (str): URL of the video.
        """
        self.title = title
        self.video_url = video_url


class Quiz:
    def __init__(self, title, questions, course):
        """
        Initializes a Quiz object.

        Args:
        - title (str): Title of the quiz.
        - questions (list): List of questions in the quiz.
        - course (Course): Course object to which the quiz belongs.
        """
        self.title = title
        self.questions = questions
        self.course = course
        # Add course attribute to store the course to which the quiz belongs



# factories.py

class VideoCourseFactory:
    """A factory class to create video courses."""

    def create_course(self, professor, title, description):
        """
        Create a new course with the given title, description, and professor.

        Args:
        - professor (Professor): The professor teaching the course.
        - title (str): The title of the course.
        - description (str): A description of the course.

        Returns:
        - Course: The newly created course object.
        """
        course = Course(title=title, description=description, author=professor)
        professor.courses_taught.append(course)
        return course


# observer.py

class CourseObserver:
    """A class representing an observer for course updates."""

    def update(self, content, course):
        """
        Update method called when a course notification is triggered.

        Args:
        - content (str): Notification content.
        - course (Course): The course associated with the notification.
        """
        print(f"Notification: {content} - Course: {course.title}")

# strategies.py

class ModuleCompletionStrategy:
    """An abstract class representing a strategy for module completion."""

    def complete_module(self, user, module):
        """
        Abstract method to complete a module.

        Args:
        - user (User): The user attempting the module.
        - module (Module): The module to be completed.
        """
        pass


class DefaultModuleCompletion(ModuleCompletionStrategy):
    """A default module completion strategy."""

    def complete_module(self, user, module):
        """
        Complete a module for a user using the default strategy.

        Args:
        - user (User): The user attempting the module.
        - module (Module): The module to be completed.
        """
        user_progress = CourseProgress(user=user, course=module.course)
        user_progress.complete_module(module)


# decorators.py

class BadgeDecorator(ABC):
    """An abstract class representing a badge decorator."""

    @abstractmethod
    def decorate(self):
        """Abstract method to decorate with a badge."""
        pass

class CourseCompletionDecorator(BadgeDecorator):
    """A decorator for course completion badges."""

    def __init__(self, user, badge_name):
        """
        Initialize CourseCompletionDecorator.

        Args:
        - user (User): The user receiving the badge.
        - badge_name (str): The name of the badge.
        """
        self.user = user
        self.badge_name = badge_name

    def decorate(self):
        """Add a completion badge to the user."""
        if not hasattr(self.user, 'badges'):
            print("Error: The user profile does not have a 'badges' attribute.")
            return

        self.user.badges.append(self.badge_name)
        print(f"Congratulations, {self.user.username}! You have earned the '{self.badge_name}' badge.")


class QuizQuestion:
    """A class representing a quiz question."""

    def __init__(self, question_text, options, correct_option):
        """
        Initialize a quiz question.

        Args:
        - question_text (str): The text of the question.
        - options (list): List of options for the question.
        - correct_option (int): The index of the correct option in the 'options' list.
        """
        self.question_text = question_text
        self.options = options
        self.correct_option = correct_option


class QuizAttempt:
    """A class representing a user's attempt at a quiz."""

    def __init__(self, user, quiz):
        """
        Initialize a quiz attempt for a user.

        Args:
        - user (User): The user attempting the quiz.
        - quiz (Quiz): The quiz being attempted.
        """
        self.user = user
        self.quiz = quiz
        self.responses = {}

    def take_quiz(self):
        """Take the quiz and record user responses."""
        for question in self.quiz.questions:
            print(f"\nQuestion: {question.question_text}")
            for i, option in enumerate(question.options, start=1):
                print(f"{i}. {option}")

            user_answer = int(input("Enter the number of your answer: "))
            self.responses[question.question_text] = user_answer

    def grade_quiz(self):
        """Grade the quiz based on user responses."""
        correct_count = 0
        total_questions = len(self.quiz.questions)

        for question in self.quiz.questions:
            if self.responses[question.question_text] == question.correct_option:
                correct_count += 1

        percentage = (correct_count / total_questions) * 100
        self.grade = percentage  # Assign the calculated grade to the 'grade' attribute
        return percentage



class ProfessorView:

    @staticmethod
    def create_video_lesson(course):
        """
        Creates a video lesson for a given course.

        Args:
        - course: The Course object for which the video lesson is created.

        Actions:
        - Prompts the user for title and video URL.
        - Creates a VideoLesson object.
        - Adds the video lesson to the provided course.
        - Prints a success message.
        """
        title = input("Enter the title of the video lesson: ")
        video_url = input("Enter the video URL: ")
        video_lesson = VideoLesson(title=title, video_url=video_url)
        course.add_video_lesson(video_lesson)
        print(f"Video lesson '{video_lesson.title}' created successfully for the course '{course.title}'.\n")

    @staticmethod
    def view_courses_created(professor, platform):
        """
        Displays courses created by the professor on the platform.

        Args:
        - professor: Professor object who created the courses.
        - platform: The Platform object where courses are created.

        Actions:
        - Displays courses created by the professor.
        - Offers an option to create a course if none exists.
        """
        courses_created = professor.courses_taught
        if courses_created:
            print(f"\nCourses Created by {professor.username}:")
            for idx, course in enumerate(courses_created, start=1):
                print(f"{idx}. {course.title}")
        else:
            print(f"No courses created by {professor.username}.")
            create_course_option = input("Would you like to create a course now? (yes/no): ")
            if create_course_option.lower() == "yes":
                platform.create_course(professor)
            else:
                print("Okay, no courses created at this time.")

    @staticmethod
    def view_student_details(course):
        """
        Displays details of students enrolled in a course.

        Args:
        - course: The Course object to view student details for.

        Actions:
        - Displays enrolled student usernames and IDs for the course.
        """
        students = course.students
        if students:
            print(f"\nEnrolled Students in {course.title}:")
            for idx, student in enumerate(students, start=1):
                print(f"{idx}. Username: {student.username}, BU ID: {student.BU_ID}")
        else:
            print(f"No students enrolled in {course.title}.")

    # Inside the respective methods in ProfessorView class
    @staticmethod
    def view_student_quiz_grades(course):
        """
        Displays quiz grades of students enrolled in a course.

        Args:
        - course: The Course object to view student quiz grades for.

        Actions:
        - Displays quiz grades of students for their attempts.
        """
        students = course.students
        if students:
            print(f"\nQuiz Grades for Students in {course.title}:")
            for student in students:
                if student.quiz_attempts:
                    print(f"{student.username}'s Quiz Grades:")
                    for quiz_attempt in student.quiz_attempts:
                        print(f"- Quiz: {quiz_attempt.quiz.title}, Grade: {quiz_attempt.grade}%")
                else:
                    print(f"{student.username} hasn't attempted any quizzes.")
        else:
            print(f"No students enrolled in {course.title}.")


    @staticmethod
    def view_courses_and_students(professor, platform):
        """
        Displays courses created by the professor and details of enrolled students.

        Args:
        - professor: Professor object who created the courses.
        - platform: The Platform object where courses are created.

        Actions:
        - Displays courses created by the professor.
        - Prompts for a course selection.
        - Displays student details, quiz grades, and video lessons watched for the selected course.
        """
        ProfessorView.view_courses_created(professor, platform)
        selected_course_index = int(input("Enter the number of the course to view details: "))
        selected_course = professor.courses_taught[selected_course_index - 1]

        ProfessorView.view_student_details(selected_course)
        ProfessorView.view_student_quiz_grades(selected_course)
        ProfessorView.view_video_lessons_watched(selected_course)

    @staticmethod
    def view_classlist(course):
        """
        Displays a list of students enrolled in a course.

        Args:
        - course: The Course object to view the classlist for.

        Actions:
        - Displays enrolled student usernames for the course.
        """
        students = course.students
        if students:
            print(f"\nEnrolled Students in {course.title}:")
            for idx, student in enumerate(students, start=1):
                print(f"{idx}. {student.username}")
        else:
            print(f"No students enrolled in {course.title}.")



    def view_courses_created_with_edit_option(professor, platform):
        """
        Displays courses created by the professor and enables course management.

        Args:
        - professor: Professor object who created the courses.
        - platform: The Platform object where courses are created.

        Actions:
        - Displays courses created by the professor.
        - Allows the user to select a course for management.
        - Provides options to view students, quiz grades, edit the course, or return to the courses menu.
        """
        courses_created = professor.courses_taught
        if courses_created:
            print(f"\nCourses Created by {professor.username}:")
            for idx, course in enumerate(courses_created, start=1):
                print(f"{idx}. {course.title}")

            # Add an option to edit the course
            print("\nSelect a course number to manage:")
            selected_course_index = int(input("Enter the number of the course: "))
            selected_course = professor.courses_taught[selected_course_index - 1]

            while True:
                print(f"\nSelected Course: {selected_course.title}")
                print("1. View Enrolled Students")
                print("2. View Student Quiz Grades")
                print("3. Edit Course")
                print("4. Back to Courses Menu")

                details_choice = input("Enter your choice: ")

                if details_choice == "1":
                    ProfessorView.view_classlist(selected_course)
                elif details_choice == "2":
                    ProfessorView.view_student_quiz_grades(selected_course)
                elif details_choice == "3":
                    platform.edit_course(selected_course)
                elif details_choice == "4":
                    break
                else:
                    print("Invalid option. Please enter a valid number.")

        else:
            print(f"No courses created by {professor.username}.")

import json

class CustomEncoder(json.JSONEncoder):
    """Custom JSON encoder for specific object serialization."""

    def default(self, obj):
        """
        Serialize objects to JSON-compatible formats.

        Args:
        - obj: Object to be serialized.

        Returns:
        - JSON-compatible representation of the object.

        Raises:
        - TypeError: If the object cannot be serialized.
        """
        if isinstance(obj, Course):
            # Serialize Course object
            return {
                "title": obj.title,
                "description": obj.description,
                "author": obj.author.username,
                "modules": [module.__dict__ for module in obj.modules],
                "video_lessons": [video_lesson.__dict__ for video_lesson in obj.video_lessons],
                "quizzes": [quiz.__dict__ for quiz in obj.quizzes],
                "students": [student.username for student in obj.students]
            }
        elif isinstance(obj, UserProfile):
            # Serialize UserProfile object
            return {
                "username": obj.username,
                "BU_ID": obj.BU_ID,
                "courses_taught": [course.title for course in obj.courses_taught],
                "achievement_badges": list(obj.achievement_badges),
                "quiz_attempts": [quiz_attempt.__dict__ for quiz_attempt in obj.quiz_attempts],
                "progress": self.serialize_progress(obj.progress)
            }
        elif isinstance(obj, CourseProgress):
            # Serialize CourseProgress object
            return {
                "user": obj.user.__dict__,
                "course": obj.course.title if obj.course else None,
                "modules_completed": list(obj.modules_completed),
                "video_lessons_watched": list(obj.video_lessons_watched),
                "quizzes_completed": list(obj.quizzes_completed),
                "score": obj.score
            }
        elif isinstance(obj, set):
            # Serialize set object
            return list(obj)
        elif isinstance(obj, QuizQuestion):
            # Serialize QuizQuestion object
            return {
                "question_text": obj.question_text,
                "options": obj.options,
                "correct_option": obj.correct_option
            }
        return super().default(obj)

    def serialize_progress(self, progress):
        """
        Serialize progress information.

        Args:
        - progress: Course progress information.

        Returns:
        - Serialized progress information.

        Note:
        - Progress may contain user, course, completed modules, watched video lessons, quizzes completed, and score.
        """
        return {
            "user": progress.user.__dict__,
            "course": progress.course.title if progress.course else None,
            "modules_completed": list(progress.modules_completed),
            "video_lessons_watched": list(progress.video_lessons_watched),
            "quizzes_completed": list(progress.quizzes_completed),
            "score": progress.score
        }


class ElearningPlatform:
    """A class representing an e-learning platform."""

    JSON_FILENAME = "elearning_data.json"
    ADMIN_PASSWORD = "admin123"  # Set your desired admin password
    STUDENT_PASSWORD = "student123"  # Set your desired student password

    def __init__(self):
        """Initialize the e-learning platform."""
        self.users = []  # List to store user profiles
        self.courses = []  # List to store courses
        self.posts = []  # List to store posts
        self.interactions = []  # List to store user interactions
        self.notifications = []  # List to store notifications
        self.user_credentials = {}  # Dictionary to store user credentials {username: (user_type, password)}

    # Define professor_emails as a class attribute
    professor_emails = {}  # Dictionary to store professor emails

    def send_email_alert(self, recipient, subject, message):
        """
        Send an email alert.

        Args:
        - recipient: The recipient's email address.
        - subject: Subject of the email.
        - message: Content of the email.

        Returns:
        None
        """
        print(f"Email sent to {recipient}: {subject}\n{message}")

    def register_user(self):
        """
        Register a new user.

        Returns:
        - If registration is successful, returns the user profile.
        - If unsuccessful, returns None.
        """
        while True:
            try:
                username = input("Enter your username: ")
                email = input("Enter your email address: ")

                # Check if the user already exists
                if username in self.user_credentials:
                    user_type, stored_password = self.user_credentials[username]
                    entered_password = input(f"Enter the password for {username}: ")

                    # Authenticate the user
                    if user_type == "1" and entered_password == stored_password:
                        print(f"Welcome back, {username}!")
                        return self.get_user_profile(username)
                    elif user_type == "2" and entered_password == stored_password:
                        print(f"Welcome back, {username}!")
                        return self.get_user_profile(username)
                    else:
                        print("Incorrect password or user type. Please try again.")
                        continue

                # Register new user
                user_type = input("Are you a Professor (1) or a Student (2)?: ")

                if user_type == "1":
                    admin_password = input("Enter the admin password: ")
                    if admin_password != self.ADMIN_PASSWORD:
                        print("Incorrect admin password. Registration denied.")
                        return None
                elif user_type == "2":
                    student_password = input("Enter the student password: ")
                    if student_password != self.STUDENT_PASSWORD:
                        print("Incorrect student password. Registration denied.")
                        return None
                else:
                    print("Invalid user type. Please choose '1' for professor or '2' for student.")
                    continue

                BU_ID = input("Enter your BU_ID: ")

                if not username:
                    raise ValueError("Username cannot be empty.")

                # Create a new user profile
                user = UserProfile(username=username, BU_ID=BU_ID)
                self.users.append(user)
                self.user_credentials[username] = (user_type, admin_password if user_type == "1" else student_password)
                return user
            except ValueError as ve:
                print(f"Error: {ve}")

    def get_user_profile(self, username):
        """
        Get the user profile by username.

        Args:
        - username: The username of the user profile to retrieve.

        Returns:
        - User profile if found, otherwise None.
        """
        for user in self.users:
            if user.username == username:
                return user
        return None


    def create_course(self, professor):
        """
        Creates a new course with provided details and manages course setup options.

        Args:
        - professor: UserProfile object representing the course author/professor.

        Comments:
        - Prompts user for title and description of the course.
        - Ensures title and description are provided; else, the course creation is aborted.
        - Adds the created course to the professor's courses_taught list and the platform's courses list.
        - Allows adding modules, video lessons, quizzes, viewing enrollments, and completing setup.
        """
        title = input("Enter the title of the course: ")
        description = input("Enter the description of the course: ")

        # Checking if title and description are provided
        if not title or not description:
            print("Title and description are required to create a course.")
            return

        # Creating the course instance and associating it with the professor
        course = Course(title=title, description=description, author=professor)
        professor.courses_taught.append(course)
        self.courses.append(course)
        print(f"Course '{course.title}' created successfully.")

        # Course setup options loop
        while True:
            print("\n=== Course Management Options ===")
            print("1. Add Module")
            print("2. Add Video Lesson")
            print("3. Add Quiz")
            print("4. View Enrollments")
            print("5. Finish Course Setup")

            choice = input("Enter the number of your choice: ")

            if choice == "1":
                # Logic for adding modules to the course
                module_title = input("Enter the title of the module: ")
                module_content = input("Enter the content of the module: ")
                module = Module(title=module_title, content=module_content)
                course.add_module(module)
                print(f"Module '{module.title}' added successfully to '{course.title}'.")
            elif choice == "2":
                # Logic for adding video lessons to the course
                video_title = input("Enter the title of the video lesson: ")
                video_url = input("Enter the video URL: ")
                video_lesson = VideoLesson(title=video_title, video_url=video_url)
                course.add_video_lesson(video_lesson)
                print(f"Video lesson '{video_lesson.title}' added successfully to '{course.title}'.")
            elif choice == "3":
                # Logic for adding quizzes to the course
                quiz_title = input("Enter the title of the quiz: ")
                num_questions = int(input("Enter the number of questions for the quiz: "))
                questions = []

                # Creating quiz questions and assembling the quiz
                for i in range(num_questions):
                    question_text = input(f"Enter the question {i + 1}: ")
                    options = [input(f"Enter option {j + 1}: ") for j in range(4)]  # Assume 4 options for each question
                    correct_option = int(input("Enter the correct option number: "))
                    question = QuizQuestion(question_text=question_text, options=options, correct_option=correct_option)
                    questions.append(question)

                quiz = Quiz(title=quiz_title, questions=questions, course=course)
                course.add_quiz(quiz)
                print(f"Quiz '{quiz.title}' added successfully to '{course.title}'.")
            elif choice == "4":
                # View enrolled students
                ProfessorView.view_classlist(course)
            elif choice == "5":
                print(f"Setup for '{course.title}' completed.")
                break
            else:
                print("Invalid option. Please enter a valid number.")

            # Ensure professor is not None before accessing its attributes
            if professor:
                # Store the professor's email address
                ElearningPlatform.professor_emails[professor.username] = getattr(professor, 'email', None)

    def edit_course(self, course):
        """
        Allows editing the provided course by adding modules, video lessons, quizzes,
        deleting the course, or returning to course details.

        Args:
        - course: Course object to be edited.

        Comments:
        - Presents options for adding modules, video lessons, quizzes, deleting, or returning.
        - Logic for adding modules or invoking external function for video lessons.
        - Handles addition of quizzes and course deletion based on user input.
        """
        while True:
            print("\n=== Edit Course ===")
            print("1. Add Module")
            print("2. Add Video Lesson")
            print("3. Add Quiz")
            print("4. Delete Course")
            print("5. Back to Course Details")

            choice = input("Enter the number of your choice: ")

            if choice == "1":
                # Logic for adding modules to the course
                module_title = input("Enter the title of the module: ")
                module_content = input("Enter the content of the module: ")
                module = Module(title=module_title, content=module_content)
                course.add_module(module)
                print(f"Module '{module.title}' added successfully to '{course.title}'.")
            elif choice == "2":
                # Logic for adding video lessons to the course
                ProfessorView.create_video_lesson(course)
            elif choice == "3":
                # Logic for adding quizzes to the course
                quiz_title = input("Enter the title of the quiz: ")
                num_questions = int(input("Enter the number of questions for the quiz: "))
                questions = []

                # Creating quiz questions and assembling the quiz
                for i in range(num_questions):
                    question_text = input(f"Enter the question {i + 1}: ")
                    options = [input(f"Enter option {j + 1}: ") for j in range(4)]  # Assume 4 options for each question
                    correct_option = int(input("Enter the correct option number: "))
                    question = QuizQuestion(question_text=question_text, options=options, correct_option=correct_option)
                    questions.append(question)

                quiz = Quiz(title=quiz_title, questions=questions, course=course)
                course.add_quiz(quiz)
                print(f"Quiz '{quiz.title}' added successfully to '{course.title}'.")
            elif choice == "4":
                # Logic to delete the course
                confirmation = input(f"Are you sure you want to delete '{course.title}'? (yes/no): ")
                if confirmation.lower() == "yes":
                    self.delete_course(course)
                    print(f"Course '{course.title}' deleted.")
                    break
            elif choice == "5":
                break
            else:
                print("Invalid option. Please enter a valid number.")

    def delete_course(self, course):
        """
        Deletes the provided course from the platform.

        Args:
        - course: Course object to be deleted.

        Comments:
        - Removes the course from the platform's courses list.
        - Removes the course from the courses_taught list of any associated professors.
        """
        if course in self.courses:
            # Remove from main list of courses
            self.courses.remove(course)

            # Remove from professor's courses_taught list if applicable
            for user in self.users:
                if isinstance(user, UserProfile) and course in user.courses_taught:
                    user.courses_taught.remove(course)

            print(f"Course '{course.title}' deleted successfully.")
        else:
            print("Course not found.")


    def enroll_user(self, student, course):
        """
        Enrolls a student in a course and notifies the course author.

        Args:
        - student: UserProfile object representing the student to enroll.
        - course: Course object to enroll the student in.

        Returns:
        - CourseProgress: Object tracking student's progress in the course.

        Raises:
        - ValueError: If the student is not an instance of UserProfile or is already enrolled.

        Comments:
        - Checks if the student is eligible for enrollment.
        - Notifies the course author about the new enrollment.
        - Creates a CourseProgress object for the enrolled student.
        """
        # Code implementation for enrolling a student
        if not isinstance(student, UserProfile):
            raise ValueError("Only students can enroll in courses.")

        while True:
            try:
                if student in course.students:
                    raise ValueError(f"{student.username} is already enrolled in the course {course.title}.")
                    break

                # Email alert when a new student enrolls
                professor = course.author
                subject = f"New Student Enrolled: {student.username}"
                message = f"{student.username} has enrolled in your course '{course.title}'."
                self.send_email_alert(professor.username, subject, message)

                user_progress = CourseProgress(user=student, course=course)
                course.students.append(student)
                return user_progress
            except ValueError as ve:
                print(f"Error: {ve}")


    def send_email_alert(self, recipient_username, subject, message):
        # Replace these with your own email server details
        sender_email = "preetchaudhari05@gmail.com"
        sender_password = "svfo baqd dvkl ttkj"
        smtp_server = "smtp.gmail.com"
        smtp_port = 587

        # Get the recipient's email from the stored emails
        recipient_email = self.professor_emails.get(recipient_username)

        if recipient_email:
            # Create a secure connection to the SMTP server
            with smtplib.SMTP(smtp_server, smtp_port) as server:
                server.starttls()
                server.login(sender_email, sender_password)

                # Create the email message
                msg = MIMEText(message)
                msg['Subject'] = subject
                msg['From'] = sender_email
                msg['To'] = recipient_email

                # Send the email
                server.sendmail(sender_email, recipient_email, msg.as_string())

            print(f"Email sent to {recipient_email}: {subject}\n{message}")
        else:
            print(f"Recipient {recipient_username} not found or does not have a valid email.")


    def assign_badge(self, student, selected_course):
        """
        Assigns a badge to a student upon course completion.

        Args:
        - student: UserProfile object representing the student.
        - selected_course: Course object for which the badge is assigned.

        Comments:
        - Checks if the student has completed the course to assign a badge.
        """
        # Code implementation for assigning a badge
        if student.progress.course_completed:
            badge_decorator = CourseCompletionDecorator(user=student, badge_name="Course Completion")
            badge_decorator.decorate()
            print(f"Badge 'Course Completion' assigned to {student.username}!")
        else:
            print(f"Badge not assigned. {student.username} has not completed the course.")


    def notify(self, message, user):
        """
        Notifies a user with a message.

        Args:
        - message: Notification message to be sent.
        - user: UserProfile object representing the user to be notified.

        Returns:
        - Notification: Object representing the notification sent.

        Raises:
        - ValueError: If the notification message is empty.

        Comments:
        - Creates a Notification object and adds it to the notifications list.
        """
        # Code implementation for sending notifications
        if not message:
            raise ValueError("Notification message cannot be empty.")

        notification = Notification(content=message, user=user)
        self.notifications.append(notification)
        return notification

    def complete_quiz(self, student, quiz):
        """
        Handles quiz completion by a student.

        Args:
        - student: UserProfile object representing the student taking the quiz.
        - quiz: Quiz object representing the quiz being completed.

        Comments:
        - Initiates and grades the quiz attempt.
        - Updates student's progress based on the quiz result.
        - Assigns a badge if the quiz is completed successfully.
        """
        # Code implementation for completing a quiz
        quiz_attempt = QuizAttempt(user=student, quiz=quiz)
        quiz_attempt.take_quiz()
        grade = quiz_attempt.grade_quiz()

        print(f"\nYour Quiz Grade: {grade}%")

        if grade > 60:
            student.progress.course_completed = True
            print(f"Congratulations! You have completed the course '{quiz.course.title}'.")
        else:
            print(f"Course '{quiz.course.title}' is incomplete.")

        student.quiz_attempts.append(quiz_attempt)
        self.assign_badge(student, quiz.course)


    def save_to_json(self, data, filename):
        """
        Saves provided data to a JSON file.

        Args:
        - data: Data to be saved in JSON format.
        - filename: Name of the JSON file to save.

        Comments:
        - Writes the provided data into a JSON file.
        """
        # Code implementation for saving data to JSON
        with open(filename, 'w') as json_file:
            json.dump(data, json_file, cls=CustomEncoder)

    def save_data_to_json(self):
        """
        Prepares platform data and saves it to a JSON file.

        Comments:
        - Gathers data for users, courses, interactions, notifications, and quiz attempts.
        - Uses a custom encoder to handle complex objects before saving to a JSON file.
        """
        # Code implementation for saving platform data to JSON
        data = {
            "users": [user.__dict__ for user in self.users],
            "courses": [course.__dict__ for course in self.courses],
            "interactions": [interaction.__dict__ for interaction in self.interactions],
            "notifications": [notification.__dict__ for notification in self.notifications],
            "quiz_attempts": [quiz_attempt.__dict__ for user in self.users for quiz_attempt in user.quiz_attempts]
        }

        # Use custom encoder to handle circular references
        json_data = json.dumps(data, cls=CustomEncoder, default=lambda o: None, indent=2)

        with open(self.JSON_FILENAME, 'w') as json_file:
            json_file.write(json_data)

        print(f"Data saved to {self.JSON_FILENAME}.")


    def serialize_courses(self):
        """
        Serializes course data for storage or transfer.

        Returns:
        - serialized_courses: A list containing serialized course information.

        Comments:
        - Iterates through courses to serialize each course's details.
        - Extracts relevant information like title, description, author, modules, video lessons, quizzes, and students.
        - Converts author and related objects' attributes to dictionaries for serialization.
        - Constructs a list of serialized courses to return.
        """
        serialized_courses = []  # Initialize an empty list to store serialized course data
        for course in self.courses:
            # Serialize each course's details
            serialized_course = {
                "title": course.title,
                "description": course.description,
                "author": course.author.__dict__,  # Serialize author's attributes
                "modules": [module.__dict__ for module in course.modules],  # Serialize modules
                "video_lessons": [video_lesson.__dict__ for video_lesson in course.video_lessons],  # Serialize video lessons
                "quizzes": [quiz.__dict__ for quiz in course.quizzes],  # Serialize quizzes
                "students": [student.__dict__ for student in course.students]  # Serialize enrolled students
            }
            serialized_courses.append(serialized_course)  # Append serialized course to the list
        return serialized_courses  # Return the list of serialized courses


    def run(self):
        while True:
            print("\n=== E-Learning Platform ===")
            print("1. Professor Registration")
            print("2. Student Registration")
            print("3. Quit")

            choice = input("Enter the number of your choice: ")

            if choice == "1":
                # Professor Registration
                print("\n=== Professor Registration ===")
                professor = self.register_user()

                if professor:
                    while True:
                        print(f"\n{professor.username}, you can now manage courses.")
                        print("1. Create a course")
                        print("2. View created courses")
                        print("3. Quit")

                        manage_choice = input("Enter the number of your choice: ")

                        if manage_choice == "1":
                            self.create_course(professor)
                        elif manage_choice == "2":
                            ProfessorView.view_courses_created_with_edit_option(professor, self)
                        elif manage_choice == "3":
                            break
                        else:
                            print("Invalid option. Please enter a valid number.")

            elif choice == "2":
                # Student Registration
                print("\n=== Student Registration ===")
                student = self.register_user()

                # Display Available Courses for Student
                print("\n=== Available Courses ===")
                if not self.courses:
                    print("No courses available.")
                else:
                    for i, course in enumerate(self.courses, start=1):
                        print(f"{i}. {course.title} - {course.description}")

                    # Student Enrolls in a Course
                    while True:
                        try:
                            selected_course_index = int(input("Enter the number of the course you want to enroll in: "))
                            selected_course = self.courses[selected_course_index - 1]
                            progress = self.enroll_user(student, selected_course)
                            break
                        except (ValueError, IndexError):
                            print("Invalid input. Please enter a valid course number.")

                    # Display Options for the Student
                    print(f"\n{student.username}, you are now enrolled in {selected_course.title}.")
                    while True:
                        print("\n=== Course Interaction Options ===")
                        print("1. Show Course Modules")
                        print("2. Take Quizzes")
                        print("3. Watch Video Lessons")
                        print("4. Rate course")
                        print("5. Quit")

                        option = input("Enter the number of your choice: ")

                        if option == "1":
                            # Student Watches Course Modules
                            print("\n=== Course Modules ===")
                            for module in selected_course.modules:
                                print(f"{module.title}: {module.content}")
                        elif option == "2":
                            # Student Takes Quizzes
                            print("\n=== Course Quizzes ===")
                            for quiz in selected_course.quizzes:
                                self.complete_quiz(student, quiz)
                        elif option == "3":
                            # Student Watches Video Lessons
                            print("\n=== Course Video Lessons ===")
                            for video_lesson in selected_course.video_lessons:
                                progress.watch_video_lesson(video_lesson)
                        elif option == "4":
                            # Student Rates the Course
                            rating = int(input("Rate the course on a scale of 1 to 5: "))
                            progress.set_course_rating(rating)
                        elif option == "5":
                            break
                        else:
                            print("Invalid option. Please enter a valid number.")

            elif choice == "3":
                # Quit
                print("Exiting the E-Learning Platform. Goodbye!")
                break

            else:
                print("Invalid option. Please enter a valid number.")

if __name__ == "__main__":
    # Instantiating the E-learning platform
    elearning_platform = ElearningPlatform()

    # Running the E-learning platform
    elearning_platform.run()

    # Saving platform data to a JSON file
    elearning_platform.save_data_to_json()

"""###"""





# In[ ]:




