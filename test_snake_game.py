import unittest
import snake_game  # Import the game module

class TestSnakeGame(unittest.TestCase):

    def setUp(self):
        # Set up initial game state variables similar to those in snake_game.py
        # These can be overridden in individual tests
        snake_game.screen_width = 600
        snake_game.screen_height = 400
        snake_game.snake_block_size = 10
        
        # Default snake starting position and body
        snake_game.snake_x = snake_game.screen_width / 2
        snake_game.snake_y = snake_game.screen_height / 2
        snake_game.snake_body = [[snake_game.snake_x, snake_game.snake_y]]
        snake_game.snake_direction = "RIGHT"
        
        # Default food position (can be changed per test)
        # For spawn_food tests, snake_body will be crucial
        snake_game.food_pos = [100, 100] 
        
        # Score
        snake_game.score = 0

        # It's good practice to avoid initializing Pygame display in unit tests unless essential.
        # Most logic here should be testable without a screen.
        # snake_game.pygame.init() # Avoid if possible
        # snake_game.screen = snake_game.pygame.display.set_mode((snake_game.screen_width, snake_game.screen_height)) # Avoid
        # snake_game.pygame.font.init() # Avoid unless testing rendering

    def test_snake_head_moves_right(self):
        snake_game.snake_x = 50
        snake_game.snake_y = 50
        snake_game.snake_direction = "RIGHT"
        new_x, new_y = snake_game.update_snake_head_logic(
            snake_game.snake_x, snake_game.snake_y, snake_game.snake_direction, snake_game.snake_block_size
        )
        self.assertEqual(new_x, 50 + snake_game.snake_block_size)
        self.assertEqual(new_y, 50)

    def test_snake_head_moves_left(self):
        snake_game.snake_x = 50
        snake_game.snake_y = 50
        snake_game.snake_direction = "LEFT"
        new_x, new_y = snake_game.update_snake_head_logic(
            snake_game.snake_x, snake_game.snake_y, snake_game.snake_direction, snake_game.snake_block_size
        )
        self.assertEqual(new_x, 50 - snake_game.snake_block_size)
        self.assertEqual(new_y, 50)

    def test_snake_head_moves_up(self):
        snake_game.snake_x = 50
        snake_game.snake_y = 50
        snake_game.snake_direction = "UP"
        new_x, new_y = snake_game.update_snake_head_logic(
            snake_game.snake_x, snake_game.snake_y, snake_game.snake_direction, snake_game.snake_block_size
        )
        self.assertEqual(new_x, 50)
        self.assertEqual(new_y, 50 - snake_game.snake_block_size)

    def test_snake_head_moves_down(self):
        snake_game.snake_x = 50
        snake_game.snake_y = 50
        snake_game.snake_direction = "DOWN"
        new_x, new_y = snake_game.update_snake_head_logic(
            snake_game.snake_x, snake_game.snake_y, snake_game.snake_direction, snake_game.snake_block_size
        )
        self.assertEqual(new_x, 50)
        self.assertEqual(new_y, 50 + snake_game.snake_block_size)

    def test_snake_body_follows_head_no_food(self):
        # Initial state: [[50,50]]
        snake_game.snake_x = 50
        snake_game.snake_y = 50
        snake_game.snake_body = [[snake_game.snake_x, snake_game.snake_y]]
        snake_game.snake_direction = "RIGHT"
        
        # Move 1
        snake_game.snake_x, snake_game.snake_y = snake_game.update_snake_head_logic(
            snake_game.snake_x, snake_game.snake_y, snake_game.snake_direction, snake_game.snake_block_size
        ) # snake_x = 60, snake_y = 50
        new_head1 = [snake_game.snake_x, snake_game.snake_y]
        snake_game.snake_body.insert(0, new_head1)
        snake_game.snake_body.pop() # No food eaten
        self.assertEqual(snake_game.snake_body, [[60,50]])
        self.assertEqual(len(snake_game.snake_body), 1)

        # Move 2 - Grow snake for this test manually to have a body
        snake_game.snake_body.insert(0, [70,50]) # Manually grow
        snake_game.snake_x, snake_game.snake_y = 70, 50
        # snake_body is now [[70,50], [60,50]]
        
        snake_game.snake_x, snake_game.snake_y = snake_game.update_snake_head_logic(
            snake_game.snake_x, snake_game.snake_y, snake_game.snake_direction, snake_game.snake_block_size
        ) # snake_x = 80, snake_y = 50
        new_head2 = [snake_game.snake_x, snake_game.snake_y]
        snake_game.snake_body.insert(0, new_head2)
        snake_game.snake_body.pop() # No food eaten
        self.assertEqual(snake_game.snake_body, [[80,50], [70,50]])
        self.assertEqual(len(snake_game.snake_body), 2)
        
    # Test for preventing immediate reversal is tricky as it's in pygame event loop.
    # The current logic functions update_snake_head_logic don't check previous direction.
    # This is typically handled before calling update_snake_head_logic.
    # We can test the behavior within game_loop_function if we could mock Pygame events,
    # or by testing a dedicated direction change function if we refactor one out.
    # For now, this aspect might be implicitly tested by playing or needs more refactoring.

    # --- Collision Detection Tests ---
    def test_wall_collision_right_boundary(self):
        head_x = snake_game.screen_width # At the boundary
        head_y = 50
        self.assertTrue(snake_game.check_wall_collision_logic(head_x, head_y, snake_game.screen_width, snake_game.screen_height))

    def test_wall_collision_left_boundary(self):
        head_x = -snake_game.snake_block_size # Past the boundary
        head_y = 50
        self.assertTrue(snake_game.check_wall_collision_logic(head_x, head_y, snake_game.screen_width, snake_game.screen_height))
    
    def test_wall_collision_top_boundary(self):
        head_x = 50
        head_y = -snake_game.snake_block_size # Past the boundary
        self.assertTrue(snake_game.check_wall_collision_logic(head_x, head_y, snake_game.screen_width, snake_game.screen_height))

    def test_wall_collision_bottom_boundary(self):
        head_x = 50
        head_y = snake_game.screen_height # At the boundary
        self.assertTrue(snake_game.check_wall_collision_logic(head_x, head_y, snake_game.screen_width, snake_game.screen_height))

    def test_no_wall_collision_inside_boundary(self):
        head_x = 50
        head_y = 50
        self.assertFalse(snake_game.check_wall_collision_logic(head_x, head_y, snake_game.screen_width, snake_game.screen_height))

    def test_self_collision(self):
        # Head at [50,50], body also contains [50,50]
        new_head = [50, 50]
        snake_game.snake_body = [[60, 50], [50, 50], [40,50]] # Head will collide with the second segment
        self.assertTrue(snake_game.check_self_collision_logic(new_head, snake_game.snake_body))

    def test_no_self_collision(self):
        new_head = [70, 50]
        snake_game.snake_body = [[60, 50], [50, 50], [40,50]]
        self.assertFalse(snake_game.check_self_collision_logic(new_head, snake_game.snake_body))
        
    def test_no_self_collision_short_snake(self):
        # A snake of length 1 or 2 cannot self-collide with the head moving to an empty space.
        # The check_self_collision_logic checks the new_head against the existing body.
        new_head = [60,50]
        snake_game.snake_body = [[50,50]] # Initial snake
        self.assertFalse(snake_game.check_self_collision_logic(new_head, snake_game.snake_body))

    # --- Food Consumption Tests ---
    def test_eat_food_increases_length_and_score(self):
        # Initial snake at [50,50], food at [60,50]
        snake_game.snake_x = 50
        snake_game.snake_y = 50
        snake_game.snake_body = [[50,50]]
        snake_game.snake_direction = "RIGHT"
        snake_game.food_pos = [60,50] # Place food in front of snake
        initial_score = snake_game.score = 0
        initial_length = len(snake_game.snake_body)

        # Simulate one game step where food is eaten
        # 1. Move head
        snake_game.snake_x, snake_game.snake_y = snake_game.update_snake_head_logic(
            snake_game.snake_x, snake_game.snake_y, snake_game.snake_direction, snake_game.snake_block_size
        )
        new_head = [snake_game.snake_x, snake_game.snake_y]
        
        # 2. Add new head to body
        snake_game.snake_body.insert(0, new_head)
        
        # 3. Check for food consumption (logic from game_loop_function)
        ate_food = False
        if new_head[0] == snake_game.food_pos[0] and new_head[1] == snake_game.food_pos[1]:
            ate_food = True
            snake_game.score += 10
            # In the actual game, new food would be spawned here.
            # For this test, we just check score and that tail is NOT popped.
        
        if not ate_food: # This path should not be taken if food is correctly placed
            snake_game.snake_body.pop() 

        self.assertTrue(ate_food)
        self.assertEqual(len(snake_game.snake_body), initial_length + 1)
        self.assertEqual(snake_game.score, initial_score + 10)

    def test_eat_food_spawns_new_food(self):
        snake_game.snake_x = 50
        snake_game.snake_y = 50
        snake_game.snake_body = [[50,50]]
        snake_game.snake_direction = "RIGHT"
        original_food_pos = [60,50]
        snake_game.food_pos = list(original_food_pos) # Use a copy

        # Simulate eating food
        snake_game.snake_x, snake_game.snake_y = snake_game.update_snake_head_logic(
            snake_game.snake_x, snake_game.snake_y, snake_game.snake_direction, snake_game.snake_block_size
        ) # Head moves to [60,50]
        new_head = [snake_game.snake_x, snake_game.snake_y]
        snake_game.snake_body.insert(0, new_head) # Snake is now [[60,50], [50,50]]
        
        # Assume food was eaten, now spawn new food
        new_food_position = snake_game.spawn_food_logic(
            snake_game.snake_body, snake_game.screen_width, snake_game.screen_height, snake_game.snake_block_size
        )
        
        self.assertNotEqual(new_food_position, original_food_pos) # New food should be at a different pos
        
        # Check that new food is not on the snake's body
        is_on_snake = False
        for segment in snake_game.snake_body:
            if segment[0] == new_food_position[0] and segment[1] == new_food_position[1]:
                is_on_snake = True
                break
        self.assertFalse(is_on_snake, "New food spawned on the snake's body")

    # --- Food Spawning Test ---
    def test_spawn_food_avoids_snake_body_nearly_full_screen(self):
        # Create a snake that covers almost the entire screen
        snake_game.snake_body = []
        for x in range(0, snake_game.screen_width - snake_game.snake_block_size, snake_game.snake_block_size):
            for y in range(0, snake_game.screen_height, snake_game.snake_block_size):
                snake_game.snake_body.append([x, y])
        
        # Leave one column empty for food to spawn
        # For example, the last column is empty.
        # The food must spawn in this last column.
        
        # Call spawn_food_logic multiple times
        possible_spawn_xs = [snake_game.screen_width - snake_game.snake_block_size]
        
        for _ in range(20): # Try spawning multiple times
            food_pos = snake_game.spawn_food_logic(
                snake_game.snake_body, snake_game.screen_width, snake_game.screen_height, snake_game.snake_block_size
            )
            self.assertIn(food_pos[0], possible_spawn_xs, "Food spawned in an occupied column.")
            
            # Also check it's not on any specific segment (already done by spawn_food_logic internally, but good for sanity)
            on_snake = any(segment[0] == food_pos[0] and segment[1] == food_pos[1] for segment in snake_game.snake_body)
            self.assertFalse(on_snake, "Food spawned directly on a snake segment despite logic.")

    # Note: Testing the "snake cannot immediately reverse direction" is more of an integration
    # test of the event handling logic within game_loop_function. The core movement functions
    # themselves don't prevent this; it's the higher-level logic that should.
    # This test suite focuses on the "logic" functions.

if __name__ == '__main__':
    unittest.main()
