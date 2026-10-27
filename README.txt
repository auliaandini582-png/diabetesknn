PROYEK DATA MINING KNN - PYTHON

Isi folder:
1. aplikasi_knn.py            Program Python dengan tampilan GUI.
2. data_pasien.csv            Dataset 10 pasien yang diambil dari Excel tugas.
3. Data_Mining_KKN_asli.xlsx  Salinan file Excel asli yang dikirim.
4. README.txt                 Panduan menjalankan program.

CARA MENJALANKAN:
1. Ekstrak file ZIP terlebih dahulu.
2. Pastikan Python 3 sudah terpasang.
3. Buka folder hasil ekstrak di Visual Studio Code.
4. Jalankan aplikasi_knn.py dengan tombol Run Python File, atau:
   python aplikasi_knn.py

Tidak perlu menginstal library tambahan untuk menjalankan aplikasi GUI karena memakai
tkinter dan pustaka standar Python. File CSV dibaca otomatis dari folder yang sama.

DESAIN APLIKASI:
- Header biru tua.
- Form input data pasien baru.
- Pilihan nilai K.
- Tombol Hitung KNN.
- Kartu hasil klasifikasi.
- Tab dataset dan urutan jarak.
- Ekspor hasil ke CSV.

DATA AWAL:
Pasien baru sesuai Excel: Usia 42, BMI 28.5, Glukosa 130,
Tekanan Darah 128, Riwayat Keluarga 1.
Nilai K awal = 3. Hasil yang diharapkan dari dataset Excel adalah TINGGI.

CATATAN:
Ini merupakan contoh pembelajaran algoritma KNN berdasarkan dataset tugas, bukan alat
diagnosis medis. Data pasien dan kategori merupakan data latihan.
