# Student ID: 011012738

import csv
import datetime
from package import Package
from hashtable import HashTable
from truck import Truck

# Create the hash table to store package objects
PackageTable = HashTable()

# File path for the csv package data
file_path = "data/packages.csv"

# TODO make this a function?
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
        return float(distance)
    # If the distance is empty then the indexes are swapped and the distance is returned
    else:
        distance = distance_matrix[index_2][index_1]
        return float(distance)


# ------------- Nearest Address Function -------------

def nearest_address(truck):
    # Holds the truck package list and its current address
    package_list = truck.packages
    current_address = truck.current_address
    # Holds a large number so that the first package in the loop automatically becomes the shortest
    shortest_dist = float(100)
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


# ------------- Deliver Function -------------

# TODO pre-sort packages list with nearest addresses instead of every while loop
# Deliver function uses nearest neighbor algorithm to deliver the packages
def deliver(truck):
    # While the truck packages list isn't empty it loops through and delivers the packages
    while len(truck.packages) > 0:
        package_list = truck.packages
        # Calculates the nearest package address and the distance away from current address
        next_address = nearest_address(truck)
        distance = betwixt(truck.current_address, next_address)

        # Loops through all packages in list and changes status to en route for all going to next address
        for package in package_list:
            if package.address == next_address:
                package.status = "EN ROUTE"
        
        # Truck mileage is updated and time to deliver is calculated and added to total time
        truck.mileage += distance

        # Time to deliver and time updating cited from C950 WGUPS Project Implementation Steps - Example - Nearest Neighbor,
        # https://srm--c.vf.force.com/apex/CourseArticle?id=kA03x000001DbBGCA0&groupId=&searchTerm=&courseCode=C950&rtn=/apex/CommonsExpandedSearch
        # Formula: time = distance / speed
        time_to_deliver = distance / 18
        truck.time = truck.time + datetime.timedelta(hours=time_to_deliver)
        truck.current_address = next_address

        # Loops through package list and updates package delivery information
        for package in package_list:
            if package.address == next_address:
                package.status = "DELIVERED"
                package.delivery_time = truck.time
                # Adds package to the delivered list and removes it from the original package list
                truck.packages_delivered.append(package)
                truck.packages.remove(package)
                print(package.__str__() + ", took " + str(round(time_to_deliver * 60, 2)) + " minutes to deliver")

    print("Truck mileage: " + str(truck.mileage))


# ------------- Back to Hub -------------

def back_to_hub(truck):
    dist_to_hub = betwixt(truck.current_address, address_list[0])
    truck.mileage += dist_to_hub

    time_to_hub = dist_to_hub / 18
    truck.time = truck.time + datetime.timedelta(hours=time_to_hub)
    truck.current_address = address_list[0]

# ------------- Create and Load the trucks -------------

# Create the truck objects
Truck_1 = Truck()
Truck_2 = Truck()
Truck_3 = Truck()

# Add truck package id's to lists to make loading easier
truck_1_package_ids = [1,7,13,14,15,16,19,20,21,29,30,31,34,37,39,40]
truck_2_package_ids = [2,3,5,6,9,12,18,25,26,27,28,32,33,35,36,38]
truck_3_package_ids = [4,8,10,11,17,22,23,24]


# For loops used to add packages to the trucks using the package id lists
for package_id in truck_1_package_ids:
    Truck_1.load(PackageTable.get_package(package_id))

for package_id in truck_2_package_ids:
    Truck_2.load(PackageTable.get_package(package_id))

for package_id in truck_3_package_ids:
    Truck_3.load(PackageTable.get_package(package_id))


# ------------- Deliver Packages -------------

deliver(Truck_1)

Truck_2.time = datetime.timedelta(hours=9, minutes=5)
deliver(Truck_2)

# There are only 2 drivers, truck 3 can only deliver once another truck is finished
if Truck_1.time < Truck_2.time:
    back_to_hub(Truck_1)
else:
    back_to_hub(Truck_2)

Truck_3.time = min(Truck_1.time, Truck_2.time)
deliver(Truck_3)

print("Total Mileage: " + str(Truck_1.mileage + Truck_2.mileage + Truck_3.mileage))

# ------------- Test -------------

