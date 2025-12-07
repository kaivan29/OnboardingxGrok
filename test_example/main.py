"""Main entry point for the calculator application."""
from calculator import Calculator, calculate_area, calculate_circumference


def main():
    """Run the calculator demo."""
    calc = Calculator()
    
    print("Calculator Demo")
    print("=" * 40)
    
    # Basic operations
    result1 = calc.add(10, 5)
    print(f"10 + 5 = {result1}")
    
    result2 = calc.multiply(7, 3)
    print(f"7 * 3 = {result2}")
    
    result3 = calc.power(2, 8)
    print(f"2 ^ 8 = {result3}")
    
    # Circle calculations
    radius = 5.0
    area = calculate_area(radius)
    circumference = calculate_circumference(radius)
    
    print(f"\nCircle with radius {radius}:")
    print(f"  Area: {area:.2f}")
    print(f"  Circumference: {circumference:.2f}")
    
    # Show history
    print("\nCalculation History:")
    for entry in calc.get_history():
        print(f"  - {entry}")


if __name__ == "__main__":
    main()

