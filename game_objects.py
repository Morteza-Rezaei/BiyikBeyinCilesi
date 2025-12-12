"""
Bıyık Bey'in Çilesi - Oyun Nesneleri
Çay, Bomba, Jilet, Terlik ve diğer oyun elementleri
"""

import pygame
import random
import math
from engine import Assets, Audio
from settings import *


class GameObject(pygame.sprite.Sprite):
    """Tüm oyun nesneleri için temel sınıf"""
    
    def __init__(self, x, y):
        super().__init__()
        self.spawn_time = pygame.time.get_ticks()
    
    def update(self, screen_w, screen_h, player_rect):
        pass


# =============================================================================
# ÇAY - Can veren nesne (Buff olarak)
# =============================================================================

class Tea(GameObject):
    """Çay bardağı - Toplandığında +1 can verir"""
    
    def __init__(self, x, y, scale=1.0):
        super().__init__(x, y)
        self.image = Assets.load_scaled('assets/game/tea.png', scale)
        self.rect = self.image.get_rect(center=(x, y))
        
        # Konum
        self.base_x = x
        self.base_y = y
        
        # Yaşam süresi
        self.lifetime = BUFF_LIFETIME
        self.age = 0
        
        # Animasyon
        self.float_offset = random.uniform(0, math.pi * 2)
        self.float_speed = 2.0
        self.float_amplitude = 5
        self.pulse_timer = 0
        self.visible = True
    
    def update(self, screen_w, screen_h, player_rect, dt):
        """Güncelle - Süzülme ve kaybolma animasyonu"""
        self.age += dt
        
        # Süre doldu mu?
        if self.age >= self.lifetime:
            return False  # Silinmeli
        
        # Yukarı aşağı süzülme
        elapsed = pygame.time.get_ticks() / 1000.0
        offset = math.sin(elapsed * self.float_speed + self.float_offset) * self.float_amplitude
        self.rect.centery = self.base_y + offset
        
        # Son 2 saniyede yanıp sönme
        if self.age >= self.lifetime - 2:
            self.pulse_timer += dt * 10
            self.visible = int(self.pulse_timer) % 2 == 0
        else:
            self.visible = True
        
        return True  # Hala yaşıyor
    
    def draw(self, screen):
        if self.visible:
            screen.blit(self.image, self.rect)


# =============================================================================
# BOMBA - Patlayan tehlikeli nesne
# =============================================================================

