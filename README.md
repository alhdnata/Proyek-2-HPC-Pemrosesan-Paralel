# Proyek 2 — High Performance Computing (HPC)

## Deskripsi

Proyek ini merupakan implementasi pembelajaran mengenai **High Performance Computing (HPC)** dengan fokus pada pemrosesan paralel menggunakan Python.

Studi kasus yang digunakan adalah pemrosesan data cuaca sintetis. Program membandingkan metode serial, yaitu pemrosesan data secara berurutan, dengan metode paralel yang membagi pekerjaan ke beberapa proses.

Hasil pengujian digunakan untuk mempelajari pengaruh pemrosesan paralel terhadap waktu eksekusi dan efisiensi komputasi.

## Tujuan

- Memahami konsep pemrosesan serial dan paralel.
- Mengukur waktu eksekusi setiap metode.
- Menghitung speedup dan efisiensi pemrosesan.
- Memastikan hasil serial dan paralel konsisten.
- Menampilkan hasil benchmark dalam bentuk grafik.
- Memahami pengaruh jumlah proses terhadap kinerja program.

## Teknologi

- Python
- Pandas
- Matplotlib
- ProcessPoolExecutor dari modul concurrent.futures

## Cara Menjalankan

Pastikan Python sudah terinstal di komputer.

Instal library yang diperlukan:

```bash
python -m pip install -r requirements.txt
```

Jalankan program:

```bash
python main.py
```

Dataset sintetis akan dibuat secara otomatis apabila belum tersedia. Setelah pengujian selesai, program menyimpan hasil benchmark dan grafik ke folder `output`.

## Metode Pengujian

### 1. Pemrosesan Serial

Setiap baris data diproses secara berurutan menggunakan satu alur eksekusi.

### 2. Pemrosesan Paralel

Data dibagi menjadi beberapa bagian dan diproses menggunakan beberapa proses melalui `ProcessPoolExecutor`.

### 3. Validasi Hasil

Hasil dari kedua metode dibandingkan untuk memeriksa apakah jumlah dan nilai hasil komputasinya sama.

### 4. Evaluasi Kinerja

Program mencatat waktu eksekusi dan menghitung dua indikator utama.

**Speedup**

Speedup menunjukkan perbandingan waktu pemrosesan serial terhadap waktu pemrosesan paralel.

Speedup lebih dari 1 menunjukkan bahwa metode paralel lebih cepat dalam pengujian tersebut.

**Efisiensi**

Efisiensi dihitung dengan membagi speedup dengan jumlah worker, kemudian mengalikannya dengan 100%.

Nilai ini memberikan gambaran sederhana mengenai pemanfaatan worker dalam pemrosesan paralel.

## Output

- `hasil_benchmark.csv`: hasil pengukuran waktu, speedup, dan efisiensi.
- `perbandingan_waktu.png`: grafik perbandingan waktu eksekusi.
- `speedup.png`: grafik speedup relatif terhadap pemrosesan serial.

## Batasan

Dataset yang digunakan merupakan data sintetis untuk demonstrasi, bukan pengukuran cuaca aktual.

Pengujian dilakukan pada satu komputer dan bukan pada cluster HPC. Hasil benchmark dapat berbeda bergantung pada spesifikasi CPU, jumlah data, penggunaan sumber daya sistem, dan overhead pembuatan proses.

Pemrosesan paralel tidak selalu lebih cepat karena pembagian pekerjaan dan komunikasi antarp proses juga memerlukan waktu.

## Kesimpulan

Proyek ini menunjukkan cara membandingkan pemrosesan serial dan paralel melalui eksperimen yang terukur. Hasil benchmark dapat digunakan untuk memahami kapan pemrosesan paralel berpotensi meningkatkan kinerja komputasi.

Proyek ini merupakan demonstrasi konsep dasar HPC dan dapat dikembangkan lebih lanjut dengan pengujian berbagai ukuran data, variasi jumlah worker, dan penggunaan infrastruktur komputasi terdistribusi.