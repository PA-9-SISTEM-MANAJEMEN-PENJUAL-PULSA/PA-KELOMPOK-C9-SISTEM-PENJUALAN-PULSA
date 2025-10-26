# =========================================================
# SISTEM MANAJEMEN PAKET INTERNET & PULSA - FLASHCELL 💻⚡
# =========================================================

import os
import csv
import pwinput
import time
import sys
from datetime import datetime
from prettytable import PrettyTable
from colorama import Fore, Style, init

# -----------------------------
# Inisialisasi
# -----------------------------
init(autoreset=True, convert=True)
os.makedirs("data", exist_ok=True)

# -----------------------------
# Header CSV
# -----------------------------
headers_user = ("username", "password", "role", "saldo", "points", "level")
headers_produk = ("id", "nama", "tipe", "harga", "masa_aktif")
headers_transaksi = ("username", "nama_produk", "tipe", "harga", "masa_aktif", "waktu", "no_hp")

# -----------------------------
# Buat file CSV jika belum ada
# -----------------------------
for file, header in [
    ("data/data_pengguna.csv", headers_user),
    ("data/data_produk.csv", headers_produk),
    ("data/riwayat_transaksi.csv", headers_transaksi)
]:
    if not os.path.exists(file):
        with open(file, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(header)

# -----------------------------
# Fungsi utilitas CSV
# -----------------------------
def load_csv(filepath):
    try:
        with open(filepath, "r", newline="", encoding="utf-8") as f:
            return list(csv.DictReader(f))
    except Exception:
        return []

def save_csv(filepath, data, fieldnames):
    with open(filepath, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)

def cetak_pelan(teks, delay=0.02):
    for huruf in teks:
        sys.stdout.write(huruf)
        sys.stdout.flush()
        time.sleep(delay)
    print()

def format_rp(angka):
    try:
        return f"Rp {int(angka):,}"
    except Exception:
        return f"Rp {angka}"

def hitung_level(points):
    try:
        p = int(points)
    except Exception:
        p = 0
    if p >= 300:
        return "Platinum"
    elif p >= 100:
        return "Gold"
    else:
        return "Silver"

# -----------------------------
# Data Default
# -----------------------------
def buat_admin_default():
    users = load_csv("data/data_pengguna.csv")
    if not any(u.get("role") == "admin" for u in users):
        users.append({
            "username": "admin",
            "password": "000",
            "role": "admin",
            "saldo": "1000000",
            "points": "0",
            "level": "Platinum"
        })
        save_csv("data/data_pengguna.csv", users, headers_user)

def buat_produk_default():
    data = load_csv("data/data_produk.csv")
    if len(data) == 0:
        produk_awal = [
            {"id": "001", "nama": "Paket Internet 5GB", "tipe": "Internet", "harga": "20000", "masa_aktif": "5"},
            {"id": "002", "nama": "Paket Internet 10GB", "tipe": "Internet", "harga": "30000", "masa_aktif": "10"},
            {"id": "003", "nama": "Pulsa 25000", "tipe": "Pulsa", "harga": "25000", "masa_aktif": "0"},
            {"id": "004", "nama": "Pulsa 50000", "tipe": "Pulsa", "harga": "50000", "masa_aktif": "0"},
            {"id": "005", "nama": "Paket Unlimited 1 Hari", "tipe": "Internet", "harga": "10000", "masa_aktif": "1"}
        ]
        save_csv("data/data_produk.csv", produk_awal, headers_produk)

# -----------------------------
# Dashboard User
# -----------------------------
def tampilkan_dashboard(user):
    cetak_pelan(f"\n💎 Dashboard {user['username']} ({user.get('level','Silver')} Member)")
    cetak_pelan(f"Saldo: {format_rp(user.get('saldo', '0'))}")
    cetak_pelan(f"Points: {user.get('points', '0')}")
    cetak_pelan("🔥 Promo Hari ini: Top-up +5% bonus saldo!")
    if int(user.get("saldo", 0)) < 50000:
        cetak_pelan(Fore.YELLOW + "⚠️ Saldo rendah! Segera lakukan top-up." + Style.RESET_ALL)

# -----------------------------
# Fungsi Registrasi
# -----------------------------
def register():
    users = load_csv("data/data_pengguna.csv")
    while True:
        try:
            username = input(Fore.CYAN + "✨ Masukkan username baru (3-12) ketik 0 batal: " + Style.RESET_ALL).strip()
            if username == "0":
                print(Fore.YELLOW + "⚠️ Registrasi dibatalkan." + Style.RESET_ALL)
                return
            if not (3 <= len(username) <= 12):
                print(Fore.RED + "❌ Username harus 3-12 karakter!" + Style.RESET_ALL)
                continue
            if any(u["username"] == username for u in users):
                print(Fore.RED + "❌ Username sudah terdaftar!" + Style.RESET_ALL)
                continue

            password = pwinput.pwinput(Fore.CYAN + "🔒 Masukkan password baru (4-8) ketik 0 batal: " + Style.RESET_ALL)
            if password == "0":
                print(Fore.YELLOW + "⚠️ Registrasi dibatalkan." + Style.RESET_ALL)
                return
            if not (4 <= len(password) <= 8):
                print(Fore.RED + "❌ Password harus 4-8 karakter!" + Style.RESET_ALL)
                continue

            users.append({
                "username": username,
                "password": password,
                "role": "user",
                "saldo": "200000",
                "points": "0",
                "level": "Silver"
            })
            save_csv("data/data_pengguna.csv", users, headers_user)
            print(Fore.GREEN + f"✅ Registrasi berhasil! Saldo awal: {format_rp(200000)} 🎉" + Style.RESET_ALL)
            return
        except (KeyboardInterrupt, EOFError):
            print(Fore.YELLOW + "\n⚠️ Registrasi dibatalkan." + Style.RESET_ALL)
            return

# -----------------------------
# Fungsi Login
# -----------------------------
def login():
    users = load_csv("data/data_pengguna.csv")
    try:
        username = input(Fore.CYAN + "👤 Masukkan username: " + Style.RESET_ALL).strip()
        password = pwinput.pwinput(Fore.CYAN + "🔑 Masukkan password: " + Style.RESET_ALL)
        for user in users:
            if user["username"] == username and user["password"] == password:
                user["level"] = hitung_level(user.get("points", "0"))
                print(Fore.GREEN + f"\n🎉 Selamat datang, {username}! Role: {user['role']}. Saldo: {format_rp(user['saldo'])}\n" + Style.RESET_ALL)
                if user["role"] == "user":
                    tampilkan_dashboard(user)
                return user
        print(Fore.RED + "❌ Login gagal! Username atau password salah." + Style.RESET_ALL)
        return None
    except (KeyboardInterrupt, EOFError):
        print(Fore.YELLOW + "\n⚠️ Login dibatalkan." + Style.RESET_ALL)
        return None

# -----------------------------
# Top-up Saldo (Bank/E-Wallet)
# -----------------------------
def top_up_saldo(username):
    users = load_csv("data/data_pengguna.csv")
    user = next((u for u in users if u["username"]==username), None)
    if not user:
        print(Fore.RED + "❌ Akun tidak ditemukan!" + Style.RESET_ALL)
        return

    percobaan = 0
    saldo_lama = int(user.get("saldo",0))
    while percobaan < 3:
        try:
            print("\n💳 Pilih metode top-up:")
            print("1. Bank Transfer")
            print("2. E-Wallet (OVO/Gopay/Dana)")
            metode = input("Pilih: ").strip()
            if metode not in ["1","2"]:
                print(Fore.RED + "❌ Pilihan tidak valid!" + Style.RESET_ALL)
                continue

            inp = input(f"💸 Masukkan jumlah top-up (min 1.000, max 500.000) atau ketik 0 batal: ").strip()
            if inp == "0":
                print(Fore.YELLOW + "⚠️ Top-up dibatalkan." + Style.RESET_ALL)
                return
            jumlah = int(inp)
            if jumlah < 1000 or jumlah > 500000:
                print(Fore.RED + "❌ Jumlah top-up tidak sesuai!" + Style.RESET_ALL)
                percobaan +=1
                continue

            # Simulasi proses top-up
            cetak_pelan("💰 Memproses top-up...",0.05)
            time.sleep(0.5)
            if metode=="1":
                cetak_pelan("🏦 Transfer Bank berhasil!")
            else:
                cetak_pelan("📱 Top-up E-Wallet berhasil!")

            bonus = int(jumlah*0.05)
            total = saldo_lama + jumlah + bonus
            user["saldo"] = str(total)
            save_csv("data/data_pengguna.csv", users, headers_user)
            print(Fore.GREEN + f"✅ Top-up berhasil! Saldo lama: {format_rp(saldo_lama)} → Saldo baru: {format_rp(total)} (bonus {format_rp(bonus)})" + Style.RESET_ALL)
            return
        except ValueError:
            print(Fore.RED + "❌ Harus berupa angka!" + Style.RESET_ALL)
            percobaan +=1
        except (KeyboardInterrupt, EOFError):
            print(Fore.YELLOW + "\n⚠️ Top-up dibatalkan." + Style.RESET_ALL)
            return

# -----------------------------
# Tampilkan Produk
# -----------------------------
def tampilkan_produk(data=None):
    if data is None:
        data = load_csv("data/data_produk.csv")
    if not data:
        print(Fore.YELLOW + "⚠️ Belum ada data produk." + Style.RESET_ALL)
        return
    tabel = PrettyTable()
    tabel.field_names = ["ID", "Nama Produk", "Tipe", "Harga", "Masa Aktif (hari)"]
    for p in data:
        masa = p.get("masa_aktif")
        try:
            masa_int = int(masa)
            if p.get("tipe")=="Internet" and masa_int < 1:
                masa_int = 1
            elif p.get("tipe")=="Pulsa":
                masa_int = 0
        except (TypeError, ValueError):
            masa_int = 1 if p.get("tipe")=="Internet" else 0
        tabel.add_row([p.get("id"), p.get("nama"), p.get("tipe"), format_rp(p.get("harga")), f"{masa_int} hari"])
    print(tabel)

# -----------------------------
# Cari Produk Interaktif
# -----------------------------
def cari_produk_interaktif(data):
    if not data:
        print(Fore.YELLOW + "⚠️ Belum ada data produk." + Style.RESET_ALL)
        return []

    keyword = input("🔍 Masukkan kata kunci (nama/tipe/harga): ").strip().lower()
    hasil = [
        p for p in data
        if keyword in p.get("nama", "").lower()
        or keyword in p.get("tipe", "").lower()
        or keyword in str(p.get("harga", "")).lower()
    ]

    if hasil:
        print(Fore.GREEN + f"\n✅ Ditemukan {len(hasil)} produk yang cocok:" + Style.RESET_ALL)
        tampilkan_produk(hasil)
    else:
        print(Fore.YELLOW + "\n⚠️ Tidak ada produk yang cocok." + Style.RESET_ALL)
    return hasil

# -----------------------------
# Urutkan Produk Interaktif
# -----------------------------
def urutkan_produk_interaktif(data):
    if not data:
        print(Fore.YELLOW + "⚠️ Belum ada data produk." + Style.RESET_ALL)
        return data

    print("\n📊 Pilihan pengurutan:")
    print("1. Harga (Termurah → Termahal)")
    print("2. Harga (Termahal → Termurah)")
    print("3. Nama (A-Z)")
    print("4. Nama (Z-A)")
    opsi = input("Pilih: ").strip()

    if opsi == "1":
        data_sorted = sorted(data, key=lambda x: int(x.get("harga", 0)))
    elif opsi == "2":
        data_sorted = sorted(data, key=lambda x: int(x.get("harga", 0)), reverse=True)
    elif opsi == "3":
        data_sorted = sorted(data, key=lambda x: x.get("nama", "").lower())
    elif opsi == "4":
        data_sorted = sorted(data, key=lambda x: x.get("nama", "").lower(), reverse=True)
    else:
        print(Fore.RED + "❌ Pilihan tidak valid!" + Style.RESET_ALL)
        return data

    print(Fore.GREEN + "\n✅ Data berhasil diurutkan:" + Style.RESET_ALL)
    tampilkan_produk(data_sorted)
    return data_sorted

# --------------------------------------
# Pilih ID Produk (untuk edit/hapus/beli)
# ---------------------------------------
def pilih_id_produk(data, max_attempt=3):
    percobaan = 0
    while percobaan < max_attempt:
        try:
            id_produk = input("🆔 Masukkan ID produk (ketik '0' untuk kembali): ").strip()
            if id_produk == "0":
                return None
            for row in data:
                if row.get("id") == id_produk:
                    return row
            percobaan += 1
            print(Fore.RED + f"❌ ID tidak ditemukan. Sisa percobaan: {max_attempt-percobaan}" + Style.RESET_ALL)
        except (KeyboardInterrupt, EOFError):
            print(Fore.YELLOW + "\n⚠️ Input dibatalkan. Kembali ke menu sebelumnya." + Style.RESET_ALL)
            return None
    print(Fore.RED + "❌ Terlalu banyak kesalahan. Kembali ke menu sebelumnya." + Style.RESET_ALL)
    return None

# -----------------------------
# Tambah Produk
# -----------------------------
def tambah_produk():
    data = load_csv("data/data_produk.csv")
    last_id = int(data[-1].get("id")) if data else 0
    id_produk = str(last_id + 1).zfill(3)
    try:
        nama = input("📝 Masukkan nama produk (0 batal): ").strip()
        if nama == "0" or nama == "":
            print(Fore.YELLOW + "⚠️ Penambahan produk dibatalkan." + Style.RESET_ALL)
            return

        while True:
            tipe = input("📦 Masukkan tipe (Internet/Pulsa): ").strip().title()
            if tipe == "0":
                print(Fore.YELLOW + "⚠️ Penambahan produk dibatalkan." + Style.RESET_ALL)
                return
            if tipe in ["Internet", "Pulsa"]:
                break
            print(Fore.RED + "❌ Tipe produk harus 'Internet' atau 'Pulsa'." + Style.RESET_ALL)

        while True:
            harga_input = input("💰 Masukkan harga (angka): ").strip()
            if harga_input == "0":
                print(Fore.YELLOW + "⚠️ Penambahan produk dibatalkan." + Style.RESET_ALL)
                return
            try:
                harga = int(harga_input)
                break
            except ValueError:
                print(Fore.RED + "❌ Harga harus berupa angka!" + Style.RESET_ALL)

        # Input masa aktif dengan pernyataan jelas
        while True:
            masa_aktif_input = input("⏳ Masukkan masa aktif (angka saja, contoh: 20 → otomatis dianggap 20 hari, min 1 untuk Internet, 0 untuk Pulsa): ").strip()
            if masa_aktif_input == "0" and tipe == "Pulsa":
                masa_aktif = "0"
                break
            if masa_aktif_input.isdigit() and int(masa_aktif_input) > 0:
                masa_aktif = masa_aktif_input
                break
            print(Fore.RED + "❌ Masa aktif harus berupa angka. Tidak perlu menulis 'hari'!" + Style.RESET_ALL)

        data.append({"id": id_produk, "nama": nama, "tipe": tipe, "harga": str(harga), "masa_aktif": masa_aktif})
        save_csv("data/data_produk.csv", data, headers_produk)
        print(Fore.GREEN + "✅ Produk berhasil ditambahkan!" + Style.RESET_ALL)
    except (KeyboardInterrupt, EOFError):
        print(Fore.YELLOW + "\n⚠️ Penambahan produk dibatalkan." + Style.RESET_ALL)


# -----------------------------
# Edit Produk
# -----------------------------
def edit_produk():
    data = load_csv("data/data_produk.csv")
    tampilkan_produk(data)
    row = pilih_id_produk(data)
    if not row:
        return
    try:
        new_name = input(f"📝 Nama baru ({row.get('nama')}) [ketik 0 batal]: ").strip()
        if new_name == "0":
            print(Fore.YELLOW + "⚠️ Edit produk dibatalkan." + Style.RESET_ALL)
            return
        if new_name:
            row["nama"] = new_name

        tipe_input = input(f"📦 Tipe baru ({row.get('tipe')}): ").strip().title()
        if tipe_input == "0":
            print(Fore.YELLOW + "⚠️ Edit produk dibatalkan." + Style.RESET_ALL)
            return
        if tipe_input in ["Internet", "Pulsa"]:
            row["tipe"] = tipe_input

        harga_input = input(f"💰 Harga baru ({row.get('harga')}): ").strip()
        if harga_input == "0":
            print(Fore.YELLOW + "⚠️ Edit produk dibatalkan." + Style.RESET_ALL)
            return
        if harga_input:
            try:
                row["harga"] = str(int(harga_input))
            except ValueError:
                print(Fore.RED + "❌ Harga tidak valid. Tetap menggunakan harga lama." + Style.RESET_ALL)

        # Input masa aktif dengan pernyataan jelas
        while True:
            masa_input = input(f"⏳ Masa aktif baru ({row.get('masa_aktif')}) (angka saja, contoh: 20 → otomatis dianggap 20 hari, min 1 untuk Internet, 0 untuk Pulsa): ").strip()
            if masa_input == "0" and row.get("tipe") == "Pulsa":
                row["masa_aktif"] = "0"
                break
            if masa_input.isdigit() and int(masa_input) > 0:
                row["masa_aktif"] = masa_input
                break
            print(Fore.RED + "❌ Masa aktif harus berupa angka. Tidak perlu menulis 'hari'!" + Style.RESET_ALL)

        save_csv("data/data_produk.csv", data, headers_produk)
        print(Fore.GREEN + "✅ Produk berhasil diedit!" + Style.RESET_ALL)
    except (KeyboardInterrupt, EOFError):
        print(Fore.YELLOW + "\n⚠️ Edit produk dibatalkan." + Style.RESET_ALL)


# -----------------------------
# Hapus Produk
# -----------------------------
def hapus_produk():
    data = load_csv("data/data_produk.csv")
    tampilkan_produk(data)
    row = pilih_id_produk(data)
    if not row:
        return
    try:
        confirm = input(f"❗ Yakin hapus produk '{row.get('nama')}'? (y/n): ").strip().lower()
        if confirm != "y":
            print(Fore.YELLOW + "⚠️ Hapus produk dibatalkan." + Style.RESET_ALL)
            return
        data.remove(row)
        # Update ID setelah hapus
        for idx in range(len(data)):
            data[idx]["id"] = str(idx + 1).zfill(3)
        save_csv("data/data_produk.csv", data, headers_produk)
        print(Fore.GREEN + "✅ Produk dihapus & ID diperbarui!" + Style.RESET_ALL)
    except (KeyboardInterrupt, EOFError):
        print(Fore.YELLOW + "\n⚠️ Hapus produk dibatalkan." + Style.RESET_ALL)

# -----------------------------
# Tampilkan Invoice
# -----------------------------
def tampilkan_invoice(username, produk_row, harga, masa_aktif, waktu, no_hp="-"):
    invoice_id = f"TRX-{int(time.time())}"

    # Minta nomor HP kalau produk Pulsa atau Internet
    if produk_row.get("tipe") in ["Pulsa", "Internet"]:
        no_hp = input("📱 Masukkan nomor HP tujuan: ").strip()
    else:
        no_hp = "-"

    def cetak_pelan(teks, delay=0.02):
        for huruf in teks:
            sys.stdout.write(huruf)
            sys.stdout.flush()
            time.sleep(delay)
        print()

    # Cetak struk
    print(Fore.YELLOW + "\n🖨️ Mencetak struk transaksi......." + Style.RESET_ALL)
    time.sleep(0.5)
    for _ in range(2): sys.stdout.write("."); sys.stdout.flush(); time.sleep(0.3)
    print("\n")

    cetak_pelan("=====================================")
    cetak_pelan("           FLASHCELL KONTER 💻         ")
    cetak_pelan("=====================================")
    time.sleep(0.1)
    cetak_pelan(f"ID Transaksi : {invoice_id}")
    cetak_pelan(f"Kasir        : {username}")
    cetak_pelan(f"Produk       : {produk_row.get('nama')}")
    cetak_pelan(f"Tipe Produk  : {produk_row.get('tipe')}")
    cetak_pelan(f"No. HP Tujuan : {no_hp}")
    cetak_pelan(f"Harga        : {format_rp(harga)}")
    cetak_pelan(f"Masa Aktif   : {masa_aktif} hari")
    cetak_pelan(f"Waktu        : {waktu}")
    cetak_pelan("-------------------------------------")
    cetak_pelan("✅ Transaksi berhasil 🎉")
    cetak_pelan("Terima kasih telah menggunakan FLASHCELL✨")
    cetak_pelan("=====================================")

    # Simpan ke file
    try:
        simpan = input("💾 Simpan struk ke file? (y/n): ").strip().lower()
        if simpan == "y":
            filename = f"data/invoice_{username}_{int(time.time())}.txt"
            with open(filename, "w", encoding="utf-8") as f:
                f.write("=====================================\n")
                f.write("           FLASHCELL KONTER 💻        \n")
                f.write("=====================================\n")
                f.write(f"ID Transaksi : {invoice_id}\n")
                f.write(f"Kasir        : {username}\n")
                f.write(f"Produk       : {produk_row.get('nama')}\n")
                f.write(f"Tipe Produk  : {produk_row.get('tipe')}\n")
                f.write(f"No. HP Tujuan : {no_hp}\n")
                f.write(f"Harga        : {format_rp(harga)}\n")
                f.write(f"Masa Aktif   : {masa_aktif} hari\n")
                f.write(f"Waktu        : {waktu}\n")
                f.write("-------------------------------------\n")
                f.write("✅ Transaksi berhasil 🎉\n")
                f.write("Terima kasih telah menggunakan FLASHCELL✨\n")
                f.write("=====================================\n")
            print(f"💾 Struk tersimpan di {filename}")
        else:
            print("⚠️ Struk tidak disimpan, hanya ditampilkan di layar.")
    except (KeyboardInterrupt, EOFError):
        print("\n⚠️ Simpan struk dibatalkan.")

# --------------------------------------
# Lihat Semua Riwayat Transaksi (Admin)
# --------------------------------------
def lihat_semua_riwayat():
    data_transaksi = load_csv("data/riwayat_transaksi.csv")
    if not data_transaksi:
        print(Fore.YELLOW + "⚠️ Belum ada transaksi sama sekali.\n" + Style.RESET_ALL)
        return
    tabel = PrettyTable()
    tabel.field_names = ["Username","Produk","Tipe","Harga","Masa Aktif","No HP","Waktu"]
    for trx in data_transaksi:
        tabel.add_row([
            trx.get("username"),
            trx.get("nama_produk"),
            trx.get("tipe"),
            format_rp(trx.get("harga")),
            trx.get("masa_aktif"),
            trx.get("no_hp","-"),
            trx.get("waktu")
        ])
    print(tabel)

# -----------------------------
# Statistik Penjualan Admin
# -----------------------------
def statistik_admin():
    data_transaksi = load_csv("data/riwayat_transaksi.csv")
    if not data_transaksi:
        print(Fore.YELLOW + "⚠️ Belum ada transaksi, statistik kosong." + Style.RESET_ALL)
        return
    
    total_transaksi = len(data_transaksi)
    total_pendapatan = sum(int(trx.get("harga",0)) for trx in data_transaksi)
    
    produk_terjual = {}
    for trx in data_transaksi:
        nama = trx.get("nama_produk","-")
        produk_terjual[nama] = produk_terjual.get(nama,0) + 1
    
    print(Fore.CYAN + f"\n📊 Statistik Penjualan FLASHCELL" + Style.RESET_ALL)
    print(f"Total Transaksi : {total_transaksi}")
    print(f"Total Pendapatan: {format_rp(total_pendapatan)}")
    print("\nProduk Terjual:")
    for produk, jumlah in produk_terjual.items():
        print(f" • {produk}: {jumlah} kali")
    print()

# -----------------------------
# Lihat Riwayat Transaksi User
# -----------------------------
def lihat_riwayat(username):
    data_transaksi = load_csv("data/riwayat_transaksi.csv")
    user_trx = [trx for trx in data_transaksi if trx.get("username")==username]
    if not user_trx:
        print(Fore.YELLOW + "\n⚠️ Belum ada riwayat transaksi.\n" + Style.RESET_ALL)
        return
    tabel = PrettyTable()
    tabel.field_names = ["Nama Produk","Tipe","Harga","Masa Aktif","Waktu"]
    for trx in user_trx:
        tabel.add_row([
            trx.get("nama_produk"),
            trx.get("tipe"),
            format_rp(trx.get("harga")),
            trx.get("masa_aktif","0"),
            trx.get("waktu")
        ])
    print(tabel)

# ---------------------------------------------------------------------------------
# Beli Produk + Update Saldo, Points, Level + Undo (dengan input no HP untuk Pulsa)
# ---------------------------------------------------------------------------------
def beli_produk(username):
    data_produk = load_csv("data/data_produk.csv")
    tampilkan_produk(data_produk)
    produk_row = pilih_id_produk(data_produk)
    if not produk_row:
        return
    users = load_csv("data/data_pengguna.csv")
    user = next((u for u in users if u["username"]==username), None)
    if not user:
        print(Fore.RED + "❌ Akun tidak ditemukan!" + Style.RESET_ALL)
        return
    harga = int(produk_row.get("harga",0))
    masa_aktif = produk_row.get("masa_aktif","0")
    saldo_user = int(user.get("saldo",0))
    if saldo_user < harga:
        print(Fore.RED + "❌ Saldo tidak cukup!" + Style.RESET_ALL)
        return

    # Input nomor HP untuk Pulsa
    no_hp = ""
    if produk_row.get("tipe") == "Pulsa":
        while True:
            no_hp = input("📱 Masukkan nomor HP tujuan (9-15 digit): ").strip()
            if no_hp.isdigit() and 9 <= len(no_hp) <= 15:
                break
            print(Fore.RED + "❌ Nomor HP harus berupa angka dan 9-15 digit!" + Style.RESET_ALL)

    try:
        confirm = input(f"❗ Konfirmasi beli '{produk_row['nama']}' seharga {format_rp(harga)}? (y/n): ").strip().lower()
        if confirm != "y":
            print(Fore.YELLOW + "⚠️ Transaksi dibatalkan." + Style.RESET_ALL)
            return
    except (KeyboardInterrupt, EOFError):
        print(Fore.YELLOW + "\n⚠️ Transaksi dibatalkan." + Style.RESET_ALL)
        return

    waktu = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    transaksi = {
        "username": username,
        "nama_produk": produk_row.get("nama"),
        "tipe": produk_row.get("tipe"),
        "harga": str(harga),
        "masa_aktif": masa_aktif,
        "waktu": waktu,
        "no_hp": no_hp if no_hp else "-"
    }

    # Update saldo, points, level
    user["saldo"] = str(saldo_user - harga)
    user["points"] = str(int(user.get("points",0))+10)
    user["level"] = hitung_level(user.get("points",0))
    save_csv("data/data_pengguna.csv", users, headers_user)

    # Simpan transaksi
    data_transaksi = load_csv("data/riwayat_transaksi.csv")
    data_transaksi.append(transaksi)
    save_csv("data/riwayat_transaksi.csv", data_transaksi, headers_transaksi)

    # Tampilkan invoice
    tampilkan_invoice(username, produk_row, harga, masa_aktif, waktu)

    print(Fore.GREEN + f"✅ Saldo sekarang: {format_rp(user['saldo'])} | Points: {user['points']} | Level: {user['level']}" + Style.RESET_ALL)
    print(Fore.GREEN + "✅ Transaksi berhasil! Terima kasih telah membeli." + Style.RESET_ALL)
    
#-------------------
# Reminder harian
#-------------------
def tampilkan_reminder_harian():
    data_produk = load_csv("data/data_produk.csv")
    daily = [p for p in data_produk if p.get("tipe") == "Internet" and str(p.get("masa_aktif")) == "1"]
    if not daily:
        return

    # Format tanggal bahasa Indonesia
    bulan_list = [
        "Januari", "Februari", "Maret", "April", "Mei", "Juni",
        "Juli", "Agustus", "September", "Oktober", "November", "Desember"
    ]
    hari_list = [
        "Senin", "Selasa", "Rabu", "Kamis",
        "Jumat", "Sabtu", "Minggu"
    ]
    now = datetime.now()
    hari = hari_list[now.weekday()]
    tanggal = f"{hari}, {now.day} {bulan_list[now.month - 1]} {now.year}"

    # Cetak reminder dengan warna
    print(Fore.MAGENTA + "\n🔔 Paket Harian Hari Ini (" + tanggal + "):" + Style.RESET_ALL)
    for p in daily:
        print(Fore.YELLOW + f" • {p.get('nama','').strip()}" + Style.RESET_ALL)
    print()

# -----------------------------
# Menu Utama Admin
# -----------------------------
def menu_admin():
    while True:
        try:
            print("\n======== MENU ADMIN FLASHCELL 👑 ========")
            print("1. Lihat Produk 🛍️")
            print("2. Tambah Produk ➕")
            print("3. Edit Produk ✏️")
            print("4. Hapus Produk 🗑️")
            print("5. Lihat Semua Riwayat Transaksi 📜")
            print("6. Statistik Penjualan 📈")
            print("7. Keluar 🔙")
            pilihan = input("Pilih menu: ").strip()
            if pilihan=="1":
                menu_lihat_produk()
            elif pilihan=="2":
                tambah_produk()
            elif pilihan=="3":
                edit_produk()
            elif pilihan=="4":
                hapus_produk()
            elif pilihan=="5":     
                lihat_semua_riwayat()
            elif pilihan=="6":
                statistik_admin()
            elif pilihan=="7":
                break
            else:
                print(Fore.RED + "❌ Pilihan tidak valid!" + Style.RESET_ALL)
        except (KeyboardInterrupt, EOFError):
            print(Fore.YELLOW + "\n⚠️ Kembali ke menu utama admin." + Style.RESET_ALL)
            break

# -----------------------------
# Menu Utama User
# -----------------------------
def menu_user(username):
    while True:
        try:
            print(f"\n======== MENU USER ({username}) 👤 ========")
            print("1. Lihat Produk 🛍️")
            print("2. Beli Produk 🛒")
            print("3. Top Up Saldo 💸")
            print("4. Lihat Riwayat Transaksi 📜")
            print("5. Keluar 🔙")
            pilihan = input("Pilih menu: ").strip()
            if pilihan=="1":
                menu_lihat_produk()
            elif pilihan=="2":
                beli_produk(username)
            elif pilihan=="3":
                top_up_saldo(username)
            elif pilihan=="4":
                lihat_riwayat(username)
            elif pilihan=="5":
                break
            else:
                print(Fore.RED + "❌ Pilihan tidak valid!" + Style.RESET_ALL)
        except (KeyboardInterrupt, EOFError):
            print(Fore.YELLOW + "\n⚠️ Kembali ke menu utama user." + Style.RESET_ALL)
            break

# -----------------------------
# Menu Lihat Produk Interaktif
# -----------------------------
def menu_lihat_produk():
    data = load_csv("data/data_produk.csv")
    while True:
        try:
            print("\n---- MENU LIHAT PRODUK ----")
            print("1. Tampilkan semua produk 🛍️")
            print("2. Cari produk 🔍")
            print("3. Urutkan produk 📊")
            print("4. Kembali 🔙")
            pilihan = input("Pilih: ").strip()
            
            if pilihan == "1":
                tampilkan_produk(data)
            elif pilihan == "2":
                cari_produk_interaktif(data)
            elif pilihan == "3":
                urutkan_produk_interaktif(data)
            elif pilihan == "4":
                break
            else:
                print(Fore.RED + "❌ Pilihan tidak valid!" + Style.RESET_ALL)
        
        except (KeyboardInterrupt, EOFError):
            print(Fore.YELLOW + "\n⚠️ Kembali ke menu sebelumnya." + Style.RESET_ALL)
            break

# -----------------------------
# Program Utama
# -----------------------------
def main():
    buat_admin_default()
    buat_produk_default()

    tampilkan_reminder_harian()

    while True:
        try:
            print("\n=== SISTEM MANAJEMEN PAKET INTERNET DAN PULSA FLASHCELL 💻 ===") 
            print("1. Login 🔑")
            print("2. Register ✨")
            print("3. Keluar 🚪")
            pilihan = input("Pilih menu: ").strip()
            if pilihan=="1":
                user = login()
                if user:
                    if user["role"]=="admin":
                        menu_admin()
                    else:
                        menu_user(user["username"])
            elif pilihan=="2":
                register()
            elif pilihan=="3":
                print(Fore.CYAN + "\nTerima kasih telah menggunakan FLASHCELL 💖" + Style.RESET_ALL)
                break
            else:
                print(Fore.RED + "❌ Pilihan tidak valid!" + Style.RESET_ALL)
        except (KeyboardInterrupt, EOFError):
            print(Fore.YELLOW + "\n⚠️ Program dihentikan oleh pengguna." + Style.RESET_ALL)
            break

# ---------------------------
# Jalankan Program
# ---------------------------
if __name__=="__main__":
    main()