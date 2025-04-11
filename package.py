class Package:

    # Package class constructor
    def __init__(self, id, address, city, state, zip, deadline, weight, notes, status = "In hub"):
        self.id = id
        self.address = address
        self.city = city
        self.state = state
        self.zip = zip
        self.deadline = deadline
        self.weight = weight
        self.notes = notes
        self.status = status