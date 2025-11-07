import psycopg2

# Database configuration
DB_CONFIG = {
    'host': 'localhost',
    'database': 'COMP3005 A3',
    'user': 'postgres',
    'password': 'password',
    'port': '5432'
}

def start_db_connection():
    """
    Establish and return a connection to PostgreSQL database.
    Parameters: 
        None.
    Returns: connection object or None if failed.
    """
    try:
        connection = psycopg2.connect(**DB_CONFIG)
        return connection
    except psycopg2.Error as e:
        print(f"ERROR connecting to database: {e}")
        print("Please check your database configuration in operations.py")
        return None

def close_db_connection(connection):
    """
    Close database connection.
    Parameters:
        connection: PostgreSQL connection object.
    """
    if connection:
        connection.close()

def execute_db_query(connection, query, params=None, fetch=False):
    """
    Execute SQL query with optional parameters.
    Parameters:
        connection: Database connection object.
        query: SQL query string.
        params: Tuple of parameters for the query.
        fetch: Boolean indicating if results should be fetched.
    Returns: Query results if fetch=True, otherwise number of affected rows (usually 1).
    """
    try:
        # Cursor acts as a 'pointer' to execute SQL and retrieve values.
        with connection.cursor() as cursor:
            cursor.execute(query, params)
            if fetch:
                # If operation returns items, return it with the cursor.
                return cursor.fetchall()
            # Make changes to databases permanent once operation is complete.
            connection.commit()
            return cursor.rowcount
        
    # Any errors regarding the database using the cursor.
    except psycopg2.Error as e:
        print(f"Database error: {e}")
        # Undo any partial changes to the database.
        connection.rollback()
        return None

def setup_database():
    """
    Create database schema and insert initial data.
    Parameters:
        None.
    Returns: Boolean indicating success
    """

    connection = start_db_connection()
    if not connection:
        return False
    
    try:
        # Create database using schema.
        with open("database/schema.sql", 'r') as file:
            schema_sql = file.read()
        execute_db_query(connection, schema_sql)
        print("Database schema created successfully.")
        
        # Fill in database with inital values.
        with open("database/initial_data.sql", 'r') as file:
            data_sql = file.read()
        execute_db_query(connection, data_sql)
        print("Initial data inserted successfully.")
        
        close_db_connection(connection)
        return True
        
    except FileNotFoundError as e:
        print(f"SQL file not found: {e}")
        close_db_connection(connection)
        return False
    except Exception as e:
        print(f"Error setting up database: {e}")
        close_db_connection(connection)
        return False

def getAllStudents():
    """
    Retrieves and displays all records from the students table.
    Parameters:
        None.
    Returns: List of student records or None if error.
    """
    
    connection = start_db_connection()
    if not connection:
        return None
    
    query = """
    SELECT student_id, first_name, last_name, email, enrollment_date 
    FROM students 
    ORDER BY student_id
    """
    
    students = execute_db_query(connection, query, fetch=True)
    close_db_connection(connection)
    
    if students:
        # Algin values
        print(f"{'ID':<5} {'First Name':<15} {'Last Name':<15} {'Email':<35} {'Enrollment Date':<15}")
        print("-" * 90)
        for student in students:
            print(f"{student[0]:<5} {student[1]:<15} {student[2]:<15} {student[3]:<35} {str(student[4]):<15}")
        print(f"\nTotal students: {len(students)}")
    else:
        print("No students found in the database.")
    
    return students

def addStudent(first_name, last_name, email, enrollment_date):
    """
    Inserts a new student record into the students table.
    Parameters:
        first_name: Student's first name.
        last_name: Student's last name.
        email: Student's email address.
        enrollment_date: Student's enrollment date (YYYY-MM-DD).
    Returns: Boolean indicating success.
    """
    
    # Validate input
    if not all([first_name, last_name, email, enrollment_date]):
        print("All fields are required.")
        return False
    
    connection = start_db_connection()
    if not connection:
        return False
    
    query = """
    INSERT INTO students (first_name, last_name, email, enrollment_date) 
    VALUES (%s, %s, %s, %s)
    """
    
    params = (first_name, last_name, email, enrollment_date)
    
    try:
        result = execute_db_query(connection, query, params)
        close_db_connection(connection)
        
        if result is not None and result > 0:
            print("Student added successfully.")
            return True
        else:
            print("Failed to add student. Student may already exist.")
            return False
            
    # Handle errors regarding database.
    except psycopg2.IntegrityError as e:
        print(f"Error: Email '{email}' already exists in the database.")
        close_db_connection(connection)
        return False
    except Exception as e:
        print(f"Error adding student: {e}")
        close_db_connection(connection)
        return False

def updateStudentEmail(student_id, new_email):
    """
    Updates the email address for a student with the specified student_id.
    Parameters:
        student_id: ID of the student to update.
        new_email: New email address.
    Returns: Boolean indicating success.
    """
    
    # Validate input
    if not new_email:
        print("Email cannot be empty.")
        return False
    
    connection = start_db_connection()
    if not connection:
        return False
    
    # First check if student exists
    check_query = "SELECT first_name, last_name FROM students WHERE student_id = %s"
    student = execute_db_query(connection, check_query, (student_id,), fetch=True)
    
    if not student:
        print(f"Student with ID {student_id} not found.")
        close_db_connection(connection)
        return False
    
    query = "UPDATE students SET email = %s WHERE student_id = %s"
    params = (new_email, student_id)
    
    try:
        result = execute_db_query(connection, query, params)
        close_db_connection(connection)
        
        if result is not None and result > 0:
            print(f"Email updated successfully for {student[0][0]} {student[0][1]} (ID: {student_id}).")
            return True
        else:
            print("Failed to update email.")
            return False
            
    except psycopg2.IntegrityError as e:
        print(f"Error: Email '{new_email}' already exists in the database.")
        close_db_connection(connection)
        return False
    except Exception as e:
        print(f"Error updating email: {e}")
        close_db_connection(connection)
        return False

def deleteStudent(student_id):
    """
    Deletes the record of the student with the specified student_id
    Args:
        student_id: ID of the student to delete
    Returns: Boolean indicating success
    """
    
    connection = start_db_connection()
    if not connection:
        return False
    
    # First check if student exists and get their name
    check_query = "SELECT first_name, last_name FROM students WHERE student_id = %s"
    student = execute_db_query(connection, check_query, (student_id,), fetch=True)
    
    if not student:
        print(f"Student with ID {student_id} not found.")
        close_db_connection(connection)
        return False
    
    query = "DELETE FROM students WHERE student_id = %s"
    
    try:
        result = execute_db_query(connection, query, (student_id,))
        close_db_connection(connection)
        
        if result is not None and result > 0:
            print(f"Student {student[0][0]} {student[0][1]} (ID: {student_id}) deleted successfully.")
            return True
        else:
            print("Failed to delete student.")
            return False
            
    except Exception as e:
        print(f"Error deleting student: {e}")
        close_db_connection(connection)
        return False

def test_connection():
    """
    Test database connection - useful for debugging
    """
    connection = start_db_connection()
    if connection:
        print("SUCCESSFUL DATABASE CONNECTION")
        close_db_connection(connection)
        return True
    return False