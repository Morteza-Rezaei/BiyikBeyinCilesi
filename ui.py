"""
Bıyık Bey'in Çilesi - Arayüz Bileşenleri
Butonlar gibi yeniden kullanılabilir UI elemanları
"""

import pygame
from engine import Audio
from settings import *


class ImageButton:
    """Görsel tabanlı buton sınıfı - Normal ve hover görselleri ile"""
    
    def __init__(self, x, y, width, height, image_path, hover_image_path):
        """
        Görsel butonu başlat
        
        Parametreler:
            x: X konumu (sol üst köşe)
            y: Y konumu (sol üst köşe)
            width: Buton genişliği
            height: Buton yüksekliği
            image_path: Normal durum görseli yolu
            hover_image_path: Hover durum görseli yolu
        """
        self.rect = pygame.Rect(x, y, width, height)
        self.is_hovered = False
        
        # Görselleri yükle ve ölçekle (convert_alpha ile performans artışı)
        img = pygame.image.load(image_path).convert_alpha()
        self.image = pygame.transform.scale(img, (width, height))
        
        hover_img = pygame.image.load(hover_image_path).convert_alpha()
        self.hover_image = pygame.transform.scale(hover_img, (width, height))
        
    def draw(self, screen):
        """
        Butonu ekrana çiz
        
        Parametreler:
            screen: Çizim yapılacak Pygame yüzeyi
        """
        current_image = self.hover_image if self.is_hovered else self.image
        screen.blit(current_image, (self.rect.x, self.rect.y))
    
    def handle_event(self, event):
        """
        Buton için fare olaylarını işle
        
        Parametreler:
            event: Pygame olayı
            
        Döndürür:
            Butona tıklandıysa True, değilse False
        """
        if event.type == pygame.MOUSEMOTION:
            self.is_hovered = self.rect.collidepoint(event.pos)
        
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if self.rect.collidepoint(event.pos):
                    # Buton tıklama sesi
                    Audio.play_sound('button_click')
                    return True
        
        return False


class VolumeControl:
    """Sol alt köşede ses seviyesi kontrolü - tıklama ile değişir"""
    
    def __init__(self, screen_width, screen_height):
        """
        Ses kontrolünü başlat
        
        Parametreler:
            screen_width: Ekran genişliği
            screen_height: Ekran yüksekliği
        """
        self.Audio = Audio  # Audio sınıfına referans
        
        self.volume_levels = VOLUME_LEVELS
        self.size = VOLUME_ICON_SIZE
        self.padding = VOLUME_ICON_PADDING
        
        # İkon resimlerini yükle
        self._load_icons()
        
        # Sol alt köşede konumlandır
        self.x = self.padding
        self.y = screen_height - self.size - self.padding
        self.rect = pygame.Rect(self.x, self.y, self.size, self.size)
        
        self.is_hovered = False
    
    def _load_icons(self):
        """İkon resimlerini yükle ve ölçekle (normal ve hover versiyonları)"""
        size = (self.size, self.size)
        
        # Normal resimleri yükle ve ölçekle
        self.icon_full = pygame.transform.scale(
            pygame.image.load('assets/volume_full.png').convert_alpha(), size)
        self.icon_medium = pygame.transform.scale(
            pygame.image.load('assets/volume_medium.png').convert_alpha(), size)
        self.icon_mute = pygame.transform.scale(
            pygame.image.load('assets/volume_mute.png').convert_alpha(), size)
        
        # Hover resimlerini yükle ve ölçekle
        self.icon_full_h = pygame.transform.scale(
            pygame.image.load('assets/volume_full_h.png').convert_alpha(), size)
        self.icon_medium_h = pygame.transform.scale(
            pygame.image.load('assets/volume_medium_h.png').convert_alpha(), size)
        self.icon_mute_h = pygame.transform.scale(
            pygame.image.load('assets/volume_mute_h.png').convert_alpha(), size)
    
    def _get_current_icon(self):
        """Ses seviyesine ve hover durumuna göre uygun ikonu döndür"""
        volume = self.get_volume()
        if volume == 0:
            return self.icon_mute_h if self.is_hovered else self.icon_mute
        elif volume >= 1.0:
            return self.icon_full_h if self.is_hovered else self.icon_full
        else:
            return self.icon_medium_h if self.is_hovered else self.icon_medium
    
    def get_volume(self):
        """Şu anki ses seviyesini döndür (Audio sınıfından al)"""
        return self.Audio.get_volume()
    
    def cycle_volume(self):
        """Bir sonraki ses seviyesine geç (Audio sınıfı üzerinden)"""
        return self.Audio.cycle_volume()
    
    def draw(self, screen):
        """
        Ses kontrolünü ekrana çiz
        
        Parametreler:
            screen: Çizim yapılacak Pygame yüzeyi
        """
        # Uygun ikonu al ve çiz (hover durumuna göre otomatik seçilir)
        current_icon = self._get_current_icon()
        screen.blit(current_icon, (self.x, self.y))
    
    def handle_event(self, event):
        """
        Ses kontrolü için fare olaylarını işle
        
        Parametreler:
            event: Pygame olayı
            
        Döndürür:
            Tıklandıysa yeni ses seviyesi, değilse None
        """
        if event.type == pygame.MOUSEMOTION:
            self.is_hovered = self.rect.collidepoint(event.pos)
        
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Sol tık
                if self.rect.collidepoint(event.pos):
                    Audio.play_sound('button_click')
                    return self.cycle_volume()
        
        return None


