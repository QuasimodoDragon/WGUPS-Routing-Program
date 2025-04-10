class Package:

    # Package class constructor, default status is in hub
    def __init__(self, id, address, city, state, zip, deadline, weight, notes, status = "IN HUB"):
        self.id = id
        self.address = address
        self.city = city
        self.state = state
        self.zip = zip
        self.deadline = deadline
        self.weight = weight
        self.notes = notes
        self.status = status

    def __str__(self):
        return f'ID: {self.id}, Address: {self.address}, City: {self.city}, Zip Code: {self.zip}, Deadline: {self.deadline}, Weight (kg): {self.weight}, Status: {self.status}'