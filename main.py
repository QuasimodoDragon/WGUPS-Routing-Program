# Kevin Bailey
# Student ID: 011012738

import csv
import datetime
from datetime import datetime as dt
from package import Package
from hashtable import HashTable
from truck import Truck

# ------------- Package Table -------------

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


# ------------- Update Special Package Information -------------

delayed_pacakge_id = [6,25,28,32]

for id in delayed_pacakge_id:
    package = PackageTable.get_package(id)
    package.status = "DELAYED"


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


# ------------- Update Status Record Function -------------

# Creates a dictionary to hold all of the update times and a dictionary of packages and their statuses
status_record = {}

def update_status_record(time):
    # A dictionary to hold packages and their status
    package_status_dict = {}

    # loop through every package in the package table
    for i in range(1, PackageTable.length + 1):
        package = PackageTable.get_package(i)
        # Updates the package status dictionary
        package_status_dict.update({package.__str__(): package.status})
    
    # Adds a time key with the package status dictionary as the value to the status record
    status_record.update({time: package_status_dict})


# ------------- Status Record List -------------

# Holds the earliest time before any truck leaves the hub
earliest_time = datetime.timedelta(hours=7, minutes=30)

# Updates the status record using the earliest time as the key
update_status_record(earliest_time)


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
    package_list = truck.packages

    # Loops through all packages in list and changes status to en route
    for package in package_list:
            package.status = "EN ROUTE"
    
    # Updates the status record once packages are set to en route
    update_status_record(truck.time)

    # While the truck packages list isn't empty it loops through and delivers the packages
    while len(truck.packages) > 0:
        # Calculates the nearest package address and the distance away from current address
        next_address = nearest_address(truck)
        distance = betwixt(truck.current_address, next_address)
        
        # Truck mileage is updated and time to deliver is calculated and added to total time
        truck.mileage += distance

        # Time to deliver and time updating cited from C950 WGUPS Project Implementation Steps - Example - Nearest Neighbor,
        # https://srm--c.vf.force.com/apex/CourseArticle?id=kA03x000001DbBGCA0&groupId=&searchTerm=&courseCode=C950&rtn=/apex/CommonsExpandedSearch
        # Formula: time = distance / speed
        time_to_deliver = distance / 18
        truck.time = truck.time + datetime.timedelta(hours=time_to_deliver)
        # Updates truck currrent address to the address just delivered to
        truck.current_address = next_address

        # Loops through package list and updates package delivery information
        for package in package_list:
            if package.address == next_address:
                package.status = "DELIVERED"
                package.delivery_time = truck.time
                # Adds package to the delivered list and removes it from the original package list
                truck.packages_delivered.append(package)
                truck.packages.remove(package)
                # print(package.__str__())
                # print(package.__str__() + ", took " + str(round(time_to_deliver * 60, 2)) + " minutes to deliver")

        # Updates the status record once packages are delivered to the address
        update_status_record(truck.time)

    # Once all packages are delivered the truck's total mileage is printed
    # print("Truck mileage: " + str(truck.mileage))


# ------------- Back to Hub -------------

# TODO Make this a truck method
def back_to_hub(truck):
    # Gets the distance between the truck's current address and the hub then adds that mileage to the truck
    dist_to_hub = betwixt(truck.current_address, address_list[0])
    truck.mileage += dist_to_hub

    # Calculates the time to the hub and adds to the truck's time
    time_to_hub = dist_to_hub / 18
    truck.time = truck.time + datetime.timedelta(hours=time_to_hub)
    # Updates the truck's current address to the hub
    truck.current_address = address_list[0]


# ------------- Closest Time -------------

def closest_time(delta):
    nearest_time = None

    # Creates a list to hold all the times from the status record and sorts them in ascending order
    times_list = list(status_record.keys())
    times_list.sort()

    for time in times_list:
        # If the user's time is greater than the status record time entry then update nearest time
        if delta >= time:
            nearest_time = time
        # If the user's time is less than the status record time then nearest time is found and break
        elif delta < time:
            break

    return nearest_time


# ------------- Create and Load the trucks -------------

# Create the truck objects
Truck_1 = Truck(name="Truck 1")
Truck_2 = Truck(name="Truck 2")
Truck_3 = Truck(name="Truck 3")

# Add truck package id's to lists to make loading easier
truck_1_package_ids = [1,7,13,14,15,16,19,20,21,29,30,31,34,37,39,40]
truck_2_package_ids = [2,3,4,5,6,12,18,25,26,27,28,32,33,35,36,38]
truck_3_package_ids = [8,9,10,11,17,22,23,24]


# For loops used to add packages to the trucks using the package id lists
for package_id in truck_1_package_ids:
    Truck_1.load(PackageTable.get_package(package_id))

for package_id in truck_2_package_ids:
    Truck_2.load(PackageTable.get_package(package_id))

for package_id in truck_3_package_ids:
    Truck_3.load(PackageTable.get_package(package_id))


# ------------- Deliver Packages -------------

deliver(Truck_1)