class Bomb(GameObject):
    """Bomba - Belirli süre sonra patlar ve yakındaki oyuncuya hasar verir"""
    
    def __init__(self, x, y, scale=0.8, fuse_time=None):
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
        self.explosion_sound_played = False  # Patlama sesi çalındı mı
        
        # Zamanlama
        self.fuse_time = fuse_time if fuse_time is not None else BOMB_FUSE_TIME  # Patlamaya kadar süre (ms)
        self.frame_index = 0
        self.anim_speed = 0.15
        
        # Patlama yarıçapı - patlama görselinin boyutuna göre dinamik hesapla
        # Patlama görseli bomba görselinden 2 kat daha büyük (scale * 2)
        # Patlama görselinin genişliği ve yüksekliğinin ortalamasının yarısı = yarıçap
        explosion_width = self.explosion_frames[0].get_width()
        explosion_height = self.explosion_frames[0].get_height()
        # Patlama görseli genellikle yuvarlak olduğu için genişlik ve yüksekliğin ortalamasının yarısı
        # Bu, patlama görselinin çapının yarısı = yarıçap
        self.explosion_radius = min(explosion_width, explosion_height) / 2
        
        # Patlama efekt görseli için
        self.damage_effect_alpha = 0  # Başlangıçta görünmez
    
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
                self.damage_effect_alpha = BOMB_EXPLOSION_EFFECT_ALPHA  # Hasar efektini göster
                # Patlama için rect'i büyüt
                center = self.rect.center
                self.image = self.explosion_frames[0]
                self.rect = self.image.get_rect(center=center)
                # Patlama sesi çal (bir kez)
                if not self.explosion_sound_played:
                    Audio.play_sound('bomb_explosion')
                    self.explosion_sound_played = True
        else:
            # Patlama animasyonu
            self.frame_index += 0.2
            if self.frame_index >= len(self.explosion_frames):
                self.exploded = True
                self.damage_effect_alpha = 0  # Efekti gizle
                return
            
            self.image = self.explosion_frames[int(self.frame_index)]
            
            # Hasar efektinin alpha değerini azalt (fade out)
            if self.damage_effect_alpha > 0:
                self.damage_effect_alpha = max(0, self.damage_effect_alpha - 5)
    
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
        
        # Hasar veren alanı göster (patlama sırasında)
        if self.is_exploding and self.damage_effect_alpha > 0:
            # Yarı saydam kırmızı çember çiz
            # Hasar alanını gösteren çember
            effect_surface = pygame.Surface((int(self.explosion_radius * 2), int(self.explosion_radius * 2)), pygame.SRCALPHA)
            pygame.draw.circle(
                effect_surface,
                (*RED, self.damage_effect_alpha),  # RGBA formatında
                (int(self.explosion_radius), int(self.explosion_radius)),
                int(self.explosion_radius)
            )
            
            # Çemberi bomba merkezine göre çiz
            center_x, center_y = self.rect.center
            screen.blit(effect_surface, (center_x - self.explosion_radius, center_y - self.explosion_radius))


# =============================================================================
# SİNSİ JİLET - Hareketli düşman (Sinsi hareket)
# =============================================================================

class SinsiJilet(GameObject):
    """Sinsi Jilet - Yavaşça oyuncuya yaklaşır, sonra aniden saldırır"""
    
    def __init__(self, x, y, scale=0.7, attack_distance=None, attack_delay=None):
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
        self.attack_distance = attack_distance if attack_distance is not None else JILET_ATTACK_DISTANCE  # Bu mesafede saldırıya geç
        self.attack_duration = attack_delay if attack_delay is not None else JILET_ATTACK_DELAY_BASE  # Saldırı modunda kalma süresi (kovalama süresi)
        self.attack_start_time = None  # Saldırı başladığında zamanı kaydet
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
        
        # Zamanı al (saniye cinsinden)
        current_time = pygame.time.get_ticks() / 1000.0
        
        # Duruma göre davran
        if self.state == 'sneaking':
            # Yavaşça yaklaş, hafif titreme
            self.shake_timer += 0.3
            self.shake_offset = math.sin(self.shake_timer) * 2
            
            # Belirli mesafede hemen saldırıya geç
            if distance < self.attack_distance:
                # Hemen saldırıya geç!
                self.state = 'attacking'
                self.attack_start_time = current_time
                self.anim_speed = 0.15  # Saldırıda biraz daha hızlı
            
            self.current_speed = self.speed_sneak
        else:  # attacking
            # SALDIRI! Hızlıca oyuncuya doğru kovalar
            self.current_speed = self.speed_attack
            self.shake_offset = 0
            
            # Kovalama süresi doldu mu?
            if self.attack_start_time is not None:
                elapsed_attack = current_time - self.attack_start_time
                if elapsed_attack >= self.attack_duration:
                    # Kovalama süresi doldu, normal hıza dön
                    self.state = 'sneaking'
                    self.attack_start_time = None
                    self.anim_speed = 0.05  # Normal animasyon hızına dön
        
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
        x, y = _get_random_edge_position(screen_w, screen_h, ENEMY_SPAWN_MARGIN)
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
        
        # Kalp ikonları (küçültülmüş)
        self.heart_full = Assets.load_scaled('assets/game/heart.png', HEALTH_UI_HEART_SCALE)
        self.heart_empty = Assets.load_scaled('assets/game/heart_broken.png', HEALTH_UI_HEART_SCALE)
        
        # Pozisyon (sol üst köşe - ESC yazısının altında)
        self.padding = HEALTH_UI_PADDING
        self.spacing = HEALTH_UI_SPACING
        self.start_x = self.padding
        self.start_y = self.padding + HEALTH_UI_OFFSET_Y  # ESC yazısının altında
        
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
            y += random.randint(-HEALTH_UI_SHAKE_AMOUNT, HEALTH_UI_SHAKE_AMOUNT)
        
        heart_w = self.heart_full.get_width()
        
        for i in range(self.max_health):
            if i < self.current_health:
                screen.blit(self.heart_full, (x, y))
            else:
                screen.blit(self.heart_empty, (x, y))
            x += heart_w + self.spacing


