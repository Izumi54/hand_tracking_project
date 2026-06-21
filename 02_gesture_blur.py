import cv2
import mediapipe as mp

# ============================================
# STEP 1: Inisialisasi MediaPipe
# ============================================
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles

hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=1,              # Cukup 1 tangan untuk gesture ini
    min_detection_confidence=0.7,
    min_tracking_confidence=0.5
)

# ============================================
# STEP 2: Fungsi Deteksi Gesture
# ============================================
def get_fingers_status(landmarks):
    """
    Cek status setiap jari: 1 = terbuka, 0 = tertutup
    
    Logika: Ujung jari (TIP) lebih tinggi (y lebih kecil) 
    dari sendi PIP = jari terbuka
    """
    fingers = []
    
    # Jempol (landmark 4 vs 3) — pakai sumbu x karena jempol ke samping
    # Untuk tangan kiri (mirror), jempol terbuka kalau x[4] < x[3]
    if landmarks[4].x < landmarks[3].x:
        fingers.append(1)  # Jempol terbuka
    else:
        fingers.append(0)  # Jempol tertutup
    
    # 4 jari lainnya (TIP vs PIP) — pakai sumbu y
    finger_tips = [8, 12, 16, 20]   # Ujung jari
    finger_pips = [6, 10, 14, 18]  # Sendi tengah
    
    for tip, pip in zip(finger_tips, finger_pips):
        if landmarks[tip].y < landmarks[pip].y:
            fingers.append(1)  # Jari terbuka (y kecil = lebih tinggi)
        else:
            fingers.append(0)  # Jari tertutup
    
    return fingers

def is_peace_sign(fingers):
    """
    Cek apakah gesture = Peace Sign ✌️
    Telunjuk & tengah TERBUKA, lainnya TERTUTUP
    fingers = [jempol, telunjuk, tengah, manis, kelingking]
    """
    return fingers == [0, 1, 1, 0, 0]

# ============================================
# STEP 3: Fungsi Blur
# ============================================
def apply_blur(image, blur_strength=51):
    """
    Blur gambar dengan Gaussian Blur
    
    blur_strength harus GANJIL (contoh: 15, 31, 51, 99)
    Semakin besar = semakin blur
    """
    # Pastikan ganjil
    if blur_strength % 2 == 0:
        blur_strength += 1
    
    # GaussianBlur(src, (kernel_width, kernel_height), sigmaX)
    blurred = cv2.GaussianBlur(image, (blur_strength, blur_strength), 0)
    return blurred

# ============================================
# STEP 4: Buka Kamera & Loop Utama
# ============================================
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("❌ Kamera tidak bisa dibuka!")
    exit()

print("🖐️  Program berjalan!")
print("✌️  Angkat telunjuk & jari tengah = BLUR ON")
print("🖐️  Ganti gesture = BLUR OFF")
print("Tekan 'q' untuk keluar")

while cap.isOpened():
    success, image = cap.read()
    if not success:
        break

    # Mirror effect
    image = cv2.flip(image, 1)
    
    # Simpan frame asli untuk proses
    original = image.copy()
    
    # Konversi ke RGB untuk MediaPipe
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results = hands.process(image_rgb)
    
    # Status default: tidak blur
    is_blurred = False
    gesture_name = "Tidak ada gesture"
    
    # ============================================
    # STEP 5: Deteksi Gesture & Apply Blur
    # ============================================
    if results.multi_hand_landmarks:
        hand_landmarks = results.multi_hand_landmarks[0]
        landmarks = hand_landmarks.landmark
        
        # Gambar landmark di frame ASLI (sebelum blur)
        # mp_drawing.draw_landmarks(
        #     original,
        #     hand_landmarks,
        #     mp_hands.HAND_CONNECTIONS,
        #     mp_drawing_styles.get_default_hand_landmarks_style(),
        #     mp_drawing_styles.get_default_hand_connections_style()
        # )
        
        # Cek gesture
        fingers = get_fingers_status(landmarks)
        gesture_name = f"Jari: {fingers}"
        
        # ✌️ PEACE SIGN = BLUR!
        if is_peace_sign(fingers):
            is_blurred = True
            # Apply blur ke frame
            original = apply_blur(original, blur_strength=51)
            gesture_name = "✌️ PEACE SIGN - BLUR ON!"
    
    # ============================================
    # STEP 6: Tampilkan Status di Layar
    # ============================================
    # Status bar di atas
    # status_color = (0, 0, 255) if is_blurred else (0, 255, 0)  # Merah = blur, Hijau = normal
    # status_text = "🔴 BLUR ON" if is_blurred else "🟢 NORMAL"
    
    # cv2.putText(original, status_text, (10, 40),
    #             cv2.FONT_HERSHEY_SIMPLEX, 1, status_color, 3)
    
    # cv2.putText(original, gesture_name, (10, 80),
    #             cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
    
    # # Instruksi di bawah
    # h, w, _ = original.shape
    # cv2.putText(original, "✌️ = Blur | Lainnya = Normal | q = Keluar", 
    #             (10, h - 20),
    #             cv2.FONT_HERSHEY_SIMPLEX, 0.6, (200, 200, 200), 1)
    
    # Tampilkan hasil
    cv2.imshow('Gesture Blur', original)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# ============================================
# STEP 7: Cleanup
# ============================================
cap.release()
cv2.destroyAllWindows()
hands.close()

print("👋 Program selesai!")