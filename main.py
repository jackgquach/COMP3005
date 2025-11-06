#!/usr/bin/env python3
"""
Simple Student Management System
Demonstrates all CRUD functions directly
"""

import operations

def main():
    print("STUDENT MANAGEMENT SYSTEM DEMONSTRATION")
    print("-" * 50)
    
    # First, setup the database
    print("\nSETTING UP DATABASE...")
    operations.setup_database()
    
    # Test connection
    print("\nTESTING DATABASE CONNECTION...")
    operations.test_connection()

    input("\nPress Enter to continue.")
    
    # Display all students (initial data)
    print("\nDISPLAYING ALL STUDENTS (Initial Data)")
    operations.getAllStudents()

    input("\nPress Enter to continue.")

    # Add a new student
    print("\nADDING A NEW STUDENT")
    operations.addStudent("Alice", "Johnson", "alice.johnson@example.com", "2023-09-03")
    
    # Display all students again to show the new addition
    print("\nDISPLAYING ALL STUDENTS (After Adding Alice)")
    operations.getAllStudents()

    input("\nPress Enter  to continue.")
    
    # Update a student's email
    print("\nUPDATING STUDENT EMAIL")
    operations.updateStudentEmail(1, "john.doe.updated@example.com")
    
    # Display all students to show the updated email
    print("\nDISPLAYING ALL STUDENTS (After Email Update)")
    operations.getAllStudents()

    input("\nPress Enter to continue.")
    
    # Delete a student
    print("\nDELETING A STUDENT")
    operations.deleteStudent(2)  # Delete Jane Smith
    
    # Final display of all students
    print("\nFINAL LIST OF STUDENTS")
    operations.getAllStudents()

    input("\nPress Enter to continue.")
    
    print("\nDEMONSTRATION COMPLETED!")
    print("All CRUD operations have been successfully demonstrated.")

if __name__ == "__main__":
    main()