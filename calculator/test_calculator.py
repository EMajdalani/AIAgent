from pkg.calculator import Calculator

calculator = Calculator()
result = calculator.evaluate("3 + 7 * 2")
assert result == 17, f"Expected 17, but got {result}"
print("Test passed!")