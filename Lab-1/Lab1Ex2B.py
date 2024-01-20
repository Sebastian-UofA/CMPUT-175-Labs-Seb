# Read the earthquake data from the file
with open('earthquake.txt', 'r') as file:
    earthquake_data = file.readlines() # readlines will read the file line by line and return a list of lines

# Create a dictionary to store the earthquake data by region
earthquake_dict = {}

# Process each line of the earthquake data
for line in earthquake_data:
    # Split the line into individual data elements
    elements = line.split()

    # Extract the (region name, magnitude, date) from the data file
    region = elements[-1]
    magnitude = elements[0]
    date = elements[1]

    # Check if the region already exists in the dictionary
    if region in earthquake_dict:
        earthquake_dict[region].append([date, magnitude])
    else:
        earthquake_dict[region] = [[date, magnitude]]

with open('earthquakefmt.txt', 'w') as file:
    for region, data in earthquake_dict.items():
        file.write(f'[{region.upper()}')
        for item in data:
            file.write(f', [{item[0]}, {item[1]}]')
        file.write(']\n')
