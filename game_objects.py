"""
Bıyık Bey'in Çilesi - Oyun Nesneleri
Çay, Bomba, Jilet, Terlik ve diğer oyun elementleri
"""

import pygame
import random
import math
from engine import Assets
from settings import *


class GameObject(pygame.sprite.Sprite):
    """Tüm oyun nesneleri için temel sınıf"""
    
    def __init__(self, x, y):
        super().__init__()
        self.spawn_time = pygame.time.get_ticks()
    
    def update(self, screen_w, screen_h, player_rect):
        pass


# =============================================================================
# ÇAY - Can veren nesne
# =============================================================================

class Tea(GameObject):
    """Çay bardağı - Toplandığında +1 can verir"""
    
    def __init__(self, x, y, scale=1.0):
        super().__init__(x, y)
        self.image = Assets.load_scaled('assets/game/tea.png', scale)
        self.rect = self.image.get_rect(center=(x, y))
        
        # Hafif sallanma animasyonu için
        self.base_y = y
        self.float_offset = random.uniform(0, math.pi * 2)
        self.float_speed = 2.0
        self.float_amplitude = 5
    
    def update(self, screen_w, screen_h, player_rect):
        """Hafif yukarı aşağı sallanma"""
        elapsed = pygame.time.get_ticks() / 1000.0
        offset = math.sin(elapsed * self.float_speed + self.float_offset) * self.float_amplitude
        self.rect.centery = self.base_y + offset
    
    def draw(self, screen):
        screen.blit(self.image, self.rect)


# =============================================================================
# BOMBA - Patlayan tehlikeli nesne
# =============================================================================

class Bomb(GameObject):
    """Bomba - Belirli süre sonra patlar ve yakındaki oyuncuya hasar verir"""
    
    def __init__(self, x, y, scale=0.8):
        super().__init__(x, y)
        
        # Bomba animasyon kareleri (tick tick tick...)
        self.tick_frames = [
            Assets.load_scaled(f'assets/game/bomb_tick_{i}.png', scale)
            for i in range(1, 8)
        ]
        
        # Patlama animasyon kareleri
        self.explosion_frames = [
            Assets.load_scaled(f'assets/game/explosion_{i}.png', scale * 2)
            for i in range(1, 6)
        ]
        
        self.image = self.tick_frames[0]
        self.rect = self.image.get_rect(center=(x, y))
        
        # Durum
        self.is_exploding = False
        self.exploded = False  # Patlama tamamlandı mı
        self.has_dealt_damage = False  # Hasar verildi mi
        
        # Zamanlama
        self.fuse_time = BOMB_FUSE_TIME  # Patlamaya kadar süre (ms)
        self.frame_index = 0
        self.anim_speed = 0.15
        
        # Patlama yarıçapı
        self.explosion_radius = BOMB_EXPLOSION_RADIUS
    
    def update(self, screen_w, screen_h, player_rect):
        """Bomba güncelleme - tick veya patlama animasyonu"""
        elapsed = pygame.time.get_ticks() - self.spawn_time
        
        if not self.is_exploding:
            # Tick animasyonu - giderek hızlanır
            progress = min(elapsed / self.fuse_time, 1.0)
            speed = 0.1 + progress * 0.4  # Hızlanarak tick
            
            self.frame_index += speed
            if self.frame_index >= len(self.tick_frames):
                self.frame_index = 0
            
            self.image = self.tick_frames[int(self.frame_index)]
            
            # Patlama zamanı geldi mi?
            if elapsed >= self.fuse_time:
                self.is_exploding = True
                self.frame_index = 0
                # Patlama için rect'i büyüt
                center = self.rect.center
                self.image = self.explosion_frames[0]
                self.rect = self.image.get_rect(center=center)
        else:
            # Patlama animasyonu
            self.frame_index += 0.2
            if self.frame_index >= len(self.explosion_frames):
                self.exploded = True
                return
            
            self.image = self.explosion_frames[int(self.frame_index)]
    
    def check_explosion_hit(self, player_rect):
        """Patlama oyuncuya isabet etti mi?"""
        if not self.is_exploding or self.has_dealt_damage:
            return False
        
        # Patlama merkezinden oyuncuya mesafe
        bomb_center = pygame.math.Vector2(self.rect.center)
        player_center = pygame.math.Vector2(player_rect.center)
        distance = bomb_center.distance_to(player_center)
        
        if distance <= self.explosion_radius:
            self.has_dealt_damage = True
            return True
        return False
    
    def draw(self, screen):
        screen.blit(self.image, self.rect)


