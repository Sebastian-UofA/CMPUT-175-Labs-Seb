# This function updates the price of a specific flower in the flower_bulbs dictionary
def update_price(flower_bulbs, flower, new_price) -> dict:
    flower_bulbs[flower] = new_price
    return flower_bulbs

# This function adds a flower and its quantity to the order dictionary
def add_to_order(order, flower, quantity) -> dict:
    order[flower] = quantity
    return order

# This function calculates the subtotal for a given quantity of bulbs and their price per bulb
def calculate_subtotal(quantity, price_per_bulb) -> float:
    return quantity * price_per_bulb

# This function prints the order of bulbs, including the bulb code, quantity, and subtotal for each type of bulb
def print_order(order_of_bulbs, order, flower_bulbs):
    print("You have purchased the following bulbs:") 
    for bulb_name in order_of_bulbs:
        if bulb_name in order:
            bulb_code = bulb_name[:3].upper()
            quantity = order[bulb_name]
            price_per_bulb = flower_bulbs[bulb_name]
            subtotal = calculate_subtotal(quantity, price_per_bulb)
            print(f"{bulb_code} * {quantity:4} = $ {subtotal:.2f}")

# This function calculates and prints the total number of bulbs and the total cost of the order
def calculate_total(order, flower_bulbs):
    total_bulbs = sum(order.values())
    total_cost = 0
    for bulb in order:
        total_cost += order[bulb] * flower_bulbs[bulb]
    print(f"Thank you for purchasing {total_bulbs} bulbs from Bluebell Greenhouses.")
    print(f"Your total comes to $ {total_cost:6.2f}")

# The main function initializes the flower_bulbs and mary_order dictionaries, updates the prices and orders, and then prints the order and calculates the total
def main():
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

    # Update prices and orders
    flower_bulbs = update_price(flower_bulbs, 'tulip', flower_bulbs['tulip'] * 1.25) #sends, (dictionary, key, value) to update_price function and returns the updated dictionary
    mary_order = add_to_order(mary_order, 'hyacinth', 30) #sends, (dictionary, key, value) to add_to_order function and returns the updated dictionary

    # Print order and calculate total
    order_of_bulbs = ['crocus', 'daffodil', 'bluebell', 'hyacinth', 'tulip']
    print_order(order_of_bulbs, mary_order, flower_bulbs)
    calculate_total(mary_order, flower_bulbs)

if __name__ == "__main__":
    main()