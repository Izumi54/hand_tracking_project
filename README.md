# 🤚 Hand Tracking Project

> **Belajar Computer Vision dengan Python & MediaPipe** — dari nol hingga bisa mengontrol komputer dengan tangan!

---

## 📋 Daftar Isi

- [Tentang Project](#-tentang-project)
- [Teknologi](#-teknologi)
- [Persiapan](#-persiapan)
- [Struktur Project](#-struktur-project)
- [Tahap 1: Basic Hand Tracking](#-tahap-1-basic-hand-tracking)
- [Troubleshooting](#-troubleshooting)
- [Roadmap](#-roadmap)
- [Lisensi](#-lisensi)

---

## 🎯 Tentang Project

Project ini adalah perjalanan belajar **Computer Vision** dan **AI** menggunakan Python. Kita akan membangun aplikasi yang bisa:

- ✅ Deteksi tangan secara real-time dari kamera
- ✅ Mengenali gesture jari (jempol, telunjuk, dll)
- ✅ Mengontrol kursor mouse dengan tangan
- ✅ Menggambar di layar seperti virtual paint
- ✅ Mengenali gesture kustom untuk shortcut

**Status:** 🚧 Sedang dalam pengembangan — Tahap 1 selesai!

---

## 🛠️ Teknologi

| Library | Versi | Fungsi |
|---------|-------|--------|
| [Python](https://www.python.org/) | 3.11 | Bahasa pemrograman |
| [OpenCV](https://opencv.org/) | 4.9.0 | Pengolahan video & gambar |
| [MediaPipe](https://mediapipe.dev/) | 0.10.11 | Deteksi tangan dengan AI |
| [NumPy](https://numpy.org/) | 1.26.4 | Komputasi numerik |
| [Pynput](https://pynput.readthedocs.io/) | 1.7.6 | Kontrol mouse & keyboard |

**Sistem Operasi:** Linux (Fedora)  
**GPU:** Intel UHD Graphics (dengan akselerasi OpenGL ES 3.2)

---

## 📦 Persiapan

### 1. Clone Repository

```bash
git clone https://github.com/username/hand-tracking-project.git
cd hand-tracking-project
```

### 2. Install Python 3.11

```bash
# Fedora
sudo dnf install python3.11 python3.11-pip python3.11-devel -y

# Verifikasi
python3.11 --version
```

### 3. Buat Virtual Environment

```bash
python3.11 -m venv venv
source venv/bin/activate
```

> ⚠️ **Jangan lupa aktifkan venv setiap buka terminal baru!**

### 4. Install Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 5. Verifikasi Installasi

```bash
python -c "import cv2, mediapipe, numpy; print('✅ Semua library terinstall!')"
```

---

## 📁 Struktur Project

```
hand-tracking-project/
│
├── 📄 README.md              # Dokumentasi project (file ini)
├── 📄 .gitignore             # File yang diabaikan Git
├── 📄 requirements.txt       # Daftar library Python
│
├── 🐍 01_basic_hand_tracking.py    # ✅ Tahap 1: Deteksi tangan dasar
├── 🐍 02_landmark_explorer.py      # 🔜 Tahap 2: Eksplorasi 21 landmark
├── 🐍 03_finger_counter.py         # 🔜 Tahap 3: Penghitung jari
├── 🐍 04_virtual_mouse.py          # 🔜 Tahap 4: Kontrol mouse
├── 🐍 05_virtual_paint.py          # 🔜 Tahap 5: Menggambar di layar
├── 🐍 06_hand_controller.py        # 🔜 Tahap 6: Project final lengkap
│
└── 📁 venv/                  # Virtual environment (di-ignore Git)
```

---

## 🖐️ Tahap 1: Basic Hand Tracking

### Apa yang Dilakukan?

Program ini membuka kamera laptop, mendeteksi tangan secara real-time, dan menampilkan:

- **21 landmark** (titik) pada tangan
- **Garis penghubung** antar titik (tulang tangan)
- **Koordinat jempol** dalam pixel di layar

### Cara Menjalankan

```bash
# Pastikan venv aktif
source venv/bin/activate

# Jalankan program
python 01_basic_hand_tracking.py
```

### Kontrol

| Tombol | Aksi |
|--------|------|
| `q` | Keluar dari program |

### Preview Output

```
┌─────────────────────────────────────┐
│  🖐️ Hand Tracking                    │
│                                      │
│    ●────●────●                       │
│   /      \    \                      │
│  ●        ●    ●                     │
│  |        |    |                     │
│  ●        ●    ●                     │
│  |        |    |                     │
│  ●        ●    ●                     │
│           |                          │
│           ●                          │
│                                      │
│  Jempol: (320, 180)                  │
└─────────────────────────────────────┘
```

### 21 Landmark Tangan

MediaPipe mendeteksi **21 titik** pada tangan dengan nomor berikut:

| Nomor | Nama | Jari |
|-------|------|------|
| 0 | WRIST | Pergelangan |
| 1-4 | THUMB | Jempol (CMC → MCP → IP → TIP) |
| 5-8 | INDEX | Telunjuk (MCP → PIP → DIP → TIP) |
| 9-12 | MIDDLE | Jari tengah (MCP → PIP → DIP → TIP) |
| 13-16 | RING | Jari manis (MCP → PIP → DIP → TIP) |
| 17-20 | PINKY | Kelingking (MCP → PIP → DIP → TIP) |

> **TIP:** MCP = Metacarpophalangeal, PIP = Proximal Interphalangeal, DIP = Distal Interphalangeal, TIP = Ujung jari

---

## 🔧 Troubleshooting

### Kamera tidak terbuka

```bash
# Cek kamera tersedia
ls /dev/video*

# Kalau ada /dev/video1, ubah kode:
cap = cv2.VideoCapture(1)  # Ganti 0 → 1
```

### Error `module 'mediapipe' has no attribute 'solutions'`

```bash
# Uninstall dan install versi yang kompatibel
pip uninstall mediapipe -y
pip install mediapipe==0.10.11
```

### Warning Wayland di Fedora

```bash
# Normal, tidak masalah. Kalau mau pakai Wayland:
export QT_QPA_PLATFORM=wayland
python 01_basic_hand_tracking.py
```

### Performa lambat

```bash
# Turunkan resolusi kamera
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
```

---

## 🗺️ Roadmap

| Tahap | Fitur | Status |
|-------|-------|--------|
| 1 | **Basic Hand Tracking** — Deteksi tangan & landmark | ✅ **Selesai** |
| 2 | **Landmark Explorer** — Visualisasi nama & koordinat semua titik | 🔜 Coming Soon |
| 3 | **Finger Counter** — Hitung jari yang terbuka | 🔜 Coming Soon |
| 4 | **Virtual Mouse** — Gerakkan kursor & klik dengan tangan | 🔜 Coming Soon |
| 5 | **Virtual Paint** — Menggambar di layar dengan gesture | 🔜 Coming Soon |
| 6 | **Hand Controller** — Project final: semua fitur digabung | 🔜 Coming Soon |

---

## 📚 Sumber Belajar

- [MediaPipe Hands Documentation](https://developers.google.com/mediapipe/solutions/vision/hand_landmarker)
- [OpenCV Python Tutorials](https://docs.opencv.org/4.x/d6/d00/tutorial_py_root.html)
- [Computer Vision Guide](https://github.com/jasmcaus/opencv-course)

---

## 🙏 Kontribusi

Project ini untuk **belajar pribadi**, tapi kalau ada ide atau saran:

1. Fork repository
2. Buat branch baru: `git checkout -b fitur-baru`
3. Commit perubahan: `git commit -m 'feat: tambah fitur X'`
4. Push ke branch: `git push origin fitur-baru`
5. Buat Pull Request

---

## 📄 Lisensi

[MIT License](LICENSE) — Bebas digunakan untuk belajar dan dikembangkan! 🎓

---

> Dibuat dengan ❤️ dan banyak ☕ untuk belajar Computer Vision di Linux Fedora.
