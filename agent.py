import argparse
import os
import google.generativeai as genai
from dotenv import load_dotenv

# --- Load environment variables from .env file ---
load_dotenv()

# Configuration - Aseprite parts can be commented out for now
CONFIG = {
    # "aseprite_path": "/Applications/Aseprite.app/Contents/MacOS/aseprite", # Not needed for direct Lua generation
    "assets_dir": "assets", # Might be used by generated Lua, or for future AI asset saving
    # "sprite_name": "player_sprite", # Less relevant for initial AI code gen
    # "sprite_width": 32,             # Less relevant for initial AI code gen
    # "sprite_height": 32,            # Less relevant for initial AI code gen
}

def ensure_dir_exists(path):
    """Creates a directory if it doesn't exist."""
    os.makedirs(path, exist_ok=True)

# --- Function to Interact with Gemini (CORE - KEEP THIS) ---
def generate_lua_with_gemini(game_concept_prompt):
    """
    Generates Love2D Lua code using the Gemini API based on a game concept.
    """
    try:
        api_key = os.environ.get("GOOGLE_API_KEY")
        if not api_key:
            print("Error: GOOGLE_API_KEY environment variable not set.")
            print("Please ensure your .env file is correct and `python-dotenv` is installed and loaded.")
            return None

        genai.configure(api_key=api_key)
        
        model = genai.GenerativeModel('gemini-2.0-flash') # Using the model we expect to work
        
        # Define the prompt template as a standard multi-line string
        prompt_template = '''
Generate a complete main.lua file for a Love2D game based on the following concept: {game_concept_prompt}.
Your primary goal is to create a simple but playable game experience using the roles and behaviors defined below.

1.  **Entity Identification and Role Assignment:**
    *   From the game concept (e.g., "a knight collects coins and fights a patrolling goblin"), identify all key game entities (knight, coins, goblin).
    *   For each entity, assign one of the roles defined below (e.g., knight -> PLAYER_CHARACTER, coins -> ITEM_COLLECTIBLE_STATIC, goblin -> ENEMY_SIMPLE_PATROL).
    *   Use the entity's name from the prompt for its Lua table and asset filename (e.g., if the prompt mentions 'brave knight', the Lua table could be `knight` and it loads 'assets/knight.png'). All asset names should be lowercase.
    *   If the prompt implies multiple instances of an entity (e.g., "three coins"), create a list of tables for them (e.g., `coins = {{{{...}}}}, {{{{...}}}}, {{{{...}}}}`).

2.  **Defined Entity Roles and Standard Behaviors:**

    A.  **`PLAYER_CHARACTER` Role:**
        *   **Purpose:** The main controllable entity. Typically, there is only one player character.
        *   **Asset:** Load from `assets/[player_entity_name_lowercase].png`.
        *   **Initialization (`love.load`):**
            *   Create a Lua table for the player (e.g., `player = {{}}` or `hero = {{}}` based on the prompt's naming).
            *   Load its image, get `width` and `height` from the image.
            *   Set initial position (e.g., `player.x`, `player.y`), often centered: `x = (800 - width) / 2`, `y = (600 - height) / 2`.
            *   Set `player.speed = 200`.
        *   **Update (`love.update(dt)`):**
            *   Implement movement controls using W (up), A (left), S (down), D (right) keys.
            *   Ensure the player does not move off-screen (boundary checks for an 800x600 window).
        *   **Drawing (`love.draw`):** Draw the player's image at its current `x, y` position.

    B.  **`ENEMY_SIMPLE_PATROL` Role:**
        *   **Purpose:** A basic enemy that moves back and forth horizontally.
        *   **Asset:** Load from `assets/[enemy_entity_name_lowercase].png`.
        *   **Initialization (`love.load`):**
            *   Create a Lua table (or list of tables if multiple) for the enemy (e.g., `goblin = {{}}`).
            *   Load its image, get `width` and `height`.
            *   Set initial position (e.g., `enemy.x = 100`, `enemy.y = 400`).
            *   Set `enemy.speed = 50`, `enemy.direction = 1` (1 for right, -1 for left).
            *   Define patrol boundaries, e.g., `enemy.patrol_min_x = 50`, `enemy.patrol_max_x = 300`.
        *   **Update (`love.update(dt)`):**
            *   Move horizontally: `enemy.x = enemy.x + enemy.speed * enemy.direction * dt`.
            *   If `enemy.x < enemy.patrol_min_x` or `enemy.x + enemy.width > enemy.patrol_max_x`, reverse `enemy.direction`.
            *   **Collision with `PLAYER_CHARACTER`:**
                *   Implement Axis-Aligned Bounding Box (AABB) collision detection. (A collision occurs if `e1.x < e2.x + e2.width` and `e1.x + e1.width > e2.x` and `e1.y < e2.y + e2.height` and `e1.y + e1.height > e2.y`).
                *   On collision, set `game_state = "game_over"`.
        *   **Drawing (`love.draw`):** Draw the enemy's image.

    C.  **`ITEM_COLLECTIBLE_STATIC` Role:**
        *   **Purpose:** An item the player can collect. It remains stationary.
        *   **Asset:** Load from `assets/[item_entity_name_lowercase].png`.
        *   **Initialization (`love.load`):**
            *   Create a Lua table (or list of tables if multiple) for the item (e.g., `coin = {{}}`).
            *   Load its image, get `width` and `height`.
            *   Set a fixed position (e.g., `item.x = 500`, `item.y = 300`).
            *   Set `item.visible = true`.
        *   **Update (`love.update(dt)`):**
            *   If `item.visible == true`, check for AABB collision with `PLAYER_CHARACTER`.
            *   On collision: Set `item.visible = false` and increment `score` by 10 (e.g., `score = score + 10`).
        *   **Drawing (`love.draw`):** If `item.visible == true`, draw the item's image.

3.  **Game State and General Logic:**
    *   In `love.load()`:
        *   Initialize `game_state = "playing"`.
        *   Initialize `score = 0`.
    *   In `love.update(dt)`:
        *   Only run entity updates (movement, collision checks) if `game_state == "playing"`.
    *   In `love.draw()`:
        *   Draw all visible game entities.
        *   Display the current `score` (e.g., `love.graphics.print("Score: " .. score, 10, 10)`).
        *   If `game_state == "game_over"`, display a "Game Over" message prominently (e.g., `love.graphics.print("Game Over!", 350, 280)`).

4.  **Standard Love2D Structure:**
    *   Include all necessary Love2D callback functions: `love.load()`, `love.update(dt)`, `love.draw()`.
    *   You may also include `love.keypressed(key)` for an "escape to quit" feature.
    *   Assume an 800x600 window. Do not generate `conf.lua`.

5.  **Code Style and Completeness:**
    *   Ensure all variables (entity tables, images, positions, dimensions, game_state, score, etc.) are properly initialized in `love.load()` before use.
    *   The Lua code must be complete and runnable in Love2D.
    *   If the user's prompt implies entities or behaviors not fitting the defined roles, make a reasonable attempt to include them as static sprites or apply the closest matching role's behavior if appropriate. Prioritize creating an interactive experience.

Output only the Lua code for main.lua. Do not include any other explanatory text or markdown formatting around the code.
'''
        
        # Format the prompt template with the actual game_concept_prompt
        full_prompt = prompt_template.format(game_concept_prompt=game_concept_prompt)
        
        print("\n--- Sending prompt to Gemini ---")
        # print(f"Prompt: {full_prompt}") # Uncomment to see the full prompt being sent
        print("Waiting for Gemini to generate code...")

        response = model.generate_content(full_prompt)
        
        print("--- Gemini Response Received ---")
        if response.parts:
            generated_code = "".join(part.text for part in response.parts)
            # Clean up potential markdown code block delimiters
            if generated_code.startswith("```lua"):
                generated_code = generated_code[len("```lua"):]
            if generated_code.startswith("```"):
                generated_code = generated_code[len("```"):]
            if generated_code.endswith("```"):
                generated_code = generated_code[:-len("```")]
            return generated_code.strip()
        else:
            print("Error: No content parts in response from Gemini.")
            if response.prompt_feedback:
                print(f"Prompt Feedback: {response.prompt_feedback}")
            return None

    except Exception as e:
        print(f"An error occurred while communicating with Gemini: {e}")
        return None

