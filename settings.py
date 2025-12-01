"""
Bıyık Bey'in Çilesi - Oyun Ayarları
Tüm oyun sabitleri ve yapılandırmaları burada tanımlanır
"""

# Renk Tanımları (RGB formatında)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
LIGHT_GRAY = (200, 200, 200)
DARK_GRAY = (64, 64, 64)

# Oyun Ayarları
FPS = 60  # Saniyedeki kare sayısı

# Yazı Boyutları (geçici ekranlar için)
TITLE_FONT_SIZE = 120       # Ana başlık
INSTRUCTION_FONT_SIZE = 42  # Talimat metni

# Ses Ayarları
VOLUME_LEVELS = [1.0, 0.5, 0.0]  # 100%, 50%, 0% (sessiz)
DEFAULT_VOLUME_INDEX = 0              # Başlangıç ses seviyesi (100%)

# Ses Kontrol UI Ayarları
VOLUME_ICON_SIZE = 150                 # İkon boyutu (piksel)
VOLUME_ICON_PADDING = 100              # Ekran kenarından mesafe


# Not: Ekran boyutları (SCREEN_WIDTH, SCREEN_HEIGHT) main.py'de
# ekran çözünürlüğüne göre dinamik olarak belirlenir
