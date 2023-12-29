import xmlrpc.server
from xmlrpc.server import SimpleXMLRPCServer
import threading
import time

# Inisialisasi database pasien dan antrian
database_pasien = {}
antrean = {}
pasien_saat_ini = {}  # Pasien yang sedang dilayani

# Inisialisasi daftar klinik dan kapasitas klinik
daftar_klinik = ['Klinik A', 'Klinik B', 'Klinik C']
kapasitas_klinik = {'Klinik A': 10, 'Klinik B': 15, 'Klinik C': 20}

for klinik in daftar_klinik:
    antrean[klinik] = []
    pasien_saat_ini[klinik] = None

# Fungsi untuk registrasi pasien
def registrasi_pasien(nomor_rekam_medis, nama, tanggal_lahir, nama_klinik_dipilih):
    if nomor_rekam_medis in database_pasien:
        return "Nomor rekam medis sudah ada."
    else:
        database_pasien[nomor_rekam_medis] = {'nama': nama, 'tanggal_lahir': tanggal_lahir}
        antrean[nama_klinik_dipilih].append(nomor_rekam_medis)
        print(antrean)
        if pasien_saat_ini[nama_klinik_dipilih] is None:
            pasien_saat_ini[nama_klinik_dipilih] = nomor_rekam_medis
            print(pasien_saat_ini)
            return f"Registrasi berhasil.\nNomor antrean Anda adalah {antrean[nama_klinik_dipilih].index(nomor_rekam_medis)+1}\nSekarang giliran anda, silahkan menuju klinik"
        print(antrean)
        return f"Registrasi berhasil.\nNomor antrean Anda adalah {antrean[nama_klinik_dipilih].index(nomor_rekam_medis)+1}"

# Fungsi untuk verifikasi ketersediaan tempat
def verifikasi_ketersediaan_tempat(nama_klinik):
    if len(antrean[nama_klinik]) < kapasitas_klinik[nama_klinik]:
        return "Tempat tersedia."
    else:
        return "Tempat penuh."

# Fungsi untuk mengecek nomor urutan antrean pasien
def cek_nomor_antrean(nomor_rekam_medis, nama_klinik):
    if nomor_rekam_medis in antrean[nama_klinik]:
        if pasien_saat_ini[nama_klinik] == nomor_rekam_medis:
            return f"Nomor antrean Anda adalah {antrean[nama_klinik].index(nomor_rekam_medis) +1}\nSekarang giliran anda, silahkan menuju klinik"
        return f"Nomor antrean Anda adalah {antrean[nama_klinik].index(nomor_rekam_medis) +1}"
    return "Anda belum terdaftar di klinik ini"

# Fungsi untuk melihat daftar klinik
def lihat_daftar_klinik():
    return daftar_klinik

# Fungsi untuk melihat daftar antrean
def lihat_daftar_antrean():
    return antrean

# Fungsi untuk konfirmasi pasien
def konfirmasi_pasien(nomor_rekam_medis, nama_klinik):
    global pasien_saat_ini
    if pasien_saat_ini[nama_klinik] == nomor_rekam_medis:
        if antrean[nama_klinik]:
            antrean[nama_klinik].pop(0)
            pasien_saat_ini[nama_klinik] = None
            if antrean[nama_klinik]:  # Jika masih ada antrian, pindahkan ke pasien berikutnya
                pasien_saat_ini[nama_klinik] = antrean[nama_klinik][0]
                print(pasien_saat_ini[nama_klinik])
            return "Konfirmasi diterima, antrian bergerak ke pasien berikutnya."
        print(pasien_saat_ini[nama_klinik])
    return "Bukan giliran anda."

# Buat server XML-RPC
server = SimpleXMLRPCServer(("localhost", 8000))
server.register_function(registrasi_pasien, "registrasi_pasien")
server.register_function(verifikasi_ketersediaan_tempat, "verifikasi_ketersediaan_tempat")
server.register_function(cek_nomor_antrean, "cek_nomor_antrean")
server.register_function(lihat_daftar_klinik, "lihat_daftar_klinik")
server.register_function(lihat_daftar_antrean, "lihat_daftar_antrean")
server.register_function(konfirmasi_pasien, "konfirmasi_pasien")

print("Server Medis siap menerima permintaan...")
server.serve_forever()
