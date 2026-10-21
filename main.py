
import os
import time
from pathlib import Path
from concurrent.futures import ProcessPoolExecutor

import pandas as pd
import matplotlib.pyplot as plt


# ==========================================
# PROYEK 2: HIGH PERFORMANCE COMPUTING (HPC)
# Studi kasus: Pemrosesan data cuaca sintetis
# ==========================================

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
OUTPUT_DIR = BASE_DIR / "output"
DATA_FILE = DATA_DIR / "data_cuaca.csv"


def buat_dataset(jumlah=30000):
    """Membuat dataset contoh jika file belum tersedia."""
    DATA_DIR.mkdir(exist_ok=True)

    if DATA_FILE.exists():
        return

    df = pd.DataFrame({
        "id": range(1, jumlah + 1),
        "suhu": [20 + (i * 7 % 1500) / 100 for i in range(jumlah)],
        "kelembapan": [
            30 + (i * 13 % 7000) / 100
            for i in range(jumlah)
        ],
        "angin": [(i * 11 % 2000) / 100 for i in range(jumlah)]
    })

    df.to_csv(DATA_FILE, index=False)
    print(f"Dataset dibuat: {DATA_FILE}")


def hitung_data(record):
    """Simulasi beban komputasi pada setiap baris."""
    suhu, kelembapan, angin = record
    hasil = 0.0

    for i in range(150):
        hasil += (
            suhu * 0.7
            + kelembapan * 0.02
            + angin * 0.3
            + i
        ) % 17

    return hasil


def proses_serial(records):
    """Memproses seluruh data secara berurutan."""
    return [hitung_data(row) for row in records]


def proses_chunk(records):
    """Memproses satu bagian data."""
    return proses_serial(records)


def bagi_data(records, jumlah_bagian):
    """Membagi data menjadi beberapa bagian."""
    ukuran = (len(records) + jumlah_bagian - 1) // jumlah_bagian

    return [
        records[i:i + ukuran]
        for i in range(0, len(records), ukuran)
    ]


def proses_paralel(records, jumlah_worker):
    """Memproses bagian data menggunakan beberapa proses."""
    chunks = bagi_data(records, jumlah_worker)

    with ProcessPoolExecutor(
        max_workers=jumlah_worker
    ) as executor:
        hasil_bagian = list(
            executor.map(proses_chunk, chunks)
        )

    return [
        nilai
        for bagian in hasil_bagian
        for nilai in bagian
    ]


def buat_grafik(hasil):
    """Membuat dan menyimpan grafik benchmark."""
    OUTPUT_DIR.mkdir(exist_ok=True)

    # Grafik waktu eksekusi
    plt.figure(figsize=(9, 5))
    plt.bar(hasil["metode"], hasil["waktu_detik"])
    plt.title("Perbandingan Waktu Pemrosesan")
    plt.xlabel("Metode")
    plt.ylabel("Waktu (detik)")
    plt.grid(axis="y", alpha=0.3)
    plt.tight_layout()
    plt.savefig(
        OUTPUT_DIR / "perbandingan_waktu.png",
        dpi=150
    )
    plt.show()

    # Grafik speedup
    plt.figure(figsize=(9, 5))
    plt.bar(hasil["metode"], hasil["speedup"])
    plt.axhline(
        y=1,
        linestyle="--",
        label="Patokan serial"
    )
    plt.title("Speedup Pemrosesan")
    plt.xlabel("Metode")
    plt.ylabel("Speedup (kali)")
    plt.legend()
    plt.grid(axis="y", alpha=0.3)
    plt.tight_layout()
    plt.savefig(
        OUTPUT_DIR / "speedup.png",
        dpi=150
    )
    plt.show()


def main():
    OUTPUT_DIR.mkdir(exist_ok=True)
    buat_dataset()

    df = pd.read_csv(DATA_FILE)
    records = list(zip(
        df["suhu"],
        df["kelembapan"],
        df["angin"]
    ))

    print("=" * 55)
    print("PROYEK 2: HIGH PERFORMANCE COMPUTING")
    print("=" * 55)
    print(f"Jumlah data       : {len(records):,}")
    print(f"CPU logis tersedia: {os.cpu_count()}")
    print("Dataset           : sintetis / data demonstrasi")

    # Benchmark serial
    print("\nMenjalankan pemrosesan serial...")
    mulai = time.perf_counter()
    hasil_serial = proses_serial(records)
    waktu_serial = time.perf_counter() - mulai

    print(f"Waktu serial: {waktu_serial:.3f} detik")

    hasil_benchmark = [{
        "metode": "Serial",
        "worker": 1,
        "waktu_detik": waktu_serial
    }]

    # Benchmark paralel
    jumlah_worker = min(4, os.cpu_count() or 2)
    jumlah_worker = max(2, jumlah_worker)

    print(f"\nMenjalankan paralel ({jumlah_worker} worker)...")
    mulai = time.perf_counter()
    hasil_paralel = proses_paralel(
        records, jumlah_worker
    )
    waktu_paralel = time.perf_counter() - mulai

    print(f"Waktu paralel: {waktu_paralel:.3f} detik")

    # Validasi hasil
    sama = (
        len(hasil_serial) == len(hasil_paralel)
        and all(
            abs(a - b) < 1e-9
            for a, b in zip(hasil_serial, hasil_paralel)
        )
    )

    print(f"\nHasil serial dan paralel sama: {sama}")

    hasil_benchmark.append({
        "metode": f"Paralel ({jumlah_worker} worker)",
        "worker": jumlah_worker,
        "waktu_detik": waktu_paralel
    })

    hasil = pd.DataFrame(hasil_benchmark)
    hasil["speedup"] = (
        waktu_serial / hasil["waktu_detik"]
    )
    hasil["efisiensi_pct"] = (
        hasil["speedup"] / hasil["worker"] * 100
    )

    hasil.to_csv(
        OUTPUT_DIR / "hasil_benchmark.csv",
        index=False
    )

    print("\nRINGKASAN BENCHMARK")
    print(hasil.to_string(
        index=False,
        formatters={
            "waktu_detik": "{:.3f}".format,
            "speedup": "{:.2f}x".format,
            "efisiensi_pct": "{:.1f}%".format
        }
    ))

    if waktu_paralel < waktu_serial:
        print("\nPemrosesan paralel lebih cepat pada percobaan ini.")
    else:
        print(
            "\nPemrosesan paralel belum lebih cepat pada percobaan ini."
        )

    print("\nMembuat grafik...")
    buat_grafik(hasil)

    print(f"\nSemua hasil disimpan di: {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
