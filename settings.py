"""
Bıyık Bey'in Çilesi - Oyun Ayarları
Tüm oyun sabitleri ve yapılandırmaları burada tanımlanır
"""

# Renk Tanımları (RGB formatında)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
LIGHT_GRAY = (200, 200, 200)
DARK_GRAY = (64, 64, 64)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Oyun Ayarları
FPS = 60  # Saniyedeki kare sayısı

# Ses Ayarları
VOLUME_LEVELS = [1.0, 0.5, 0.0]  # 100%, 50%, 0% (sessiz)
DEFAULT_VOLUME_INDEX = 0              # Başlangıç ses seviyesi (100%)

# Ses Kontrol UI Ayarları
VOLUME_ICON_SIZE = 150                 # İkon boyutu (piksel)
VOLUME_ICON_PADDING = 100              # Ekran kenarından mesafe

# =============================================================================
# OYUNCU AYARLARI
# =============================================================================
PLAYER_MAX_HEALTH = 5           # Maksimum can
PLAYER_START_HEALTH = 5         # Başlangıç canı
PLAYER_INVINCIBILITY_TIME = 1.5 # Hasar sonrası dokunulmazlık (saniye)

# =============================================================================
# ÇAY AYARLARI
# =============================================================================
TEA_SPAWN_TIME = 5.0            # Çay spawn süresi (saniye)
TEA_MAX_COUNT = 3               # Aynı anda maksimum çay sayısı
TEA_SCALE = 1.2                 # Çay boyutu

# =============================================================================
# BOMBA AYARLARI
# =============================================================================
BOMB_SPAWN_TIME = 8.0           # Bomba spawn süresi (saniye)
BOMB_MAX_COUNT = 3              # Aynı anda maksimum bomba sayısı
BOMB_SCALE = 1.3                # Bomba boyutu
BOMB_FUSE_TIME = 3000           # Patlamaya kadar süre (ms)
BOMB_EXPLOSION_RADIUS = 150     # Patlama yarıçapı (piksel)

# =============================================================================
# SİNSİ JİLET AYARLARI
# =============================================================================
JILET_SPAWN_TIME = 6.0          # Jilet spawn süresi (saniye)
JILET_MAX_COUNT = 2             # Aynı anda maksimum jilet sayısı
JILET_SCALE = 1.2               # Jilet boyutu
JILET_SNEAK_SPEED = 1.5         # Sinsi yürüme hızı
JILET_ATTACK_SPEED = 8.0        # Saldırı hızı
JILET_ATTACK_DISTANCE = 200     # Saldırıya geçme mesafesi

# =============================================================================
# UÇAN TERLİK AYARLARI
# =============================================================================
TERLIK_SPAWN_TIME = 4.0         # Terlik spawn süresi (saniye)
TERLIK_MAX_COUNT = 5            # Aynı anda maksimum terlik sayısı
TERLIK_SCALE = 1.0              # Terlik boyutu
TERLIK_SPEED = 7.0              # Terlik hızı


# Not: Ekran boyutları (SCREEN_WIDTH, SCREEN_HEIGHT) main.py'de
# ekran çözünürlüğüne göre dinamik olarak belirlenir
