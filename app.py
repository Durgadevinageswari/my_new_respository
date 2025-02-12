import csv
import random

class SecretSantaAssigner:
    def __init__(self, employees_file: str, previous_assignments_file: str):
        self.employees_file = employees_file
        self.previous_assignments_file = previous_assignments_file
        self.employees = self._load_employees()
        self.previous_assignments = self._load_previous_assignments()

    def _load_employees(self):
        employees = []
        try:
            with open(self.employees_file, newline='') as csvfile:
                reader = csv.reader(csvfile)
                next(reader)  # Skip header
                employees = [(row[0], row[1]) for row in reader]
        except Exception as e:
            print(f"Error reading employees file: {e}")
        return employees

    def _load_previous_assignments(self):
        assignments = {}
        try:
            with open(self.previous_assignments_file, newline='') as csvfile:
                reader = csv.reader(csvfile)
                next(reader)  
                for row in reader:
                    assignments[row[1]] = row[3] 
        except Exception as e:
            print(f"Error reading previous assignments file: {e}")
        return assignments

    def assign_secret_santa(self):
        employees = self.employees[:]
        available_receivers = {email for _, email in employees}
        assignments = []

        for giver_name, giver_email in employees:
            valid_choices = available_receivers - {giver_email} - {self.previous_assignments.get(giver_email)}

            
            if not valid_choices:
                print("Assignment failed, retrying...")
                return self.assign_secret_santa()

            receiver_email = random.choice(list(valid_choices))
            receiver_name = next(name for name, email in employees if email == receiver_email)
            assignments.append((giver_name, giver_email, receiver_name, receiver_email))
            available_receivers.remove(receiver_email)

        return assignments

    def save_assignments(self, output_file: str):
        assignments = self.assign_secret_santa()
        try:
            with open(output_file, 'w', newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(["Employee_Name", "Employee_EmailID", "Secret_Child_Name", "Secret_Child_EmailID"])
                writer.writerows(assignments)
            print(f"Assignments saved to {output_file}")
        except Exception as e:
            print(f"Error saving assignments file: {e}")

assigner = SecretSantaAssigner("employees.csv", "previous_assignment.csv")
assigner.save_assignments("new_assignments.csv")
