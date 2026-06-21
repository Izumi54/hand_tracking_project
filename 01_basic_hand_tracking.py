# ==============================
# ====    import Library    ====
# ==============================
import cv2              # untuk video dan gambar
import mediapipe as mp  # deteksi tangan
# ----------


# =========================================
# ====    instalasi MediaPipe Hacds    ====
# =========================================
# ambil modul dari MediaPipe
mp_hands            = mp.solutions.hands            # Module deteksi tangan
mp_drawing          = mp.solutions.drawing_utils    # module menggambar di layar
mp_drawing_styles   = mp.solutions.drawing_styles   # Gaya menggambar

# Buat tangan pengaturan
hands = mp_hands.Hands(
    static_image_mode = False,          # False = video(real-time), True = gambar diam
    max_num_hands = 2,                  # maksimal deteksi 2 tangan
    min_detection_confidence = 0.7,     # Minimal 70% yakin ini tangan baru dianggap tangan
    min_tracking_confidence = 0.5       # minimal 50% yakin ini tangan yang sama dari frame sebelumnya
)
# -----------

# ===========================
# ====    Buka Kamera    ====
# ===========================
# buka kamera default
cap = cv2.VideoCapture(0)       # 0 = kaemra laptop utama

# cek apakah kamera berhasil di buka
if not cap.isOpened():
    print("-- Kamera tidak bisa dibuka!! --")
    exit()
print("== program berjalan! Tekan 'q' untuk keluar ==")
# ----------

# ==========================
# ====    Loop Utama    ====
# ==========================
while cap.isOpened():                # selama kamera terbuka
    success, image = cap.read()     # baca 1 frame dari kamera

    if not success:     # kalau gagal break
        print("--- Gagal membaca frame dari kamera")
        break
# ----------

    # ===============================
    # ====    flip Horizontal    ====
    # ===============================
    image = cv2.flip(image, 1)      # Flip gambar secara horizontal (mirror)
    # ----------
    # =========================================
    # ====    Konversi Warna BGR -> RGB    ====
    # =========================================
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    # ----------

    # ==============================
    # ====    Deteksi Tangan    ====
    # ==============================
    result = hands.process(image_rgb)


    # ===============================
    # ====    Gambar Landmark    ====
    # ===============================
    if result.multi_hand_landmarks:     # kalau ada tangan terdeteksi
        
        for hand_landmarks in result.multi_hand_landmarks:
            
            # jika tidak ingin etrlihat garis gambar comment code di bawah ini
            mp_drawing.draw_landmarks(
                image,          # Gambar dimana? di dalam frame kamera
                hand_landmarks, # Koordinat tangan

                mp_hands.HAND_CONNECTIONS,      # gambar garis penghubung antara titik
                mp_drawing_styles.get_default_hand_landmarks_style(),       # gaya titik
                mp_drawing_styles.get_default_hand_connections_style()      # gaya garis
            )

    # 0  = WRIST (Pergelangan)
    # 1-4 = THUMB (Jempol: CMC, MCP, IP, TIP)
    # 5-8 = INDEX (Telunjuk: MCP, PIP, DIP, TIP)
    # 9-12 = MIDDLE (Jari tengah: MCP, PIP, DIP, TIP)
    # 13-16 = RING (Jari manis: MCP, PIP, DIP, TIP)
    # 17-20 = PINKY (Kelingking: MCP, PIP, DIP, TIP)
    # ------------

    # ==========================================
    # ====    Tampilkan koordiant Jempol    ====
    # ==========================================
            # ambil landmarks jempol nomor 4
            thumb = hand_landmarks.landmark[4]

            # konversi koordinat nomalized (0.0 - 1.0) ke pixel
            h, w, _ = image.shape # Tinggi, Lebar, channel gambar
            cx = int(thumb.x * w) # x * lebar gambar
            cy = int(thumb.y * h) # y * tinggi gambar

            # jika tidak ingin ada tulisan di layar comment code di bawah ini
            # Tulis teks di layar
            cv2.putText(
                image,                          # gamabr di mana? 
                f"jempol: ({cx}, {cy})",        # Teks apa?
                (10, 30),                        # posisi (x, y) dipixel
                cv2.FONT_HERSHEY_SIMPLEX,       # font
                1,                              # ukuran font
                (0, 255, 0),                    # warna (BGR) = hujau
                2                               # Ketebalan garis
            )

    # ===============================
    # ====     tampilan layar    ====
    # ===============================

    # tampilkan frame yang sudah di gambar
    cv2.imshow('hand tracking', image)


    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Lepas kamera
cap.release()

# Tutup semua window OpenCV
cv2.destroyAllWindows()

# Tutup MediaPipe
hands.close()

print("👋 Program selesai!")