# --- 'handle_scaffold' is now the primary function for testing AI code generation (CORE - KEEP THIS) ---
def handle_scaffold(args):
    print("--- Running scaffold (AI Code Generation) --- ")
    if not args.prompt:
        print("Error: No prompt provided for scaffolding. Use --prompt 'your game concept'.")
        print("-------------------------------------- ")
        return

    print(f"Game Concept: {args.prompt}")
    
    lua_code = generate_lua_with_gemini(args.prompt)
    
    if lua_code:
        print("\n--- Generated Lua Code (main.lua) ---")
        print(lua_code)
        print("-------------------------------------- ")
        
        output_dir = "generated_game" # Directory to save the generated game
        ensure_dir_exists(output_dir)
        
        # Ensure the assets directory exists within the output directory
        assets_path = os.path.join(output_dir, CONFIG["assets_dir"])
        ensure_dir_exists(assets_path)
        print(f"Ensure assets directory exists at: {assets_path}") # For debugging

        file_path = os.path.join(output_dir, "main.lua")
        try:
            with open(file_path, "w") as f:
                f.write(lua_code)
            print(f"\nSuccessfully saved generated code to: {file_path}")
            print(f"To test, 'cd {output_dir}' and then run 'love .'")
            print("-------------------------------------- ")
        except IOError as e:
            print(f"Error saving generated code to file: {e}")
            print("-------------------------------------- ")
    else:
        print("Failed to generate Lua code.")
        print("-------------------------------------- ")

def main():
    parser = argparse.ArgumentParser(description="AI Game Creator (Local Testbed for Love2D Code Generation)")
    subparsers = parser.add_subparsers(dest="command", required=True, help="Available commands")

    # --- 'scaffold' is the main command we're focusing on ---
    parser_scaffold = subparsers.add_parser("scaffold", help="Generate Lua game code from a concept using AI.")
    parser_scaffold.add_argument("--prompt", required=True, help="The game concept prompt for the AI.")
    parser_scaffold.set_defaults(func=handle_scaffold)

    args = parser.parse_args()
    if hasattr(args, 'func'):
        args.func(args)
    else:
        # Fallback or error if a command somehow gets through without a function
        # (shouldn't happen with required=True on subparsers and set_defaults)
        parser.print_help()


if __name__ == "__main__":
    main() 