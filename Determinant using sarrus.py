def determinant_sarrus(matrix):
    if len(matrix) != 3 or any(len(row) != 3 for row in matrix):
        raise ValueError("Matrix must be 3x3")
    
    a, b, c = matrix[0]
    d, e, f = matrix[1]
    g, h, i = matrix[2]
    
    det = a*e*i + b*f*g + c*d*h - c*e*g - b*d*i - a*f*h
    return det

print("Enter a 3x3 matrix row by row, with elements separated by spaces (e.g., 1 2 3):")
matrix = []
try:
    for i in range(3):
        row_input = input(f"Row {i+1}: ").strip()
        row = list(map(int, row_input.split()))
        if len(row) != 3:
            raise ValueError("Each row must have exactly 3 integers.")
        matrix.append(row)
    
    det = determinant_sarrus(matrix)
    print(f"The determinant is: {det}")
except ValueError as e:
    print(f"Error: {e}")