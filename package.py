class Package:

    # Package class constructor, default status is in hub
    def __init__(self, id, address, city, state, zip, deadline, weight, notes, status = "IN HUB", delivery_time = 0):
        self.id = id
        self.address = address
        self.city = city
        self.state = state
        self.zip = zip
        self.deadline = deadline
        self.weight = weight
        self.notes = notes
        self.status = status
        self.delivery_time = delivery_time

    # Returns a a string of the package's data
    def __str__(self):
        return f'ID: {self.id}, Address: {self.address}, City: {self.city}, Zip Code: {self.zip}, Deadline: {self.deadline}, Weight (kg): {self.weight}, Status: {self.status}, Delivered at {self.delivery_time}'