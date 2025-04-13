class Truck:

    def __init__(self, mileage = 0):
        self.packages = []
        self.mileage = mileage

    def load(self, package):
        # Get the length of the packages list
        length = len(self.packages)

        # A truck can only hold 16 packages. If the list is at capacity return none
        if length >= 16:
            return None
        # If the packages list is not at capacity add the package to the list
        else:
            self.packages.append(package)

    def unload(self, id):
        # Loops through all packages in the package list
        for package in self.packages:
            # If the passed id matches the package id then it is removed from the package list
            if package.id == id:
                self.packages.remove(package)
            else:
                return None

    # Adds mileage to the truck
    def add_mileage(self, num):
        self.mileage += num