"""
Bıyık Bey'in Çilesi - Oyun Motoru
Tüm temel oyun sistemleri burada
"""

import pygame
import sys
from settings import *


# =============================================================================
# GAME STATE - Oyun Durumu Temel Sınıfı
# =============================================================================

class GameState:
    """Tüm oyun durumları bu sınıftan türetilir (menü, oyun, pause, vb.)"""
    
    def __init__(self, engine):
        self.engine = engine
        self.screen_width = engine.screen_width
        self.screen_height = engine.screen_height
    
    def enter(self):
        """Duruma girildiğinde"""
        pass
    
    def exit(self):
        """Durumdan çıkıldığında"""
        pass
    
    def handle_event(self, event):
        """Olayları işle"""
        pass
    
    def update(self, dt):
        """Güncelle (dt = delta time)"""
        pass
    
    def draw(self, screen):
        """Ekrana çiz"""
        pass


# =============================================================================
# ASSET MANAGER - Görsel/Ses Yöneticisi
# =============================================================================

class Assets:
    """Görselleri ve sesleri önbellekte tutar"""
    
    _cache = {}
    _preloaded = False
    
    @classmethod
    def preload_game_assets(cls, screen_width, screen_height):
        """Oyun asset'lerini önceden yükle - kasma önleme"""
        if cls._preloaded:
            return
        
        # Oyuncu animasyonları
        scale = 1.3
        cls.load_scaled('assets/player/idle_stand.png', scale)
        for dir in ['down', 'up', 'left', 'right']:
            cls.load_scaled(f'assets/player/walk_{dir}_1.png', scale)
            cls.load_scaled(f'assets/player/walk_{dir}_2.png', scale)
        
        # Oyun arka planı
        cls.load_image('assets/game_bg.png', (screen_width, screen_height))
        
        # Çay
        cls.load_scaled('assets/game/tea.png', 1.2)
        
        # Bomba animasyonları
        for i in range(1, 8):
            cls.load_scaled(f'assets/game/bomb_tick_{i}.png', 1.3)
        for i in range(1, 6):
            cls.load_scaled(f'assets/game/explosion_{i}.png', 1.3 * 2)
        
        # Jilet animasyonları
        for i in range(1, 9):
            cls.load_scaled(f'assets/game/sinsi_jilet_{i}.png', 1.2)
        
        # Terlik animasyonları
        for i in range(1, 9):
            cls.load_scaled(f'assets/game/ucan_terlik_{i}.png', 1.0)
        
        # Buff/Debuff
        cls.load_scaled('assets/game/speed_buff.png', 1.0)
        cls.load_scaled('assets/game/speed_debuff.png', 1.0)
        cls.load_scaled('assets/game/speed_buff.png', 0.6)
        cls.load_scaled('assets/game/speed_debuff.png', 0.6)
        
        # Can göstergesi (küçültülmüş)
        cls.load_scaled('assets/game/heart.png', 0.45)
        cls.load_scaled('assets/game/heart_broken.png', 0.45)
        
        cls._preloaded = True
        print("Oyun asset'leri önceden yüklendi!")
    
    @classmethod
    def load_image(cls, path, size=None):
        """Görsel yükle ve ölçekle"""
        key = f"{path}_{size}"
        if key not in cls._cache:
            img = pygame.image.load(path).convert_alpha()
            if size:
                img = pygame.transform.scale(img, size)
            cls._cache[key] = img
        return cls._cache[key]
    
    @classmethod
    def load_scaled(cls, path, scale=1.0):
        """Görseli çarpanla ölçekle"""
        key = f"{path}_x{scale}"
        if key not in cls._cache:
            img = pygame.image.load(path).convert_alpha()
            w, h = int(img.get_width() * scale), int(img.get_height() * scale)
            cls._cache[key] = pygame.transform.scale(img, (w, h))
        return cls._cache[key]
    
    @classmethod
    def load_to_height(cls, path, height):
        """Görseli yüksekliğe göre ölçekle (oranı koru)"""
        key = f"{path}_h{height}"
        if key not in cls._cache:
            img = pygame.image.load(path).convert_alpha()
            ratio = img.get_width() / img.get_height()
            cls._cache[key] = pygame.transform.scale(img, (int(height * ratio), height))
        return cls._cache[key]
    
    @classmethod
    def load_to_width(cls, path, width):
        """Görseli genişliğe göre ölçekle (oranı koru)"""
        key = f"{path}_w{width}"
        if key not in cls._cache:
            img = pygame.image.load(path).convert_alpha()
            ratio = img.get_width() / img.get_height()
            cls._cache[key] = pygame.transform.scale(img, (width, int(width / ratio)))
        return cls._cache[key]
    
    @classmethod
    def get_font(cls, size, name=None):
        """Font al"""
        key = f"font_{name}_{size}"
        if key not in cls._cache:
            cls._cache[key] = pygame.font.Font(name, size)
        return cls._cache[key]