# Truck 2 has packages that won't arrive until 9:05 am and cannot depart until then
Truck_2.time = datetime.timedelta(hours=9, minutes=5)
deliver(Truck_2)

# Takes the truck with the earliest last delivery and returns it to the hub
if Truck_1.time < Truck_2.time:
    back_to_hub(Truck_1)
    # Updates Truck 3's departure time to the truck returned to the hub
    Truck_3.time = Truck_1.time
else:
    back_to_hub(Truck_2)
    # Updates Truck 3's departure time to the truck returned to the hub
    Truck_3.time = Truck_2.time

deliver(Truck_3)


# ------------- UI -------------

while True:
    # Prints the UI header
    print('''
    ------------- WGUPS Routing Program -------------

    Menu Options:
    1. Get a package's status at a certain time
    2. Get all package status at a certain time
    3. Print all package status and total mileage
    4. Close the program
    ''')

    # Uses a try except block to catch errors in the input
    try:
        # Holds the user's input
        option = input("Enter a number associated with a menu option: ")
        print()
        # Throws an error if the input is not an int
        option = int(option)
        
        # If input is greater than 4 throw exception
        if option > 5:
            raise ValueError()
    except ValueError:
        print("\nInvalid: Enter a number from the desired menu options.\n")
    
    if option == 1: # 1. Get a package's status at a certain time
        # Loop to validate user time input
        while True:
            try:
                # Gets the user's entered time in string format
                time_str = input("Enter the time in HH:MM military time format: ")
                # Converts the time string to a datetime object
                dt_object = dt.strptime(time_str, '%H:%M')
                # Converts the date time object to time delta to be consistent with the program's other time format
                delta = datetime.timedelta(hours=dt_object.hour, minutes=dt_object.minute)

                # Holds the time in the status record that is nearest the user's entered time without going over
                nearest_time = closest_time(delta)
                print("Nearest recorded time is: " + str(nearest_time) + "\n")

                break
            except ValueError:
                print("Invalid: Enter a number in HH:MM military time format")
            except NameError as e:
                print(e)

        # Loop to validate user package number input
        while True:
            try:
                package_num = input("Enter the package number: ")
                print()
                # Validates user input is int
                package_num = int(package_num)

                # If package number input is 0 or greater than the amount off packages then throw exception
                if package_num == 0 or package_num > PackageTable.length:
                    raise ValueError()
                
                # Holds the packages and their status for the user's desired time
                time_packages = status_record.get(nearest_time)
                # Uses a string to find the correct package
                id_string = "ID: " + str(package_num) + ","

                # Loops through the packages and prints the package's status at the desired time
                for packages, status in time_packages.items():
                    if packages.find(id_string) != -1:
                        print("Package Status as of " + str(nearest_time))
                        print(f"{packages}")
                
                break
            except ValueError:
                print("Invalid: Enter a valid package number.\n")
    elif option == 2: # 2. Get all package status at a certain time
        while True:
            try:
                # Gets the user's entered time in string format
                time_str = input("Enter the time in HH:MM military time format: ")
                print()
                # Converts the time string to a datetime object
                dt_object = dt.strptime(time_str, '%H:%M')
                # Converts the date time object to time delta to be consistent with the program's other time format
                delta = datetime.timedelta(hours=dt_object.hour, minutes=dt_object.minute)

                # Holds the time in the status record that is nearest the user's entered time without going over
                nearest_time = closest_time(delta)

                # Holds the packages and their status for the user's desired time
                time_packages = status_record.get(nearest_time)
                print("Nearest recorded time is: " + str(nearest_time) + "\n")
                print("Package Status as of " + str(nearest_time))

                # Loops through packages and their status at desired time and prints status
                for packages, status in time_packages.items():
                    print(f"{packages}")
                
                break
            except ValueError:
                print("Invalid: Enter the time in HH:MM military time format")
            except AttributeError:
                print("Invalid: The earliest recorded time is 8:00")
    elif option == 3: # 3. Print all package status and total mileage
        time_packages = PackageTable
        print("Package Status as of EOD")

        # Loops through package table and prints package information after deliveries complete
        for i in range(1, PackageTable.length + 1):
            print(PackageTable.lookup(i))

        print()
        # Gets total truck mileage and prints
        total_mileage = Truck_1.mileage + Truck_2.mileage + Truck_3.mileage
        print("Total Mileage: " + str(total_mileage))
    elif option == 4: # 4. Close the program
        print("WGUPS Routing Program Closed\n")
        
        break   
    else:
        continue


# ------------- TODO -------------

# TODO - [x] keep track of which truck each package is on
# TODO - [ ] Move all code above to another py file and having UI in main
# TODO - [ ] Automatically update package 9 incorrect address at 10:20
# TODO - [ ] Presort packages list to decrease time complexity
# TODO - [x] Validate user input in UI
# TODO - [x] Validate entering nothing in UI
# TODO - [ ] Implement continue in UI while loops to optimize flow
# TODO - [x] Add delayed as status and add it to needed packages
# TODO - [ ] Create nearest time function