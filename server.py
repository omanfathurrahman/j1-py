import xmlrpc.server
from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.server import SimpleXMLRPCRequestHandler

# Inisialisasi database pasien dan antrean
database_pasien = {}
antrean = {}

# Fungsi untuk registrasi pasien
def registrasi_pasien(nomor_rekam_medis, nama, tanggal_lahir, nama_klinik_dipilih):
    # Mengecek nomor rekam medis pada database pasien
    if nomor_rekam_medis in database_pasien:
        return "Nomor rekam medis sudah ada."
    else:
        # Memasukkan data baru pada database pasien
        database_pasien[nomor_rekam_medis] = {'nama': nama, 'tanggal_lahir': tanggal_lahir}
        
        # Menambahkan nomor rekam medis pasien ke antrean klinik
        antrean[nama_klinik_dipilih].append(nomor_rekam_medis)
        
        return f"Registrasi berhasil.\nNomor antrean Anda adalah {antrean[nama_klinik_dipilih].index(nomor_rekam_medis)+1}"
    

# Fungsi untuk verifikasi ketersediaan tempat
def verifikasi_ketersediaan_tempat(nama_klinik):
    # Mengecek kesediaan tempat pada klinik yang dipilih
    if len(antrean[nama_klinik]) < kapasitas_klinik[nama_klinik]:
        return "Tempat tersedia."
    else:
        return "Tempat penuh."

# Fungsi untuk mengecek nomor urutan atrean pasien
def cek_nomor_antrean(nomor_rekam_medis, nama_klinik):
    # Mengecek nomor rekam medis pasien pada antrean klinik
    if nomor_rekam_medis in antrean[nama_klinik]:
        return f"Nomor antrean Anda adalah {antrean[nama_klinik].index(nomor_rekam_medis) +1}"
    return "Anda belum terdaftar di klinik ini"

# Inisialisasi daftar klinik dan kapasitas klinik
daftar_klinik = ['Klinik A', 'Klinik B', 'Klinik C']

# Fungsi Untuk melihat daftar klinik
def lihat_daftar_klinik():
    return daftar_klinik

# Fungsi Untuk melihat daftar antrean
def lihat_daftar_antrean():
    return antrean


kapasitas_klinik = {'Klinik A': 10, 'Klinik B': 15, 'Klinik C': 20}

for i in daftar_klinik:
    antrean[i] = []

# Buat server XML-RPC
server = SimpleXMLRPCServer(("localhost", 8000))
server.register_function(registrasi_pasien, "registrasi_pasien")
server.register_function(verifikasi_ketersediaan_tempat, "verifikasi_ketersediaan_tempat")
server.register_function(lihat_daftar_antrean, "lihat_daftar_antrean")
server.register_function(cek_nomor_antrean, "cek_nomor_antrean")
server.register_function(lihat_daftar_klinik, "lihat_daftar_klinik")

# Jalankan server
print("Server Medis siap menerima permintaan...")
server.serve_forever()
