import tkinter as tk
from tkinter import filedialog, messagebox
import threading
import queue
from tkinter import ttk

try:
    from ocr_handler import parse_sudoku_grid
    from sat_solver import find_all_solutions
except ImportError:
    def parse_sudoku_grid(path): return [[0]*9 for _ in range(9)]
    def find_all_solutions(grid): return False, []

RENK_ARKA = "#FFF0F5"
RENK_PANEL = "#FFE4E1"
RENK_BUTON = "#DB7093"
RENK_BUTON_AKTIF = "#C71585"
RENK_YAZI = "#2F4F4F"
RENK_COZUM = "#2E8B57"

RENK_HOVER = "#E57AA0"
RENK_FOCUS = "#8B008B"
RENK_GRID_BORDER = "#8B008B"
RENK_BLOCK_BG_1 = "#FFFFFF"
RENK_BLOCK_BG_2 = "#FFF7FB"

class SudokuGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Sudoku SAT Solver")
        self.root.geometry("900x650")
        self.root.configure(bg=RENK_ARKA)
        self.root.resizable(False, False)

        self.grid_entries = []
        self.solutions = []
        self.current_solution_index = 0
        self.original_grid = None
        self.image_path = None

        self.queue = queue.Queue()

        self._status_anim_job = None
        self._status_anim_base = ""
        self._status_anim_step = 0

        self.setup_ui()
        self.check_queue()

        try:
            self.root.attributes("-alpha", 0.0)
            self._fade_in(0.0)
        except Exception:
            pass

    def setup_ui(self):
        main_frame = tk.Frame(self.root, bg=RENK_ARKA)
        main_frame.pack(expand=True, fill="both", padx=30, pady=30)

        grid_border = tk.Frame(main_frame, bg=RENK_GRID_BORDER, bd=2)
        grid_border.pack(side=tk.LEFT, padx=(0, 30))

        grid_frame = tk.Frame(grid_border, bg="black")
        grid_frame.pack()

        self.create_grid(grid_frame)

        control_frame = tk.Frame(main_frame, bg=RENK_PANEL, bd=1, relief="ridge")
        control_frame.pack(side=tk.RIGHT, fill="both", expand=True, ipadx=20)

        tk.Label(
            control_frame,
            text="Sudoku Çözücü ✨",
            font=("Helvetica", 22, "bold"),
            bg=RENK_PANEL,
            fg=RENK_BUTON_AKTIF
        ).pack(pady=(30, 10))

        tk.Label(
            control_frame,
            text="Code with pink ≽^•⩊•^≼ ₊˚⊹♡",
            font=("Helvetica", 11, "bold italic"),
            bg=RENK_PANEL,
            fg="#C71585" 
        ).pack(pady=(0, 10))

        style = ttk.Style()
        try:
            style.theme_use("clam")
        except Exception:
            pass
        style.configure("pink.Horizontal.TProgressbar", troughcolor="white", background=RENK_BUTON)

        self.progress = ttk.Progressbar(
            control_frame,
            mode="indeterminate",
            style="pink.Horizontal.TProgressbar",
            length=220
        )
        self.progress.pack(pady=(0, 12))

        self.info_box = tk.Label(
            control_frame,
            text="Lütfen bir görsel seçin\nveya sayıları elle girin.",
            font=("Arial", 11),
            bg="white",
            fg=RENK_YAZI,
            width=25,
            height=3,
            relief="sunken",
            bd=1
        )
        self.info_box.pack(pady=10)

        btn_frame = tk.Frame(control_frame, bg=RENK_PANEL)
        btn_frame.pack(pady=20)

        self.btn_img = self.create_button(btn_frame, "📁 Resim Yükle (OCR)", self.select_image)
        self.btn_solve = self.create_button(btn_frame, "✨ Çözümü Bul", self.start_solve_thread)
        self.btn_clear = self.create_button(btn_frame, "🗑️ Temizle", self.clear_grid)

        tk.Label(
            control_frame,
            text="Çözüm Gezgini",
            font=("Arial", 10, "bold"),
            bg=RENK_PANEL,
            fg=RENK_YAZI
        ).pack(pady=(20, 5))

        nav_frame = tk.Frame(control_frame, bg=RENK_PANEL)
        nav_frame.pack()

        self.btn_prev = tk.Button(
            nav_frame, text="◀️", command=self.prev_solution,
            font=("Arial", 14, "bold"),
            bg="white", fg=RENK_BUTON,
            activebackground=RENK_BUTON, activeforeground="white",
            relief="raised", width=3, state=tk.DISABLED, cursor="hand2"
        )
        self.btn_prev.pack(side=tk.LEFT, padx=10)
        self._wire_btn_fx(self.btn_prev)

        self.lbl_count = tk.Label(nav_frame, text="0 / 0", font=("Arial", 12, "bold"), bg=RENK_PANEL, width=8)
        self.lbl_count.pack(side=tk.LEFT)

        self.btn_next = tk.Button(
            nav_frame, text="▶️", command=self.next_solution,
            font=("Arial", 14, "bold"),
            bg="white", fg=RENK_BUTON,
            activebackground=RENK_BUTON, activeforeground="white",
            relief="raised", width=3, state=tk.DISABLED, cursor="hand2"
        )
        self.btn_next.pack(side=tk.LEFT, padx=10)
        self._wire_btn_fx(self.btn_next)

    def create_grid(self, parent):
        vcmd = (self.root.register(self.validate_input), "%P")

        CELL_FONT = ("Helvetica", 22, "bold")
        CELL_IPAD = 6 

        for r in range(9):
            row_entries = []
            for c in range(9):
                block_row = r // 3
                block_col = c // 3
                bg_color = RENK_BLOCK_BG_1 if (block_row + block_col) % 2 == 0 else RENK_BLOCK_BG_2

                cell = tk.Entry(
                    parent,
                    font=CELL_FONT,
                    justify="center",
                    bg=bg_color,
                    fg=RENK_YAZI,
                    relief="flat",
                    validate="key",
                    validatecommand=vcmd
                )
                cell.configure(width=2)  

                pad_y = (1, 1)
                pad_x = (1, 1)
                if r % 3 == 0 and r != 0: pad_y = (4, 1)
                if c % 3 == 0 and c != 0: pad_x = (4, 1)

                cell.grid(
                    row=r, column=c,
                    padx=pad_x, pady=pad_y,
                    ipadx=CELL_IPAD, ipady=CELL_IPAD
                )

                try:
                    cell.configure(highlightthickness=1, highlightbackground="#E0E0E0")
                except Exception:
                    pass

                cell.bind("<FocusIn>", lambda e, ent=cell: self._focus_cell(ent, True))
                cell.bind("<FocusOut>", lambda e, ent=cell: self._focus_cell(ent, False))

                row_entries.append(cell)
            self.grid_entries.append(row_entries)

    def create_button(self, parent, text, command):
        btn = tk.Button(
            parent,
            text=text,
            command=lambda b=None: self._btn_press_fx(btn, command),
            font=("Arial", 11, "bold"),
            bg=RENK_BUTON, fg="white",
            activebackground=RENK_BUTON_AKTIF, activeforeground="white",
            highlightbackground=RENK_BUTON,
            relief="flat",
            width=20, height=2,
            cursor="hand2"
        )
        btn.pack(pady=6)
        self._wire_btn_fx(btn)
        return btn

    def _wire_btn_fx(self, btn):
        def on_enter(_):
            if str(btn["state"]) != "disabled":
                btn.configure(bg=RENK_HOVER)

        def on_leave(_):
            if str(btn["state"]) != "disabled":
                if btn in (self.btn_prev, self.btn_next):
                    btn.configure(bg="white")
                else:
                    btn.configure(bg=RENK_BUTON)

        btn.bind("<Enter>", on_enter)
        btn.bind("<Leave>", on_leave)

    def _btn_press_fx(self, btn, real_command):
        if str(btn["state"]) == "disabled":
            return
        old_relief = btn.cget("relief")
        btn.configure(relief="sunken")
        self.root.after(90, lambda: btn.configure(relief=old_relief))
        real_command()

    def _focus_cell(self, entry, is_in):
        try:
            if is_in:
                entry.configure(highlightthickness=2, highlightbackground=RENK_FOCUS, highlightcolor=RENK_FOCUS)
            else:
                entry.configure(highlightthickness=1, highlightbackground="#E0E0E0")
        except Exception:
            pass

    def _fade_in(self, alpha):
        try:
            alpha = min(alpha + 0.08, 1.0)
            self.root.attributes("-alpha", alpha)
            if alpha < 1.0:
                self.root.after(20, lambda: self._fade_in(alpha))
        except Exception:
            pass

    def _status_set(self, text, fg=RENK_YAZI, animate=False):
        if self._status_anim_job is not None:
            try:
                self.root.after_cancel(self._status_anim_job)
            except Exception:
                pass
            self._status_anim_job = None

        self._status_anim_base = text
        self._status_anim_step = 0
        self.info_box.config(text=text, fg=fg)

        if animate:
            self._status_anim_tick(fg)

    def _status_anim_tick(self, fg):
        dots = "." * (self._status_anim_step % 4)
        self.info_box.config(text=self._status_anim_base + dots, fg=fg)
        self._status_anim_step += 1
        self._status_anim_job = self.root.after(350, lambda: self._status_anim_tick(fg))

    def _progress_on(self):
        try:
            self.progress.start(10)
        except Exception:
            pass

    def _progress_off(self):
        try:
            self.progress.stop()
        except Exception:
            pass

    def validate_input(self, new_value):
        if new_value == "":
            return True
        return new_value.isdigit() and len(new_value) == 1 and new_value != "0"

    def select_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png *.jpg *.jpeg")])
        if file_path:
            self.image_path = file_path
            self._status_set("Görsel işleniyor\nLütfen bekleyin (Gemini API)", fg="#E67E22", animate=True)
            self._progress_on()
            self.btn_img.config(state=tk.DISABLED)
            threading.Thread(target=self.run_ocr_thread, daemon=True).start()

    def run_ocr_thread(self):
        try:
            grid = parse_sudoku_grid(self.image_path)
            self.queue.put(("ocr_success", grid))
        except Exception as e:
            self.queue.put(("error", str(e)))

    def populate_grid(self, grid):
        self.clear_grid()
        if not grid:
            return
        for r in range(9):
            for c in range(9):
                val = grid[r][c]
                if val != 0:
                    self.grid_entries[r][c].insert(0, str(val))
                    self.grid_entries[r][c].config(fg="black")

    def get_grid_from_ui(self):
        grid = [[0]*9 for _ in range(9)]
        for r in range(9):
            for c in range(9):
                val = self.grid_entries[r][c].get()
                if val.isdigit():
                    grid[r][c] = int(val)
        return grid

    def start_solve_thread(self):
        current_grid = self.get_grid_from_ui()
        is_empty = all(all(cell == 0 for cell in row) for row in current_grid)
        if is_empty:
            messagebox.showwarning("Uyarı", "Grid boş! Lütfen sayı girin veya resim yükleyin.")
            return

        self.original_grid = [row[:] for row in current_grid]
        self._status_set("SAT Solver çalışıyor\nÇözümler aranıyor", fg="blue", animate=True)
        self._progress_on()
        self.btn_solve.config(state=tk.DISABLED)

        threading.Thread(target=self.run_solve_thread, args=(current_grid,), daemon=True).start()

    def run_solve_thread(self, grid):
        try:
            is_solvable, solutions = find_all_solutions(grid)
            self.queue.put(("solve_result", (is_solvable, solutions)))
        except Exception as e:
            self.queue.put(("error", str(e)))

    def display_solution(self, solution_grid):
        for r in range(9):
            for c in range(9):
                entry = self.grid_entries[r][c]
                if self.original_grid and self.original_grid[r][c] != 0:
                    entry.delete(0, tk.END)
                    entry.insert(0, str(self.original_grid[r][c]))
                    entry.config(fg="black")
                else:
                    entry.delete(0, tk.END)
                    entry.insert(0, str(solution_grid[r][c]))
                    entry.config(fg=RENK_COZUM)

    def prev_solution(self):
        if self.solutions and self.current_solution_index > 0:
            self.current_solution_index -= 1
            self.update_nav_ui()

    def next_solution(self):
        if self.solutions and self.current_solution_index < len(self.solutions) - 1:
            self.current_solution_index += 1
            self.update_nav_ui()

    def update_nav_ui(self):
        self.display_solution(self.solutions[self.current_solution_index])
        self.lbl_count.config(text=f"{self.current_solution_index + 1} / {len(self.solutions)}")
        self.btn_prev.config(state=tk.NORMAL if self.current_solution_index > 0 else tk.DISABLED)
        self.btn_next.config(state=tk.NORMAL if self.current_solution_index < len(self.solutions) - 1 else tk.DISABLED)

    def clear_grid(self):
        for row in self.grid_entries:
            for entry in row:
                entry.delete(0, tk.END)
                entry.config(fg=RENK_YAZI)

        self.solutions = []
        self.original_grid = None

        self._progress_off()
        self._status_set("Grid temizlendi.", fg=RENK_YAZI, animate=False)

        self.lbl_count.config(text="0 / 0")
        self.btn_prev.config(state=tk.DISABLED)
        self.btn_next.config(state=tk.DISABLED)
        self.btn_solve.config(state=tk.NORMAL)
        self.btn_img.config(state=tk.NORMAL)

    def check_queue(self):
        try:
            while True:
                msg_type, data = self.queue.get_nowait()

                if msg_type == "ocr_success":
                    self._progress_off()
                    self.btn_img.config(state=tk.NORMAL)
                    if data:
                        self.populate_grid(data)
                        self._status_set("OCR Başarılı!\nHataları elle düzeltebilirsiniz.", fg=RENK_COZUM, animate=False)
                    else:
                        self._status_set("Sayı okunamadı!", fg="red", animate=False)

                elif msg_type == "solve_result":
                    self._progress_off()
                    self.btn_solve.config(state=tk.NORMAL)
                    is_solvable, solutions = data

                    if is_solvable and solutions:
                        self.solutions = solutions
                        self.current_solution_index = 0
                        self.update_nav_ui()
                        self._status_set(f"Çözüm Bulundu!\nToplam: {len(solutions)}", fg=RENK_COZUM, animate=False)
                    else:
                        self._status_set("Çözüm Yok (UNSAT)", fg="red", animate=False)
                        messagebox.showerror("Sonuç", "Bu Sudoku çözülemez!")

                elif msg_type == "error":
                    self._progress_off()
                    self.btn_img.config(state=tk.NORMAL)
                    self.btn_solve.config(state=tk.NORMAL)
                    self._status_set("Hata oluştu", fg="red", animate=False)
                    messagebox.showerror("Hata", f"İşlem hatası: {data}")

        except queue.Empty:
            pass
        finally:
            self.root.after(100, self.check_queue)

if __name__ == "__main__":
    root = tk.Tk()
    app = SudokuGUI(root)
    root.mainloop()