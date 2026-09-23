import sqlite3

# Connect to SQLite database (this creates the database file if it does not exist)
connection = sqlite3.connect("company.db")
cursor = connection.cursor()

# Drop old tables if they exist so the script can be run again without duplicate data
cursor.execute("DROP TABLE IF EXISTS employee")
cursor.execute("DROP TABLE IF EXISTS department")

# Create the department table
cursor.execute(
    """
    CREATE TABLE department (
        id INTEGER PRIMARY KEY,
        name TEXT,
        location TEXT
    )
    """
)

# Create the employee table
cursor.execute(
    """
    CREATE TABLE employee (
        id INTEGER PRIMARY KEY,
        name TEXT,
        deptid INTEGER
    )
    """
)

# Insert 5 dummy records into the department table
# This data is designed to support later JOIN examples
# (one department has no employees, and one employee has no matching department)
departments = [
    (1, "HR", "Delhi"),
    (2, "IT", "Bengaluru"),
    (3, "Sales", "Mumbai"),
    (4, "Finance", "Hyderabad"),
    (5, "Support", "Chennai")
]

cursor.executemany(
    "INSERT INTO department (id, name, location) VALUES (?, ?, ?)",
    departments
)

# Insert 5 dummy records into the employee table
# One employee has a deptid that does not match any department
# One department has no assigned employees
employees = [
    (101, "Aman Sharma", 1),
    (102, "Neha Verma", 2),
    (103, "Rohan Mehta", 99),
    (104, "Priya Nair", 1),
    (105, "Suresh Iyer", 5)
]

cursor.executemany(
    "INSERT INTO employee (id, name, deptid) VALUES (?, ?, ?)",
    employees
)

# Save the changes to the database
connection.commit()

# Execute SQL to fetch all employees
cursor.execute("SELECT id, name, deptid FROM employee ORDER BY id")
employee_rows = cursor.fetchall()

# Execute SQL to fetch all departments
cursor.execute("SELECT id, name, location FROM department ORDER BY id")
department_rows = cursor.fetchall()

# Query to find employees who work in the HR department
cursor.execute(
    """
    SELECT e.name
    FROM employee e
    JOIN department d ON e.deptid = d.id
    WHERE d.name = 'HR'
    ORDER BY e.name
    """
)
hr_employees = cursor.fetchall()

# Print employee records in a beginner-friendly format
print("Employees:")
print("ID | Name | DeptID")
print("------------------")
for emp_id, name, deptid in employee_rows:
    print(f"{emp_id:<3} | {name:<15} | {deptid}")

print()

# Print department records in a beginner-friendly format
print("Departments:")
print("ID | Name | Location")
print("-----------------------------")
for dept_id, name, location in department_rows:
    print(f"{dept_id:<2} | {name:<10} | {location}")

print()

# Print employees working in HR
print("Employees in HR:")
if hr_employees:
    for (name,) in hr_employees:
        print(name)
else:
    print("No employees found in HR")

# Close the cursor and database connection properly
cursor.close()
connection.close()