# =============================================================================
# PAUSE MENU - Oyun duraklatma menüsü
# =============================================================================

class PauseMenu:
    """ESC ile açılan pause menüsü - Ses kontrolü, Devam ve Çık butonları"""
    
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.is_open = False
        
        # Overlay (karartma)
        self.overlay = pygame.Surface((screen_width, screen_height))
        self.overlay.fill((0, 0, 0))
        self.overlay.set_alpha(180)
        
        # Buton boyutları
        btn_width = int(screen_width * 0.2)
        btn_height = int(screen_height * 0.08)
        center_x = screen_width // 2
        center_y = screen_height // 2
        
        # Continue butonu
        self.continue_btn = ImageButton(
            center_x - btn_width // 2,
            center_y - btn_height - 20,
            btn_width, btn_height,
            'assets/button_continue.png',
            'assets/button_continue_h.png'
        )
        
        # Quit butonu
        self.quit_btn = ImageButton(
            center_x - btn_width // 2,
            center_y + 20,
            btn_width, btn_height,
            'assets/button_quit.png',
            'assets/button_quit_h.png'
        )
        
        # Ses kontrolü (ekranın ortasında, butonların üstünde)
        self.volume = VolumeControl(screen_width, screen_height)
        # Ses kontrolünü ortaya taşı
        vol_size = VOLUME_ICON_SIZE
        self.volume.x = center_x - vol_size // 2
        self.volume.y = center_y - btn_height - 60 - vol_size
        self.volume.rect = pygame.Rect(self.volume.x, self.volume.y, vol_size, vol_size)
    
    def open(self):
        """Menüyü aç"""
        self.is_open = True
    
    def close(self):
        """Menüyü kapat"""
        self.is_open = False
    
    def handle_event(self, event):
        """
        Olayları işle
        
        Döndürür:
            'continue' - Devam butonuna tıklandı veya ESC
            'quit' - Çık butonuna tıklandı
            None - Hiçbir şey olmadı
        """
        if not self.is_open:
            return None
        
        # ESC ile kapat
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self.close()
            return 'continue'
        
        # Ses kontrolü (Audio.cycle_volume zaten müzik sesini ayarlıyor)
        self.volume.handle_event(event)
        
        # Continue butonu
        if self.continue_btn.handle_event(event):
            self.close()
            return 'continue'
        
        # Quit butonu
        if self.quit_btn.handle_event(event):
            return 'quit'
        
        return None
    
    def draw(self, screen):
        """Menüyü çiz"""
        if not self.is_open:
            return
        
        # Karartma overlay
        screen.blit(self.overlay, (0, 0))
        
        # Ses kontrolü
        self.volume.draw(screen)
        
        # Butonlar
        self.continue_btn.draw(screen)
        self.quit_btn.draw(screen)


# =============================================================================
# HINT BUTTON - Oyun içi yardım butonu
# =============================================================================

