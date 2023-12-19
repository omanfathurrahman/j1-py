import xmlrpc.client

# Fungsi untuk menampilkan menu perintah
def tampilkan_menu():
    print("Pilih perintah:")
    print("1. Registrasi Pasien")
    print("2. Informasi Antrean")
    print("3. Nomor Antrean")
    print("4. Tampil Informasi Antrean")
    print("6. Panggil Pasien")
    print("7. Pembaruan Antrean dan Database")
    print("8. Rekam Medis Diperbarui")
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
    
    print("\n")
    
    # Menampilkan daftar klinik
    print("Daftar Klinik:")
    daftar_klinik = menampilkan_daftar_klinik(server)
    
    # Meminta input klinik yang dipilih
    klinik_dipilih = input(f"Pilih klinik [1-{len(daftar_klinik)}]:")
    nama_klinik_dipilih = daftar_klinik[int(klinik_dipilih) - 1]
    
    # Mengecek kesediaan tempat
    kesediaan_tempat = server.verifikasi_ketersediaan_tempat(nama_klinik_dipilih)
    if kesediaan_tempat == "Tempat penuh.":
        print("Antrean penuh")
        return
    
    # Meminta informasi pribadi dari client
    nomor_rekam_medis = input("Masukkan nomor rekam medis: ")
    nama = input("Masukkan nama: ")
    tanggal_lahir = input("Masukkan tanggal lahir (YYYY-MM-DD): ")
    
    # Registrasi pasien dan pemberian nomor antrean
    print(server.registrasi_pasien(nomor_rekam_medis, nama, tanggal_lahir, nama_klinik_dipilih))

# Fungsi untuk mengecek antrian clien
def cek_nomor_antrean_client(server):
    # Meminta input klinik dan nomor rekam medis
    daftar_klinik = menampilkan_daftar_klinik(server)
    klinik_dipilih = input(f"Pilih klinik [1-{len(daftar_klinik)}]")
    nomor_rekam_medis = input("Masukkan nomor rekam medis: ")
    nama_klinik_dipilih = daftar_klinik[int(klinik_dipilih) - 1]
    
    # Mengecek antrean pasian pada klinik yang dipilih
    print(server.cek_nomor_antrean(nomor_rekam_medis, nama_klinik_dipilih))
    print("_"*20)

if __name__ == "__main__":
    server = xmlrpc.client.ServerProxy("http://localhost:8000/")

    while True:
        tampilkan_menu()
        pilihan = input("Masukkan pilihan (1-9): ")

        if pilihan == "1":
            registrasi_pasien(server)
        elif pilihan == "2":
            cek_nomor_antrean_client(server)
        elif pilihan == "9":
            print("Terima kasih. Keluar dari program.")
            break
        else:
            print("Pilihan tidak valid. Silakan pilih kembali.")
