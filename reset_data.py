'''
Reset User Data Script - Clear save file and start fresh
'''

import os


def reset_player_data() -> None:
    '''
    Delete player save file to reset game progress.
    
    Removes the save file so the next game launch starts from scratch.
    '''
    save_file = "player_data.txt"
    
    print("\n" + "=" * 50)
    print("Reset User Data")
    print("=" * 50)
    
    # Check if save file exists
    if not os.path.exists(save_file):
        print("\nNo save file found. Already at initial state!")
        return
    
    # Confirm action
    print("\nThis will delete all game progress:")
    print("  - All collected idols")
    print("  - Coin balance")
    print("  - Draw statistics")
    
    response = input("\nAre you sure? Type 'YES' to confirm: ")
    
    if response.strip().upper() == "YES":
        try:
            # Delete save file
            os.remove(save_file)
            print("\n✓ User data has been reset!")
            print("✓ Next launch will start fresh.\n")
            
        except Exception as e:
            print(f"\n✗ Error: {e}\n")
    else:
        print("\n✗ Reset cancelled.\n")


if __name__ == "__main__":
    reset_player_data()
