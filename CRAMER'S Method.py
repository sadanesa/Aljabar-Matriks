import flet as ft
import numpy as np

def main(page: ft.Page):
    page.title = "Cramer's Rule Calculator"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.padding = 10
    page.scroll = "adaptive"
    page.window_width = 400
    page.window_height = 800
    page.window_resizable = False
    
    ukuran_matrix = 2
    input_matrix = []
    input_konstanta = []
    container_hasil = ft.Column(spacing=10)
    container_langkah = ft.Column(spacing=15)
    
    def hitung_determinan(matrix):
        return np.linalg.det(matrix)
    
    def solve_cramers(A, b):
        ukuran = len(A)
        det_A = hitung_determinan(A)
        
        if abs(det_A) < 0.0000000001:
            return None, None
        
        solusi = []
        semua_delta = []
        
        for i in range(ukuran):
            A_temp = A.copy()
            A_temp[:, i] = b
            det_temp = hitung_determinan(A_temp)
            
            semua_delta.append((A_temp, det_temp))
            solusi.append(det_temp / det_A)
        
        return solusi, (A, det_A, semua_delta)
    
    def buat_visual_matrix(matrix):
        baris_matrix = []
        
        for baris in matrix:
            kolom_matrix = []
            for nilai in baris:
                kolom_matrix.append(
                    ft.Container(
                        content=ft.Text(
                            f"{nilai:.2f}",
                            size=16,
                            text_align=ft.TextAlign.CENTER,
                            weight=ft.FontWeight.W_500
                        ),
                        width=70,
                        height=40,
                        alignment=ft.alignment.center
                    )
                )
            
            baris_matrix.append(
                ft.Row(kolom_matrix, spacing=5, alignment=ft.MainAxisAlignment.CENTER)
            )
        
        isi_matrix = ft.Column(baris_matrix, spacing=5, alignment=ft.MainAxisAlignment.CENTER)
        
        return ft.Container(
            content=isi_matrix,
            padding=ft.padding.only(left=15, right=15, top=5, bottom=5),
            border=ft.border.only(
                left=ft.BorderSide(3, "#000000"),
                right=ft.BorderSide(3, "#000000")
            )
        )
    
    def buat_input_matrix():
        nonlocal input_matrix, input_konstanta
        input_matrix = []
        input_konstanta = []
        
        semua_kontrol = []
        
        semua_kontrol.append(
            ft.Text(
                f"Masukkan Matriks Koefisien {ukuran_matrix}x{ukuran_matrix} dan Konstanta",
                size=16,
                weight=ft.FontWeight.BOLD,
                color="#0D47A1"
            )
        )
        
        for i in range(ukuran_matrix):
            baris = []
            kontrol_baris = []
            
            for j in range(ukuran_matrix):
                field = ft.TextField(
                    width=70,
                    height=50,
                    text_align=ft.TextAlign.CENTER,
                    border_radius=10,
                    value="",
                    keyboard_type=ft.KeyboardType.NUMBER,
                    hint_text="0"
                )
                baris.append(field)
                kontrol_baris.append(field)
            
            kontrol_baris.append(ft.Text("=", size=20, weight=ft.FontWeight.BOLD))
            
            field_konstanta = ft.TextField(
                width=70,
                height=50,
                text_align=ft.TextAlign.CENTER,
                border_radius=10,
                value="",
                keyboard_type=ft.KeyboardType.NUMBER,
                bgcolor="#FFF8E1",
                hint_text="0"
            )
            input_konstanta.append(field_konstanta)
            kontrol_baris.append(field_konstanta)
            
            input_matrix.append(baris)
            semua_kontrol.append(
                ft.Row(kontrol_baris, spacing=8, alignment=ft.MainAxisAlignment.CENTER)
            )
        
        return ft.Container(
            content=ft.Column(semua_kontrol, spacing=10),
            padding=15,
            border_radius=15,
            bgcolor="#FFFFFF",
            shadow=ft.BoxShadow(blur_radius=8, color="#90A4AE")
        )
    
    def tombol_hitung_diklik(e):
        try:
            matrix_A = []
            for baris in input_matrix:
                matrix_A.append([
                    float(field.value) if field.value.strip() else 0 
                    for field in baris
                ])
            matrix_A = np.array(matrix_A)
            
            vector_b = np.array([
                float(field.value) if field.value.strip() else 0 
                for field in input_konstanta
            ])
            
            solusi, langkah = solve_cramers(matrix_A, vector_b)
            
            container_hasil.controls.clear()
            container_langkah.controls.clear()
            
            if solusi is None:
                container_hasil.controls.append(
                    ft.Container(
                        content=ft.Text(
                            "Determinan = 0, sistem tidak memiliki solusi unik!",
                            color="#C62828",
                            size=16,
                            weight=ft.FontWeight.BOLD
                        ),
                        padding=20,
                        border_radius=10,
                        bgcolor="#FFEBEE"
                    )
                )
                page.update()
                return
            
            nama_variabel = ['x', 'y', 'z', 'w', 'u', 'v']
            
            teks_hasil = []
            for i, nilai in enumerate(solusi):
                var = nama_variabel[i] if i < len(nama_variabel) else f'x{i+1}'
                teks_hasil.append(
                    ft.Text(
                        f"{var} = {nilai:.4f}",
                        size=24,
                        weight=ft.FontWeight.BOLD,
                        color="#0D47A1",
                        text_align=ft.TextAlign.CENTER
                    )
                )
            
            container_hasil.controls.append(
                ft.Container(
                    content=ft.Column([
                        ft.Text(
                            "Hasil:",
                            size=20,
                            weight=ft.FontWeight.BOLD,
                            color="#1565C0",
                            text_align=ft.TextAlign.CENTER
                        ),
                        ft.Divider(height=5, color="transparent"),
                        ft.Column(
                            teks_hasil,
                            spacing=8,
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER
                        )
                    ], 
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=10),
                    padding=25,
                    border_radius=15,
                    bgcolor="#E3F2FD",
                    border=ft.border.all(2, "#42A5F5"),
                    shadow=ft.BoxShadow(
                        spread_radius=1,
                        blur_radius=8,
                        color="#90CAF9",
                        offset=ft.Offset(0, 2)
                    )
                )
            )
            
            A_asli, det_A, semua_delta = langkah
            
            container_langkah.controls.append(
                ft.Text(
                    "Langkah 1: Hitung Determinan Δ",
                    size=16,
                    weight=ft.FontWeight.BOLD,
                    color="#0D47A1"
                )
            )
            
            container_langkah.controls.append(
                ft.Container(
                    content=ft.Column([
                        ft.Row([
                            ft.Text("Δ = ", size=18, weight=ft.FontWeight.BOLD),
                            buat_visual_matrix(A_asli)
                        ], alignment=ft.MainAxisAlignment.CENTER),
                        ft.Divider(height=10, color="transparent"),
                        ft.Text(
                            f"Δ = {det_A:.4f}",
                            weight=ft.FontWeight.BOLD,
                            size=18,
                            color="#1565C0"
                        )
                    ]),
                    padding=20,
                    border_radius=10,
                    border=ft.border.all(1, "#E0E0E0")
                )
            )
            
            for i, (matrix_temp, det_temp) in enumerate(semua_delta):
                var = nama_variabel[i] if i < len(nama_variabel) else f'x{i+1}'
                
                container_langkah.controls.append(
                    ft.Text(
                        f"Langkah {i+2}: Hitung Δ{i+1} untuk {var}",
                        size=16,
                        weight=ft.FontWeight.BOLD,
                        color="#0D47A1"
                    )
                )
                
                container_langkah.controls.append(
                    ft.Container(
                        content=ft.Column([
                            ft.Row([
                                ft.Text(f"Δ{i+1} = ", size=18, weight=ft.FontWeight.BOLD),
                                buat_visual_matrix(matrix_temp)
                            ], alignment=ft.MainAxisAlignment.CENTER),
                            ft.Divider(height=10, color="transparent"),
                            ft.Text(
                                f"Δ{i+1} = {det_temp:.4f}",
                                weight=ft.FontWeight.BOLD,
                                size=18,
                                color="#6A1B9A"
                            ),
                            ft.Divider(height=10, color="#E0E0E0"),
                            ft.Text(
                                f"{var} = Δ{i+1}/Δ = {det_temp:.4f}/{det_A:.4f} = {solusi[i]:.4f}",
                                size=16,
                                weight=ft.FontWeight.BOLD,
                                color="#424242"
                            )
                        ]),
                        padding=20,
                        border_radius=10,
                        border=ft.border.all(1, "#E0E0E0")
                    )
                )
            
            page.update()
            
        except Exception as error:
            container_hasil.controls.clear()
            container_hasil.controls.append(
                ft.Text(f"Error: {str(error)}", color="#C62828")
            )
            page.update()
    
    def ubah_ukuran_matrix(e):
        nonlocal ukuran_matrix
        try:
            ukuran_baru = int(input_ukuran.value)
            if ukuran_baru < 2:
                input_ukuran.value = "2"
                ukuran_baru = 2
            
            ukuran_matrix = ukuran_baru
            
            page.controls[0].content.controls[2] = buat_input_matrix()
            container_hasil.controls.clear()
            container_langkah.controls.clear()
            page.update()
        except:
            input_ukuran.value = str(ukuran_matrix)
            page.update()
    
    input_ukuran = ft.TextField(
        label="Ukuran Matriks (n×n)",
        value="2",
        width=120,
        height=50,
        text_align=ft.TextAlign.CENTER,
        border_radius=10,
        keyboard_type=ft.KeyboardType.NUMBER,
        on_submit=ubah_ukuran_matrix
    )
    
    tombol_generate = ft.ElevatedButton(
        "Generate",
        on_click=ubah_ukuran_matrix,
        style=ft.ButtonStyle(
            color="#FFFFFF",
            bgcolor="#1976D2",
            shape=ft.RoundedRectangleBorder(radius=10),
        ),
        height=50
    )
    
    tombol_hitung = ft.ElevatedButton(
        "Hitung",
        on_click=tombol_hitung_diklik,
        style=ft.ButtonStyle(
            color="#FFFFFF",
            bgcolor="#1565C0",
            shape=ft.RoundedRectangleBorder(radius=12),
            padding=18
        ),
        width=180,
        height=50
    )
    
    panel_langkah = ft.ExpansionTile(
        title=ft.Text(
            "Lihat Cara Penyelesaian",
            weight=ft.FontWeight.BOLD,
            color="#0D47A1"
        ),
        controls=[
            ft.Container(content=container_langkah, padding=20)
        ],
    )
    
    page.add(
        ft.Container(
            content=ft.Column([
                ft.Container(
                    content=ft.Text(
                        "Kalkulator Cramer's Rule",
                        size=24,
                        weight=ft.FontWeight.BOLD,
                        color="#0D47A1",
                        text_align=ft.TextAlign.CENTER
                    ),
                    padding=15
                ),
                ft.Row(
                    [input_ukuran, tombol_generate],
                    alignment=ft.MainAxisAlignment.CENTER,
                    spacing=8
                ),
                buat_input_matrix(),
                ft.Container(
                    content=tombol_hitung,
                    alignment=ft.alignment.center,
                    padding=15
                ),
                container_hasil,
                panel_langkah
            ], 
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=15),
            padding=10
        )
    )

ft.app(target=main, view=ft.AppView.FLET_APP)