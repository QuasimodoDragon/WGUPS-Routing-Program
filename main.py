import csv
from package import Package
from hashtable import HashTable
from truck import Truck

# Create the hash table to store package objects
packageTable = HashTable()

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
            packageTable.add(id, package)
# If the file is not found print this exception
except FileNotFoundError:
    print("The file was not found")
# If the user doesn't have permission to open the file print the exception
except PermissionError:
    print("Permission to open the file not granted")

# print(packageTable.lookup(3))

# truck1 = Truck()
# truck1.add(packageTable.lookup(2))
# print(truck1.packages[0].__str__())

# ------------- Distance Matrix ------------- 

# Create a distance matrix that will become a 2D array
distance_matrix = []

# Open the distances csv file and use it to create the distance matrix
with open("data/distances.csv", "r") as csv_file:
    reader = csv.reader(csv_file, delimiter=",")

    # Add every row to the distance matrix to create a 2D array
    for row in reader:
        distance_matrix.append(row)

# print(distance_matrix[3][2])


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

# print(address_list)

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
        return distance

# print(betwixt("300 State St", "1330 2100 S"))