# =============================================================================
# SPAWN MANAGER - Nesne Oluşturucu (Level Sistemi ile)
# =============================================================================

def _get_random_edge_position(screen_w, screen_h, spawn_margin):
    """Rastgele ekran kenarından pozisyon al"""
    edge = random.choice(['top', 'bottom', 'left', 'right'])
    
    if edge == 'top':
        return (random.randint(spawn_margin, screen_w - spawn_margin), -spawn_margin)
    elif edge == 'bottom':
        return (random.randint(spawn_margin, screen_w - spawn_margin), screen_h + spawn_margin)
    elif edge == 'left':
        return (-spawn_margin, random.randint(spawn_margin, screen_h - spawn_margin))
    else:  # right
        return (screen_w + spawn_margin, random.randint(spawn_margin, screen_h - spawn_margin))


class SpawnManager:
    """Oyun nesnelerini zamanla oluşturur - Level bazlı zorluk"""
    
    def __init__(self, screen_w, screen_h):
        self.screen_w = screen_w
        self.screen_h = screen_h
        
        # Level sistemi
        self.level = 1
        self.level_timer = 0
        self.level_complete = False
        self.speed_multiplier = 1.0
        
        # Spawn zamanlayıcıları ve hedefleri (random aralık)
        self.bomb_timer = 0
        self.bomb_next_spawn = self._random_spawn_time()
        
        self.jilet_timer = 0
        self.jilet_next_spawn = self._random_spawn_time()
        
        self.terlik_timer = 0
        self.terlik_next_spawn = self._random_spawn_time()
        
        self.buff_timer = 0
        self.buff_next_spawn = self._random_spawn_time()
    
    def _random_spawn_time(self):
        """Level'e göre spawn zamanı - level arttıkça kısalır (exponential)"""
        # Exponential reduction: her levelde %15 azalır
        reduction_factor = (1.0 - SPAWN_TIME_REDUCTION_RATE) ** (self.level - 1)
        reduction_factor = max(MIN_SPAWN_TIME / BUFF_SPAWN_MIN_TIME, reduction_factor)
        min_time = max(MIN_SPAWN_TIME, BUFF_SPAWN_MIN_TIME * reduction_factor)
        max_time = max(MIN_SPAWN_TIME * 1.5, BUFF_SPAWN_MAX_TIME * reduction_factor)
        return random.uniform(min_time, max_time)
    
    def get_max_enemies(self):
        """Level'e göre maksimum düşman sayısı (daha agresif)"""
        return BASE_ENEMY_COUNT + (self.level - 1) * ENEMY_COUNT_PER_LEVEL
    
    def get_max_bombs(self):
        """Level'e göre maksimum bomba sayısı"""
        return int(BOMB_MAX_COUNT + (self.level - 1) * BOMB_MAX_COUNT_PER_LEVEL)
    
    def get_max_jilets(self):
        """Level'e göre maksimum jilet sayısı"""
        return int(JILET_MAX_COUNT + (self.level - 1) * JILET_MAX_COUNT_PER_LEVEL)
    
    def get_max_terliks(self):
        """Level'e göre maksimum terlik sayısı"""
        return int(TERLIK_MAX_COUNT + (self.level - 1) * TERLIK_MAX_COUNT_PER_LEVEL)
    
    def get_bomb_fuse_time(self):
        """Level'e göre bomba fünye süresi (level arttıkça kısalır)"""
        fuse_time = BOMB_FUSE_TIME - (self.level - 1) * BOMB_FUSE_REDUCTION_PER_LEVEL
        return max(MIN_BOMB_FUSE_TIME, fuse_time)
    
    def get_jilet_attack_distance(self):
        """Level'e göre jilet saldırı mesafesi (level arttıkça artar, maksimum sınır var)"""
        distance = JILET_ATTACK_DISTANCE + (self.level - 1) * JILET_ATTACK_DISTANCE_PER_LEVEL
        return min(distance, JILET_MAX_ATTACK_DISTANCE)
    
    def get_jilet_attack_delay(self):
        """Level'e göre jilet saldırı gecikmesi (level arttıkça artar)"""
        delay = JILET_ATTACK_DELAY_BASE + (self.level - 1) * JILET_ATTACK_DELAY_PER_LEVEL
        return delay
    
    def get_speed_multiplier(self):
        """Level'e göre hız çarpanı - her level hız artışı (sınır yok)"""
        # Base hız + level başına %5 hız artışı - sınır yok!
        return 1.0 + (self.level - 1) * SPEED_INCREASE_AMOUNT
    
    def reset_for_new_level(self):
        """Yeni level için sıfırla"""
        self.level_timer = 0
        self.level_complete = False
        
        # Hız çarpanını güncelle - her level için
        self.speed_multiplier = self.get_speed_multiplier()
        
        # Zamanlayıcıları sıfırla ve hemen spawn için hazırla
        self.bomb_timer = 0
        self.jilet_timer = 0
        self.terlik_timer = 0
        self.buff_timer = 0
        
        # Level 1 başlangıcında: ilk düşman hemen, sonraki her 1 saniyede bir
        if self.level == 1:
            # İlk düşman hemen spawn edilecek (timer 0, next_spawn 0)
            self.jilet_timer = 0
            self.jilet_next_spawn = 0.0  # Hemen spawn
            self.terlik_timer = 0
            self.terlik_next_spawn = 1.0  # 1 saniye sonra ilk terlik
        else:
            # Diğer leveller için normal spawn süreleri
            self.jilet_next_spawn = 1.0  # 1 saniye sonra ilk jilet
            self.terlik_next_spawn = 1.0  # 1 saniye sonra ilk terlik
        
        self.bomb_next_spawn = self._random_spawn_time()  # Bomba normal spawn zamanı
        self.buff_next_spawn = self._random_spawn_time() * 0.5  # Buff biraz daha geç
    
    def spawn_initial_enemies(self, bombs, jilets, terliks, player_rect):
        """Level başlangıcında hemen 1 terlik ve 1 sinsi jilet spawn et"""
        # Her level başında kesinlikle 1 terlik ve 1 jilet spawn et
        if len(jilets) < self.get_max_jilets():
            self._spawn_jilet(jilets, player_rect)
        
        if len(terliks) < self.get_max_terliks():
            self._spawn_terlik(terliks, player_rect)
    
    def update(self, dt, bombs, jilets, terliks, player_rect, active_buff=None):
        """Spawn zamanlayıcılarını güncelle ve nesneler oluştur"""
        # Level tamamlandıysa spawn yapma
        if self.level_complete:
            return
        
        # Level timer
        self.level_timer += dt
        if self.level_timer >= LEVEL_DURATION:
            self.level_complete = True
            return
        
        max_enemies = self.get_max_enemies()
        
        # Bomba spawn
        self.bomb_timer += dt
        if self.bomb_timer >= self.bomb_next_spawn:
            self.bomb_timer = 0
            self.bomb_next_spawn = self._random_spawn_time()
            max_bombs = min(self.get_max_bombs(), max_enemies)
            if len(bombs) < max_bombs:
                self._spawn_bomb(bombs, player_rect)
        
        # Jilet spawn
        self.jilet_timer += dt
        if self.jilet_timer >= self.jilet_next_spawn:
            self.jilet_timer = 0
            # Level 1 başlangıcında: her 1 saniyede bir düşman
            if self.level == 1:
                self.jilet_next_spawn = 1.0
            else:
                self.jilet_next_spawn = self._random_spawn_time()
            max_jilets = min(self.get_max_jilets(), max_enemies)
            if len(jilets) < max_jilets:
                self._spawn_jilet(jilets, player_rect)
        
        # Terlik spawn
        self.terlik_timer += dt
        if self.terlik_timer >= self.terlik_next_spawn:
            self.terlik_timer = 0
            # Level 1 başlangıcında: her 1 saniyede bir düşman
            if self.level == 1:
                self.terlik_next_spawn = 1.0
            else:
                self.terlik_next_spawn = self._random_spawn_time()
            max_terliks = min(self.get_max_terliks(), max_enemies)
            if len(terliks) < max_terliks:
                self._spawn_terlik(terliks, player_rect)
        
        # Buff spawn (sadece haritada buff yoksa)
        if active_buff is None:
            self.buff_timer += dt
            if self.buff_timer >= self.buff_next_spawn:
                self.buff_timer = 0
                self.buff_next_spawn = self._random_spawn_time()
                return self._create_random_buff()
        
        return None
    
    def _create_random_buff(self):
        """Ağırlıklı random buff oluştur (çay nadir)"""
        x = random.randint(BUFF_SPAWN_MARGIN, self.screen_w - BUFF_SPAWN_MARGIN)
        y = random.randint(BUFF_SPAWN_MARGIN, self.screen_h - BUFF_SPAWN_MARGIN)
        
        # Ağırlıklı seçim
        choices = []
        for buff_type, weight in BUFF_WEIGHTS.items():
            choices.extend([buff_type] * weight)
        
        selected = random.choice(choices)
        
        if selected == 'tea':
            return ('tea', Tea(x, y, TEA_SCALE))
        elif selected == 'speed_buff':
            return ('speed_buff', SpeedBuff(x, y, BUFF_SCALE))
        else:
            return ('speed_debuff', SpeedDebuff(x, y, BUFF_SCALE))
    
    def _spawn_bomb(self, bombs, player_rect):
        """Bomba oluştur - Oyuncudan uzakta (level bazlı fünye süresi)"""
        fuse_time = self.get_bomb_fuse_time()
        
        for _ in range(SPAWN_RETRY_ATTEMPTS):
            x = random.randint(SPAWN_MARGIN, self.screen_w - SPAWN_MARGIN)
            y = random.randint(SPAWN_MARGIN, self.screen_h - SPAWN_MARGIN)
            
            # Oyuncudan uzakta mı?
            dist = pygame.math.Vector2(x - player_rect.centerx, 
                                       y - player_rect.centery).length()
            if dist >= SPAWN_MIN_DISTANCE_FROM_PLAYER:
                bombs.add(Bomb(x, y, BOMB_SCALE, fuse_time))
                return
        
        # Uygun yer bulunamadıysa yine de oluştur
        bombs.add(Bomb(x, y, BOMB_SCALE, fuse_time))
    
    def _spawn_jilet(self, jilets, player_rect):
        """Jilet oluştur - Ekran kenarından (level bazlı hız, saldırı mesafesi ve gecikme)"""
        attack_distance = self.get_jilet_attack_distance()
        attack_delay = self.get_jilet_attack_delay()
        
        # Jilet için offset kullan (farklı offset değeri)
        edge = random.choice(['top', 'bottom', 'left', 'right'])
        
        if edge == 'top':
            x = random.randint(ENEMY_SPAWN_MARGIN, self.screen_w - ENEMY_SPAWN_MARGIN)
            y = -ENEMY_SPAWN_OFFSET
        elif edge == 'bottom':
            x = random.randint(ENEMY_SPAWN_MARGIN, self.screen_w - ENEMY_SPAWN_MARGIN)
            y = self.screen_h + ENEMY_SPAWN_OFFSET
        elif edge == 'left':
            x = -ENEMY_SPAWN_OFFSET
            y = random.randint(ENEMY_SPAWN_MARGIN, self.screen_h - ENEMY_SPAWN_MARGIN)
        else:  # right
            x = self.screen_w + ENEMY_SPAWN_OFFSET
            y = random.randint(ENEMY_SPAWN_MARGIN, self.screen_h - ENEMY_SPAWN_MARGIN)
        
        jilet = SinsiJilet(x, y, JILET_SCALE, attack_distance, attack_delay)
        jilet.speed_sneak *= self.speed_multiplier
        jilet.speed_attack *= self.speed_multiplier
        jilets.add(jilet)
    
    def _spawn_terlik(self, terliks, player_rect):
        """Terlik oluştur - Oyuncuya doğru fırlat (level bazlı hız)"""
        terlik = UcanTerlik(
            self.screen_w, 
            self.screen_h, 
            player_rect.center,
            TERLIK_SCALE
        )
        terlik.speed *= self.speed_multiplier
        terliks.add(terlik)


