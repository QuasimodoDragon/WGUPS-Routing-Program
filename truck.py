class Truck:

    def __init__(self):
        self.packages = []

    def load(self, package):
        # Get the length of the packages list
        length = self.packages.len()

        # A truck can only hold 16 packages. If the list is at capacity return none
        if length >= 16:
            return None
        # If the packages list is not at capacity add the package to the list
        else:
            self.packages.append(package)