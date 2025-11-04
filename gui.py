'''
GUI Interface for Shine On, Idol!
Simple Tkinter-based graphical interface
'''

import tkinter as tk
from tkinter import messagebox
from typing import TYPE_CHECKING
import os

try:
    from PIL import Image, ImageTk
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False
    print("Warning: PIL not available. Images will not be displayed.")

from player import Player
from config import RARITY_SYMBOLS

if TYPE_CHECKING:
    from idol_card import IdolCard


class IdolGameGUI:
    '''Main GUI window for the idol gacha game.'''
    
    def __init__(self, root: tk.Tk) -> None:
        '''
        Initialize the GUI with main window.
        
        Parameters:
            root (tk.Tk): The main Tkinter window
        '''
        self.root = root
        self.root.title("✨ Shine On, Idol! ✨")
        self.root.geometry("800x600")
        self.root.resizable(False, False)
        
        # Initialize player
        self.player = Player()
        is_new = not self.player.load_from_file()
        
        # Images directory (no caching)
        self.images_dir = "images"
        
        # Window references to prevent duplicates
        self.collection_window = None
        self.profiles_window = None
        
        # Set up GUI
        self.setup_styles()
        self.create_widgets()
        self.update_display()
        
        # Show welcome message
        if is_new:
            messagebox.showinfo(
                "Welcome!",
                "🎤 Welcome to Shine On, Idol!\n\n"
                "✨ You're now an idol producer!\n"
                "💼 Draw cards and build your dream team!"
            )
        else:
            # Welcome back message for returning players
            collection_count = len(self.player.collection)
            messagebox.showinfo(
                "Welcome Back!",
                f"🌟 Welcome back, Producer!\n\n"
                f"📚 Collection: {collection_count}/26 idols\n"
                f"💰 Coins: {self.player.coins}\n\n"
                f"✨ Ready to continue your journey?"
            )
    
    def setup_styles(self) -> None:
        '''Configure colors and styles for the GUI.'''
        self.colors = {
            'bg': '#FFE4E1',  # Misty Rose
            'frame_bg': '#FFF0F5',  # Lavender Blush
            'button_bg': '#FFB6C1',  # Light Pink
            'button_active': '#FF69B4',  # Hot Pink
            'text': '#4B0082',  # Indigo
        }
        
        self.root.configure(bg=self.colors['bg'])
    
    def load_idol_image(self, idol_name: str, size: tuple = (150, 150)) -> ImageTk.PhotoImage | None:
        '''
        Load idol portrait image from images folder.
        
        Parameters:
            idol_name (str): Name of the idol
            size (tuple): Max image size (width, height)
        
        Returns:
            ImageTk.PhotoImage or None: The loaded image or None if failed
        '''
        if not PIL_AVAILABLE:
            return None
        
        # Try to load idol-specific image (support both .png and .jpg)
        idol_name_lower = idol_name.lower()
        image_path = None
        
        # Try different image formats
        for ext in ['.png', '.jpg', '.jpeg']:
            test_path = os.path.join(self.images_dir, f"{idol_name_lower}{ext}")
            if os.path.exists(test_path):
                image_path = test_path
                break
        
        # If not found, try default images
        if image_path is None:
            for ext in ['.png', '.jpg', '.jpeg']:
                test_path = os.path.join(self.images_dir, f"default{ext}")
                if os.path.exists(test_path):
                    image_path = test_path
                    break
        
        # If still not found, return None
        if image_path is None:
            return None
        
        try:
            # Load image
            img = Image.open(image_path)
            
            # Calculate new size maintaining aspect ratio
            img.thumbnail(size, Image.Resampling.LANCZOS)
            
            photo = ImageTk.PhotoImage(img)
            return photo
        except Exception as e:
            print(f"Error loading image for {idol_name}: {e}")
            return None
    
    def create_widgets(self) -> None:
        '''Create all GUI widgets.'''
        # Title
        title_label = tk.Label(
            self.root,
            text="✨ SHINE ON, IDOL! ✨",
            font=("Arial", 24, "bold"),
            bg=self.colors['bg'],
            fg=self.colors['text']
        )
        title_label.pack(pady=20)
        
        # Status Frame
        self.create_status_frame()
        
        # Action Buttons Frame
        self.create_action_buttons()
        
        # Bottom Buttons
        self.create_bottom_buttons()
    
    def create_status_frame(self) -> None:
        '''Create the player status display frame.'''
        status_frame = tk.Frame(
            self.root,
            bg=self.colors['frame_bg'],
            relief=tk.RIDGE,
            borderwidth=3
        )
        status_frame.pack(pady=20, padx=50, fill=tk.BOTH)
        
        tk.Label(
            status_frame,
            text="Producer Status",
            font=("Arial", 16, "bold"),
            bg=self.colors['frame_bg'],
            fg=self.colors['text']
        ).pack(pady=10)
        
        # Coins
        self.coins_label = tk.Label(
            status_frame,
            text="",
            font=("Arial", 14),
            bg=self.colors['frame_bg']
        )
        self.coins_label.pack(pady=5)
        
        # Collection
        self.collection_label = tk.Label(
            status_frame,
            text="",
            font=("Arial", 14),
            bg=self.colors['frame_bg']
        )
        self.collection_label.pack(pady=5)
        
        # Draws
        self.draws_label = tk.Label(
            status_frame,
            text="",
            font=("Arial", 14),
            bg=self.colors['frame_bg']
        )
        self.draws_label.pack(pady=5)
    
    def create_action_buttons(self) -> None:
        '''Create the main action buttons (draw buttons).'''
        button_frame = tk.Frame(self.root, bg=self.colors['bg'])
        button_frame.pack(pady=30)
        
        # Single Draw Button
        single_btn = tk.Button(
            button_frame,
            text="🎲 Single Draw\n(10 coins)",
            font=("Arial", 14, "bold"),
            bg=self.colors['button_bg'],
            activebackground=self.colors['button_active'],
            fg=self.colors['text'],
            width=15,
            height=3,
            command=self.single_draw
        )
        single_btn.grid(row=0, column=0, padx=20)
        
        # Ten Draw Button
        ten_btn = tk.Button(
            button_frame,
            text="🎲🎲🎲 Ten-Draw\n(100 coins)\nGuaranteed Rare+",
            font=("Arial", 14, "bold"),
            bg=self.colors['button_bg'],
            activebackground=self.colors['button_active'],
            fg=self.colors['text'],
            width=15,
            height=3,
            command=self.ten_draw
        )
        ten_btn.grid(row=0, column=1, padx=20)
    
    def create_bottom_buttons(self) -> None:
        '''Create the bottom menu buttons.'''
        bottom_frame = tk.Frame(self.root, bg=self.colors['bg'])
        bottom_frame.pack(pady=20)
        
        # View Collection Button
        collection_btn = tk.Button(
            bottom_frame,
            text="📚 View Collection",
            font=("Arial", 12),
            bg=self.colors['button_bg'],
            activebackground=self.colors['button_active'],
            width=20,
            command=self.view_collection
        )
        collection_btn.grid(row=0, column=0, padx=10, pady=5)
        
        # View Profiles Button
        profiles_btn = tk.Button(
            bottom_frame,
            text="📖 Idol Profiles",
            font=("Arial", 12),
            bg=self.colors['button_bg'],
            activebackground=self.colors['button_active'],
            width=20,
            command=self.view_profiles
        )
        profiles_btn.grid(row=0, column=1, padx=10, pady=5)
        
        # Help Button
        help_btn = tk.Button(
            bottom_frame,
            text="❓ Help",
            font=("Arial", 12),
            bg=self.colors['button_bg'],
            activebackground=self.colors['button_active'],
            width=20,
            command=self.show_help
        )
        help_btn.grid(row=1, column=0, padx=10, pady=5)
        
        # Reset Data Button
        reset_btn = tk.Button(
            bottom_frame,
            text="🔄 Reset Data",
            font=("Arial", 12),
            bg=self.colors['button_bg'],
            activebackground=self.colors['button_active'],
            width=20,
            command=self.reset_data
        )
        reset_btn.grid(row=1, column=1, padx=10, pady=5)
        
        # Save & Exit Button
        exit_btn = tk.Button(
            bottom_frame,
            text="💾 Save & Exit",
            font=("Arial", 12),
            bg=self.colors['button_bg'],
            activebackground=self.colors['button_active'],
            width=20,
            command=self.save_and_exit
        )
        exit_btn.grid(row=2, column=0, columnspan=2, padx=10, pady=5)
    
    def update_display(self) -> None:
        '''Update all display labels with current player data.'''
        self.coins_label.config(text=f"💰 Coins: {self.player.coins}")
        self.collection_label.config(
            text=f"📚 Collection: {len(self.player.collection)}/26 idols"
        )
        self.draws_label.config(text=f"🎲 Total Draws: {self.player.total_draws}")
    
    def single_draw(self) -> None:
        '''Handle single draw button click.'''
        try:
            idol, is_duplicate, refund, bankruptcy = self.player.single_draw()
            
            # Show bankruptcy message if triggered
            if bankruptcy:
                messagebox.showinfo(
                    "💰 Bankruptcy Protection!",
                    f"You didn't have enough coins for a draw!\n\n"
                    f"🎁 Here's 50 coins to help you continue!\n"
                    f"Keep shining, Producer!"
                )

            self.show_draw_result(idol, is_duplicate, refund)
            self.update_display()

            # Auto-save after each draw
            self.player.save_to_file()

            # Check if collection is complete
            if len(self.player.collection) == 26 and not is_duplicate:
                messagebox.showinfo(
                    "🎉 CONGRATULATIONS! 🎉",
                    "✨ You've collected all 26 idols! ✨\n\n"
                    "🌟 Amazing work, Producer!\n"
                    "💪 Continue playing to level up your idols!"
                )
        except Exception as e:
            messagebox.showerror("Error", f"Draw failed: {e}")

    def ten_draw(self) -> None:
        '''Handle ten-draw button click.'''
        try:
            results, bankruptcy = self.player.ten_draw()

            # Show bankruptcy message if triggered
            if bankruptcy:
                messagebox.showinfo(
                    "💰 Bankruptcy Protection!",
                    f"You didn't have enough coins for a ten-draw!\n\n"
                    f"🎁 Here's 100 coins to help you continue!\n"
                    f"Keep shining, Producer!"
                )

            # Check if we just completed the collection
            new_idols = [r for r in results if not r[1]]  # Get non-duplicates
            collection_completed = len(self.player.collection) == 26 and len(new_idols) > 0

            self.show_ten_draw_results(results)
            self.update_display()

            # Auto-save after each draw
            self.player.save_to_file()

            # Show completion message after results
            if collection_completed:
                messagebox.showinfo(
                    "🎉 CONGRATULATIONS! 🎉",
                    "✨ You've collected all 26 idols! ✨\n\n"
                    "🌟 Amazing work, Producer!\n"
                    "💪 Continue playing to level up your idols!"
                )
        except Exception as e:
            messagebox.showerror("Error", f"Draw failed: {e}")

    def show_draw_result(self, idol: 'IdolCard', is_duplicate: bool, refund: int) -> None:
        '''
        Display single draw result in a popup window.

        Parameters:
            idol (IdolCard): The drawn idol card
            is_duplicate (bool): Whether it's a duplicate
            refund (int): Refund amount if duplicate
        '''
        result_window = tk.Toplevel(self.root)
        result_window.title("Draw Result")
        result_window.geometry("450x700")
        result_window.configure(bg=self.colors['frame_bg'])

        # Make it modal - user must close before continuing
        result_window.transient(self.root)
        result_window.grab_set()

        if is_duplicate:
            tk.Label(
                result_window,
                text="🔄 Duplicate!",
                font=("Arial", 18, "bold"),
                bg=self.colors['frame_bg'],
                fg="orange"
            ).pack(pady=10)

            tk.Label(
                result_window,
                text=f"{idol.name} leveled up to Lv.{idol.level}!",
                font=("Arial", 14),
                bg=self.colors['frame_bg']
            ).pack(pady=5)
        else:
            tk.Label(
                result_window,
                text="🎉 NEW IDOL!",
                font=("Arial", 18, "bold"),
                bg=self.colors['frame_bg'],
                fg="green"
            ).pack(pady=10)

        # Always show refund amount
        tk.Label(
            result_window,
            text=f"💰 Refund: +{refund} coins",
            font=("Arial", 12),
            bg=self.colors['frame_bg']
        ).pack(pady=5)

        # Display idol image
        idol_image = self.load_idol_image(idol.name, size=(150, 150))
        if idol_image:
            image_label = tk.Label(
                result_window,
                image=idol_image,
                bg=self.colors['frame_bg']
            )
            image_label.image = idol_image  # Keep a reference
            image_label.pack(pady=10)

        # Idol info
        symbol = RARITY_SYMBOLS.get(idol.rarity, "⭐")
        tk.Label(
            result_window,
            text=f"{symbol} {idol.rarity}",
            font=("Arial", 14, "bold"),
            bg=self.colors['frame_bg']
        ).pack(pady=5)

        tk.Label(
            result_window,
            text=idol.name,
            font=("Arial", 16, "bold"),
            bg=self.colors['frame_bg'],
            fg=self.colors['text']
        ).pack(pady=5)

        tk.Label(
            result_window,
            text=f"Lv.{idol.level} | {idol.fans:,} fans",
            font=("Arial", 12),
            bg=self.colors['frame_bg']
        ).pack(pady=5)

        tk.Label(
            result_window,
            text=f"💫 Mood: {idol.mood}",
            font=("Arial", 11),
            bg=self.colors['frame_bg']
        ).pack(pady=2)

        tk.Label(
            result_window,
            text=f"🎨 Color: {idol.color}",
            font=("Arial", 11),
            bg=self.colors['frame_bg']
        ).pack(pady=2)

        tk.Label(
            result_window,
            text=f"🎯 Hobby: {idol.hobby}",
            font=("Arial", 11),
            bg=self.colors['frame_bg']
        ).pack(pady=2)

        tk.Label(
            result_window,
            text=f'📝 "{idol.description}"',
            font=("Arial", 10),
            bg=self.colors['frame_bg'],
            wraplength=350
        ).pack(pady=10)

        # Reminder to close window - make it prominent
        tk.Label(
            result_window,
            text="⚠️ Please close this window to continue ⚠️",
            font=("Arial", 12, "bold"),
            bg=self.colors['frame_bg'],
            fg="red"
        ).pack(pady=10)

        # Close button
        tk.Button(
            result_window,
            text="OK",
            font=("Arial", 12),
            bg=self.colors['button_bg'],
            command=result_window.destroy,
            width=10
        ).pack(pady=10)

    def show_ten_draw_results(self, results: list) -> None:
        '''
        Display ten-draw results in a popup window.

        Parameters:
            results (list): List of (idol, is_duplicate, refund) tuples
        '''
        result_window = tk.Toplevel(self.root)
        result_window.title("Ten-Draw Results")
        result_window.geometry("650x700")
        result_window.configure(bg=self.colors['frame_bg'])

        # Make it modal - user must close before continuing
        result_window.transient(self.root)
        result_window.grab_set()

        tk.Label(
            result_window,
            text="🎲🎲🎲 TEN-DRAW RESULTS! 🎲🎲🎲",
            font=("Arial", 16, "bold"),
            bg=self.colors['frame_bg'],
            fg=self.colors['text']
        ).pack(pady=10)

        # Create scrollable frame
        canvas = tk.Canvas(result_window, bg=self.colors['frame_bg'])
        scrollbar = tk.Scrollbar(result_window, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=self.colors['frame_bg'])

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        # Display results
        new_count = 0
        duplicate_count = 0
        total_refund = 0

        for i, (idol, is_dup, refund) in enumerate(results, 1):
            status = "🔄 DUP" if is_dup else "🎉 NEW"
            symbol = RARITY_SYMBOLS.get(idol.rarity, "⭐")

            result_text = f"{i:2d}. {status} | {symbol} {idol.name} ({idol.rarity})"

            tk.Label(
                scrollable_frame,
                text=result_text,
                font=("Arial", 11),
                bg=self.colors['frame_bg'],
                anchor="w"
            ).pack(fill=tk.X, padx=20, pady=3)

            if is_dup:
                duplicate_count += 1
                total_refund += refund
            else:
                new_count += 1

        canvas.pack(side="top", fill="both", expand=True, padx=10, pady=(0, 10))
        scrollbar.pack(side="right", fill="y", before=canvas)

        # Summary - moved to bottom with horizontal layout
        summary_frame = tk.Frame(result_window, bg=self.colors['frame_bg'])
        summary_frame.pack(side="bottom", fill="x", pady=15)

        tk.Label(
            summary_frame,
            text=f"📊 Summary: {new_count} new, {duplicate_count} duplicates",
            font=("Arial", 13, "bold"),
            bg=self.colors['frame_bg']
        ).pack(pady=3)

        # Always show total refund with green text color
        tk.Label(
            summary_frame,
            text=f"💰 Total refund: +{total_refund} coins",
            font=("Arial", 14, "bold"),
            bg=self.colors['frame_bg'],
            fg="green"
        ).pack(pady=5)

        # Reminder to close window - make it prominent
        tk.Label(
            summary_frame,
            text="⚠️ Please close this window to continue ⚠️",
            font=("Arial", 12, "bold"),
            bg=self.colors['frame_bg'],
            fg="red"
        ).pack(pady=10)

        # Close button
        tk.Button(
            summary_frame,
            text="OK",
            font=("Arial", 12),
            bg=self.colors['button_bg'],
            command=result_window.destroy,
            width=10
        ).pack(pady=5)

    def view_collection(self) -> None:
        '''Open collection view window.'''
        # Check if window already exists
        if self.collection_window and self.collection_window.winfo_exists():
            self.collection_window.lift()  # Bring to front
            self.collection_window.focus_force()
            return

        if not self.player.collection:
            messagebox.showinfo(
                "Empty Collection",
                "📚 Your collection is empty!\n\n"
                "💡 Try drawing some idols first!"
            )
            return

        # Create collection window
        self.collection_window = tk.Toplevel(self.root)
        self.collection_window.title("Your Idol Collection")
        self.collection_window.geometry("750x550")
        self.collection_window.configure(bg=self.colors['frame_bg'])

        # Make it modal - user must close before continuing
        self.collection_window.transient(self.root)
        self.collection_window.grab_set()

        tk.Label(
            self.collection_window,
            text="📚 YOUR IDOL COLLECTION",
            font=("Arial", 16, "bold"),
            bg=self.colors['frame_bg'],
            fg=self.colors['text']
        ).pack(pady=10)

        # Main content frame
        content_frame = tk.Frame(self.collection_window, bg=self.colors['frame_bg'])
        content_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        # Left side - scrollable list
        list_frame = tk.Frame(content_frame, bg=self.colors['frame_bg'])
        list_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        canvas = tk.Canvas(list_frame, bg=self.colors['frame_bg'])
        scrollbar = tk.Scrollbar(list_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=self.colors['frame_bg'])

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        # Display idols
        idols = self.player.get_collection_list("rarity")
        for i, idol in enumerate(idols, 1):
            symbol = RARITY_SYMBOLS.get(idol.rarity, "⭐")
            idol_text = f"{i:2d}. {symbol} {idol.name} | Lv.{idol.level} | {idol.fans:,} fans"

            tk.Label(
                scrollable_frame,
                text=idol_text,
                font=("Arial", 11),
                bg=self.colors['frame_bg'],
                anchor="w"
            ).pack(fill=tk.X, padx=10, pady=3)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Right side - statistics (vertically centered)
        stats_frame = tk.Frame(content_frame, bg=self.colors['frame_bg'])
        stats_frame.pack(side=tk.RIGHT, padx=20)

        # Add spacer to push stats to center
        tk.Frame(stats_frame, bg=self.colors['frame_bg'], height=50).pack()

        total_fans = self.player.get_total_fans()
        stats_text = (
            f"📊 Total: {len(self.player.collection)}/26 idols\n"
            f"👥 Total Fans: {total_fans:,}\n"
            f"⭐ Collection Rate: {len(self.player.collection)/26*100:.1f}%"
        )

        tk.Label(
            stats_frame,
            text=stats_text,
            font=("Arial", 11, "bold"),
            bg=self.colors['frame_bg'],
            justify=tk.LEFT
        ).pack()

        # Close button
        tk.Button(
            self.collection_window,
            text="Close",
            font=("Arial", 12),
            bg=self.colors['button_bg'],
            command=self.collection_window.destroy,
            width=10
        ).pack(pady=10)

    def view_profiles(self) -> None:
        '''Open idol profiles window.'''
        # Check if window already exists
        if self.profiles_window and self.profiles_window.winfo_exists():
            self.profiles_window.lift()  # Bring to front
            self.profiles_window.focus_force()
            return

        if not self.player.collection:
            messagebox.showinfo(
                "Empty Collection",
                "📚 Your collection is empty!\n\n"
                "💡 Draw some idols first to see their profiles!"
            )
            return

        # Create profiles window
        self.profiles_window = tk.Toplevel(self.root)
        self.profiles_window.title("Idol Profiles")
        self.profiles_window.geometry("700x650")
        self.profiles_window.configure(bg=self.colors['frame_bg'])

        # Make it modal - user must close before continuing
        self.profiles_window.transient(self.root)
        self.profiles_window.grab_set()

        tk.Label(
            self.profiles_window,
            text="📖 IDOL PROFILES - DETAILED VIEW",
            font=("Arial", 16, "bold"),
            bg=self.colors['frame_bg'],
            fg=self.colors['text']
        ).pack(pady=10)

        tk.Label(
            self.profiles_window,
            text="Select an idol to view their full profile:",
            font=("Arial", 12),
            bg=self.colors['frame_bg']
        ).pack(pady=5)

        # Create listbox
        listbox_frame = tk.Frame(self.profiles_window, bg=self.colors['frame_bg'])
        listbox_frame.pack(pady=10, padx=20, fill=tk.BOTH, expand=True)

        scrollbar = tk.Scrollbar(listbox_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        listbox = tk.Listbox(
            listbox_frame,
            font=("Arial", 11),
            yscrollcommand=scrollbar.set,
            height=15
        )
        listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=listbox.yview)

        # Populate listbox
        idols = self.player.get_collection_list("rarity")
        for i, idol in enumerate(idols):
            listbox.insert(tk.END, idol.get_compact_profile())

        def show_idol_detail():
            selection = listbox.curselection()
            if not selection:
                messagebox.showwarning("No Selection", "Please select an idol first!")
                return

            idx = selection[0]
            idol = idols[idx]

            # Create profile detail window
            detail_window = tk.Toplevel(self.profiles_window)
            detail_window.title(f"{idol.name}'s Profile")
            detail_window.geometry("500x700")
            detail_window.configure(bg=self.colors['frame_bg'])

            # Make it modal
            detail_window.transient(self.profiles_window)
            detail_window.grab_set()

            # Title
            symbol = RARITY_SYMBOLS.get(idol.rarity, "⭐")
            tk.Label(
                detail_window,
                text=f"{symbol} {idol.name}'s Profile {symbol}",
                font=("Arial", 18, "bold"),
                bg=self.colors['frame_bg'],
                fg=self.colors['text']
            ).pack(pady=15)

            # Display idol image (larger size for profile)
            idol_image = self.load_idol_image(idol.name, size=(250, 250))
            if idol_image:
                image_label = tk.Label(
                    detail_window,
                    image=idol_image,
                    bg=self.colors['frame_bg']
                )
                image_label.image = idol_image  # Keep reference
                image_label.pack(pady=10)
            else:
                # Placeholder if no image
                tk.Label(
                    detail_window,
                    text="🎭",
                    font=("Arial", 80),
                    bg=self.colors['frame_bg']
                ).pack(pady=10)

            # Rarity and name
            tk.Label(
                detail_window,
                text=f"{symbol} {idol.rarity}",
                font=("Arial", 14, "bold"),
                bg=self.colors['frame_bg']
            ).pack(pady=5)

            # Level and fans
            tk.Label(
                detail_window,
                text=f"Level: {idol.level} | Fans: {idol.fans:,}",
                font=("Arial", 12),
                bg=self.colors['frame_bg']
            ).pack(pady=5)

            # Personality traits
            traits_frame = tk.Frame(detail_window, bg=self.colors['frame_bg'])
            traits_frame.pack(pady=10)

            tk.Label(
                traits_frame,
                text=f"💫 Mood: {idol.mood}",
                font=("Arial", 11),
                bg=self.colors['frame_bg']
            ).pack()

            tk.Label(
                traits_frame,
                text=f"🎨 Color: {idol.color}",
                font=("Arial", 11),
                bg=self.colors['frame_bg']
            ).pack()

            tk.Label(
                traits_frame,
                text=f"🎯 Hobby: {idol.hobby}",
                font=("Arial", 11),
                bg=self.colors['frame_bg']
            ).pack()

            # Description
            tk.Label(
                detail_window,
                text="📝 Profile:",
                font=("Arial", 11, "bold"),
                bg=self.colors['frame_bg']
            ).pack(pady=(10, 5))

            tk.Label(
                detail_window,
                text=f'"{idol.description}"',
                font=("Arial", 10, "italic"),
                bg=self.colors['frame_bg'],
                wraplength=380,
                justify=tk.CENTER
            ).pack(pady=5)

            # Close button
            tk.Button(
                detail_window,
                text="Close",
                font=("Arial", 12),
                bg=self.colors['button_bg'],
                command=detail_window.destroy,
                width=10
            ).pack(pady=15)

        # View button
        tk.Button(
            self.profiles_window,
            text="View Profile",
            font=("Arial", 12),
            bg=self.colors['button_bg'],
            command=show_idol_detail,
            width=15
        ).pack(pady=5)

        # Close button
        tk.Button(
            self.profiles_window,
            text="Close",
            font=("Arial", 12),
            bg=self.colors['button_bg'],
            command=self.profiles_window.destroy,
            width=15
        ).pack(pady=5)

    def show_modal_info(self, title: str, message: str) -> None:
        '''
        Show modal information dialog that blocks main window interaction.

        Parameters:
            title (str): Dialog title
            message (str): Dialog message
        '''
        # Create modal info window
        info_window = tk.Toplevel(self.root)
        info_window.title(title)
        info_window.geometry("400x200")
        info_window.configure(bg=self.colors['frame_bg'])

        # Make it modal
        info_window.transient(self.root)
        info_window.grab_set()

        # Message
        tk.Label(
            info_window,
            text=message,
            font=("Arial", 11),
            bg=self.colors['frame_bg'],
            wraplength=350,
            justify=tk.CENTER
        ).pack(pady=30)

        # OK button
        tk.Button(
            info_window,
            text="OK",
            font=("Arial", 12),
            bg=self.colors['button_bg'],
            command=info_window.destroy,
            width=10
        ).pack(pady=10)

    def show_help(self) -> None:
        '''Display help window with game instructions.'''
        help_window = tk.Toplevel(self.root)
        help_window.title("Help - Game Guide")
        help_window.geometry("500x600")
        help_window.configure(bg=self.colors['frame_bg'])

        # Make it modal
        help_window.transient(self.root)
        help_window.grab_set()

        # Title
        tk.Label(
            help_window,
            text="❓ HOW TO PLAY ❓",
            font=("Arial", 18, "bold"),
            bg=self.colors['frame_bg'],
            fg=self.colors['text']
        ).pack(pady=15)

        # Help content
        help_text = """
1. GAME BASICS:
   You are an idol producer! Draw cards to collect all 26 idols.

2. DRAWING COSTS:
   • Single Draw: 10 coins
   • Ten-Draw: 100 coins (Guaranteed Rare or better!)

3. RARITY LEVELS:
   • ⭐ Common (50%) - 10 idols
   • ⭐⭐ Rare (35%) - 8 idols
   • ⭐⭐⭐ Epic (13%) - 5 idols
   • ⭐⭐⭐⭐ Legendary (2%) - 3 idols

4. DUPLICATES:
   When you draw a duplicate, the idol levels up!
   You also get a coin refund:
   • Common: 2 coins
   • Rare: 4 coins
   • Epic: 6 coins
   • Legendary: 8 coins

5. BANKRUPTCY PROTECTION:
   If you run out of coins, you'll get a bonus:
   • Single draw: +50 coins
   • Ten-draw: +100 coins

6. FEATURES:
   • Collection: View all your collected idols
   • Profiles: See detailed idol information
   • Reset Data: Delete all progress and start fresh
   • Auto-Save: Progress saved after every draw
"""

        tk.Label(
            help_window,
            text=help_text,
            font=("Arial", 10),
            bg=self.colors['frame_bg'],
            justify=tk.LEFT
        ).pack(padx=20, pady=10)

        # Close button
        tk.Button(
            help_window,
            text="Close",
            font=("Arial", 12),
            bg=self.colors['button_bg'],
            command=help_window.destroy,
            width=10
        ).pack(pady=10)

    def reset_data(self) -> None:
        '''Reset all player data after confirmation.'''
        # Show warning with confirmation
        response = messagebox.askyesno(
            "Reset Data",
            "⚠️ WARNING ⚠️\n\n"
            "This will delete ALL game progress:\n"
            "• All collected idols\n"
            "• Coin balance\n"
            "• Draw statistics\n\n"
            "Are you sure you want to reset?"
        )

        if response:
            try:
                # Delete save file
                if os.path.exists("player_data.txt"):
                    os.remove("player_data.txt")

                # Show success message and exit
                messagebox.showinfo(
                    "Reset Complete",
                    "✅ All data has been reset!\n\n"
                    "The game will now exit.\n"
                    "Please restart to start fresh."
                )

                # Exit game
                self.root.quit()

            except Exception as e:
                messagebox.showerror(
                    "Error",
                    f"Failed to reset data:\n{e}"
                )

    def save_and_exit(self) -> None:
        '''Save game and exit.'''
        self.player.save_to_file(silent=False)
        self.root.quit()