# =============================================================================
# SPEED POWERUP - Hız Değiştirici (Buff veya Debuff)
# =============================================================================

class SpeedPowerup(GameObject):
    """Hız Değiştirici - Buff veya Debuff olabilir"""
    
    def __init__(self, x, y, is_buff=True, scale=1.0):
        super().__init__(x, y)
        self.is_buff = is_buff
        
        # Görsel yükle
        image_name = 'speed_buff.png' if is_buff else 'speed_debuff.png'
        self.image = Assets.load_scaled(f'assets/game/{image_name}', scale)
        self.rect = self.image.get_rect(center=(x, y))
        
        # Konum
        self.base_x = x
        self.base_y = y
        
        # Yaşam süresi
        self.lifetime = BUFF_LIFETIME
        self.age = 0
        
        # Animasyon - buff daha hızlı, debuff daha yavaş
        self.float_offset = random.uniform(0, math.pi * 2)
        self.float_speed = 3.0 if is_buff else 2.0
        self.float_amplitude = 8 if is_buff else 6
        self.pulse_timer = 0
        self.visible = True
    
    def update(self, screen_w, screen_h, player_rect, dt):
        """Güncelle - Süzülme ve kaybolma animasyonu"""
        self.age += dt
        
        # Süre doldu mu?
        if self.age >= self.lifetime:
            return False  # Silinmeli
        
        # Yukarı aşağı süzülme
        elapsed = pygame.time.get_ticks() / 1000.0
        offset = math.sin(elapsed * self.float_speed + self.float_offset) * self.float_amplitude
        self.rect.centery = self.base_y + offset
        
        # Son 2 saniyede yanıp sönme
        if self.age >= self.lifetime - 2:
            self.pulse_timer += dt * 10
            self.visible = int(self.pulse_timer) % 2 == 0
        else:
            self.visible = True
        
        return True  # Hala yaşıyor
    
    def draw(self, screen):
        if self.visible:
            screen.blit(self.image, self.rect)


# Geriye uyumluluk için alias'lar
def SpeedBuff(x, y, scale=1.0):
    """Hız Artışı - Toplandığında oyuncuyu hızlandırır"""
    return SpeedPowerup(x, y, is_buff=True, scale=scale)


def SpeedDebuff(x, y, scale=1.0):
    """Hız Azalması - Toplandığında oyuncuyu yavaşlatır"""
    return SpeedPowerup(x, y, is_buff=False, scale=scale)