# =============================================================================
# SİNSİ JİLET - Hareketli düşman (Sinsi hareket)
# =============================================================================

class SinsiJilet(GameObject):
    """Sinsi Jilet - Yavaşça oyuncuya yaklaşır, sonra aniden saldırır"""
    
    def __init__(self, x, y, scale=0.7):
        super().__init__(x, y)
        
        # Animasyon kareleri (8 kare)
        self.frames = [
            Assets.load_scaled(f'assets/game/sinsi_jilet_{i}.png', scale)
            for i in range(1, 9)
        ]
        
        self.image = self.frames[0]
        self.rect = self.image.get_rect(center=(x, y))
        
        # Hareket
        self.speed_sneak = JILET_SNEAK_SPEED  # Sinsi yürüme hızı
        self.speed_attack = JILET_ATTACK_SPEED  # Saldırı hızı
        self.current_speed = self.speed_sneak
        
        # Durum
        self.state = 'sneaking'  # 'sneaking' veya 'attacking'
        self.attack_distance = JILET_ATTACK_DISTANCE  # Bu mesafede saldırıya geç
        self.direction = pygame.math.Vector2(0, 0)
        
        # Animasyon
        self.frame_index = 0
        self.anim_speed = 0.05  # Yavaş animasyon
        
        # Titreme efekti (sinsi modda)
        self.shake_offset = 0
        self.shake_timer = 0
    
    def update(self, screen_w, screen_h, player_rect):
        """Jilet güncelleme - Oyuncuya doğru sinsi hareket"""
        # Oyuncuya doğru yön hesapla
        my_pos = pygame.math.Vector2(self.rect.center)
        player_pos = pygame.math.Vector2(player_rect.center)
        
        to_player = player_pos - my_pos
        distance = to_player.length()
        
        if distance > 0:
            self.direction = to_player.normalize()
        
        # Duruma göre davran
        if self.state == 'sneaking':
            # Yavaşça yaklaş, hafif titreme
            self.shake_timer += 0.3
            self.shake_offset = math.sin(self.shake_timer) * 2
            
            # Belirli mesafede saldırıya geç
            if distance < self.attack_distance:
                self.state = 'attacking'
                self.anim_speed = 0.15  # Saldırıda biraz daha hızlı
            
            self.current_speed = self.speed_sneak
        else:
            # SALDIRI! Hızlıca oyuncuya doğru
            self.current_speed = self.speed_attack
            self.shake_offset = 0
        
        # Hareket
        self.rect.x += self.direction.x * self.current_speed + self.shake_offset
        self.rect.y += self.direction.y * self.current_speed
        
        # Animasyon
        self.frame_index += self.anim_speed
        if self.frame_index >= len(self.frames):
            self.frame_index = 0
        self.image = self.frames[int(self.frame_index)]
        
        # Ekran sınırları (biraz dışarı çıkabilir)
        margin = 50
        self.rect.left = max(-margin, self.rect.left)
        self.rect.right = min(screen_w + margin, self.rect.right)
        self.rect.top = max(-margin, self.rect.top)
        self.rect.bottom = min(screen_h + margin, self.rect.bottom)
    
    def draw(self, screen):
        screen.blit(self.image, self.rect)


# =============================================================================
# UÇAN TERLİK - Hareketli düşman (Fırlatma hareketi)
# =============================================================================

