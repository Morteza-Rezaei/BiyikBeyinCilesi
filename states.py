"""
Bıyık Bey'in Çilesi - Oyun Durumları
Menü, oyun ve diğer ekranlar
"""

import pygame
from engine import GameState, Assets, Audio
from ui import ImageButton, VolumeControl, HintButton, HintPopup, PauseMenu, LevelSelector
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
        
        # Reset butonu rect'i başlat
        self.reset_btn_rect = None
        
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
        
        # Level seçim dialogu
        self.level_selector = LevelSelector(self.screen_width, self.screen_height)
    
    def _create_volume_control(self):
        """Ses kontrolü oluştur"""
        self.volume = VolumeControl(self.screen_width, self.screen_height)
    
    def handle_event(self, event):
        """Olayları işle"""
        Audio.handle_music_end(event)
        
        # Level seçim dialogu açıksa önce onu işle
        if self.level_selector.is_open:
            result = self.level_selector.handle_event(event)
            if result == 'cancel':
                return
            elif isinstance(result, tuple) and result[0] == 'start':
                # Girilen level ile oyunu başlat
                self.engine.change_state(PlayingState(self.engine, result[1]))
                return
            return
        
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self.engine.quit()
            return
        
        if self.start_btn.handle_event(event):
            # CTRL tuşu basılıysa level seçimi aç, değilse normal başlat
            keys = pygame.key.get_mods()
            if keys & pygame.KMOD_CTRL:
                # Level seçim dialogunu aç
                self.level_selector.open(1)
            else:
                # Normal olarak level 1'den başlat
                self.engine.change_state(PlayingState(self.engine))
        
        if self.quit_btn.handle_event(event):
            self.engine.quit()
        
        # Rekor sıfırlama butonu
        highscore = load_highscore()
        if highscore['level'] > 0 and self.reset_btn_rect:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if self.reset_btn_rect.collidepoint(event.pos):
                    Audio.play_sound('button_click')
                    reset_highscore()
                    return  # Menüyü yeniden çizmek için return
        
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
        
        # Level seçim dialogu (varsa)
        self.level_selector.draw(screen)
        
        # Rekor bilgisi (sağ üst köşe)
        highscore = load_highscore()
        if highscore['level'] > 0:
            font = Assets.get_font(48)
            record_text = f"Rekor: Level {highscore['level']}"
            record_surf = font.render(record_text, True, YELLOW)
            record_shadow = font.render(record_text, True, BLACK)
            
            # Sağ üst köşe
            record_x = self.screen_width - record_surf.get_width() - 40
            record_y = 40
            
            screen.blit(record_shadow, (record_x + 3, record_y + 3))
            screen.blit(record_surf, (record_x, record_y))
            
            # Tarih
            if highscore['date']:
                date_text = f"({highscore['date']})"
                date_surf = Assets.get_font(32).render(date_text, True, LIGHT_GRAY)
                screen.blit(date_surf, (record_x + (record_surf.get_width() - date_surf.get_width()) // 2, record_y + 55))
            
            # Reset butonu (rekorun altında)
            reset_font = Assets.get_font(24)
            reset_text = "[Rekoru Sıfırla]"
            reset_surf = reset_font.render(reset_text, True, LIGHT_GRAY)
            reset_hover_surf = reset_font.render(reset_text, True, WHITE)
            
            reset_x = record_x + (record_surf.get_width() - reset_surf.get_width()) // 2
            reset_y = record_y + 90
            self.reset_btn_rect = pygame.Rect(reset_x, reset_y, reset_surf.get_width(), reset_surf.get_height())
            
            # Hover durumunu kontrol et
            mouse_pos = pygame.mouse.get_pos()
            is_hovered = self.reset_btn_rect and self.reset_btn_rect.collidepoint(mouse_pos)
            screen.blit(reset_hover_surf if is_hovered else reset_surf, (reset_x, reset_y))
        else:
            # Rekor yoksa reset butonu da yok
            self.reset_btn_rect = None
        
        # Level seçim ipucu (sol alt köşe)
        hint_font = Assets.get_font(24)
        hint_text = "Ctrl+Start = Level Seç"
        hint_surf = hint_font.render(hint_text, True, LIGHT_GRAY)
        screen.blit(hint_surf, (40, self.screen_height - 60))


# =============================================================================
# PLAYING STATE - Oyun Ekranı
# =============================================================================

class PlayingState(GameState):
    """Ana oyun ekranı - Survivor Mode"""
    
    def __init__(self, engine, start_level=1):
        super().__init__(engine)
        self._load_assets()
        self._create_player()
        self._init_game_objects()
        
        # Başlangıç levelini ayarla
        self.start_level = max(1, start_level)
        # Level'i direkt başlangıç leveline ayarla
        self.spawn_manager.level = self.start_level
        self.spawn_manager.reset_for_new_level()
        
        # Level sistemi
        self.waiting_for_start = True  # Level başlangıcında bekle
        self.game_over = False
        
        # Aktif buff (haritada sadece 1 tane)
        self.active_buff = None  # (type, object) tuple
        self.active_buff_type = None  # 'tea', 'speed_buff', 'speed_debuff'
        
        # Ses efektleri için flag'ler
        self.level_complete_sound_played = False
        self.game_over_sound_played = False
    
    def enter(self):
        """Oyuna girildiğinde müziği başlat ve fareyi gizle"""
        # Oyun müziği kaldırıldı (kullanıcı isteği)
        # Audio.play_music('assets/music/game_music.mp3')
        pygame.mouse.set_visible(False)  # Oyun aktifken fareyi gizle
    
    def exit(self):
        """Oyundan çıkıldığında müziği durdur, rekor kaydet ve fareyi göster"""
        save_highscore(self.spawn_manager.level, self.start_level)
        Audio.stop()
        pygame.mouse.set_visible(True)  # Menüye dönünce fareyi göster
    
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
        self.bombs = pygame.sprite.Group()
        self.jilets = pygame.sprite.Group()
        self.terliks = pygame.sprite.Group()
        
        # Spawn yöneticisi
        self.spawn_manager = SpawnManager(self.screen_width, self.screen_height)
        
        # Can UI
        self.health_ui = HealthUI(self.screen_width, self.screen_height)
        self.health_ui.set_health(self.player.health)  # Başlangıçta senkronize et
        
        # Hint sistemi
        self.hint_button = HintButton(self.screen_width, self.screen_height)
        self.hint_popup = HintPopup(self.screen_width, self.screen_height)
        
        # Pause menüsü
        self.pause_menu = PauseMenu(self.screen_width, self.screen_height)
        
        # Level tamamlama popup için font
        self.level_font = Assets.get_font(72)
        self.info_font = Assets.get_font(36)
        self.game_over_font = Assets.get_font(96)
        
        # Game Over butonları
        btn_width = int(self.screen_width * 0.2)
        btn_height = int(self.screen_height * 0.08)
        center_x = self.screen_width // 2
        center_y = self.screen_height // 2
        
        self.retry_btn = ImageButton(
            center_x - btn_width // 2,
            center_y + 50,
            btn_width, btn_height,
            'assets/button_again.png',
            'assets/button_again_h.png'
        )
        
        self.gameover_quit_btn = ImageButton(
            center_x - btn_width // 2,
            center_y + 50 + btn_height + 20,
            btn_width, btn_height,
            'assets/button_quit.png',
            'assets/button_quit_h.png'
        )
        
        # Game over overlay
        self.game_over_overlay = pygame.Surface((self.screen_width, self.screen_height))
        self.game_over_overlay.fill((0, 0, 0))
        self.game_over_overlay.set_alpha(200)
    
    def _clear_enemies(self):
        """Tüm düşmanları temizle"""
        self.bombs.empty()
        self.jilets.empty()
        self.terliks.empty()
        self.active_buff = None
        self.active_buff_type = None
    
    def _start_next_level(self):
        """Sonraki leveli başlat"""
        self._clear_enemies()
        self.spawn_manager.level += 1
        self.spawn_manager.reset_for_new_level()
        # Level başlangıcında hemen 1 terlik ve 1 jilet spawn et
        self.spawn_manager.spawn_initial_enemies(
            self.bombs, self.jilets, self.terliks, self.player.rect
        )
        self.waiting_for_start = False
        # Ses flag'ini sıfırla
        self.level_complete_sound_played = False
        # Oyuncuyu merkeze al
        self.player.rect.center = (self.screen_width // 2, self.screen_height // 2)
    
    def _restart_game(self):
        """Oyunu yeniden başlat"""
        # Tüm sesleri durdur
        Audio.stop_all_sounds()
        # Yeni PlayingState oluştur
        self.engine.change_state(PlayingState(self.engine))
    
    def handle_event(self, event):
        """Olayları işle"""
        # Game Over ekranı
        if self.game_over:
            # Game over ekranında fareyi göster (butonlar için)
            pygame.mouse.set_visible(True)
            if self.retry_btn.handle_event(event):
                self._restart_game()
                return
            if self.gameover_quit_btn.handle_event(event):
                self.engine.change_state(MenuState(self.engine))
                return
            return
        
        # Level tamamlandı ve başlat bekleniyor
        if self.spawn_manager.level_complete and not self.game_over:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                self._start_next_level()
                return
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self._start_next_level()
                return
        
        # Level başlangıcında başlat bekleniyor
        if self.waiting_for_start:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                self.waiting_for_start = False
                # Eğer start_level > 1 ise, initial enemies spawn et
                if self.start_level > 1:
                    self.spawn_manager.spawn_initial_enemies(
                        self.bombs, self.jilets, self.terliks, self.player.rect
                    )
                return
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.waiting_for_start = False
                # Eğer start_level > 1 ise, initial enemies spawn et
                if self.start_level > 1:
                    self.spawn_manager.spawn_initial_enemies(
                        self.bombs, self.jilets, self.terliks, self.player.rect
                    )
                return
            # ESC ile çıkış
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.engine.change_state(MenuState(self.engine))
                return
            return
        
        # Pause menüsü açıksa önce onu işle
        if self.pause_menu.is_open:
            result = self.pause_menu.handle_event(event)
            if result == 'quit':
                pygame.mouse.set_visible(True)  # Menüye dönünce fareyi göster
                self.engine.change_state(MenuState(self.engine))
            elif result == 'continue':
                pygame.mouse.set_visible(False)  # Oyuna devam edince fareyi gizle
            return  # Pause açıkken diğer eventleri işleme
        
        # Hint popup açıksa önce onu işle
        if self.hint_popup.is_open:
            result = self.hint_popup.handle_event(event)
            if result == 'close':
                pygame.mouse.set_visible(False)  # Popup kapandığında fareyi gizle
            return  # Popup açıkken diğer eventleri işleme
        
        # ESC ile pause menüsünü aç (fareyi göster)
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self.pause_menu.open()
            pygame.mouse.set_visible(True)  # Pause menüsü açıldığında fareyi göster
            return
        
        # H tuşu ile hint popup aç (fareyi göster)
        if event.type == pygame.KEYDOWN and event.key == pygame.K_h:
            self.hint_popup.open()
            pygame.mouse.set_visible(True)  # Hint popup açıldığında fareyi göster
            return
        
        # Oyun aktifken tüm mouse event'lerini ignore et (performans için)
        if event.type in (pygame.MOUSEMOTION, pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP):
            return
    
    def update(self, dt):
        """Güncelle"""
        # Level tamamlandı sesi (bir kez) - return'den önce kontrol et
        if self.spawn_manager.level_complete and not self.level_complete_sound_played:
            Audio.play_sound('level_complete')
            self.level_complete_sound_played = True
        
        # Game over, beklemede veya level tamamlandıysa güncelleme yapma
        if self.game_over or self.waiting_for_start or self.spawn_manager.level_complete:
            return
        
        # Pause menüsü veya hint popup açıksa oyunu durdur
        if self.pause_menu.is_open or self.hint_popup.is_open:
            return
        
        # Oyuncu öldüyse game over
        if self.player.is_dead():
            self.game_over = True
            # Game over ekranında fareyi göster (butonlar için)
            pygame.mouse.set_visible(True)
            # Game over sesi (bir kez)
            if not self.game_over_sound_played:
                Audio.play_sound('game_over')
                self.game_over_sound_played = True
            # Rekor kaydet (sadece level 1'den başlayanlar için)
            from settings import save_highscore
            save_highscore(self.spawn_manager.level, self.start_level)
            return
        
        # Oyuncuyu güncelle
        self.player.update(self.screen_width, self.screen_height, dt)
        
        # Spawn manager güncelle (sadece aktif buff yoksa yeni buff spawn olabilir)
        new_buff = self.spawn_manager.update(
            dt, 
            self.bombs, 
            self.jilets, 
            self.terliks,
            self.player.rect,
            self.active_buff
        )
        
        # Yeni buff oluşturuldu mu?
        if new_buff:
            self.active_buff_type, self.active_buff = new_buff
        
        # Nesneleri güncelle
        player_rect = self.player.get_collision_rect()
        
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
        
        # Aktif buff'ı güncelle
        if self.active_buff:
            if not self.active_buff.update(self.screen_width, self.screen_height, player_rect, dt):
                self.active_buff = None
                self.active_buff_type = None
        
        # Çarpışma kontrolü
        self._check_collisions()
        
        # UI güncelle
        self.health_ui.update()
    
    def _check_collisions(self):
        """Çarpışma kontrolü"""
        player_rect = self.player.get_collision_rect()
        
        # Aktif buff ile çarpışma kontrolü
        if self.active_buff and player_rect.colliderect(self.active_buff.rect):
            if self.active_buff_type == 'tea':
                if self.player.heal(1):
                    self.health_ui.set_health(self.player.health)
                    Audio.play_sound('buff_tea')
                    self.active_buff = None
                    self.active_buff_type = None
            elif self.active_buff_type == 'speed_buff':
                self.player.apply_speed_buff()
                Audio.play_sound('buff_speed_apply')
                self.active_buff = None
                self.active_buff_type = None
            elif self.active_buff_type == 'speed_debuff':
                self.player.apply_speed_debuff()
                Audio.play_sound('debuff_speed_apply')
                self.active_buff = None
                self.active_buff_type = None
        
        # Bomba patlaması (ses zaten bomb.update() içinde çalıyor)
        for bomb in self.bombs:
            if bomb.check_explosion_hit(player_rect):
                if self.player.take_damage(1):
                    self.health_ui.set_health(self.player.health)
        
        # Jilet çarpışması
        for jilet in list(self.jilets):
            if player_rect.colliderect(jilet.rect):
                if self.player.take_damage(1):
                    self.health_ui.set_health(self.player.health)
                    Audio.play_sound('jilet_hit')
                    self.jilets.remove(jilet)
        
        # Terlik çarpışması
        for terlik in list(self.terliks):
            if player_rect.colliderect(terlik.rect):
                if self.player.take_damage(1):
                    self.health_ui.set_health(self.player.health)
                    Audio.play_sound('terlik_hit')
                    self.terliks.remove(terlik)
    
    def draw(self, screen):
        """Çiz"""
        screen.blit(self.background, (0, 0))
        
        # Bombaları çiz
        for bomb in self.bombs:
            bomb.draw(screen)
        
        # Aktif buff'ı çiz
        if self.active_buff:
            self.active_buff.draw(screen)
        
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
        
        # Level ve zaman bilgisi (üstte ortalanmış)
        self._draw_level_info(screen)
        
        # Buff göstergesi (sol üstte, can altında)
        self._draw_buff_indicator(screen)
        
        # Hint butonu (oyun aktifken fare gizli, hover kontrolü yok)
        if self.pause_menu.is_open or self.hint_popup.is_open:
            # Sadece pause/hint açıkken hint butonu hover kontrolü yap
            self.hint_button.draw(screen)
        else:
            # Normal durumda hint butonunu çiz (hover yok)
            self.hint_button.is_hovered = False
            self.hint_button.draw(screen)
        
        # Hint popup (en üstte çizilmeli)
        self.hint_popup.draw(screen)
        
        # Pause menüsü (en üstte)
        self.pause_menu.draw(screen)
        
        # Level başlangıcı veya tamamlanma ekranı
        if self.waiting_for_start or self.spawn_manager.level_complete:
            self._draw_level_screen(screen)
        
        # Game Over ekranı (en üstte)
        if self.game_over:
            self._draw_game_over(screen)
    
    def _draw_game_over(self, screen):
        """Game Over ekranı"""
        # Karartma
        screen.blit(self.game_over_overlay, (0, 0))
        
        center_x = self.screen_width // 2
        center_y = self.screen_height // 2
        
        # GAME OVER başlık
        title = "GAME OVER"
        title_surf = self.game_over_font.render(title, True, RED)
        title_shadow = self.game_over_font.render(title, True, BLACK)
        screen.blit(title_shadow, (center_x - title_surf.get_width() // 2 + 4, center_y - 120 + 4))
        screen.blit(title_surf, (center_x - title_surf.get_width() // 2, center_y - 120))
        
        # Ulaşılan level
        level_text = f"Level {self.spawn_manager.level}'e ulaştın!"
        level_surf = self.info_font.render(level_text, True, WHITE)
        screen.blit(level_surf, (center_x - level_surf.get_width() // 2, center_y - 30))
        
        # Rekor bilgisi
        from settings import load_highscore
        highscore = load_highscore()
        if highscore['level'] > 0:
            if self.spawn_manager.level >= highscore['level']:
                record_text = "*** YENI REKOR! ***"
                record_color = YELLOW
            else:
                record_text = f"Rekor: Level {highscore['level']}"
                record_color = LIGHT_GRAY
            record_surf = self.info_font.render(record_text, True, record_color)
            screen.blit(record_surf, (center_x - record_surf.get_width() // 2, center_y + 10))
        
        # Butonlar
        self.retry_btn.draw(screen)
        self.gameover_quit_btn.draw(screen)
    
    def _draw_level_info(self, screen):
        """Level ve kalan süre bilgisi (üstte ortalanmış)"""
        # Level
        level_text = f"Level {self.spawn_manager.level}"
        level_surf = self.info_font.render(level_text, True, WHITE)
        level_shadow = self.info_font.render(level_text, True, BLACK)
        
        # Kalan süre
        remaining = max(0, LEVEL_DURATION - self.spawn_manager.level_timer)
        time_text = f"{int(remaining)}s"
        time_surf = self.info_font.render(time_text, True, YELLOW)
        time_shadow = self.info_font.render(time_text, True, BLACK)
        
        # Ortalanmış çiz
        center_x = self.screen_width // 2
        
        screen.blit(level_shadow, (center_x - level_surf.get_width() // 2 + 2, 22))
        screen.blit(level_surf, (center_x - level_surf.get_width() // 2, 20))
        
        screen.blit(time_shadow, (center_x - time_surf.get_width() // 2 + 2, 62))
        screen.blit(time_surf, (center_x - time_surf.get_width() // 2, 60))
    
    def _draw_level_screen(self, screen):
        """Level başlangıç/bitiş ekranı"""
        # Karartma
        overlay = pygame.Surface((self.screen_width, self.screen_height))
        overlay.fill((0, 0, 0))
        overlay.set_alpha(180)
        screen.blit(overlay, (0, 0))
        
        center_x = self.screen_width // 2
        center_y = self.screen_height // 2
        
        if self.waiting_for_start:
            # Level başlangıcı
            title = f"Level {self.spawn_manager.level}"
            subtitle = "Başlamak için tıkla veya SPACE'e bas"
        else:
            # Level tamamlandı
            title = f"Level {self.spawn_manager.level} Tamamlandı!"
            subtitle = "Sonraki level için tıkla veya SPACE'e bas"
        
        # Başlık
        title_surf = self.level_font.render(title, True, WHITE)
        title_shadow = self.level_font.render(title, True, BLACK)
        screen.blit(title_shadow, (center_x - title_surf.get_width() // 2 + 3, center_y - 50 + 3))
        screen.blit(title_surf, (center_x - title_surf.get_width() // 2, center_y - 50))
        
        # Alt başlık
        sub_surf = self.info_font.render(subtitle, True, LIGHT_GRAY)
        screen.blit(sub_surf, (center_x - sub_surf.get_width() // 2, center_y + 30))
        
        # Rekor bilgisi
        from settings import load_highscore
        highscore = load_highscore()
        if highscore['level'] > 0:
            record_text = f"Rekor: Level {highscore['level']} ({highscore['date']})"
            record_surf = self.info_font.render(record_text, True, YELLOW)
            screen.blit(record_surf, (center_x - record_surf.get_width() // 2, center_y + 80))
    
    def _draw_buff_indicator(self, screen):
        """Aktif buff/debuff göstergesi çiz (sol üstte, can altında)"""
        # Pozisyon: can göstergesinin altında (kalpler ~60-110 px arası)
        indicator_x = 20
        indicator_y = 130  # Kalplerin altı - biraz boşluk bırak
        
        if self.player.has_active_buff():
            # Yeşil hız göstergesi
            icon = Assets.load_scaled('assets/game/speed_buff.png', 0.7)
            screen.blit(icon, (indicator_x, indicator_y))
            
            # Kalan süre çubuğu
            bar_width = icon.get_width()
            bar_height = 6
            bar_x = indicator_x
            bar_y = indicator_y + icon.get_height() + 3
            
            remaining = self.player.speed_buff_timer / self.player.buff_duration
            pygame.draw.rect(screen, DARK_GRAY, (bar_x, bar_y, bar_width, bar_height))
            pygame.draw.rect(screen, GREEN, (bar_x, bar_y, int(bar_width * remaining), bar_height))
        
        elif self.player.has_active_debuff():
            # Kırmızı yavaşlık göstergesi
            icon = Assets.load_scaled('assets/game/speed_debuff.png', 0.7)
            screen.blit(icon, (indicator_x, indicator_y))
            
            # Kalan süre çubuğu
            bar_width = icon.get_width()
            bar_height = 6
            bar_x = indicator_x
            bar_y = indicator_y + icon.get_height() + 3
            
            remaining = self.player.speed_debuff_timer / self.player.buff_duration
            pygame.draw.rect(screen, DARK_GRAY, (bar_x, bar_y, bar_width, bar_height))
            pygame.draw.rect(screen, RED, (bar_x, bar_y, int(bar_width * remaining), bar_height))
