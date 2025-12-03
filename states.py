"""
Bıyık Bey'in Çilesi - Oyun Durumları
Menü, oyun ve diğer ekranlar
"""

import pygame
from engine import GameState, Assets, Audio
from ui import ImageButton, VolumeControl
from settings import *


# =============================================================================
# MENU STATE - Ana Menü
# =============================================================================

class MenuState(GameState):
    """Ana menü ekranı"""
    
    def __init__(self, engine):
        super().__init__(engine)
        self._load_assets()
        self._calculate_layout()
        self._create_buttons()
        self._create_volume_control()
    
    def enter(self):
        """Menüye girildiğinde müziği başlat"""
        Audio.play_with_intro(
            'assets/music/menu_music_intro.mp3',
            'assets/music/menu_music_loop.mp3'
        )
    
    def exit(self):
        """Menüden çıkıldığında müziği durdur"""
        Audio.stop()
    
    def _load_assets(self):
        """Görselleri yükle"""
        self.background = Assets.load_image(
            'assets/Forest.png',
            (self.screen_width, self.screen_height)
        )
        
        char_height = int(self.screen_height * 0.23)
        self.character = Assets.load_to_height(
            'assets/biyik_adam/biyik_adam_right.png',
            char_height
        )
        
        title_width = int(self.screen_width * 0.5)
        self.title = Assets.load_to_width('assets/title.png', title_width)
        
        instruction_width = int(self.screen_width * 0.35)
        self.instruction = Assets.load_to_width('assets/instruction.png', instruction_width)
    
    def _calculate_layout(self):
        """Elemanların konumlarını hesapla"""
        gap1, gap2, gap3, btn_gap = 40, 30, 40, 20
        self.btn_height = int(self.screen_height * 0.08)
        
        total = (self.character.get_height() + gap1 +
                 self.title.get_height() + gap2 +
                 self.instruction.get_height() + gap3 +
                 self.btn_height * 2 + btn_gap)
        
        y = (self.screen_height - total) // 2
        self.char_y = y
        y += self.character.get_height() + gap1
        self.title_y = y
        y += self.title.get_height() + gap2
        self.instruction_y = y
        y += self.instruction.get_height() + gap3
        self.start_btn_y = y
        self.quit_btn_y = y + self.btn_height + btn_gap
    
    def _create_buttons(self):
        """Butonları oluştur"""
        btn_w = int(self.screen_width * 0.25)
        btn_x = (self.screen_width - btn_w) // 2
        
        self.start_btn = ImageButton(
            btn_x, self.start_btn_y, btn_w, self.btn_height,
            'assets/button_start.png', 'assets/button_start_h.png'
        )
        self.quit_btn = ImageButton(
            btn_x, self.quit_btn_y, btn_w, self.btn_height,
            'assets/button_quit.png', 'assets/button_quit_h.png'
        )
    
    def _create_volume_control(self):
        """Ses kontrolü oluştur"""
        self.volume = VolumeControl(self.screen_width, self.screen_height)
    
    def handle_event(self, event):
        """Olayları işle"""
        Audio.handle_music_end(event)
        
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self.engine.quit()
            return
        
        if self.start_btn.handle_event(event):
            self.engine.change_state(PlayingState(self.engine))
        
        if self.quit_btn.handle_event(event):
            self.engine.quit()
        
        new_vol = self.volume.handle_event(event)
        if new_vol is not None:
            pygame.mixer.music.set_volume(new_vol)
    
    def draw(self, screen):
        """Menüyü çiz"""
        screen.blit(self.background, (0, 0))
        
        # Karakter
        x = (self.screen_width - self.character.get_width()) // 2
        screen.blit(self.character, (x, self.char_y))
        
        # Başlık
        x = (self.screen_width - self.title.get_width()) // 2
        screen.blit(self.title, (x, self.title_y))
        
        # Talimat
        x = (self.screen_width - self.instruction.get_width()) // 2
        screen.blit(self.instruction, (x, self.instruction_y))
        
        # Butonlar
        self.start_btn.draw(screen)
        self.quit_btn.draw(screen)
        self.volume.draw(screen)


# =============================================================================
# PLAYING STATE - Oyun Ekranı
# =============================================================================