# =============================================================================
# AUDIO MANAGER - Ses Yöneticisi
# =============================================================================

class Audio:
    """Müzik ve ses efektlerini yönetir"""
    
    _volume_index = DEFAULT_VOLUME_INDEX
    _music_state = None
    MUSIC_END = pygame.USEREVENT + 1
    
    @classmethod
    def init(cls):
        """Ses sistemini başlat"""
        pygame.mixer.init()
        pygame.mixer.music.set_endevent(cls.MUSIC_END)
    
    @classmethod
    def get_volume(cls):
        """Mevcut ses seviyesi"""
        return VOLUME_LEVELS[cls._volume_index]
    
    @classmethod
    def cycle_volume(cls):
        """Ses seviyesini değiştir (döngüsel)"""
        cls._volume_index = (cls._volume_index + 1) % len(VOLUME_LEVELS)
        pygame.mixer.music.set_volume(cls.get_volume())
        return cls.get_volume()
    
    @classmethod
    def play_music(cls, path, loops=-1):
        """Müzik çal"""
        pygame.mixer.music.load(path)
        pygame.mixer.music.set_volume(cls.get_volume())
        pygame.mixer.music.play(loops)
    
    @classmethod
    def play_with_intro(cls, intro_path, loop_path):
        """Intro + loop müzik çal"""
        cls._music_state = {'state': 'intro', 'loop': loop_path}
        pygame.mixer.music.load(intro_path)
        pygame.mixer.music.set_volume(cls.get_volume())
        pygame.mixer.music.play()
    
    @classmethod
    def handle_music_end(cls, event):
        """Müzik bitişini işle"""
        if event.type != cls.MUSIC_END:
            return False
        if cls._music_state and cls._music_state['state'] == 'intro':
            cls._music_state['state'] = 'loop'
            pygame.mixer.music.load(cls._music_state['loop'])
            pygame.mixer.music.set_volume(cls.get_volume())
            pygame.mixer.music.play(-1)
            return True
        return False
    
    @classmethod
    def stop(cls):
        """Müziği durdur"""
        pygame.mixer.music.stop()
        cls._music_state = None


# =============================================================================
# GAME ENGINE - Ana Oyun Motoru
# =============================================================================

class GameEngine:
    """Ana oyun motoru - Oyunu başlatır ve yönetir"""
    
    def __init__(self):
        pygame.init()
        Audio.init()
        
        # Tam ekran
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        pygame.display.set_caption("Bıyık Bey'in Çilesi")
        
        self.screen_width = self.screen.get_width()
        self.screen_height = self.screen.get_height()
        self.clock = pygame.time.Clock()
        self.running = False
        
        # Durum yığını
        self._states = []
        
        print(f"Oyun başlatıldı: {self.screen_width}x{self.screen_height}")
    
    @property
    def current_state(self):
        """Mevcut durum"""
        return self._states[-1] if self._states else None
    
    def push_state(self, state):
        """Yeni durum ekle"""
        self._states.append(state)
        state.enter()
    
    def pop_state(self):
        """Mevcut durumu çıkar"""
        if self._states:
            self._states.pop().exit()
    
    def change_state(self, state):
        """Durumu değiştir"""
        if self._states:
            self._states.pop().exit()
        self._states.append(state)
        state.enter()
    
    def run(self):
        """Ana oyun döngüsü"""
        from states import MenuState
        self.push_state(MenuState(self))
        
        self.running = True
        while self.running:
            dt = self.clock.tick(FPS) / 1000.0
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif self.current_state:
                    self.current_state.handle_event(event)
            
            if self.current_state:
                self.current_state.update(dt)
                self.current_state.draw(self.screen)
            
            pygame.display.flip()
        
        pygame.quit()
        sys.exit()
    
    def quit(self):
        """Oyundan çık"""
        self.running = False
