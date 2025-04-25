class Package:

    # Package class constructor, default status is in hub
    def __init__(self, id, address, city, state, zip, deadline, weight, notes, status = "IN HUB", truck = None, delayed = False):
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
        self.en_route_time = None
        self.delivery_time = None
        self.delayed = delayed

    # Returns a a string of the package's data
    def __str__(self):
        if self.status == "DELIVERED":
            return f'ID: {self.id}, Address: {self.address}, City: {self.city}, Zip Code: {self.zip}, Deadline: {self.deadline}, Weight (kg): {self.weight}, Truck: {self.truck}, Status: {self.status}, Delivered on {self.delivery_time}'
        else:
            return f'ID: {self.id}, Address: {self.address}, City: {self.city}, Zip Code: {self.zip}, Deadline: {self.deadline}, Weight (kg): {self.weight}, Truck: {self.truck}, Status: {self.status}'
        
    # Sets status corresponding to time parameter and object attributes
    def set_status(self, time_delta):
        if self.delayed is True and time_delta < self.en_route_time:
            self.status = "DELAYED"
        elif time_delta < self.en_route_time:
            self.status = "IN HUB"
        elif time_delta >= self.en_route_time and time_delta < self.delivery_time:
            self.status = "EN ROUTE"
        elif time_delta >= self.delivery_time:
            self.status = "DELIVERED"