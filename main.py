import csv
from package import Package
from hashtable import HashTable

# Create the hash table to store package objects
packageTable = HashTable()

# File path for the csv package data
file_path = "data/packages.csv"

# Reads the packages csv file and uses the data to create a package object and add it to the package hash table
# Surround with a try block to catch exceptions
try:
    # Opens the packages csv file
    with open(file_path, "r") as csv_file:
        # Holds the csv content in reader with a comma delimiter
        reader = csv.reader(csv_file, delimiter=',')
        # Skips the header row
        next(reader)

        for row in reader:
            id = int(row[0])
            address = row[1]
            city = row[2]
            state = row[3]
            zip = row[4]
            deadline = row[5]
            weight = row[6]
            notes = row[7]

            package = Package(id, address, city, state, zip, deadline, weight, notes)
            packageTable.add(id, package)
except FileNotFoundError:
    print("The file was not found")
except PermissionError:
    print("Permission to open the file not granted")