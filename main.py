# Student ID: 011012738

import csv
from package import Package
from hashtable import HashTable
from truck import Truck

# Create the hash table to store package objects
PackageTable = HashTable()

# File path for the csv package data
file_path = "data/packages.csv"

# TODO make this a function
# Reads the packages csv file and uses the data to create a package object and add it to the package hash table
# Surround with a try block to catch exceptions
try:
    # Opens the packages csv file and reads the data
    with open(file_path, "r") as csv_file:
        # Holds the csv content in reader with a comma delimiter
        reader = csv.reader(csv_file, delimiter=',')
        # Skips the header row
        next(reader)

        # Loops through the rows and adds the column data to create a package object
        for row in reader:
            id = int(row[0])
            address = row[1]
            city = row[2]
            state = row[3]
            zip = row[4]
            deadline = row[5]
            weight = row[6]
            notes = row[7]

            # Creates a package object from the csv data
            package = Package(id, address, city, state, zip, deadline, weight, notes)
            # Adds the package object to the package hash table
            PackageTable.add(id, package)
# If the file is not found print this exception
except FileNotFoundError:
    print("The file was not found")
# If the user doesn't have permission to open the file print the exception
except PermissionError:
    print("Permission to open the file not granted")

# ------------- Distance Matrix ------------- 

# Create a distance matrix that will become a 2D array
distance_matrix = []

# Open the distances csv file and use it to create the distance matrix
with open("data/distances.csv", "r") as csv_file:
    reader = csv.reader(csv_file, delimiter=",")

    # Add every row to the distance matrix to create a 2D array
    for row in reader:
        distance_matrix.append(row)

# ------------- Address List -------------

# Create an array to hold the addresses
address_list = []

# Open the addresses csv file and use it to create the address list
with open("data/addresses.csv", "r") as csv_file:
    reader = csv.reader(csv_file, delimiter=",")
    # Skip the header row
    next(reader)

    # For every row add only the address to the array
    for row in reader:
        address_list.append(row[1])

# ------------- Distance Betwixt Function -------------

# Function that returns the distance between two addresses
def betwixt(address_1, address_2):
    # Gets the index of both addresses from the address list
    index_1 = address_list.index(address_1)
    index_2 = address_list.index(address_2)
    # Uses the indexes to find the distance between the addresses from the distance matrix
    distance = distance_matrix[index_1][index_2]

    # The distance matrix is only half filled so if statement returns if the distance is not empty
    if distance != "":
        return distance
    # If the distance is empty then the indexes are swapped and the distance is returned
    else:
        distance = distance_matrix[index_2][index_1]
        return float(distance)

# ------------- Nearest Address Function -------------

def nearest_address(truck, current_address):
    package_list = truck.packages
    # Holds a large number so that the first package in the loop automatically becomes the shortest
    shortest_dist = 100
    nearest = None

    # Loops through all of the package objects in the truck's package list
    for package in package_list:
        # Holds the package address
        dest_address = package.address
        # Uses the betwixt function to get the distance between package address and current address
        distance = betwixt(current_address, dest_address)

        # If the distance is shorter than the shortest distance then update the nearest address and the shortest dist
        if distance < shortest_dist:
            shortest_dist = distance
            nearest = dest_address
    
    return nearest

# Create the truck objects
Truck_1 = Truck()
Truck_2 = Truck()
# Truck 3 likely won't be used since there are only 2 drivers
Truck_3 = Truck()

# Can only be loaded on truck 2
Truck_2.load(PackageTable.get_package(3))
Truck_2.load(PackageTable.get_package(18))
Truck_2.load(PackageTable.get_package(36))
Truck_2.load(PackageTable.get_package(38))

# Load the rest of truck 2
Truck_2.load(PackageTable.get_package(23))
Truck_2.load(PackageTable.get_package(24))
Truck_2.load(PackageTable.get_package(26))
Truck_2.load(PackageTable.get_package(27))
Truck_2.load(PackageTable.get_package(29))
Truck_2.load(PackageTable.get_package(30))
Truck_2.load(PackageTable.get_package(31))
Truck_2.load(PackageTable.get_package(33))
Truck_2.load(PackageTable.get_package(34))
Truck_2.load(PackageTable.get_package(35))
Truck_2.load(PackageTable.get_package(37))
Truck_2.load(PackageTable.get_package(39))

# Packages 13, 15, 19 need to be delivered together
Truck_1.load(PackageTable.get_package(13))
Truck_1.load(PackageTable.get_package(15))
Truck_1.load(PackageTable.get_package(19))

# Load the rest of truck 1
Truck_1.load(PackageTable.get_package(1))
Truck_1.load(PackageTable.get_package(2))
Truck_1.load(PackageTable.get_package(4))
Truck_1.load(PackageTable.get_package(5))
Truck_1.load(PackageTable.get_package(7))
Truck_1.load(PackageTable.get_package(8))
Truck_1.load(PackageTable.get_package(10))
Truck_1.load(PackageTable.get_package(11))
Truck_1.load(PackageTable.get_package(12))
Truck_1.load(PackageTable.get_package(14))
Truck_1.load(PackageTable.get_package(20))
Truck_1.load(PackageTable.get_package(21))
Truck_1.load(PackageTable.get_package(22))

# Delayed
# Truck_1.load(PackageTable.get_package(6))
# Truck_2.load(PackageTable.get_package(25))
# Truck_2.load(PackageTable.get_package(28))
# Truck_2.load(PackageTable.get_package(32))

# Wrong address
# Truck_1.load(PackageTable.get_package(9))


# ------------- Test -------------

# Truck_1.unload(22)
yo = nearest_address(Truck_2, "4001 South 700 East")
print(yo)