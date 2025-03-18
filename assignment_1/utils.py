def print_products(products):
    """Print all products in a user-friendly format."""
    if not products:
        print("No products available.")
    else:
        print("\nProduct List:")
        print("-" * 30)
        for product in products:
            print(f"ID: {product[0]}, Name: {product[1]}, Price: ${product[2]:.2f}")
        print("-" * 30)
