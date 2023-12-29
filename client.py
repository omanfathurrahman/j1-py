import xmlrpc.client

# Fungsi untuk menampilkan menu perintah
def tampilkan_menu():
    print("Pilih perintah:")
    print("1. Registrasi Pasien")
    print("2. Cek Nomor Antrean")
    print("3. Menuju Klinik")
    print("9. Keluar")

# Fungsi Untuk menampilkan daftar klinik
def menampilkan_daftar_klinik(server):
    daftar_klinik = server.lihat_daftar_klinik()
    print("_____________")
    for index, klinik in enumerate(daftar_klinik):
        print(f"{index+1}. {klinik}")
    print("_____________")
    return daftar_klinik

# Fungsi untuk registrasi pasien
def registrasi_pasien(server):
    print("\nDaftar Klinik:")
    daftar_klinik = menampilkan_daftar_klinik(server)
    
    klinik_dipilih = input(f"Pilih klinik [1-{len(daftar_klinik)}]: ")
    nama_klinik_dipilih = daftar_klinik[int(klinik_dipilih) - 1]
    
    kesediaan_tempat = server.verifikasi_ketersediaan_tempat(nama_klinik_dipilih)
    if kesediaan_tempat == "Tempat penuh.":
        print("Antrean penuh")
        return
    
    nomor_rekam_medis = input("Masukkan nomor rekam medis: ")
    nama = input("Masukkan nama: ")
    tanggal_lahir = input("Masukkan tanggal lahir (YYYY-MM-DD): ")
    
    print(server.registrasi_pasien(nomor_rekam_medis, nama, tanggal_lahir, nama_klinik_dipilih))

# Fungsi untuk mengecek nomor antrean
def cek_nomor_antrean_client(server):
    daftar_klinik = menampilkan_daftar_klinik(server)
    klinik_dipilih = input(f"Pilih klinik [1-{len(daftar_klinik)}]: ")
    nomor_rekam_medis = input("Masukkan nomor rekam medis: ")
    nama_klinik_dipilih = daftar_klinik[int(klinik_dipilih) - 1]
    
    print(server.cek_nomor_antrean(nomor_rekam_medis, nama_klinik_dipilih))
    print("_" * 20)

# Fungsi untuk konfirmasi kehadiran
def konfirmasi_kehadiran(server):
    daftar_klinik = menampilkan_daftar_klinik(server)
    klinik_dipilih = input(f"Pilih klinik [1-{len(daftar_klinik)}]: ")
    nomor_rekam_medis = input("Masukkan nomor rekam medis: ")
    nama_klinik_dipilih = daftar_klinik[int(klinik_dipilih) - 1]

    print(server.konfirmasi_pasien(nomor_rekam_medis, nama_klinik_dipilih))

if __name__ == "__main__":
    server = xmlrpc.client.ServerProxy("http://localhost:8000/")

    while True:
        tampilkan_menu()
        pilihan = input("Masukkan pilihan (1-9): ")

        if pilihan == "1":
            registrasi_pasien(server)
        elif pilihan == "2":
            cek_nomor_antrean_client(server)
        elif pilihan == "3":
            konfirmasi_kehadiran(server)
        elif pilihan == "9":
            print("Terima kasih. Keluar dari program.")
            break
        else:
            print("Pilihan tidak valid. Silakan pilih kembali.")
