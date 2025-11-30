"""
Bıyık Bey'in Çilesi - Arayüz Bileşenleri
Butonlar ve metin çizim yardımcıları gibi yeniden kullanılabilir UI elemanları
"""

import pygame
from settings import *


class Button:
    """Hover efektli ve tıklama algılamalı buton sınıfı - Retro Piksel Tarzı"""
    
    def __init__(self, x, y, width, height, text, font_size=BUTTON_FONT_SIZE):
        """
        Butonu başlat
        
        Parametreler:
            x: X konumu (sol üst köşe)
            y: Y konumu (sol üst köşe)
            width: Buton genişliği
            height: Buton yüksekliği
            text: Buton metni
            font_size: Yazı boyutu
        """
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.font = pygame.font.Font(None, font_size)
        self.is_hovered = False
        
    def draw(self, screen):
        """
        Butonu ekrana retro piksel sanat tarzında çiz
        
        Parametreler:
            screen: Çizim yapılacak Pygame yüzeyi
        """
        # Fare üzerindeyse rengi değiştir
        color = BUTTON_HOVER_COLOR if self.is_hovered else BUTTON_COLOR
        
        # Basılı efekti için Y ekseninde kayma
        offset_y = 2 if self.is_hovered else 0
        draw_rect = self.rect.copy()
        draw_rect.y += offset_y
        
        # Gölge çiz
        shadow_rect = draw_rect.copy()
        shadow_rect.x += 4
        shadow_rect.y += 4
        pygame.draw.rect(screen, (0, 0, 0, 100), shadow_rect)
        
        # Ana buton gövdesini çiz
        pygame.draw.rect(screen, color, draw_rect)
        
        # Piksel sanat hissi için çift kenarlık
        pygame.draw.rect(screen, CYAN, draw_rect, 3)
        inner_border = draw_rect.inflate(-8, -8)
        pygame.draw.rect(screen, WHITE, inner_border, 1)
        
        # Metin gölgesi çiz
        text_shadow = self.font.render(self.text, True, BLACK)
        shadow_rect = text_shadow.get_rect(center=(draw_rect.centerx + 2, draw_rect.centery + 2))
        screen.blit(text_shadow, shadow_rect)
        
        # Ana metni çiz
        text_color = WHITE if self.is_hovered else BUTTON_TEXT_COLOR
        text_surface = self.font.render(self.text, True, text_color)
        text_rect = text_surface.get_rect(center=draw_rect.center)
        screen.blit(text_surface, text_rect)
    
    def handle_event(self, event):
        """
        Buton için fare olaylarını işle
        
        Parametreler:
            event: Pygame olayı
            
        Döndürür:
            Butona tıklandıysa True, değilse False
        """
        if event.type == pygame.MOUSEMOTION:
            # Fare butonun üzerinde mi kontrol et
            self.is_hovered = self.rect.collidepoint(event.pos)
        
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # Sol tıklama kontrolü
            if event.button == 1:
                if self.rect.collidepoint(event.pos):
                    return True
        
        return False


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