class PlayingState(GameState):
    """Ana oyun ekranı"""
    
    def __init__(self, engine):
        super().__init__(engine)
        self._load_assets()
        self._create_player()
        self._init_game_objects()
    
    def _load_assets(self):
        """Görselleri yükle"""
        self.background = Assets.load_image(
            'assets/Forest.png',
            (self.screen_width, self.screen_height)
        )
    
    def _create_player(self):
        """Oyuncuyu oluştur"""
        from player import Player
        self.player = Player(self.screen_width // 2, self.screen_height // 2)
    
    def _init_game_objects(self):
        """Oyun nesnelerini başlat"""
        from game_objects import SpawnManager, HealthUI
        import pygame
        
        # Nesne grupları
        self.teas = pygame.sprite.Group()
        self.bombs = pygame.sprite.Group()
        self.jilets = pygame.sprite.Group()
        self.terliks = pygame.sprite.Group()
        
        # Spawn yöneticisi
        self.spawn_manager = SpawnManager(self.screen_width, self.screen_height)
        
        # Can UI
        self.health_ui = HealthUI(self.screen_width, self.screen_height)
    
    def handle_event(self, event):
        """Olayları işle"""
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self.engine.change_state(MenuState(self.engine))
    
    def update(self, dt):
        """Güncelle"""
        # Oyuncu öldüyse menüye dön
        if self.player.is_dead():
            self.engine.change_state(MenuState(self.engine))
            return
        
        # Oyuncuyu güncelle
        self.player.update(self.screen_width, self.screen_height, dt)
        
        # Spawn manager güncelle
        self.spawn_manager.update(
            dt, 
            self.teas, 
            self.bombs, 
            self.jilets, 
            self.terliks,
            self.player.rect
        )
        
        # Nesneleri güncelle
        player_rect = self.player.get_collision_rect()
        
        for tea in self.teas:
            tea.update(self.screen_width, self.screen_height, player_rect)
        
        for bomb in list(self.bombs):
            bomb.update(self.screen_width, self.screen_height, player_rect)
            if bomb.exploded:
                self.bombs.remove(bomb)
        
        for jilet in self.jilets:
            jilet.update(self.screen_width, self.screen_height, player_rect)
        
        for terlik in list(self.terliks):
            terlik.update(self.screen_width, self.screen_height, player_rect)
            if terlik.is_off_screen():
                self.terliks.remove(terlik)
        
        # Çarpışma kontrolü
        self._check_collisions()
        
        # UI güncelle
        self.health_ui.update()
    
    def _check_collisions(self):
        """Çarpışma kontrolü"""
        player_rect = self.player.get_collision_rect()
        
        # Çay toplama
        for tea in list(self.teas):
            if player_rect.colliderect(tea.rect):
                if self.player.heal(1):
                    self.teas.remove(tea)
                    self.health_ui.set_health(self.player.health)
                else:
                    # Can zaten dolu, çay kaybolmasın
                    pass
        
        # Bomba patlaması
        for bomb in self.bombs:
            if bomb.check_explosion_hit(player_rect):
                if self.player.take_damage(1):
                    self.health_ui.set_health(self.player.health)
        
        # Jilet çarpışması
        for jilet in list(self.jilets):
            if player_rect.colliderect(jilet.rect):
                if self.player.take_damage(1):
                    self.health_ui.set_health(self.player.health)
                    self.jilets.remove(jilet)
        
        # Terlik çarpışması
        for terlik in list(self.terliks):
            if player_rect.colliderect(terlik.rect):
                if self.player.take_damage(1):
                    self.health_ui.set_health(self.player.health)
                    self.terliks.remove(terlik)
    
    def draw(self, screen):
        """Çiz"""
        screen.blit(self.background, (0, 0))
        
        # Çayları çiz
        for tea in self.teas:
            tea.draw(screen)
        
        # Bombaları çiz
        for bomb in self.bombs:
            bomb.draw(screen)
        
        # Jileti çiz
        for jilet in self.jilets:
            jilet.draw(screen)
        
        # Terlikleri çiz
        for terlik in self.terliks:
            terlik.draw(screen)
        
        # Oyuncuyu çiz
        self.player.draw(screen)
        
        # Can UI
        self.health_ui.draw(screen)
        
        # ESC ipucu
        font = Assets.get_font(32)
        shadow = font.render("ESC - Menüye Dön", True, BLACK)
        text = font.render("ESC - Menüye Dön", True, WHITE)
        screen.blit(shadow, (22, 22 + 60))
        screen.blit(text, (20, 20 + 60))
