import tkinter as tk
from tkinter import ttk
import tkinter.messagebox as msg
import sqlite3

def koneksi():
    return sqlite3.connect("nilai_siswa.db")

def create_table():
    con = koneksi()
    cur = con.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS nilai_siswa (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nama_siswa TEXT NOT NULL,
            biologi INTEGER,
            fisika INTEGER,
            inggris INTEGER,
            prediksi_fakultas TEXT
        )
    """)
    con.commit()
    con.close()

def prediksi_fakultas(bio, fis, eng):
    if bio > fis and bio > eng:
        return "Kedokteran"
    elif fis > bio and fis > eng:
        return "Teknik"
    elif eng > bio and eng > fis:
        return "Bahasa"
    else:
        return "Tidak Diketahui"

def insert_data(nama, bio, fis, eng, prediksi):
    con = koneksi()
    cur = con.cursor()
    cur.execute("INSERT INTO nilai_siswa (nama_siswa, biologi, fisika, inggris, prediksi_fakultas) VALUES (?, ?, ?, ?, ?)",
                (nama, bio, fis, eng, prediksi))
    con.commit()
    con.close()

def read_data():
    con = koneksi()
    cur = con.cursor()
    cur.execute("SELECT nama_siswa, biologi, fisika, inggris, prediksi_fakultas FROM nilai_siswa ORDER BY id")
    rows = cur.fetchall()
    con.close()
    return rows

def update_data(nama, bio, fis, eng, prediksi):
        con = koneksi()
        cur = con.cursor()
        cur.execute("""
        UPDATE nilai_siswa 
        SET biologi=?, fisika=?, inggris=?, prediksi_fakultas=? 
        WHERE nama_siswa=?
        """, (bio, fis, eng, prediksi, nama))
        con.commit()
        con.close()

def delete_data(nama):
     con = koneksi()
     cur = con.cursor()
     cur.execute("DELETE FROM nilai_siswa WHERE nama_siswa=?", (nama,))
     con.commit()
     con.close()

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Prediksi Fakultas Siswa")
        self.geometry("700x500")
        self.configure(bg="#f0f0f0")

        frame = tk.Frame(self, bg="#ffffff", padx=10, pady=10)
        frame.pack(padx=10, pady=10, fill="x")

        
        tk.Label(frame, text="Nama Siswa:", bg="#ffffff").grid(row=0, column=0, sticky="w")
        self.ent_nama = tk.Entry(frame, width=30)
        self.ent_nama.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(frame, text="Nilai Biologi:", bg="#ffffff").grid(row=1, column=0, sticky="w")
        self.ent_bio = tk.Entry(frame, width=30)
        self.ent_bio.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(frame, text="Nilai Fisika:", bg="#ffffff").grid(row=2, column=0, sticky="w")
        self.ent_fis = tk.Entry(frame, width=30)
        self.ent_fis.grid(row=2, column=1, padx=5, pady=5)

        tk.Label(frame, text="Nilai Inggris:", bg="#ffffff").grid(row=3, column=0, sticky="w")
        self.ent_eng = tk.Entry(frame, width=30)
        self.ent_eng.grid(row=3, column=1, padx=5, pady=5)

        # Tombol
        btn_frame = tk.Frame(frame, bg="#ffffff")
        btn_frame.grid(row=4, column=0, columnspan=2, pady=10)

        tk.Button(btn_frame, text="Submit", command=self.submit_data, width=12).pack(side="left", padx=5)
        tk.Button(btn_frame, text="Clear", command=self.clear_inputs, width=12).pack(side="left", padx=5)
        tk.Button(btn_frame, text="Refresh", command=self.refresh_table, width=12).pack(side="left", padx=5)
        tk.Button(btn_frame, text="Update", command=self.update_data, width=12).pack(side="left", padx=5)
        tk.Button(btn_frame, text="Delete", command=self.delete_data, width=12).pack(side="left", padx=5)
   
        columns = ("Nama Siswa", "Biologi", "Fisika", "Inggris", "Prediksi Fakultas")
        self.tree = ttk.Treeview(self, columns=columns, show="headings")
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=120, anchor="center")
        self.tree.pack(padx=10, pady=10, fill="both", expand=True)

        self.refresh_table()

    def submit_data(self):
        nama = self.ent_nama.get()
        try:
            bio = int(self.ent_bio.get())
            fis = int(self.ent_fis.get())
            eng = int(self.ent_eng.get())
        except ValueError:
            msg.showerror("Input Error", "Semua nilai harus berupa angka.")
            return
        
        prediksi = prediksi_fakultas(bio, fis, eng)
        insert_data(nama, bio, fis, eng, prediksi)
        self.refresh_table()
        self.clear_inputs()

    def clear_inputs(self):
        self.ent_nama.delete(0, tk.END)
        self.ent_bio.delete(0, tk.END)
        self.ent_fis.delete(0, tk.END)
        self.ent_eng.delete(0, tk.END)

    def refresh_table(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        for data in read_data():
            self.tree.insert("", "end", values=data)

    def update_data(self):
        nama = self.ent_nama.get()
        try:
            bio = int(self.ent_bio.get())
            fis = int(self.ent_fis.get())
            eng = int(self.ent_eng.get())
        except ValueError:
            msg.showerror("Input Error", "Semua nilai harus berupa angka.")
            return

        prediksi = prediksi_fakultas(bio, fis, eng)
        update_data(nama, bio, fis, eng, prediksi)
        self.refresh_table()
        self.clear_inputs()
        msg.showinfo("Update", f"Data {nama} berhasil diperbarui.")

    def delete_data(self):
        nama = self.ent_nama.get()
        if not nama:
            msg.showerror("Delete Error", "Masukkan nama siswa yang ingin dihapus.")
            return

        delete_data(nama)
        self.refresh_table()
        self.clear_inputs()
        msg.showinfo("Delete", f"Data {nama} berhasil dihapus.")

if __name__ == "__main__":
    create_table()
    app = App()
    app.mainloop()    

