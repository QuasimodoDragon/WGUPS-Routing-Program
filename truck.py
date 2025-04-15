import datetime

class Truck:

    def __init__(self, current_address = "4001 South 700 East", mileage = 0, time = datetime.timedelta(hours=8)):
        self.packages = []
        self.packages_delivered = []
        self.current_address = current_address
        self.mileage = mileage
        self.time = time

    def load(self, package):
        # Get the length of the packages list
        length = len(self.packages)

        # A truck can only hold 16 packages. If the list is at capacity return none
        if length >= 16:
            return None
        # If the packages list is not at capacity add the package to the list
        else:
            self.packages.append(package)