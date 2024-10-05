#!/usr/bin/env python3
import tkinter as tk
import time
import random
import pygame  # For playing sound

class FNaF3RebootPanel(tk.Tk):
    def __init__(self):
        super().__init__()
        self.attributes('-fullscreen', True)
        self.BOOT_TIME = 5 #How long a reboot takes
        
        # Initialize pygame mixer for sound playback
        pygame.mixer.init()
        self.alarm_sound = pygame.mixer.Sound("alarm.wav")

        # Window setup
        self.title("FNaF 3 Reboot Terminal")
        self.geometry("500x400")
        self.configure(bg="black")

        # Monospace font for terminal-like appearance
        #self.font = ("Courier", 12)
        self.font = ("Classic Console Neue", 25)
        # Index to keep track of the selected system
        self.current_selection = 0
        self.options = ["audio devices", "camera system", "ventilation", "Reboot All Systems"]

        # Track error state for each system (True if the system has an error)
        self.error_state = [False, False, False, False]  # First three for individual systems, last for "Reboot All"

        # Title label
        self.panel_title = tk.Label(self, text="system restart\r\nmenu>>>", fg="green", bg="black", font=self.font, anchor="w")
        self.panel_title.pack(pady=10, anchor="w")

        # System buttons as labels for terminal feel
        self.option_labels = []
        for i, option in enumerate(self.options):
            label = tk.Label(self, text=f"      {option}", bg="black", fg="green", font=self.font, anchor="w")
            label.pack(pady=5, anchor="w", padx=20)
            self.option_labels.append(label)

        # Status label - shows the current operation (e.g., rebooting)
        self.status_label = tk.Label(self, text=">>> all systems operational...", fg="green", bg="black", font=self.font)
        self.status_label.pack(pady=5, anchor="w", padx=20)

        # History label - shows reboot completion messages (simulates terminal output)
        self.history_label = tk.Label(self, text="", fg="green", bg="black", font=self.font, anchor="w", justify="left")
        self.history_label.pack(pady=5, anchor="w", padx=20)

        # Cursor label for the blinking effect
        self.cursor_label = tk.Label(self, text="|", fg="lime", bg="black", font=self.font)
        self.cursor_label.pack(anchor="w", padx=20)

        # Start blinking cursor
        self.blink_cursor()

        # Highlight the first option initially
        self.update_selection()

        # Bind the arrow keys for navigation
        self.bind("<Up>", self.move_up)
        self.bind("<Down>", self.move_down)
        self.bind("<Return>", self.select_option)

        # Store history of reboot messages
        self.reboot_history = []

        # Start the error generation process
        self.generate_random_errors()

    def update_selection(self):
        # Reset all labels to normal green without the arrow and handle errors
        for i, label in enumerate(self.option_labels):
            label_text = f"      {self.options[i]}"  # Normal text with proper indentation
            if self.error_state[i]:  # If there's an error, append "ERROR" in red
                label_text += "  [ERROR]"
            label.config(text=label_text, fg="green" if not self.error_state[i] else "red")

        # Highlight the current selection and add ">>>"
        selected_label_text = f">>>   {self.options[self.current_selection]}"
        if self.error_state[self.current_selection]:
            selected_label_text += "  [ERROR]"
        self.option_labels[self.current_selection].config(text=selected_label_text, fg="lime")

    def move_up(self, event):
        # Move selection up
        if self.current_selection > 0:
            self.current_selection -= 1
            self.update_selection()

    def move_down(self, event):
        # Move selection down
        if self.current_selection < len(self.options) - 1:
            self.current_selection += 1
            self.update_selection()

    def select_option(self, event):
        # Activate the selected option
        selected_option = self.options[self.current_selection]
        if "audio" in selected_option:
            self.reboot_system(0, "Audio Devices")
        elif "camera" in selected_option:
            self.reboot_system(1, "Camera System")
        elif "ventilation" in selected_option:
            self.reboot_system(2, "Ventilation")
        elif "Reboot All" in selected_option:
            self.reboot_all_systems()

    def reboot_system(self, index, system_name):
        # Display rebooting message
        self.status_label.config(text=f">>> Rebooting {system_name}...", fg="yellow")
        self.update()  # Update the GUI immediately to show the change
        time.sleep(self.BOOT_TIME)  # Simulate reboot process

        # Clear the error for this system if it exists
        self.error_state[index] = False

        # Stop the alarm sound if there are no more errors
        if not any(self.error_state[:3]):
            self.stop_alarm()

        # Reboot is always successful now
        self.status_label.config(text=f">>> {system_name} Reboot Complete", fg="yellow")
        self.update()  # Update the GUI immediately to show the change
        time.sleep(1)
        self.status_label.config(text=f">>> all systems operational...", fg="green")
        # Add to the reboot history
        self.reboot_history.append(f">>> {system_name} successfully rebooted.")

        # Update the system options to show error status if applicable
        self.update_selection()
        
        #   Schedule next error
        self.generate_random_errors()

    def reboot_all_systems(self):
        # Display rebooting all message
        self.status_label.config(text=">>> Rebooting All Systems...", fg="yellow")
        self.update()
        time.sleep(2)  # Simulate reboot process for all systems

        # Stop the alarm sound after all systems are rebooted
        self.stop_alarm()

        self.status_label.config(text=">>> All Systems Reboot Complete", fg="lime")
        self.update()  # Update the GUI immediately to show the change
        time.sleep(0.8)
        self.status_label.config(text=f">>> all systems operational...", fg="lime")
        
        # Clear errors for all systems
        self.error_state = [False, False, False, False]

        # Update the system options to show error status if applicable
        self.update_selection()

        #   Schedule next error
        self.generate_random_errors()

    def update_history_label(self):
        # Update the history label with the latest reboot history
        self.history_label.config(text="\n".join(self.reboot_history[-1:]))  # Show the last reboot message
        self.update()
        time.sleep(1)
        self.history_label.config(text="")

    def blink_cursor(self):
        # Blink the cursor to mimic terminal effect
        current_color = self.cursor_label.cget("fg")
        new_color = "black" if current_color == "lime" else "lime"
        self.cursor_label.config(fg=new_color)
        self.after(500, self.blink_cursor)  # Blink every 500ms

    def generate_random_errors(self):
        # Choose a random time between now and 15 seconds for the next error
        random_delay = random.randint(30000, 60000)  # Between 5 and 15 seconds
        self.after(random_delay, self.trigger_random_error)

    def trigger_random_error(self):
        # Trigger an error on a random system (audio, camera, or ventilation)
        if not any(self.error_state[:3]):  # Ensure there is no active error
            error_index = random.choice([0, 1, 2])  # Pick one of the first three systems
            self.error_state[error_index] = True
            self.update_selection()
            self.status_label.config(text=f"> ERROR: {self.options[error_index]} system error", fg="red")
            self.play_alarm()  # Play alarm when error occurs

    def play_alarm(self):
        """Play the alarm sound in a loop."""
        self.alarm_sound.play(loops=-1)  # Play continuously

    def stop_alarm(self):
        """Stop the alarm sound."""
        self.alarm_sound.stop()  # Stop sound

if __name__ == "__main__":
    app = FNaF3RebootPanel()
    app.mainloop()
