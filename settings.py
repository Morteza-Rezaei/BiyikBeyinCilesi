"""
Bıyık Bey'in Çilesi - Oyun Ayarları
Tüm oyun sabitleri ve yapılandırmaları burada tanımlanır
"""

import os
import json
from datetime import datetime

# Renk Tanımları (RGB formatında)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
LIGHT_GRAY = (200, 200, 200)
DARK_GRAY = (64, 64, 64)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
BLUE = (100, 150, 255)

# Oyun Ayarları
FPS = 60  # Saniyedeki kare sayısı

# Ses Ayarları
VOLUME_LEVELS = [1.0, 0.5, 0.0]  # 100%, 50%, 0% (sessiz)
DEFAULT_VOLUME_INDEX = 0              # Başlangıç ses seviyesi (100%)

# Ses Kontrol UI Ayarları
VOLUME_ICON_SIZE = 150                 # İkon boyutu (piksel)
VOLUME_ICON_PADDING = 100              # Ekran kenarından mesafe

# =============================================================================
# LEVEL SİSTEMİ AYARLARI
# =============================================================================
LEVEL_DURATION = 60.0           # Her level süresi (saniye) - 1 dakika
BASE_ENEMY_COUNT = 2            # Başlangıç düşman sayısı
ENEMY_COUNT_PER_LEVEL = 1       # Her levelde eklenen düşman sayısı (dengeli)
SPEED_INCREASE_LEVELS = 3       # Kaç levelde bir hız artışı
SPEED_INCREASE_AMOUNT = 0.12    # Hız artış miktarı (%12 - dengeli)
SPAWN_TIME_REDUCTION_RATE = 0.08  # Her levelde spawn süresi azalma oranı (%8 - dengeli)
MIN_SPAWN_TIME = 0.8            # Minimum spawn süresi (saniye)
INITIAL_ENEMY_SPAWN_COUNT = 2   # Level başlangıcında hemen spawn edilecek düşman sayısı
BOMB_FUSE_REDUCTION_PER_LEVEL = 50  # Her levelde bomba fünye süresi azalması (ms - dengeli)
MIN_BOMB_FUSE_TIME = 1500       # Minimum bomba fünye süresi (ms)

# =============================================================================
# OYUNCU AYARLARI
# =============================================================================
PLAYER_MAX_HEALTH = 5           # Maksimum can
PLAYER_START_HEALTH = 5        # Başlangıç canı
PLAYER_INVINCIBILITY_TIME = 1.5 # Hasar sonrası dokunulmazlık (saniye)
PLAYER_COLLISION_SHRINK = 20    # Çarpışma rect'i için küçültme miktarı (piksel)
HEALTH_UI_SHAKE_AMOUNT = 3      # Can UI titreme miktarı (piksel)
HEALTH_UI_PADDING = 20          # Can UI kenar boşluğu (piksel)
HEALTH_UI_SPACING = 5           # Can UI kalpler arası mesafe (piksel)
HEALTH_UI_OFFSET_Y = 40         # Can UI ESC yazısından mesafe (piksel)
HEALTH_UI_HEART_SCALE = 0.45    # Can UI kalp ölçekleme çarpanı

# =============================================================================
# BUFF AYARLARI (Çay, Hızlandırma, Yavaşlatma)
# =============================================================================
BUFF_SPAWN_MIN_TIME = 5.0       # Minimum spawn aralığı (saniye)
BUFF_SPAWN_MAX_TIME = 10.0      # Maksimum spawn aralığı (saniye)
BUFF_LIFETIME = 8.0             # Buff haritada kalma süresi (saniye)
BUFF_EFFECT_DURATION = 10.0     # Buff efekt süresi (saniye)
BUFF_SCALE = 0.8                # Buff boyutu
SPEED_BUFF_MULTIPLIER = 1.5     # Hız artış çarpanı (%50 hız artışı)
SPEED_DEBUFF_MULTIPLIER = 0.5   # Hız azalma çarpanı (%50 hız azalması)

# Çay nadir çıksın - ağırlıklı random için
BUFF_WEIGHTS = {
    'tea': 1,           # Çay (nadir)
    'speed_buff': 3,    # Hızlandırma
    'speed_debuff': 3,  # Yavaşlatma
}

TEA_SCALE = 0.8                 # Çay boyutu

# =============================================================================
# BOMBA AYARLARI
# =============================================================================
BOMB_SPAWN_MIN_TIME = 5.0       # Minimum spawn aralığı (base)
BOMB_SPAWN_MAX_TIME = 10.0      # Maksimum spawn aralığı (base)
BOMB_MAX_COUNT = 3              # Aynı anda maksimum bomba sayısı (base)
BOMB_MAX_COUNT_PER_LEVEL = 0.3  # Her levelde eklenen bomba sayısı (0.3 = her 3 levelde 1 - dengeli)
BOMB_SCALE = 2                # Bomba boyutu
BOMB_FUSE_TIME = 3000           # Patlamaya kadar süre (ms) - base
BOMB_EXPLOSION_EFFECT_ALPHA = 64  # Patlama efektinin opaklığı (0-255, 0=tamamen şeffaf, 255=tamamen opak)

