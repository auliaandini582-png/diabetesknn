"""
Aplikasi Klasifikasi Data Mining KNN
Jalankan: python aplikasi_knn.py
Persyaratan: pandas, openpyxl (untuk ekspor Excel)
"""
import math
import csv
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from pathlib import Path

APP_DIR = Path(__file__).resolve().parent
DATA_FILE = APP_DIR / "data_pasien.csv"

def load_data():
    rows = []
    with open(DATA_FILE, newline="", encoding="utf-8-sig") as f:
        for row in csv.DictReader(f):
            rows.append({
                "Pasien": row["Pasien"],
                "Usia": float(row["Usia"]),
                "BMI": float(row["BMI"]),
                "Glukosa": float(row["Glukosa"]),
                "Tekanan Darah": float(row["Tekanan Darah"]),
                "Riwayat Keluarga": float(row["Riwayat Keluarga"]),
                "Kelas": row["Kelas"]
            })
    return rows

FEATURES = ["Usia", "BMI", "Glukosa", "Tekanan Darah", "Riwayat Keluarga"]

class KNNApp:
    def __init__(self, root):
        self.root = root
        self.root.title("KNN Data Mining | Klasifikasi Pasien")
        self.root.geometry("1120x740")
        self.root.minsize(940, 650)
        self.data = load_data()
        self.result_rows = []
        self.setup_style()
        self.build_ui()
        self.show_dataset()

    def setup_style(self):
        style = ttk.Style()
        try:
            style.theme_use("clam")
        except tk.TclError:
            pass
        style.configure("Treeview", rowheight=28, font=("Arial", 10))
        style.configure("Treeview.Heading", font=("Arial", 10, "bold"))
        style.configure("Title.TLabel", font=("Arial", 20, "bold"))
        style.configure("Sub.TLabel", font=("Arial", 10))
        style.configure("Accent.TButton", font=("Arial", 10, "bold"), padding=8)

    def build_ui(self):
        self.root.configure(bg="#f3f6fb")
        header = tk.Frame(self.root, bg="#183153", padx=24, pady=18)
        header.pack(fill="x")
        tk.Label(header, text="DATA MINING • ALGORITMA KNN", bg="#183153",
                 fg="white", font=("Arial", 20, "bold")).pack(anchor="w")
        tk.Label(header, text="Aplikasi klasifikasi data pasien menggunakan jarak Euclidean",
                 bg="#183153", fg="#dbeafe", font=("Arial", 10)).pack(anchor="w", pady=(5, 0))

        body = tk.Frame(self.root, bg="#f3f6fb", padx=18, pady=14)
        body.pack(fill="both", expand=True)

        form = tk.LabelFrame(body, text="  Data Pasien Baru  ", bg="white",
                             font=("Arial", 11, "bold"), padx=12, pady=10)
        form.pack(fill="x", pady=(0, 12))
        self.entries = {}
        labels = [
            ("Usia", "42"), ("BMI", "28.5"), ("Glukosa", "130"),
            ("Tekanan Darah", "128"), ("Riwayat Keluarga (0=Tidak, 1=Ada)", "1")
        ]
        for i, (label, default) in enumerate(labels):
            col = i % 3
            row = i // 3
            cell = tk.Frame(form, bg="white")
            cell.grid(row=row, column=col, sticky="ew", padx=8, pady=5)
            tk.Label(cell, text=label, bg="white", fg="#344054",
                     font=("Arial", 9, "bold")).pack(anchor="w")
            entry = ttk.Entry(cell, width=24)
            entry.insert(0, default)
            entry.pack(fill="x", pady=(4, 0))
            key = FEATURES[i]
            self.entries[key] = entry
            form.grid_columnconfigure(col, weight=1)

        controls = tk.Frame(form, bg="white")
        controls.grid(row=1, column=2, sticky="ew", padx=8, pady=5)
        tk.Label(controls, text="Nilai K (jumlah tetangga)", bg="white",
                 fg="#344054", font=("Arial", 9, "bold")).pack(anchor="w")
        self.k_var = tk.StringVar(value="3")
        self.k_box = ttk.Combobox(controls, textvariable=self.k_var,
                                  values=["1", "3", "5", "7", "9"], state="readonly", width=20)
        self.k_box.pack(fill="x", pady=(4, 0))
        ttk.Button(controls, text="Hitung KNN", style="Accent.TButton",
                   command=self.calculate).pack(fill="x", pady=(8, 0))

        self.result_card = tk.Frame(body, bg="white", padx=16, pady=12,
                                    highlightbackground="#d8e1ee", highlightthickness=1)
        self.result_card.pack(fill="x", pady=(0, 12))
        tk.Label(self.result_card, text="HASIL KLASIFIKASI", bg="white",
                 fg="#667085", font=("Arial", 9, "bold")).pack(anchor="w")
        self.result_label = tk.Label(self.result_card, text="Klik “Hitung KNN” untuk melihat hasil",
                                     bg="white", fg="#183153", font=("Arial", 16, "bold"))
        self.result_label.pack(anchor="w", pady=(5, 2))
        self.detail_label = tk.Label(self.result_card, text="Data pasien lama: 10 baris • Metode: Euclidean",
                                     bg="white", fg="#667085", font=("Arial", 9))
        self.detail_label.pack(anchor="w")

        tabs = ttk.Notebook(body)
        tabs.pack(fill="both", expand=True)
        data_tab = tk.Frame(tabs, bg="white")
        result_tab = tk.Frame(tabs, bg="white")
        tabs.add(data_tab, text="Dataset Pasien")
        tabs.add(result_tab, text="Urutan Jarak KNN")
        self.dataset_tree = self.make_tree(data_tab,
            ["Pasien", "Usia", "BMI", "Glukosa", "Tekanan Darah", "Riwayat Keluarga", "Kelas"])
        self.result_tree = self.make_tree(result_tab,
            ["Peringkat", "Pasien", "Jumlah Kuadrat", "Jarak Euclidean", "Kelas"])
        bottom = tk.Frame(body, bg="#f3f6fb")
        bottom.pack(fill="x", pady=(10, 0))
        ttk.Button(bottom, text="Ekspor hasil ke CSV", command=self.export_csv).pack(side="left")
        tk.Label(bottom, text="Dataset dapat dilihat pada file data_pasien.csv",
                 bg="#f3f6fb", fg="#667085", font=("Arial", 9)).pack(side="right")

    def make_tree(self, parent, columns):
        frame = tk.Frame(parent, bg="white")
        frame.pack(fill="both", expand=True, padx=8, pady=8)
        tree = ttk.Treeview(frame, columns=columns, show="headings")
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=125, anchor="center")
        yscroll = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
        xscroll = ttk.Scrollbar(frame, orient="horizontal", command=tree.xview)
        tree.configure(yscrollcommand=yscroll.set, xscrollcommand=xscroll.set)
        tree.grid(row=0, column=0, sticky="nsew")
        yscroll.grid(row=0, column=1, sticky="ns")
        xscroll.grid(row=1, column=0, sticky="ew")
        frame.grid_rowconfigure(0, weight=1)
        frame.grid_columnconfigure(0, weight=1)
        return tree

    def show_dataset(self):
        for row in self.data:
            vals = [row["Pasien"], f'{row["Usia"]:g}', f'{row["BMI"]:g}',
                    f'{row["Glukosa"]:g}', f'{row["Tekanan Darah"]:g}',
                    int(row["Riwayat Keluarga"]), row["Kelas"]]
            self.dataset_tree.insert("", "end", values=vals)

    def calculate(self):
        try:
            target = {key: float(entry.get().strip()) for key, entry in self.entries.items()}
            if target["Riwayat Keluarga"] not in (0, 1):
                raise ValueError("Riwayat Keluarga harus 0 atau 1.")
            if target["Usia"] < 0 or target["BMI"] <= 0 or target["Glukosa"] < 0 or target["Tekanan Darah"] < 0:
                raise ValueError("Nilai angka harus masuk akal dan tidak negatif.")
            k = int(self.k_var.get())
            if k > len(self.data):
                raise ValueError("Nilai K tidak boleh melebihi jumlah data.")
        except ValueError as exc:
            messagebox.showerror("Input tidak valid", str(exc) or "Pastikan semua isian berupa angka.")
            return

        results = []
        for person in self.data:
            parts = {feature: (person[feature] - target[feature]) ** 2 for feature in FEATURES}
            total = sum(parts.values())
            results.append({
                "Pasien": person["Pasien"], "Jumlah Kuadrat": total,
                "Jarak Euclidean": math.sqrt(total), "Kelas": person["Kelas"]
            })
        results.sort(key=lambda item: item["Jarak Euclidean"])
        for i, item in enumerate(results, 1):
            item["Peringkat"] = i
        nearest = results[:k]
        votes = {}
        for item in nearest:
            votes[item["Kelas"]] = votes.get(item["Kelas"], 0) + 1
        # Jika suara seri, pilih kelas dengan jumlah jarak total paling kecil.
        winner = sorted(votes, key=lambda cls: (
            -votes[cls], sum(r["Jarak Euclidean"] for r in nearest if r["Kelas"] == cls)
        ))[0]
        self.result_rows = results

        for item in self.result_tree.get_children():
            self.result_tree.delete(item)
        for item in results:
            self.result_tree.insert("", "end", values=(
                item["Peringkat"], item["Pasien"], f'{item["Jumlah Kuadrat"]:.2f}',
                f'{item["Jarak Euclidean"]:.6f}', item["Kelas"]
            ))
        self.result_label.config(text=f"Hasil klasifikasi: {winner.upper()}",
                                 fg="#16803c" if winner.lower() == "rendah" else "#b54708")
        nearest_names = ", ".join(f'{r["Pasien"]} ({r["Kelas"]})' for r in nearest)
        self.detail_label.config(text=f"K={k} • Tetangga terdekat: {nearest_names} • Suara: " +
                                      ", ".join(f"{c}={n}" for c, n in votes.items()))

    def export_csv(self):
        if not self.result_rows:
            messagebox.showinfo("Belum ada hasil", "Klik Hitung KNN terlebih dahulu.")
            return
        path = filedialog.asksaveasfilename(
            title="Simpan hasil KNN", defaultextension=".csv",
            filetypes=[("CSV", "*.csv")], initialfile="hasil_knn.csv"
        )
        if not path:
            return
        with open(path, "w", newline="", encoding="utf-8-sig") as f:
            writer = csv.DictWriter(f, fieldnames=[
                "Peringkat", "Pasien", "Jumlah Kuadrat", "Jarak Euclidean", "Kelas"
            ])
            writer.writeheader()
            writer.writerows(self.result_rows)
        messagebox.showinfo("Berhasil", f"Hasil tersimpan di:\n{path}")

if __name__ == "__main__":
    root = tk.Tk()
    app = KNNApp(root)
    root.mainloop()
