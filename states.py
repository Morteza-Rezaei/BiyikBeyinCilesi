"""
Bıyık Bey'in Çilesi - Oyun Durumları
Menü, oyun ve diğer ekranlar
"""

import pygame
from engine import GameState, Assets, Audio
from ui import ImageButton, VolumeControl, HintButton, HintPopup, PauseMenu
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
        
        # Oyun asset'lerini arka planda önceden yükle (kasma önleme)
        Assets.preload_game_assets(self.screen_width, self.screen_height)
    
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
            'assets/home_bg.jpg',
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
        
        # Ses kontrolü (Audio.cycle_volume zaten müzik sesini ayarlıyor)
        self.volume.handle_event(event)
    
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
    
    def enter(self):
        """Oyuna girildiğinde müziği başlat"""
        Audio.play_music('assets/music/game_music.mp3')
    
    def exit(self):
        """Oyundan çıkıldığında müziği durdur"""
        Audio.stop()
    
    def _load_assets(self):
        """Görselleri yükle"""
        self.background = Assets.load_image(
            'assets/game_bg.png',
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
        
        # Buff/Debuff listeleri
        self.speed_buffs = []
        self.speed_debuffs = []
        
        # Spawn yöneticisi
        self.spawn_manager = SpawnManager(self.screen_width, self.screen_height)
        
        # Can UI
        self.health_ui = HealthUI(self.screen_width, self.screen_height)
        
        # Hint sistemi
        self.hint_button = HintButton(self.screen_width, self.screen_height)
        self.hint_popup = HintPopup(self.screen_width, self.screen_height)
        
        # Pause menüsü
        self.pause_menu = PauseMenu(self.screen_width, self.screen_height)
    
    def handle_event(self, event):
        """Olayları işle"""
        # Pause menüsü açıksa önce onu işle
        if self.pause_menu.is_open:
            result = self.pause_menu.handle_event(event)
            if result == 'quit':
                self.engine.change_state(MenuState(self.engine))
            return  # Pause açıkken diğer eventleri işleme
        
        # Hint popup açıksa önce onu işle
        if self.hint_popup.is_open:
            result = self.hint_popup.handle_event(event)
            return  # Popup açıkken diğer eventleri işleme
        
        # ESC ile pause menüsünü aç
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self.pause_menu.open()
            return
        
        # Hint butonuna tıklandı mı?
        if self.hint_button.handle_event(event):
            self.hint_popup.open()
            return
    
    def update(self, dt):
        """Güncelle"""
        # Pause menüsü veya hint popup açıksa oyunu durdur
        if self.pause_menu.is_open or self.hint_popup.is_open:
            return
        
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
            self.player.rect,
            self.speed_buffs,
            self.speed_debuffs
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
        
        # Speed Buff'ları güncelle
        for buff in self.speed_buffs[:]:
            if not buff.update(self.screen_width, self.screen_height, player_rect, dt):
                self.speed_buffs.remove(buff)
        
        # Speed Debuff'ları güncelle
        for debuff in self.speed_debuffs[:]:
            if not debuff.update(self.screen_width, self.screen_height, player_rect, dt):
                self.speed_debuffs.remove(debuff)
        
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
        
        # Speed Buff toplama
        for buff in self.speed_buffs[:]:
            if player_rect.colliderect(buff.rect):
                self.player.apply_speed_buff()
                self.speed_buffs.remove(buff)
        
        # Speed Debuff toplama
        for debuff in self.speed_debuffs[:]:
            if player_rect.colliderect(debuff.rect):
                self.player.apply_speed_debuff()
                self.speed_debuffs.remove(debuff)
    
    def draw(self, screen):
        """Çiz"""
        screen.blit(self.background, (0, 0))
        
        # Çayları çiz
        for tea in self.teas:
            tea.draw(screen)
        
        # Bombaları çiz
        for bomb in self.bombs:
            bomb.draw(screen)
        
        # Speed Buff'ları çiz
        for buff in self.speed_buffs:
            buff.draw(screen)
        
        # Speed Debuff'ları çiz
        for debuff in self.speed_debuffs:
            debuff.draw(screen)
        
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
        
        # Buff/Debuff göstergesi (sağ üst köşe)
        self._draw_buff_indicator(screen)
        
        # ESC ipucu (üstte)
        font = Assets.get_font(28)
        shadow = font.render("ESC - Duraklat", True, BLACK)
        text = font.render("ESC - Duraklat", True, WHITE)
        screen.blit(shadow, (22, 22))
        screen.blit(text, (20, 20))
        
        # Hint butonu
        self.hint_button.draw(screen)
        
        # Hint popup (en üstte çizilmeli)
        self.hint_popup.draw(screen)
        
        # Pause menüsü (en üstte)
        self.pause_menu.draw(screen)
    
    def _draw_buff_indicator(self, screen):
        """Aktif buff/debuff göstergesi çiz"""
        if self.player.has_active_buff():
            # Yeşil hız göstergesi
            icon = Assets.load_scaled('assets/game/speed_buff.png', 0.6)
            icon_x = self.screen_width - icon.get_width() - 20
            icon_y = 20
            screen.blit(icon, (icon_x, icon_y))
            
            # Kalan süre çubuğu
            bar_width = icon.get_width()
            bar_height = 8
            bar_x = icon_x
            bar_y = icon_y + icon.get_height() + 5
            
            remaining = self.player.speed_buff_timer / self.player.buff_duration
            pygame.draw.rect(screen, DARK_GRAY, (bar_x, bar_y, bar_width, bar_height))
            pygame.draw.rect(screen, GREEN, (bar_x, bar_y, int(bar_width * remaining), bar_height))
        
        elif self.player.has_active_debuff():
            # Kırmızı yavaşlık göstergesi
            icon = Assets.load_scaled('assets/game/speed_debuff.png', 0.6)
            icon_x = self.screen_width - icon.get_width() - 20
            icon_y = 20
            screen.blit(icon, (icon_x, icon_y))
            
            # Kalan süre çubuğu
            bar_width = icon.get_width()
            bar_height = 8
            bar_x = icon_x
            bar_y = icon_y + icon.get_height() + 5
            
            remaining = self.player.speed_debuff_timer / self.player.buff_duration
            pygame.draw.rect(screen, DARK_GRAY, (bar_x, bar_y, bar_width, bar_height))
            pygame.draw.rect(screen, RED, (bar_x, bar_y, int(bar_width * remaining), bar_height))
