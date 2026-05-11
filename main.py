# main.py
# Role 1 - Entry point and main game loop

import sys
import os

# Import core systems
from engine.game_engine import run_scene
from engine.state import create_initial_state

# Import security/logging (with fallbacks)
try:
    from security.security import log_event, audit_log_path
except ImportError:
    def log_event(event_type, detail="", result=""):
        pass
    audit_log_path = "audit_log.txt"

try:
    from security.save_load import load_game
except ImportError:
    def load_game():
        return None


def print_title():
    """Display the game title."""
    print("\n")
    print("╔════════════════════════════════════════════════════════╗")
    print("║        CYSE-130 Final Project | Spring 2026            ║")
    print("╚════════════════════════════════════════════════════════╝")
    print("\n")


def print_menu():
    """Display the main menu."""
    print()
    print("  1. Start New Game")
    print("  2. Load Saved Game")
    print("  3. View Audit Log")
    print("  4. Credits")
    print("  5. Quit")
    print()


def get_menu_choice():
    """Get and validate menu input from player."""
    while True:
        raw = input("  Enter your choice (1-5): ").strip()
        log_event("INPUT", detail=f"MainMenu input='{raw}'")
        
        try:
            choice = int(raw)
            if 1 <= choice <= 5:
                return choice
            else:
                log_event("INPUT_INVALID", detail=f"MainMenu out-of-range='{raw}'")
                print("  Please enter 1-5.\n")
        except ValueError:
            log_event("INPUT_INVALID", detail=f"MainMenu non-integer='{raw}'")
            print("  Invalid input. Enter a number.\n")


def show_credits():
    """Display game credits."""
    print()
    print("  SECTOR 8 — Text-Based Adventure Game")
    print("  CYSE-130 Final Project | Spring 2026")
    print()
    print("  DEVELOPMENT TEAM:")
    print("    Role 1 (Core Engine): Abdulrahman, Rehan, Raki")
    print("    Role 2 (Story & NPCs): Nithin, Nawaf")
    print("    Role 3 (Systems & Security): Sami, Bader")
    print()


def show_audit_log():
    """Display the audit log."""
    if not os.path.exists(audit_log_path):
        print(f"\n  No audit log found.\n")
        return

    print()
    print("  ════════ AUDIT LOG (last 30 entries) ════════")
    print()
    
    try:
        with open(audit_log_path, "r") as f:
            lines = f.readlines()
            for line in lines[-30:]:
                print(f"  {line.rstrip()}")
    except Exception as e:
        print(f"  Error reading log: {e}")
    
    print()


def run_game(game_state):
    """
    Main game loop - runs scenes until player quits or reaches an ending.
    Returns True if player quit, False if reached an ending.
    """
    current_scene = "start"
    
    while True:
        next_scene = run_scene(current_scene, game_state)
        
        if next_scene is None:
            # Player quit from action menu
            return True
        elif next_scene == "end":
            # Reached an ending
            return False
        else:
            # Move to next scene
            current_scene = next_scene


def play_again_menu():
    """Ask player what to do after game ends."""
    while True:
        choice = input("\n  Play again (Y/N)? ").strip().upper()
        
        if choice == "Y":
            return True
        elif choice == "N":
            return False
        else:
            print("  Enter Y or N.\n")


def main():
    """Main entry point - menu loop."""
    print_title()
    log_event("APPLICATION_START")
    
    while True:
        print_menu()
        choice = get_menu_choice()
        
        if choice == 1:
            # Start New Game
            print("\n  Starting new game...\n")
            log_event("GAME_START", detail="New game")
            game_state = create_initial_state()
            
            quit_early = run_game(game_state)
            
            if quit_early:
                print("\n  Game ended.\n")
                log_event("GAME_END", detail="Player quit")
            else:
                print("\n  Thank you for playing!\n")
                log_event("GAME_END", detail="Reached ending")
            
            if not play_again_menu():
                break
        
        elif choice == 2:
            # Load Saved Game
            print("\n  Loading saved game...\n")
            game_state = load_game()
            
            if game_state is None:
                print("  No save file found. Starting new game.\n")
                log_event("LOAD_ATTEMPT", result="FAILED")
                game_state = create_initial_state()
            else:
                print("  Game loaded!\n")
                log_event("LOAD_ATTEMPT", result="SUCCESS")
            
            quit_early = run_game(game_state)
            
            if quit_early:
                print("\n  Game ended.\n")
                log_event("GAME_END", detail="Player quit")
            else:
                print("\n  Thank you for playing!\n")
                log_event("GAME_END", detail="Reached ending")
            
            if not play_again_menu():
                break
        
        elif choice == 3:
            # View Audit Log
            show_audit_log()
        
        elif choice == 4:
            # Show Credits
            show_credits()
        
        elif choice == 5:
            # Quit
            print("\n  Thank you for playing Sector 8!\n")
            log_event("APPLICATION_END", detail="Quit from menu")
            break


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n  [Game interrupted]\n")
        log_event("APPLICATION_END", detail="Interrupted")
        sys.exit(0)
    except Exception as e:
        print(f"\n  [Error: {e}]\n")
        log_event("ERROR", detail=str(e))
        sys.exit(1)
# main.py
# Role 1 - Entry point
