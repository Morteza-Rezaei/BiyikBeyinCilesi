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
    
    # Ses efektleri cache'i
    _sound_cache = {}
    _loop_sounds = {}  # Sürekli çalan sesler için
    _active_sound_channels = {}  # Çalan seslerin kanallarını takip et
    
    # Çakışmaması gereken sesler (aynı anda sadece bir örnek çalabilir)
    NON_OVERLAPPING_SOUNDS = {
        'button_click',
        'jilet_hit',
        'terlik_hit',
        'buff_tea',
        'buff_speed_apply',
        'debuff_speed_apply',
        'level_complete',
        'game_over',
    }
    
    # Ses dosyası yolları
    SOUND_PATHS = {
        'button_click': 'assets/music/button_click.mp3',
        'bomb_explosion': 'assets/music/bomb_explosion.mp3',
        'jilet_hit': 'assets/music/jilet_hit.mp3',
        'terlik_hit': 'assets/music/terlik_hit.mp3',
        'buff_tea': 'assets/music/buff_tea.mp3',
        'buff_speed_apply': 'assets/music/buff_speed_apply.mp3',
        'debuff_speed_apply': 'assets/music/debuff_speed_apply.mp3',
        'level_complete': 'assets/music/level_complete.mp3',
        'game_over': 'assets/music/game_over.mp3',
        # Loop sesleri (opsiyonel - dosya yoksa sessizce atlanır)
        'buff_speed_loop': 'assets/music/buff_speed_loop.mp3',
        'debuff_speed_loop': 'assets/music/debuff_speed_loop.mp3',
    }
    
    @classmethod
    def init(cls):
        """Ses sistemini başlat"""
        pygame.mixer.init()
        pygame.mixer.music.set_endevent(cls.MUSIC_END)
        # Ses efektleri için yeterli kanal ayarla
        pygame.mixer.set_num_channels(16)
    
    @classmethod
    def get_volume(cls):
        """Mevcut ses seviyesi"""
        return VOLUME_LEVELS[cls._volume_index]
    
    @classmethod
    def cycle_volume(cls):
        """Ses seviyesini değiştir (döngüsel)"""
        cls._volume_index = (cls._volume_index + 1) % len(VOLUME_LEVELS)
        volume = cls.get_volume()
        pygame.mixer.music.set_volume(volume)
        # Tüm ses efektlerinin ses seviyesini güncelle
        for sound in cls._sound_cache.values():
            if sound:
                sound.set_volume(volume)
        return volume
    
    @classmethod
    def _load_sound(cls, sound_name):
        """Ses efektini yükle ve cache'le"""
        if sound_name not in cls._sound_cache:
            if sound_name in cls.SOUND_PATHS:
                import os
                sound_path = cls.SOUND_PATHS[sound_name]
                # Dosya yoksa sessizce None döndür (opsiyonel sesler için)
                if not os.path.exists(sound_path):
                    cls._sound_cache[sound_name] = None
                    return None
                try:
                    sound = pygame.mixer.Sound(sound_path)
                    sound.set_volume(cls.get_volume())
                    cls._sound_cache[sound_name] = sound
                except Exception as e:
                    print(f"Ses yüklenemedi: {sound_name} - {e}")
                    cls._sound_cache[sound_name] = None
            else:
                print(f"Bilinmeyen ses: {sound_name}")
                cls._sound_cache[sound_name] = None
        return cls._sound_cache[sound_name]
    
    @classmethod
    def _cleanup_finished_channels(cls):
        """Tamamlanan ses kanallarını temizle"""
        finished = []
        for sound_name, channel in cls._active_sound_channels.items():
            if channel is None or not channel.get_busy():
                finished.append(sound_name)
        for sound_name in finished:
            del cls._active_sound_channels[sound_name]
    
    @classmethod
    def play_sound(cls, sound_name):
        """Tek seferlik ses çal - çakışmayı önle"""
        sound = cls._load_sound(sound_name)
        if sound:
            try:
                # Tamamlanan kanalları temizle
                cls._cleanup_finished_channels()
                
                # Eğer bu ses çakışmaması gereken bir ses ise, önceki örneği durdur
                if sound_name in cls.NON_OVERLAPPING_SOUNDS:
                    if sound_name in cls._active_sound_channels:
                        channel = cls._active_sound_channels[sound_name]
                        if channel and channel.get_busy():
                            channel.stop()
                
                # Yeni kanalda çal
                channel = sound.play()
                
                # Çakışmaması gereken sesler için kanalı takip et
                if sound_name in cls.NON_OVERLAPPING_SOUNDS:
                    cls._active_sound_channels[sound_name] = channel
                # Çakışabilen sesler için kanalı takip etme (çoklu örnekler olabilir)
            except Exception as e:
                print(f"Ses çalınamadı: {sound_name} - {e}")
    
    @classmethod
    def play_sound_loop(cls, sound_name):
        """Sürekli çalan ses başlat"""
        sound = cls._load_sound(sound_name)
        if sound:
            try:
                # Eğer zaten çalıyorsa durdur
                if sound_name in cls._loop_sounds:
                    cls.stop_sound_loop(sound_name)
                # Yeni kanalda çal
                channel = sound.play(loops=-1)
                cls._loop_sounds[sound_name] = channel
            except Exception as e:
                print(f"Loop ses çalınamadı: {sound_name} - {e}")
    
    @classmethod
    def stop_sound_loop(cls, sound_name):
        """Sürekli çalan sesi durdur"""
        if sound_name in cls._loop_sounds:
            channel = cls._loop_sounds[sound_name]
            if channel:
                channel.stop()
            del cls._loop_sounds[sound_name]
    
    @classmethod
    def stop_all_sounds(cls):
        """Tüm ses efektlerini durdur"""
        for sound_name in list(cls._loop_sounds.keys()):
            cls.stop_sound_loop(sound_name)
        # Aktif ses kanallarını temizle
        for sound_name in list(cls._active_sound_channels.keys()):
            channel = cls._active_sound_channels[sound_name]
            if channel and channel.get_busy():
                channel.stop()
        cls._active_sound_channels.clear()
    
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
        cls.stop_all_sounds()


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
