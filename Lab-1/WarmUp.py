flower_bulbs = {
    'daffodil': 0.35,
    'tulip': 0.33,
    'crocus': 0.25,
    'hyacinth': 0.75,
    'bluebell': 0.50
}

mary_order = {
    'daffodil': 50,
    'tulip': 100
}


flower_bulbs['tulip'] *= 1.25 # Update tulip price
flower_bulbs['tulip'] = round(flower_bulbs['tulip'], 2)


mary_order['hyacinth'] = 30 # Added hyacinth bulbs to Mary's order


print("You have purchased the following bulbs:") # Display Mary's purchase order
order_of_bulbs = ['crocus', 'daffodil', 'bluebell', 'hyacinth', 'tulip']
for bulb_name in order_of_bulbs:
    if bulb_name in mary_order:
        bulb_code = bulb_name[:3].upper()
        quantity = mary_order[bulb_name]
        price_per_bulb = flower_bulbs[bulb_name]
        subtotal = quantity * price_per_bulb
        print(f"{bulb_code} * {quantity:4} = $ {subtotal:.2f}")

# Calculate the total number of bulbs and total cost
total_bulbs = sum(mary_order.values())
total_cost = 0
for bulb in mary_order:
    total_cost += mary_order[bulb] * flower_bulbs[bulb]
print(f"Thank you for purchasing {total_bulbs} bulbs from Bluebell Greenhouses.")
print(f"Your total comes to $ {total_cost:6.2f}")