class HintButton:
    """Oyun ekranında sağ üst köşede hint butonu"""
    
    def __init__(self, screen_width, screen_height):
        # İkonu yükle - orijinal oranı koru
        icon_original = pygame.image.load('assets/hint/hint_button.png').convert_alpha()
        
        # Yüksekliğe göre ölçekle, oranı koru
        target_height = HINT_BUTTON_SIZE
        original_w = icon_original.get_width()
        original_h = icon_original.get_height()
        ratio = original_w / original_h
        target_width = int(target_height * ratio)
        
        # Normal ve hover görsellerini önceden oluştur (cache)
        self.icon = pygame.transform.smoothscale(icon_original, (target_width, target_height))
        self.icon_hover = pygame.transform.smoothscale(icon_original, (target_width + 10, target_height + 10))
        
        self.width = target_width
        self.height = target_height
        
        # Sağ üst köşede konumlandır
        self.x = screen_width - self.width - HINT_BUTTON_PADDING_RIGHT
        self.y = HINT_BUTTON_PADDING_TOP
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        
        self.is_hovered = False
    
    def draw(self, screen):
        """Hint butonunu çiz"""
        if self.is_hovered:
            screen.blit(self.icon_hover, (self.x - 5, self.y - 5))
        else:
            screen.blit(self.icon, (self.x, self.y))
    
    def handle_event(self, event):
        """Fare olaylarını işle"""
        if event.type == pygame.MOUSEMOTION:
            self.is_hovered = self.rect.collidepoint(event.pos)
        
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if self.rect.collidepoint(event.pos):
                    # Buton tıklama sesi
                    Audio.play_sound('button_click')
                    return True
        
        return False


# =============================================================================
# HINT POPUP - Hint kartları popup'ı
# =============================================================================