# =============================================================================
# SİNSİ JİLET AYARLARI
# =============================================================================
JILET_SPAWN_MIN_TIME = 5.0      # Minimum spawn aralığı (base)
JILET_SPAWN_MAX_TIME = 10.0     # Maksimum spawn aralığı (base)
JILET_MAX_COUNT = 2             # Aynı anda maksimum jilet sayısı (base)
JILET_MAX_COUNT_PER_LEVEL = 0.3  # Her levelde eklenen jilet sayısı (0.3 = her 3 levelde 1 - dengeli)
JILET_SCALE = 1.0               # Jilet boyutu
JILET_SNEAK_SPEED = 1.5         # Sinsi yürüme hızı (base)
JILET_ATTACK_SPEED = 8.0        # Saldırı hızı (base)
JILET_ATTACK_DISTANCE = 200     # Saldırıya geçme mesafesi (base)
JILET_ATTACK_DISTANCE_PER_LEVEL = 1  # Her levelde saldırı mesafesi artışı (dengeli)
JILET_MAX_ATTACK_DISTANCE = 300  # Maksimum saldırı mesafesi (sınır)
JILET_ATTACK_DELAY_BASE = 4.0   # Saldırı modunda kalma süresi - kovalama süresi (saniye) - base
JILET_ATTACK_DELAY_PER_LEVEL = 0.5  # Her levelde eklenen kovalama süresi (saniye)

# =============================================================================
# UÇAN TERLİK AYARLARI
# =============================================================================
TERLIK_SPAWN_MIN_TIME = 5.0     # Minimum spawn aralığı (base)
TERLIK_SPAWN_MAX_TIME = 10.0    # Maksimum spawn aralığı (base)
TERLIK_MAX_COUNT = 5            # Aynı anda maksimum terlik sayısı (base)
TERLIK_MAX_COUNT_PER_LEVEL = 0.8  # Her levelde eklenen terlik sayısı (dengeli)
TERLIK_SCALE = 1.0              # Terlik boyutu
TERLIK_SPEED = 7.0              # Terlik hızı (base)

# =============================================================================
# HINT SİSTEMİ AYARLARI
# =============================================================================
HINT_BUTTON_SIZE = 140           # Hint butonu boyutu (piksel)
HINT_BUTTON_PADDING_RIGHT = 20   # Hint butonu sağ kenardan mesafe
HINT_BUTTON_PADDING_TOP = 20    # Hint butonu üst kenardan mesafe
HINT_POPUP_BTN_SIZE = 100        # Popup içi butonlar (next, close) boyutu
HINT_CARD_HEIGHT_RATIO = 0.5    # Kart yüksekliği (ekranın yüzde kaçı)

# =============================================================================
# SPAWN AYARLARI (Genel)
# =============================================================================
SPAWN_RETRY_ATTEMPTS = 10        # Spawn için maksimum deneme sayısı
SPAWN_MARGIN = 100               # Spawn için ekran kenarından mesafe
SPAWN_MIN_DISTANCE_FROM_PLAYER = 200  # Oyuncudan minimum spawn mesafesi
BUFF_SPAWN_MARGIN = 150          # Buff spawn için ekran kenarından mesafe
ENEMY_SPAWN_MARGIN = 50          # Düşman spawn için ekran kenarından mesafe
ENEMY_SPAWN_OFFSET = 30          # Düşman spawn için ekran dışı offset

# =============================================================================
# REKOR SİSTEMİ
# =============================================================================
SAVE_FILE = 'highscore.json'

def load_highscore():
    """Kayıtlı rekoru yükle"""
    if os.path.exists(SAVE_FILE):
        try:
            with open(SAVE_FILE, 'r') as f:
                return json.load(f)
        except:
            pass
    return {'level': 0, 'date': None}

def save_highscore(level, start_level=1):
    """Yeni rekor kaydet - sadece level 1'den başlayanlar için"""
    # Sadece level 1'den başlayanlar için rekor kaydet
    if start_level != 1:
        return False
    
    current = load_highscore()
    if level > current['level']:
        data = {
            'level': level,
            'date': datetime.now().strftime('%Y-%m-%d %H:%M')
        }
        with open(SAVE_FILE, 'w') as f:
            json.dump(data, f)
        return True
    return False

def reset_highscore():
    """Rekoru sıfırla"""
    if os.path.exists(SAVE_FILE):
        try:
            os.remove(SAVE_FILE)
            return True
        except:
            return False
    return True


# Not: Ekran boyutları (SCREEN_WIDTH, SCREEN_HEIGHT) main.py'de
# ekran çözünürlüğüne göre dinamik olarak belirlenir
