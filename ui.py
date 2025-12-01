"""
Bıyık Bey'in Çilesi - Arayüz Bileşenleri
Butonlar ve metin çizim yardımcıları gibi yeniden kullanılabilir UI elemanları
"""

import pygame
from settings import *


def draw_text_centered(screen, text, font_size, color, y_position, shadow=True, shadow_color=BLACK):
    """
    Belirtilen Y konumunda ortalanmış metin çiz (retro gölge efektli)
    
    Parametreler:
        screen: Çizim yapılacak Pygame yüzeyi
        text: Görüntülenecek metin
        font_size: Yazı boyutu
        color: RGB renk değeri
        y_position: Metnin Y koordinatı (merkez)
        shadow: Gölge çizilsin mi
        shadow_color: Gölge rengi
    """
    font = pygame.font.Font(None, font_size)
    
    # Gölge çiz
    if shadow:
        shadow_surface = font.render(text, True, shadow_color)
        shadow_rect = shadow_surface.get_rect(center=(screen.get_width() // 2 + 3, y_position + 3))
        screen.blit(shadow_surface, shadow_rect)
    
    # Ana metni çiz
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=(screen.get_width() // 2, y_position))
    screen.blit(text_surface, text_rect)


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
        
        # Görselleri yükle ve ölçekle
        self.image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(self.image, (width, height))
        
        self.hover_image = pygame.image.load(hover_image_path)
        self.hover_image = pygame.transform.scale(self.hover_image, (width, height))
        
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
        self.volume_levels = VOLUME_LEVELS
        self.current_index = DEFAULT_VOLUME_INDEX
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
        # Normal resimleri yükle
        self.icon_full = pygame.image.load('assets/volume_full.png')
        self.icon_medium = pygame.image.load('assets/volume_medium.png')
        self.icon_mute = pygame.image.load('assets/volume_mute.png')
        
        # Hover resimlerini yükle
        self.icon_full_h = pygame.image.load('assets/volume_full_h.png')
        self.icon_medium_h = pygame.image.load('assets/volume_medium_h.png')
        self.icon_mute_h = pygame.image.load('assets/volume_mute_h.png')
        
        # Hepsini aynı boyuta ölçekle - Normal
        self.icon_full = pygame.transform.scale(self.icon_full, (self.size, self.size))
        self.icon_medium = pygame.transform.scale(self.icon_medium, (self.size, self.size))
        self.icon_mute = pygame.transform.scale(self.icon_mute, (self.size, self.size))
        
        # Hepsini aynı boyuta ölçekle - Hover
        self.icon_full_h = pygame.transform.scale(self.icon_full_h, (self.size, self.size))
        self.icon_medium_h = pygame.transform.scale(self.icon_medium_h, (self.size, self.size))
        self.icon_mute_h = pygame.transform.scale(self.icon_mute_h, (self.size, self.size))
    
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
        """Şu anki ses seviyesini döndür (0.0 - 1.0)"""
        return self.volume_levels[self.current_index]
    
    def cycle_volume(self):
        """Bir sonraki ses seviyesine geç (döngüsel)"""
        self.current_index = (self.current_index + 1) % len(self.volume_levels)
        return self.get_volume()
    
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
                    return self.cycle_volume()
        
        return None