class HintPopup:
    """Hint kartlarını gösteren popup"""
    
    HINTS = [
        {'image': 'hint_wasd.png', 'title': 'KONTROLLER', 'subtitle': 'WASD tuşları ile hareket et'},
        {'image': 'hint_cay.png', 'title': 'ÇAY', 'subtitle': 'Topla ve +1 can kazan!'},
        {'image': 'hint_sinsi_jilet.png', 'title': 'SİNSİ JİLET', 'subtitle': 'Yavaşça yaklaşır, sonra SALDIRI!'},
        {'image': 'hint_ucan_terlik.png', 'title': 'UÇAN TERLİK', 'subtitle': 'Annenin gazabı! Kaç!'},
        {'image': 'hint_speed_buff.png', 'title': 'HIZ ARTIŞ', 'subtitle': 'Topla ve daha hızlı ol!'},
        {'image': 'hint_speed_debuff.png', 'title': 'HIZ AZALIŞ', 'subtitle': 'Dikkat! Yavaşlatır!'},
    ]
    
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.is_open = False
        self.current_index = 0
        
        # Overlay'i önceden oluştur (performans için cache)
        self.overlay = pygame.Surface((screen_width, screen_height))
        self.overlay.fill((0, 0, 0))
        self.overlay.set_alpha(180)
        
        # Hint kartlarını yükle
        self.hint_images = []
        for hint in self.HINTS:
            img = pygame.image.load(f'assets/hint/{hint["image"]}')
            # Kartı ekrana sığacak şekilde ölçekle
            card_height = int(screen_height * HINT_CARD_HEIGHT_RATIO)
            ratio = img.get_width() / img.get_height()
            card_width = int(card_height * ratio)
            img = pygame.transform.scale(img, (card_width, card_height))
            self.hint_images.append(img)
        
        # Butonları yükle - orijinal oranlarını koru
        target_height = HINT_POPUP_BTN_SIZE
        
        # Next butonu - normal ve hover cache
        btn_next_original = pygame.image.load('assets/hint/button_hint_next.png').convert_alpha()
        next_ratio = btn_next_original.get_width() / btn_next_original.get_height()
        self.btn_next_width = int(target_height * next_ratio)
        self.btn_next_height = target_height
        self.btn_next = pygame.transform.smoothscale(btn_next_original, (self.btn_next_width, self.btn_next_height))
        self.btn_next_hover = pygame.transform.smoothscale(btn_next_original, (self.btn_next_width + 10, self.btn_next_height + 10))
        
        # Close butonu - normal ve hover cache
        btn_close_original = pygame.image.load('assets/hint/button_close.png').convert_alpha()
        close_ratio = btn_close_original.get_width() / btn_close_original.get_height()
        self.btn_close_width = int(target_height * close_ratio)
        self.btn_close_height = target_height
        self.btn_close = pygame.transform.smoothscale(btn_close_original, (self.btn_close_width, self.btn_close_height))
        self.btn_close_hover = pygame.transform.smoothscale(btn_close_original, (self.btn_close_width + 10, self.btn_close_height + 10))
        
        # Hover durumları
        self.next_hovered = False
        self.close_hovered = False
        
        # Font cache (her frame oluşturmamak için)
        self.page_font = pygame.font.Font(None, 36)
        
        self._calculate_positions()
    
    def _calculate_positions(self):
        """Kart ve buton pozisyonlarını hesapla"""
        if len(self.hint_images) > 0:
            card = self.hint_images[0]
            self.card_x = (self.screen_width - card.get_width()) // 2
            self.card_y = (self.screen_height - card.get_height()) // 2
            
            # Butonlar kartın altında - alt alta
            center_x = self.screen_width // 2
            gap = 20  # Butonlar arası dikey mesafe
            
            # Next butonu (üstte)
            btn_y = self.card_y + card.get_height() + 30
            self.next_rect = pygame.Rect(
                center_x - self.btn_next_width // 2, 
                btn_y, 
                self.btn_next_width, 
                self.btn_next_height
            )
            
            # Close butonu (altta)
            self.close_rect = pygame.Rect(
                center_x - self.btn_close_width // 2, 
                btn_y + self.btn_next_height + gap, 
                self.btn_close_width, 
                self.btn_close_height
            )
    
    def open(self):
        """Popup'ı aç"""
        self.is_open = True
        self.current_index = 0
    
    def close(self):
        """Popup'ı kapat"""
        self.is_open = False
    
    def next_hint(self):
        """Sonraki hint'e geç"""
        self.current_index = (self.current_index + 1) % len(self.HINTS)
    
    def draw(self, screen):
        """Popup'ı çiz"""
        if not self.is_open:
            return
        
        # Karartma overlay (cache'lenmiş)
        screen.blit(self.overlay, (0, 0))
        
        # Mevcut hint kartı
        if self.current_index < len(self.hint_images):
            card = self.hint_images[self.current_index]
            card_x = (self.screen_width - card.get_width()) // 2
            card_y = (self.screen_height - card.get_height()) // 2
            screen.blit(card, (card_x, card_y))
        
        # Close butonu (cache'lenmiş hover)
        if self.close_hovered:
            screen.blit(self.btn_close_hover, (self.close_rect.x - 5, self.close_rect.y - 5))
        else:
            screen.blit(self.btn_close, (self.close_rect.x, self.close_rect.y))
        
        # Next butonu (cache'lenmiş hover)
        if self.next_hovered:
            screen.blit(self.btn_next_hover, (self.next_rect.x - 5, self.next_rect.y - 5))
        else:
            screen.blit(self.btn_next, (self.next_rect.x, self.next_rect.y))
        
        # Sayfa göstergesi (cache'lenmiş font)
        page_text = f"{self.current_index + 1} / {len(self.HINTS)}"
        text_surf = self.page_font.render(page_text, True, WHITE)
        text_x = (self.screen_width - text_surf.get_width()) // 2
        text_y = self.close_rect.y + self.btn_close_height + 20
        screen.blit(text_surf, (text_x, text_y))
    
    def handle_event(self, event):
        """
        Fare olaylarını işle
        
        Döndürür:
            'next' - Sonraki butonuna tıklandı
            'close' - Kapat butonuna tıklandı
            None - Hiçbir şey olmadı
        """
        if not self.is_open:
            return None
        
        if event.type == pygame.MOUSEMOTION:
            self.next_hovered = self.next_rect.collidepoint(event.pos)
            self.close_hovered = self.close_rect.collidepoint(event.pos)
        
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if self.next_rect.collidepoint(event.pos):
                    Audio.play_sound('button_click')
                    self.next_hint()
                    return 'next'
                elif self.close_rect.collidepoint(event.pos):
                    Audio.play_sound('button_click')
                    self.close()
                    return 'close'
        
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                Audio.play_sound('button_click')
                self.close()
                return 'close'
            elif event.key in (pygame.K_SPACE, pygame.K_RETURN, pygame.K_RIGHT):
                Audio.play_sound('button_click')
                self.next_hint()
                return 'next'
        
        return None


# =============================================================================
# LEVEL SELECTOR - Level Seçim Dialogu
# =============================================================================

