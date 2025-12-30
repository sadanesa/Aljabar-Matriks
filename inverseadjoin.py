def determinant_sarrus(matrix):
    """Menghitung determinan matriks 3x3 menggunakan aturan Sarrus"""
    if len(matrix) != 3 or any(len(row) != 3 for row in matrix):
        raise ValueError("Matrix must be 3x3")
    
    a, b, c = matrix[0]
    d, e, f = matrix[1]
    g, h, i = matrix[2]
    
    det = a*e*i + b*f*g + c*d*h - c*e*g - b*d*i - a*f*h
    return det

def matrix_minor(matrix, i, j):
    """Mengembalikan matriks minor dengan menghapus baris i dan kolom j"""
    return [[matrix[r][c] for c in range(len(matrix)) if c != j] 
            for r in range(len(matrix)) if r != i]

def cofactor(matrix, i, j):
    """Menghitung elemen kofaktor pada posisi (i, j)"""
    minor_matrix = matrix_minor(matrix, i, j)
    # Determinan matriks 2x2 [a, b; c, d] adalah ad - bc
    minor_det = minor_matrix[0][0] * minor_matrix[1][1] - minor_matrix[0][1] * minor_matrix[1][0]
    return ((-1) ** (i + j)) * minor_det

def adjoint_matrix(matrix):
    """Menghitung matriks adjoin (transpos dari matriks kofaktor)"""
    cofactor_matrix = []
    for i in range(3):
        cofactor_row = []
        for j in range(3):
            cofactor_row.append(cofactor(matrix, i, j))
        cofactor_matrix.append(cofactor_row)
    
    # Transpose matriks kofaktor untuk mendapatkan adjoin
    adjoint = []
    for j in range(3):
        adjoint_row = []
        for i in range(3):
            adjoint_row.append(cofactor_matrix[i][j])
        adjoint.append(adjoint_row)
    
    return adjoint

def inverse_adjoint(matrix):
    """Menghitung invers matriks menggunakan metode adjoin"""
    if len(matrix) != 3 or any(len(row) != 3 for row in matrix):
        raise ValueError("Matrix must be 3x3")
    
    det = determinant_sarrus(matrix)
    if det == 0:
        raise ValueError("Matrix is not invertible (determinant is zero)")
    
    adjoint = adjoint_matrix(matrix)
    
    # Bagi setiap elemen matriks adjoin dengan determinan
    inverse = []
    for i in range(3):
        inv_row = []
        for j in range(3):
            inv_row.append(adjoint[i][j] / det)
        inverse.append(inv_row)
    
    return inverse

def print_matrix(matrix, title="Matrix"):
    """Mencetak matriks dengan format rapi"""
    print(f"\n{title}:")
    for row in matrix:
        print([f"{elem:8.3f}" for elem in row])

# Contoh penggunaan
print("Enter a 3x3 matrix row by row, with elements separated by spaces (e.g., 1 2 3):")
matrix = []
try:
    for i in range(3):
        row_input = input(f"Row {i+1}: ").strip()
        row = list(map(float, row_input.split()))  # Gunakan float untuk mendukung desimal
        if len(row) != 3:
            raise ValueError("Each row must have exactly 3 numbers.")
        matrix.append(row)
    
    det = determinant_sarrus(matrix)
    print(f"\nThe determinant is: {det}")
    
    if det == 0:
        print("The matrix is not invertible.")
    else:
        inverse = inverse_adjoint(matrix)
        print_matrix(matrix, "Original Matrix (A)")
        print_matrix(inverse, "Inverse Matrix (A^(-1))")
        
        # Verifikasi: A * A^(-1) seharusnya mendekati matriks identitas
        print("\nVerification (A * A^(-1) should be close to Identity matrix):")
        result = []
        for i in range(3):
            result_row = []
            for j in range(3):
                sum_product = sum(matrix[i][k] * inverse[k][j] for k in range(3))
                result_row.append(sum_product)
            result.append(result_row)
        print_matrix(result, "A * A^(-1)")

except ValueError as e:
    print(f"Error: {e}")