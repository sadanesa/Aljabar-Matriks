import tkinter as tk
from tkinter import ttk, messagebox
from fractions import Fraction

def minor(matrix, i, j):
    return [row[:j] + row[j+1:] for row in (matrix[:i] + matrix[i+1:])]

def determinant(matrix):
    n = len(matrix)
    if n == 1:
        return matrix[0][0]
    if n == 2:
        return matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0]

    det = 0
    for c in range(n):
        det += ((-1) ** c) * matrix[0][c] * determinant(minor(matrix, 0, c))
    return det

def inverse_by_obe(matrix):
    n = len(matrix)

    aug = []
    for i in range(n):
        row = []
        for j in range(n):
            row.append(Fraction(matrix[i][j]))
        for j in range(n):
            row.append(Fraction(1 if i == j else 0))
        aug.append(row)

    steps = []

    for col in range(n):
        pivot_row = -1
        for r in range(col, n):
            if aug[r][col] != 0:
                pivot_row = r
                break

        if pivot_row == -1:
            return None, ["Matriks singular (tidak punya invers)."]

        if pivot_row != col:
            aug[col], aug[pivot_row] = aug[pivot_row], aug[col]
            steps.append(f"[Tukar R{col+1} dan R{pivot_row+1}]")

        pivot_val = aug[col][col]
        if pivot_val != 1:
            for j in range(2*n):
                aug[col][j] /= pivot_val
            steps.append(f"[R{col+1} → R{col+1} / {pivot_val}]")

        for r in range(col+1, n):
            factor = aug[r][col]
            if factor != 0:
                for j in range(2*n):
                    aug[r][j] -= factor * aug[col][j]
                steps.append(f"[R{r+1} → R{r+1} - ({factor})R{col+1}]")

    for col in range(n-1, -1, -1):
        for r in range(col-1, -1, -1):
            factor = aug[r][col]
            if factor != 0:
                for j in range(2*n):
                    aug[r][j] -= factor * aug[col][j]
                steps.append(f"[R{r+1} → R{r+1} - ({factor})R{col+1}]")

    inverse = []
    for i in range(n):
        row = []
        for j in range(n, 2*n):
            row.append(aug[i][j])
        inverse.append(row)

    return inverse, steps

def format_fraction(frac):
    if frac.denominator == 1:
        return str(frac.numerator)
    else:
        return f"{frac.numerator}/{frac.denominator}"

PRIMARY = "#4A90E2"
PRIMARY_HOVER = "#357ABD"
ACCENT_RED = "#e25555"
ACCENT_RED_HOVER = "#c74747"

FONT_TITLE = ("Arial", 20, "bold")
FONT_BUTTON = ("Segoe UI", 11, "bold")
FONT_INPUT = ("Consolas", 12)

class ModernButton(tk.Button):
    def __init__(self, master=None, bg=PRIMARY, hover_bg=None, **kwargs):

        if hover_bg is None:
            hover_bg = PRIMARY_HOVER

        super().__init__(
            master,
            bg=bg,
            fg="white",
            activebackground=hover_bg,
            cursor="hand2",
            relief="flat",
            bd=0,
            padx=14,
            pady=7,
            font=FONT_BUTTON,
            **kwargs
        )

        self.default_bg = bg
        self.hover_bg = hover_bg

        self.bind("<Enter>", lambda e: self.config(bg=self.hover_bg))
        self.bind("<Leave>", lambda e: self.config(bg=self.default_bg))

class MatrixCalculatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Kalkulator Matriks")
        self.root.geometry("900x720")
        self.root.configure(bg="#eef6ff")

        self.order = tk.StringVar(value="2x2")
        self.entries = []
        self.result_widgets = []

        self.create_widgets()

    def create_widgets(self):

        header = tk.Label(
            self.root, 
            text="Kalkulator Matriks\nDeterminan & Invers (OBE)",
            font=FONT_TITLE,
            bg="#eef6ff",
            fg="#2c3e50"
        )
        header.pack(pady=15)

        order_frame = tk.Frame(self.root, bg="#eef6ff")
        order_frame.pack(pady=10)

        tk.Label(order_frame, text="Pilih Ordo:", bg="#eef6ff", font=("Segoe UI", 11)).pack(side=tk.LEFT)
        
        order_combo = ttk.Combobox(order_frame, textvariable=self.order, state="readonly", width=8)
        order_combo['values'] = ("2x2", "3x3", "4x4")
        order_combo.pack(side=tk.LEFT, padx=10)
        order_combo.bind("<<ComboboxSelected>>", lambda e: self.create_matrix_input())

        btn_frame = tk.Frame(self.root, bg="#eef6ff")
        btn_frame.pack(pady=15)

        ModernButton(
            btn_frame, text="Hitung Determinan",
            command=self.calculate_determinant
        ).pack(side=tk.LEFT, padx=10)

        ModernButton(
            btn_frame, text="Hitung Invers (OBE)",
            bg="#22a7f0",
            hover_bg="#1b8ac7",
            command=self.calculate_inverse
        ).pack(side=tk.LEFT, padx=10)

        ModernButton(
            btn_frame, text="Reset",
            bg=ACCENT_RED,
            hover_bg=ACCENT_RED_HOVER,
            command=self.reset
        ).pack(side=tk.LEFT, padx=10)

        self.input_frame = tk.Frame(self.root, bg="#eef6ff")
        self.input_frame.pack(pady=10)

        self.output_frame = tk.Frame(self.root, bg="#eef6ff")
        self.output_frame.pack(pady=10)

        self.create_matrix_input()

    def create_matrix_input(self):
        for widget in self.input_frame.winfo_children():
            widget.destroy()

        self.entries = []
        n = int(self.order.get()[0])

        matrix_box = tk.Frame(self.input_frame, bg="#dceeff", bd=2, relief="ridge")
        matrix_box.pack(pady=10)

        for i in range(n):
            row_entries = []
            for j in range(n):
                entry = tk.Entry(matrix_box, width=7, justify="center", font=FONT_INPUT)
                entry.grid(row=i, column=j, padx=5, pady=5)
                row_entries.append(entry)
            self.entries.append(row_entries)

    def get_matrix_from_entries(self):
        n = len(self.entries)
        matrix = []

        for i in range(n):
            row = []
            for j in range(n):
                val = self.entries[i][j].get().strip()
                if val == "":
                    val = "0"
                try:
                    num = float(val)
                    if num.is_integer():
                        num = int(num)
                    row.append(num)
                except:
                    messagebox.showerror("Error", f"Input tidak valid di ({i+1}, {j+1})!")
                    return None
            matrix.append(row)

        return matrix

    def calculate_determinant(self):
        self.clear_output()
        matrix = self.get_matrix_from_entries()
        if matrix is None: return
        
        det = determinant(matrix)
        self.show_result(f"Determinan Matriks = {det}")

    def calculate_inverse(self):
        self.clear_output()
        matrix = self.get_matrix_from_entries()
        if matrix is None: return

        det = determinant(matrix)
        if det == 0:
            self.show_result("Matriks tidak memiliki invers (det = 0).")
            return
        
        inverse, steps = inverse_by_obe(matrix)

        self.show_result("Langkah-langkah OBE:")
        for s in steps:
            self.show_result("  " + s)

        self.show_inverse_matrix(inverse)

    def show_result(self, text):
        label = tk.Label(self.output_frame, text=text, bg="#eef6ff", anchor="w", font=("Consolas", 10))
        label.pack(anchor="w")
        self.result_widgets.append(label)

    def show_inverse_matrix(self, inv):
        n = len(inv)
        box = tk.Frame(self.output_frame, bg="#dceeff", bd=2, relief="ridge")
        box.pack(pady=10)

        tk.Label(box, text="Matriks Invers:", bg="#dceeff", font=("Segoe UI", 11, "bold")).grid(row=0, column=0, columnspan=n)

        for i in range(n):
            for j in range(n):
                val = format_fraction(inv[i][j])
                cell = tk.Label(box, text=val, bg="white", relief="solid", width=10, font=("Consolas", 12))
                cell.grid(row=i+1, column=j, padx=3, pady=3)

        self.result_widgets.append(box)

    def clear_output(self):
        for w in self.result_widgets:
            w.destroy()
        self.result_widgets = []

    def reset(self):
        self.clear_output()
        self.create_matrix_input()

if __name__ == "__main__":
    root = tk.Tk()
    app = MatrixCalculatorApp(root)
    root.mainloop()