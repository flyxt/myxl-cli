# Panduan Deploy Aplikasi ke VPS

Dokumen ini memberikan panduan langkah demi langkah untuk men-deploy dan menjalankan aplikasi ini di server VPS yang menggunakan sistem operasi Linux seperti Ubuntu atau Debian.

## 1. Persiapan Awal

Pastikan Anda sudah memiliki akses SSH ke VPS Anda.

## 2. Instalasi Kebutuhan Dasar

Pertama, perbarui daftar paket dan instalasi `git`, `python3`, dan `pip` jika belum ada.

```bash
sudo apt update && sudo apt full-upgrade -y
sudo apt install git python3 python3-pip -y
```

## 3. Clone Repositori

Clone repositori aplikasi ini dari GitHub.

```bash
git clone https://github.com/flyxt/myxl-cli
```

## 4. Masuk ke Direktori Aplikasi

Pindah ke direktori aplikasi yang baru saja di-clone.

```bash
cd myxl-cli
```

## 5. Instalasi Dependensi

Instal semua paket Python yang dibutuhkan oleh aplikasi menggunakan `pip`.

```bash
pip3 install -r requirements.txt
```

## 6. Menjalankan Aplikasi

Sekarang Anda bisa menjalankan aplikasi secara langsung.

```bash
python3 main.py
```

Aplikasi akan berjalan di foreground. Jika Anda menutup sesi SSH, aplikasi akan berhenti. Untuk menjalankannya secara terus-menerus, ikuti langkah di bawah ini.

## 7. Menjalankan Aplikasi di Latar Belakang (Persistent)

Kami merekomendasikan menggunakan `screen` untuk menjaga aplikasi tetap berjalan bahkan setelah Anda menutup koneksi SSH.

### a. Instal `screen`

```bash
sudo apt install screen -y
```

### b. Mulai Sesi `screen`

Buat sesi `screen` baru dengan nama yang mudah diingat, misalnya `myxl-session`.

```bash
screen -S myxl-session
```

Anda akan masuk ke dalam sebuah sesi terminal baru.

### c. Jalankan Aplikasi di dalam `screen`

Di dalam sesi `screen` tersebut, jalankan aplikasi seperti biasa.

```bash
python3 main.py
```

### d. Keluar dari Sesi `screen` (Detach)

Aplikasi sekarang berjalan di dalam `screen`. Untuk keluar dari sesi `screen` tanpa menghentikan aplikasi, tekan `Ctrl+A` lalu tekan `D`.

Anda akan kembali ke terminal utama dengan pesan `[detached from ...]`.

### e. Kembali ke Sesi `screen` (Reattach)

Jika Anda ingin melihat kembali aplikasi yang sedang berjalan, Anda bisa masuk kembali ke sesi `screen` dengan perintah:

```bash
screen -r myxl-session
```

Dengan cara ini, aplikasi Anda akan terus berjalan di VPS selama server aktif.
