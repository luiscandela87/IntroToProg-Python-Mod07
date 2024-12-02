import json  # Importing json module to work with JSON data files

# Define the Data Constants
MENU: str = '''  # Defining the menu constant as a string
---- Course Registration Program ----
  Select from the following menu:
    1. Register a Student for a Course.
    2. Show current data.
    3. Save data to a file.
    4. Exit the program.
-----------------------------------------
'''

FILE_NAME: str = "Enrollments.json"  # Define the file name for saving/loading student data

# Define the Data Variables
students: list = []  # A list to hold student data (initially empty)
menu_choice: str  # Variable to hold the user's menu choice

# Define the Person Class (Base Class)
class Person:
    # A class that represents a person with a first name, last name, and course name.

    def __init__(self, first_name: str = '', last_name: str = ''):
        # Initialize the Person object with first name, last name, and course name.
        self.__first_name = first_name
        self.__last_name = last_name

    @property
    def first_name(self):
        # Getter for first_name property, returns the title-cased first name.
        return self.__first_name.title()

    @first_name.setter
    def first_name(self, value: str):
        # Setter for first_name property, ensures value is alphabetic or empty.
        if value.isalpha() or value == "":
            self.__first_name = value
        else:
            raise ValueError("The first name should not contain numbers.")

    @property
    def last_name(self):
        # Getter for last_name property, returns the title-cased last name.
        return self.__last_name.title()

    @last_name.setter
    def last_name(self, value: str):
        # Setter for last_name property, ensures value is alphabetic or empty.
        if value.isalpha() or value == "":
            self.__last_name = value
        else:
            raise ValueError("The last name should not contain numbers.")

    def __str__(self):
        # Override the __str__() method to return a formatted string representation of the Person.
        return f'{self.first_name} {self.last_name}'  # Returning the person's full name


# Define the Student Class (Derived Class from Person)
class Student(Person):
    # A subclass that represents a student. Inherits from Person class.
    # Adds functionality specific to students, such as course name.

    def __init__(self, first_name: str = '', last_name: str = '', course_name: str = ''):
        # Initialize the Student object with first name, last name, and course name.
        super().__init__(first_name=first_name, last_name=last_name)
        self.__course_name = course_name

    @property
    def course_name(self):
        # Getter for course_name property.
        return self.__course_name

    @course_name.setter
    def course_name(self, value: str):
        # Setter for course_name property.
        if isinstance(value, str) and value.strip():
            self.__course_name = value
        else:
            raise ValueError("Course name must be a non-empty string.")

    def __str__(self):
        # Override __str__() method to include course information.
        return f'{super().__str__()} is enrolled in {self.course_name}'  # Calls Person's __str__


# Processing Layer (File handling and data loading/saving)
class FileProcessor:
    # A class to process reading and writing student data from/to a JSON file.

    @staticmethod
    def read_data_from_file(file_name: str, student_data: list):
        # Reads data from a JSON file and loads it into a list of dictionaries.
        try:
            with open(file_name, "r") as file:
                student_dicts = json.load(file)  # Load data from the file as a list of dictionaries
                # Convert dictionaries back to Student objects
                for student_dict in student_dicts:
                    student = Student(
                        first_name=student_dict["FirstName"],
                        last_name=student_dict["LastName"],
                        course_name=student_dict["CourseName"]
                    )
                    student_data.append(student)
        except Exception as e:
            IO.output_error_messages(message="Error: There was a problem with reading the file.", error=e)
        return student_data

    @staticmethod
    def write_data_to_file(file_name: str, student_data: list):
        # Writes student data to a JSON file.
        try:
            # Convert Student objects to dictionaries before saving
            student_dicts = [{
                "FirstName": student.first_name,
                "LastName": student.last_name,
                "CourseName": student.course_name
            } for student in student_data]
            with open(file_name, "w") as file:
                json.dump(student_dicts, file)  # Save list of dictionaries
            IO.output_student_and_course_names(student_data)  # Display saved data
        except Exception as e:
            message = "Error: There was a problem with writing to the file.\nPlease check that the file is not open by another program."
            IO.output_error_messages(message=message, error=e)


# Presentation Layer (Handling user input and output)
class IO:
    # A collection of functions that manage user input/output.

    @staticmethod
    def output_error_messages(message: str, error: Exception = None):
        # Displays error messages to the user.
        print(message, end="\n\n")
        if error is not None:
            print("-- Technical Error Message -- ")
            print(error, error.__doc__, type(error), sep='\n')

    @staticmethod
    def output_menu(menu: str):
        # Displays the main menu to the user.
        print()  # Adding extra space to make it look nicer.
        print(menu)
        print()  # Adding extra space to make it look nicer.

    @staticmethod
    def input_menu_choice():
        # Prompts the user to enter a menu choice.
        choice = "0"
        try:
            choice = input("Enter your menu choice number: ")
            if choice not in ("1", "2", "3", "4"):  # Ensure valid choice
                raise Exception("Please, choose only 1, 2, 3, or 4")
        except Exception as e:
            IO.output_error_messages(e.__str__())  # Display error message

        return choice

    @staticmethod
    def output_student_courses(student_data: list):
        # Displays the names and courses of all registered students.
        print("-" * 50)
        for student in student_data:
            print(student)  # Automatically calls the __str__ method of the Student class
        print("-" * 50)

    @staticmethod
    def input_student_data(student_data: list):
        # Prompts the user for a student's details and adds them to the student_data list.
        try:
            # Get student details
            student_first_name = input("Enter the student's first name: ")
            if not student_first_name.isalpha():
                raise ValueError("First name should only contain letters.")
            student_last_name = input("Enter the student's last name: ")
            if not student_last_name.isalpha():
                raise ValueError("Last name should only contain letters.")
            course_name = input("Please enter the name of the course: ")

            # Create a Student object and add it to the list
            student = Student(first_name=student_first_name, last_name=student_last_name, course_name=course_name)
            student_data.append(student)
            print(f"You have registered {student_first_name} {student_last_name} for {course_name}.")
        except ValueError as e:
            IO.output_error_messages(message="Input data is not valid!", error=e)
        except Exception as e:
            IO.output_error_messages(message="Error: There was a problem with your entered data.", error=e)
        return student_data


# Main Program Execution

# When the program starts, read the file data into a list of students
students = FileProcessor.read_data_from_file(file_name=FILE_NAME, student_data=students)

# Main program loop
while True:
    # Show the menu to the user
    IO.output_menu(menu=MENU)

    # Get the user's menu choice
    menu_choice = IO.input_menu_choice()

    # Handle user choice
    if menu_choice == "1":
        # Register a new student
        students = IO.input_student_data(student_data=students)
        continue
    elif menu_choice == "2":
        # Show current student data
        IO.output_student_courses(students)
        continue
    elif menu_choice == "3":
        # Save data to file
        FileProcessor.write_data_to_file(file_name=FILE_NAME, student_data=students)
        continue
    elif menu_choice == "4":
        # Exit the program
        break
    else:
        print("Please only choose option 1, 2, 3, or 4")

print("Program Ended")  # Indicate program termination