class UcanTerlik(GameObject):
    """Uçan Terlik - Ekranın kenarından fırlatılır, düz çizgide gider"""
    
    def __init__(self, screen_w, screen_h, target_pos, scale=0.7):
        # Rastgele kenardan başla
        edge = random.choice(['top', 'bottom', 'left', 'right'])
        
        if edge == 'top':
            x = random.randint(50, screen_w - 50)
            y = -50
        elif edge == 'bottom':
            x = random.randint(50, screen_w - 50)
            y = screen_h + 50
        elif edge == 'left':
            x = -50
            y = random.randint(50, screen_h - 50)
        else:  # right
            x = screen_w + 50
            y = random.randint(50, screen_h - 50)
        
        super().__init__(x, y)
        
        # Animasyon kareleri (dönen terlik - 8 kare)
        self.frames = [
            Assets.load_scaled(f'assets/game/ucan_terlik_{i}.png', scale)
            for i in range(1, 9)
        ]
        
        self.image = self.frames[0]
        self.rect = self.image.get_rect(center=(x, y))
        
        # Hedef yönünü hesapla (oyuncuya doğru)
        my_pos = pygame.math.Vector2(x, y)
        target = pygame.math.Vector2(target_pos)
        
        direction = target - my_pos
        if direction.length() > 0:
            self.direction = direction.normalize()
        else:
            self.direction = pygame.math.Vector2(1, 0)
        
        # Hız ve hareket
        self.speed = TERLIK_SPEED
        
        # Animasyon (dönme efekti)
        self.frame_index = 0
        self.rotation_speed = 0.12  # Yavaş dönme - daha görünür
        
        # Ekran dışına çıkınca silinecek
        self.screen_w = screen_w
        self.screen_h = screen_h
    
    def update(self, screen_w, screen_h, player_rect):
        """Terlik güncelleme - Düz çizgide uç"""
        # Hareket
        self.rect.x += self.direction.x * self.speed
        self.rect.y += self.direction.y * self.speed
        
        # Dönerek animasyon
        self.frame_index += self.rotation_speed
        if self.frame_index >= len(self.frames):
            self.frame_index = 0
        self.image = self.frames[int(self.frame_index)]
    
    def is_off_screen(self):
        """Ekran dışında mı?"""
        margin = 100
        return (self.rect.right < -margin or 
                self.rect.left > self.screen_w + margin or
                self.rect.bottom < -margin or 
                self.rect.top > self.screen_h + margin)
    
    def draw(self, screen):
        screen.blit(self.image, self.rect)


# =============================================================================
# HEALTH UI - Can Göstergesi
# =============================================================================

class HealthUI:
    """Ekranda can göstergesi - Kalp ikonları"""
    
    def __init__(self, screen_w, screen_h, max_health=5):
        self.max_health = max_health
        self.current_health = max_health
        
        # Kalp ikonları
        heart_scale = 1.0
        self.heart_full = Assets.load_scaled('assets/game/heart.png', heart_scale)
        self.heart_empty = Assets.load_scaled('assets/game/heart_broken.png', heart_scale)
        
        # Pozisyon (sol üst köşe)
        self.padding = 20
        self.spacing = 10
        self.start_x = self.padding
        self.start_y = self.padding
        
        # Hasar animasyonu
        self.shake_timer = 0
        self.is_shaking = False
    
    def set_health(self, health):
        """Can güncelle"""
        old_health = self.current_health
        self.current_health = max(0, min(health, self.max_health))
        
        # Hasar aldıysa titreme efekti
        if self.current_health < old_health:
            self.is_shaking = True
            self.shake_timer = 10
    
    def update(self):
        """Animasyonları güncelle"""
        if self.is_shaking:
            self.shake_timer -= 1
            if self.shake_timer <= 0:
                self.is_shaking = False
    
    def draw(self, screen):
        """Kalpleri çiz"""
        x = self.start_x
        y = self.start_y
        
        # Titreme efekti
        if self.is_shaking:
            y += random.randint(-3, 3)
        
        heart_w = self.heart_full.get_width()
        
        for i in range(self.max_health):
            if i < self.current_health:
                screen.blit(self.heart_full, (x, y))
            else:
                screen.blit(self.heart_empty, (x, y))
            x += heart_w + self.spacing


# =============================================================================
# SPAWN MANAGER - Nesne Oluşturucu
# =============================================================================