class LevelSelector:
    """Level seçim popup'ı - Hangi leveldan başlanacağını seç"""
    
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.is_open = False
        
        # Level girişi
        self.level_input = ""
        self.input_rect = pygame.Rect(0, 0, 200, 50)
        self.input_rect.center = (screen_width // 2, screen_height // 2 - 50)
        
        # Butonlar
        btn_width = 150
        btn_height = 50
        btn_y = screen_height // 2 + 50
        
        self.ok_rect = pygame.Rect(screen_width // 2 - 160, btn_y, btn_width, btn_height)
        self.cancel_rect = pygame.Rect(screen_width // 2 + 10, btn_y, btn_width, btn_height)
        
        self.ok_hovered = False
        self.cancel_hovered = False
        
        # Font
        self.font = pygame.font.Font(None, 36)
        self.label_font = pygame.font.Font(None, 28)
    
    def open(self, current_level=1):
        """Dialog'u aç"""
        self.is_open = True
        self.level_input = ""  # Boş başlat
    
    def close(self):
        """Dialog'u kapat"""
        self.is_open = False
        self.level_input = ""
    
    def draw(self, screen):
        """Dialog'u çiz"""
        if not self.is_open:
            return
        
        # Karanlık overlay
        overlay = pygame.Surface((self.screen_width, self.screen_height))
        overlay.fill((0, 0, 0))
        overlay.set_alpha(150)
        screen.blit(overlay, (0, 0))
        
        # Dialog kutusu
        dialog_width = 400
        dialog_height = 280
        dialog_rect = pygame.Rect(0, 0, dialog_width, dialog_height)
        dialog_rect.center = (self.screen_width // 2, self.screen_height // 2)
        
        pygame.draw.rect(screen, (50, 50, 50), dialog_rect)
        pygame.draw.rect(screen, (200, 200, 200), dialog_rect, 3)
        
        # Başlık
        title = self.label_font.render("Hangi leveldan başlayalım?", True, WHITE)
        title_rect = title.get_rect(center=(self.screen_width // 2, dialog_rect.top + 30))
        screen.blit(title, title_rect)
        
        # Input kutusu
        pygame.draw.rect(screen, WHITE, self.input_rect)
        pygame.draw.rect(screen, (0, 0, 0), self.input_rect, 2)
        
        # Boş olduğunda boş göster, değilse girilen değeri göster
        input_text = self.font.render(self.level_input, True, BLACK)
        screen.blit(input_text, (self.input_rect.x + 10, self.input_rect.y + 8))
        
        # OK butonu
        btn_color = (100, 200, 100) if self.ok_hovered else (70, 170, 70)
        pygame.draw.rect(screen, btn_color, self.ok_rect)
        pygame.draw.rect(screen, WHITE, self.ok_rect, 2)
        ok_text = self.label_font.render("BAŞLA", True, WHITE)
        ok_text_rect = ok_text.get_rect(center=self.ok_rect.center)
        screen.blit(ok_text, ok_text_rect)
        
        # Cancel butonu
        btn_color = (200, 100, 100) if self.cancel_hovered else (170, 70, 70)
        pygame.draw.rect(screen, btn_color, self.cancel_rect)
        pygame.draw.rect(screen, WHITE, self.cancel_rect, 2)
        cancel_text = self.label_font.render("İPTAL", True, WHITE)
        cancel_text_rect = cancel_text.get_rect(center=self.cancel_rect.center)
        screen.blit(cancel_text, cancel_text_rect)
    
    def handle_event(self, event):
        """
        Olayları işle
        
        Döndürür:
            ('start', level) - Girilen levelle oyunu başlat
            'cancel' - Dialog'u kapat
            None - Hiçbir şey olmadı
        """
        if not self.is_open:
            return None
        
        if event.type == pygame.MOUSEMOTION:
            self.ok_hovered = self.ok_rect.collidepoint(event.pos)
            self.cancel_hovered = self.cancel_rect.collidepoint(event.pos)
        
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if self.ok_rect.collidepoint(event.pos):
                    # Boş olduğunda başlatma
                    if not self.level_input:
                        return None
                    Audio.play_sound('button_click')
                    try:
                        level = int(self.level_input)
                        if level < 1:
                            level = 1
                        self.close()
                        return ('start', level)
                    except ValueError:
                        self.level_input = ""  # Geçersiz input, temizle
                elif self.cancel_rect.collidepoint(event.pos):
                    Audio.play_sound('button_click')
                    self.close()
                    return 'cancel'
        
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                Audio.play_sound('button_click')
                self.close()
                return 'cancel'
            elif event.key == pygame.K_RETURN:
                # Boş olduğunda başlatma
                if not self.level_input:
                    return None
                Audio.play_sound('button_click')
                try:
                    level = int(self.level_input)
                    if level < 1:
                        level = 1
                    self.close()
                    return ('start', level)
                except ValueError:
                    self.level_input = ""
            elif event.key == pygame.K_BACKSPACE:
                self.level_input = self.level_input[:-1]
            elif event.unicode.isdigit() and len(self.level_input) < 4:
                # Max 4 digit (9999)
                self.level_input += event.unicode
        
        return None
