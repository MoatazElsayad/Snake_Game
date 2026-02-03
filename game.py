import pygame
import sys
from config import *
from sprites import Snake, Food
from ui import Button, InputBox, ColorPicker, ThemeToggle

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Sophisticated Snake Game")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("Segoe UI", 24)
        self.title_font = pygame.font.SysFont("Segoe UI", 48, bold=True)
        
        self.current_theme_name = "DARK"
        self.theme = THEMES[self.current_theme_name]
        
        self.state = "MENU" # MENU, PLAYING, GAME_OVER, VICTORY
        self.difficulty = "MEDIUM"
        self.username = "Player1"
        self.snake_color = GREEN
        
        self.snake = Snake(self.snake_color)
        self.food = Food()
        
        self.setup_ui()

    def setup_ui(self):
        # Center X helpers
        cx = SCREEN_WIDTH // 2
        
        # Main Menu UI
        self.username_input = InputBox(cx - 100, 150, 200, 40, "Player1")
        
        self.theme_btn = ThemeToggle(SCREEN_WIDTH - 160, 20, 140, 40, self.current_theme_name)
        self.theme_btn.action = self.toggle_theme
        
        self.color_picker = ColorPicker(cx - 150, 220, 300)
        
        # Difficulty Buttons
        self.diff_btns = []
        diffs = ["EASY", "MEDIUM", "HARD"]
        for i, d in enumerate(diffs):
            btn = Button(cx - 160 + (i * 110), 300, 100, 40, d, self.set_difficulty, d)
            self.diff_btns.append(btn)
            
        self.start_btn = Button(cx - 100, 400, 200, 50, "START GAME", self.start_game)
        
        # Game Over / Victory UI
        self.restart_btn = Button(cx - 100, 350, 200, 50, "PLAY AGAIN", self.reset_game)
        self.menu_btn = Button(cx - 100, 420, 200, 50, "MAIN MENU", self.return_to_menu)

    def toggle_theme(self):
        self.current_theme_name = self.theme_btn.toggle()
        self.theme = THEMES[self.current_theme_name]

    def set_difficulty(self, diff):
        self.difficulty = diff

    def start_game(self):
        self.username = self.username_input.text
        if not self.username:
            self.username = "Player1"
        
        # self.snake_color is already updated by the event loop
        self.snake = Snake(self.snake_color) 
        self.snake.reset()
        self.food.randomize_position(self.snake.positions)
        self.state = "PLAYING"

    def reset_game(self):
        self.snake.reset()
        self.food.randomize_position(self.snake.positions)
        self.state = "PLAYING"

    def return_to_menu(self):
        self.state = "MENU"

    def handle_events(self):
        mouse_pos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if self.state == "MENU":
                self.username_input.handle_event(event)
                
                self.theme_btn.check_hover(mouse_pos)
                self.theme_btn.handle_event(event)
                
                # Difficulty selection
                for btn in self.diff_btns:
                    btn.check_hover(mouse_pos)
                    action = btn.handle_event(event)
                    
                # Color Picker
                new_color = self.color_picker.handle_event(event)
                if new_color:
                    self.snake_color = new_color
                
                self.start_btn.check_hover(mouse_pos)
                self.start_btn.handle_event(event)

            elif self.state == "PLAYING":
                # Snake controls
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP: self.snake.turn((0, -1))
                    elif event.key == pygame.K_DOWN: self.snake.turn((0, 1))
                    elif event.key == pygame.K_LEFT: self.snake.turn((-1, 0))
                    elif event.key == pygame.K_RIGHT: self.snake.turn((1, 0))

            elif self.state in ["GAME_OVER", "VICTORY"]:
                self.restart_btn.check_hover(mouse_pos)
                self.restart_btn.handle_event(event)
                self.menu_btn.check_hover(mouse_pos)
                self.menu_btn.handle_event(event)

    def update(self):
        if self.state == "PLAYING":
            self.snake.move()
            
            # Check Food Collision
            if self.snake.get_head_position() == self.food.position:
                self.snake.length += 1
                self.snake.score += 1
                self.food.randomize_position(self.snake.positions)
                
            # Check Win Condition
            if self.snake.length >= TARGET_LENGTH[self.difficulty]:
                self.state = "VICTORY"
                
            # Check Death
            if not self.snake.alive:
                self.state = "GAME_OVER"

    def draw(self):
        self.screen.fill(self.theme["background"])
        
        if self.state == "MENU":
            # Title
            title = self.title_font.render("SNAKE GAME", True, self.theme["text"])
            self.screen.blit(title, (SCREEN_WIDTH//2 - title.get_width()//2, 50))
            
            # Username
            lbl = self.font.render("Username:", True, self.theme["text"])
            self.screen.blit(lbl, (SCREEN_WIDTH//2 - 100, 120))
            self.username_input.draw(self.screen, self.font, self.theme)
            
            # Color Picker
            lbl = self.font.render("Snake Color:", True, self.theme["text"])
            self.screen.blit(lbl, (SCREEN_WIDTH//2 - 150, 200))
            self.color_picker.draw(self.screen, self.theme)
            
            # Difficulty
            lbl = self.font.render(f"Difficulty: {self.difficulty}", True, self.theme["text"])
            self.screen.blit(lbl, (SCREEN_WIDTH//2 - lbl.get_width()//2, 270))
            for btn in self.diff_btns:
                # Highlight selected
                if btn.text == self.difficulty:
                    # Manually highlight or just rely on text feedback above
                    pygame.draw.rect(self.screen, self.theme["text"], btn.rect, 3, 5)
                btn.draw(self.screen, self.font, self.theme)
                
            # Start
            self.start_btn.draw(self.screen, self.font, self.theme)
            
            # Theme Toggle
            self.theme_btn.draw(self.screen, self.font, self.theme)

        elif self.state == "PLAYING":
            # Draw Grid (Optional, makes it look "Solid")
            for x in range(0, SCREEN_WIDTH, GRID_SIZE):
                pygame.draw.line(self.screen, self.theme["grid"], (x, 0), (x, SCREEN_HEIGHT))
            for y in range(0, SCREEN_HEIGHT, GRID_SIZE):
                pygame.draw.line(self.screen, self.theme["grid"], (0, y), (SCREEN_WIDTH, y))
                
            self.snake.draw(self.screen)
            self.food.draw(self.screen)
            
            # HUD
            score_text = f"Score: {self.snake.score} | Length: {self.snake.length}/{TARGET_LENGTH[self.difficulty]}"
            user_text = f"Player: {self.username}"
            
            s_surf = self.font.render(score_text, True, self.theme["text"])
            u_surf = self.font.render(user_text, True, self.theme["text"])
            
            # Background for HUD
            pygame.draw.rect(self.screen, self.theme["ui_bg"], (0, 0, SCREEN_WIDTH, 40))
            pygame.draw.line(self.screen, self.theme["ui_border"], (0, 40), (SCREEN_WIDTH, 40), 2)
            
            self.screen.blit(u_surf, (10, 5))
            self.screen.blit(s_surf, (SCREEN_WIDTH - s_surf.get_width() - 10, 5))

        elif self.state == "GAME_OVER":
            msg = self.title_font.render("GAME OVER", True, RED)
            score_msg = self.font.render(f"Final Score: {self.snake.score}", True, self.theme["text"])
            
            self.screen.blit(msg, (SCREEN_WIDTH//2 - msg.get_width()//2, 150))
            self.screen.blit(score_msg, (SCREEN_WIDTH//2 - score_msg.get_width()//2, 220))
            
            self.restart_btn.draw(self.screen, self.font, self.theme)
            self.menu_btn.draw(self.screen, self.font, self.theme)

        elif self.state == "VICTORY":
            msg = self.title_font.render("LEVEL COMPLETE!", True, GREEN)
            score_msg = self.font.render(f"You reached length {self.snake.length}!", True, self.theme["text"])
            
            self.screen.blit(msg, (SCREEN_WIDTH//2 - msg.get_width()//2, 150))
            self.screen.blit(score_msg, (SCREEN_WIDTH//2 - score_msg.get_width()//2, 220))
            
            self.restart_btn.draw(self.screen, self.font, self.theme)
            self.menu_btn.draw(self.screen, self.font, self.theme)

        pygame.display.flip()

    def run(self):
        while True:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(DIFFICULTY[self.difficulty] if self.state == "PLAYING" else 60)
