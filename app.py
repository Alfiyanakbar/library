import streamlit as st
import sqlite3
from datetime import datetime

# Fungsi untuk setup database
def setup_database():
    conn = sqlite3.connect("RentalBukuDB.db")
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Buku (
        id_buku INTEGER PRIMARY KEY AUTOINCREMENT,
        judul TEXT NOT NULL,
        penulis TEXT NOT NULL,
        stok INTEGER NOT NULL
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Pelanggan (
        id_pelanggan INTEGER PRIMARY KEY AUTOINCREMENT,
        nama TEXT NOT NULL,
        alamat TEXT NOT NULL,
        telepon TEXT NOT NULL
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Transaksi (
        id_transaksi INTEGER PRIMARY KEY AUTOINCREMENT,
        id_buku INTEGER NOT NULL,
        id_pelanggan INTEGER NOT NULL,
        tanggal_pinjam DATE NOT NULL,
        tanggal_kembali DATE,
        denda REAL DEFAULT 0,
        FOREIGN KEY (id_buku) REFERENCES Buku (id_buku),
        FOREIGN KEY (id_pelanggan) REFERENCES Pelanggan (id_pelanggan)
    );
    """)
    conn.commit()
    conn.close()

# Fungsi untuk menambah data Buku
def add_buku(judul, penulis, stok):
    if not (judul and penulis and stok.isdigit()):
        st.error("Masukkan data yang valid!")
        return

    conn = sqlite3.connect("RentalBukuDB.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO Buku (judul, penulis, stok) VALUES (?, ?, ?)", (judul, penulis, int(stok)))
    conn.commit()
    conn.close()

    st.success("Data buku berhasil ditambahkan!")

# Fungsi untuk menambah data Pelanggan
def add_pelanggan(nama, alamat, telepon):
    if not (nama and alamat and telepon):
        st.error("Masukkan data yang valid!")
        return

    conn = sqlite3.connect("RentalBukuDB.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO Pelanggan (nama, alamat, telepon) VALUES (?, ?, ?)", (nama, alamat, telepon))
    conn.commit()
    conn.close()

    st.success("Data pelanggan berhasil ditambahkan!")

# Fungsi untuk menambah data Transaksi
def add_transaksi(id_buku, id_pelanggan, tanggal_pinjam, tanggal_kembali, denda):
    if not (id_buku.isdigit() and id_pelanggan.isdigit() and tanggal_pinjam and tanggal_kembali and denda.replace(".", "").isdigit()):
        st.error("Masukkan data yang valid!")
        return

    conn = sqlite3.connect("RentalBukuDB.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO Transaksi (id_buku, id_pelanggan, tanggal_pinjam, tanggal_kembali, denda) VALUES (?, ?, ?, ?, ?)",
                   (int(id_buku), int(id_pelanggan), tanggal_pinjam, tanggal_kembali, float(denda)))
    conn.commit()
    conn.close()

    st.success("Transaksi berhasil ditambahkan!")

# Fungsi untuk menampilkan data Buku
def show_buku():
    conn = sqlite3.connect("RentalBukuDB.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Buku")
    rows = cursor.fetchall()
    conn.close()

    st.write("### Data Buku")
    for row in rows:
        st.write(f"ID: {row[0]}, Judul: {row[1]}, Penulis: {row[2]}, Stok: {row[3]}")

# Fungsi untuk menampilkan data Pelanggan
def show_pelanggan():
    conn = sqlite3.connect("RentalBukuDB.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Pelanggan")
    rows = cursor.fetchall()
    conn.close()

    st.write("### Data Pelanggan")
    for row in rows:
        st.write(f"ID: {row[0]}, Nama: {row[1]}, Alamat: {row[2]}, Telepon: {row[3]}")

# Fungsi untuk menampilkan data Transaksi
def show_transaksi():
    conn = sqlite3.connect("RentalBukuDB.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Transaksi")
    rows = cursor.fetchall()
    conn.close()

    st.write("### Data Transaksi")
    for row in rows:
        st.write(f"ID Transaksi: {row[0]}, ID Buku: {row[1]}, ID Pelanggan: {row[2]}, Tanggal Pinjam: {row[3]}, Tanggal Kembali: {row[4]}, Denda: {row[5]}")

# Setup Database
setup_database()

# Streamlit Interface
st.title("Sistem Penyewaan Buku")

# Tab Buku
st.subheader("Tambah Buku")
judul = st.text_input("Judul Buku")
penulis = st.text_input("Penulis Buku")
stok = st.text_input("Stok Buku")
if st.button("Tambah Buku"):
    add_buku(judul, penulis, stok)

# Tampilkan Buku
if st.button("Tampilkan Buku"):
    show_buku()

# Tab Pelanggan
st.subheader("Tambah Pelanggan")
nama = st.text_input("Nama Pelanggan")
alamat = st.text_input("Alamat Pelanggan")
telepon = st.text_input("Telepon Pelanggan")
if st.button("Tambah Pelanggan"):
    add_pelanggan(nama, alamat, telepon)

# Tampilkan Pelanggan
if st.button("Tampilkan Pelanggan"):
    show_pelanggan()

# Tab Transaksi
st.subheader("Tambah Transaksi")
id_buku = st.text_input("ID Buku")
id_pelanggan = st.text_input("ID Pelanggan")
tanggal_pinjam = st.date_input("Tanggal Pinjam")
tanggal_kembali = st.date_input("Tanggal Kembali")
denda = st.text_input("Denda")
if st.button("Tambah Transaksi"):
    add_transaksi(id_buku, id_pelanggan, str(tanggal_pinjam), str(tanggal_kembali), denda)

# Tampilkan Transaksi
if st.button("Tampilkan Transaksi"):
    show_transaksi()