class SpawnManager:
    """Oyun nesnelerini zamanla oluşturur"""
    
    def __init__(self, screen_w, screen_h):
        self.screen_w = screen_w
        self.screen_h = screen_h
        
        # Spawn zamanlayıcıları
        self.tea_timer = 0
        self.bomb_timer = 0
        self.jilet_timer = 0
        self.terlik_timer = 0
        
        # Zorluk artışı
        self.difficulty = 1.0
        self.difficulty_timer = 0
    
    def update(self, dt, teas, bombs, jilets, terliks, player_rect):
        """Spawn zamanlayıcılarını güncelle ve nesneler oluştur"""
        # Zorluk zamanla artar
        self.difficulty_timer += dt
        if self.difficulty_timer >= 10:  # Her 10 saniyede zorluk artar
            self.difficulty_timer = 0
            self.difficulty = min(self.difficulty + 0.1, 2.0)
        
        # Çay spawn
        self.tea_timer += dt
        if self.tea_timer >= TEA_SPAWN_TIME:
            self.tea_timer = 0
            if len(teas) < TEA_MAX_COUNT:
                self._spawn_tea(teas)
        
        # Bomba spawn
        self.bomb_timer += dt
        if self.bomb_timer >= BOMB_SPAWN_TIME / self.difficulty:
            self.bomb_timer = 0
            if len(bombs) < BOMB_MAX_COUNT:
                self._spawn_bomb(bombs, player_rect)
        
        # Jilet spawn
        self.jilet_timer += dt
        if self.jilet_timer >= JILET_SPAWN_TIME / self.difficulty:
            self.jilet_timer = 0
            if len(jilets) < JILET_MAX_COUNT:
                self._spawn_jilet(jilets, player_rect)
        
        # Terlik spawn
        self.terlik_timer += dt
        if self.terlik_timer >= TERLIK_SPAWN_TIME / self.difficulty:
            self.terlik_timer = 0
            if len(terliks) < TERLIK_MAX_COUNT:
                self._spawn_terlik(terliks, player_rect)
    
    def _spawn_tea(self, teas):
        """Çay oluştur - Rastgele konumda"""
        margin = 100
        x = random.randint(margin, self.screen_w - margin)
        y = random.randint(margin, self.screen_h - margin)
        teas.add(Tea(x, y, TEA_SCALE))
    
    def _spawn_bomb(self, bombs, player_rect):
        """Bomba oluştur - Oyuncudan uzakta"""
        margin = 100
        min_distance = 200
        
        for _ in range(10):  # 10 deneme
            x = random.randint(margin, self.screen_w - margin)
            y = random.randint(margin, self.screen_h - margin)
            
            # Oyuncudan uzakta mı?
            dist = pygame.math.Vector2(x - player_rect.centerx, 
                                       y - player_rect.centery).length()
            if dist >= min_distance:
                bombs.add(Bomb(x, y, BOMB_SCALE))
                return
        
        # Uygun yer bulunamadıysa yine de oluştur
        bombs.add(Bomb(x, y, BOMB_SCALE))
    
    def _spawn_jilet(self, jilets, player_rect):
        """Jilet oluştur - Ekran kenarından"""
        edge = random.choice(['top', 'bottom', 'left', 'right'])
        margin = 50
        
        if edge == 'top':
            x = random.randint(margin, self.screen_w - margin)
            y = -30
        elif edge == 'bottom':
            x = random.randint(margin, self.screen_w - margin)
            y = self.screen_h + 30
        elif edge == 'left':
            x = -30
            y = random.randint(margin, self.screen_h - margin)
        else:
            x = self.screen_w + 30
            y = random.randint(margin, self.screen_h - margin)
        
        jilets.add(SinsiJilet(x, y, JILET_SCALE))
    
    def _spawn_terlik(self, terliks, player_rect):
        """Terlik oluştur - Oyuncuya doğru fırlat"""
        terliks.add(UcanTerlik(
            self.screen_w, 
            self.screen_h, 
            player_rect.center,
            TERLIK_SCALE
        ))
