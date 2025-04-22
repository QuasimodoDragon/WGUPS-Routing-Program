class Package:

    # Package class constructor, default status is in hub
    def __init__(self, id, address, city, state, zip, deadline, weight, notes, status = "IN HUB", truck = None):
        self.id = id
        self.address = address
        self.city = city
        self.state = state
        self.zip = zip
        self.deadline = deadline
        self.weight = weight
        self.notes = notes
        self.status = status
        self.truck = truck
        self.delivery_time = None

    # Returns a a string of the package's data
    def __str__(self):
        if self.status == "DELIVERED":
            return f'ID: {self.id}, Address: {self.address}, City: {self.city}, Zip Code: {self.zip}, Deadline: {self.deadline}, Weight (kg): {self.weight}, Truck: {self.truck}, Status: {self.status}, Delivered on {self.delivery_time}'
        else:
            return f'ID: {self.id}, Address: {self.address}, City: {self.city}, Zip Code: {self.zip}, Deadline: {self.deadline}, Weight (kg): {self.weight}, Truck: {self.truck}, Status: {self.status}'