# Capture_AttendenceSystem
Capture is an online attendence system which uses face recognition to recognize face and mark the attendance. This attendance is then stored in the MonogoDB DataBase.

# Overview 
Taking attendance is time consuming and has many flaws in it. It had become more difficult during the pandemic in the online mode where proxies are being recorded. 
The solution should be in such a way that it should live to the standards of the current evolving world (not the outdated methods) and with most accuracy.

# Goals 
### Machine Learning: 
The problem of attendance can be solved using current major technologies like ML. This project uses Machine Learning in order to identify the person in front of camera to mark the attendance.

### <u>Facial Recognition:</u>
Using Facial Recognition we identify the person in front of the camera and mark the attendance accordingly.

### Interface: 
This project has two different interfaces, one for faculty and other for students to mark their attendance. Faculty can generate the pin for marking attendance in certain period of time and students using that pin can mark their attendance in the interface provided

### DataBase: 
The recorded attendance will be stored inside the database marking the students who are present. (All the details of the students are present earlier in the database with their images to compare against)

# Working Methodology
The project is developed to mark the attendance of students using facial recognition. Inorder to start taking attendance the faculty need to generate a pin inside the interface provided. This pin is random and defines which faculty is taking attendance at which day and time. Students need to enter this pin in another interface which will be authenticated and need to sit in front of the camera. The ML algorithm runs against the person and marks him present. This data is transferred into the database where all the students' attendance will be recorded.

# Specifications 

Flask server to run the python code in the backend. 
HTML, Js for making interface
OpenCV for Facial Recognition.
MongoDB for Storing the attendance Data
