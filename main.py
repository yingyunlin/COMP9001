'''
Shine On, Idol! - Main Entry Point

HOW TO RUN:
1. Install required library: pip install pillow
2. Run this file: python main.py

REQUIREMENTS:
- External library: Pillow (for image display)
- This is a graphical application using Tkinter + Pillow
- Requires images/ folder with 26 idol image files

NOTE: This is the main script to run.
'''

import sys

def main():
    '''Main entry point - launches the GUI version of the game.'''
    
    print("Starting Shine On, Idol!...")
    
    try:
        # Import and run GUI
        from gui import IdolGameGUI
        import tkinter as tk
        
        root = tk.Tk()
        app = IdolGameGUI(root)
        root.mainloop()
        
    except ImportError as e:
        print(f"Error: Missing required module - {e}")
        print("Please install required packages:")
        print("  pip install pillow")
        sys.exit(1)
        
    except Exception as e:
        print(f"Error starting game: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
