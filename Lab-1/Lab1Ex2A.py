# Define the rainfall categories
categories = ["[50-60 mm)", "[60-70 mm)", "[70-80 mm)", "[80-90 mm)", "[90-100 mm]"]

# Initialize an empty dictionary
rainfall_data = {}

# Use a for loop to add each category to the dictionary with an empty list as its value
for category in categories:
    rainfall_data[category] = []

# Read the data from the file
with open("rainfall.txt", "r") as file:
    for line in file:
        # Split the line into city and rainfall
        parts = line.split()
        city = parts[0]
        rainfall = float(parts[1])

        # Determine the category for the rainfall
        for category in categories:
            # Extract the lower and upper bounds from the category
            bounds = category[1:-4].split("-")
            lower = float(bounds[0])
            upper = float(bounds[1])

            # Check if the rainfall falls within the bounds
            if lower <= rainfall < upper:
                # Add the city and rainfall to the category
                rainfall_data[category].append((city, rainfall))
                break

# Write the processed data to the file
with open("rainfallfmt.txt", "w") as file:
    for category in categories:
        file.write(category + "\n")
        # Sort the cities in the category by rainfall
        sorted_cities = sorted(rainfall_data[category], key=lambda x: x[1])
        for city, rainfall in sorted_cities:
            # Write the city and rainfall to the file
            city_line = city.upper().center(25) + str(rainfall).rjust(5, ' ') + "\n"
            file.write(city_line)