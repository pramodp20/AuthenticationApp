import tkinter as tk
import pyotp
import pyperclip
from key import SECRET_KEY_DIT, SECRET_KEY_USB
# Replace these with your actual TOTP secret keys


# Timer duration in seconds
TIMER_DURATION = 30

def generate_totp(secret):
    """Generate TOTP using the provided secret key."""
    totp = pyotp.TOTP(secret)
    return totp.now()

def copy_to_clipboard(code, button, label):
    """Copy the code to the clipboard and temporarily change the button text."""
    pyperclip.copy(code)
    button.config(text="Copied!")
    # Reset the button text after 5 seconds
    root.after(5000, lambda: button.config(text=f"Copy {label} TOTP"))

def update_totps_and_timer():
    """Update the TOTP labels and timer every second."""
    global countdown
    
    remaining_time.set(f"Time remaining: {countdown} seconds")
    
    # If the countdown reaches zero, refresh TOTPs and reset the timer
    if countdown == 0:
        totp_dit.set(generate_totp(SECRET_KEY_DIT))
        totp_usb.set(generate_totp(SECRET_KEY_USB))
        reset_timer()
    else:
        countdown -= 1

    # Schedule the next update after 1 second
    root.after(1000, update_totps_and_timer)

def reset_timer():
    """Reset the countdown timer to 30 seconds."""
    global countdown
    countdown = TIMER_DURATION

# Create the main application window
root = tk.Tk()
root.title("TOTP Generator")
root.geometry("400x200")

root.attributes("-topmost", True)

# Variables to store the generated TOTP codes and countdown timer
totp_dit = tk.StringVar()
totp_usb = tk.StringVar()
remaining_time = tk.StringVar()

# Initial countdown value
countdown = TIMER_DURATION

# DIT row
label_dit = tk.Label(root, text="DIT:", font=("Arial", 12))
label_dit.grid(row=0, column=0, padx=5, pady=10)
totp_label_dit = tk.Label(root, textvariable=totp_dit, font=("Arial", 14), fg="blue")
totp_label_dit.grid(row=0, column=1, padx=5, pady=10)
copy_button_dit = tk.Button(root, text="Copy DIT TOTP", command=lambda: copy_to_clipboard(totp_dit.get(), copy_button_dit, "DIT"))
copy_button_dit.grid(row=0, column=2, padx=5, pady=10)

# USB row
label_usb = tk.Label(root, text="USB:", font=("Arial", 12))
label_usb.grid(row=1, column=0, padx=5, pady=10)
totp_label_usb = tk.Label(root, textvariable=totp_usb, font=("Arial", 14), fg="blue")
totp_label_usb.grid(row=1, column=1, padx=5, pady=10)
copy_button_usb = tk.Button(root, text="Copy USB TOTP", command=lambda: copy_to_clipboard(totp_usb.get(), copy_button_usb, "USB"))
copy_button_usb.grid(row=1, column=2, padx=5, pady=10)

# Timer row
timer_label = tk.Label(root, textvariable=remaining_time, font=("Arial", 12))
timer_label.grid(row=2, column=0, columnspan=3, pady=10)

# Initialize the first TOTP codes and start the timer
totp_dit.set(generate_totp(SECRET_KEY_DIT))
totp_usb.set(generate_totp(SECRET_KEY_USB))
reset_timer()
update_totps_and_timer()

# Run the main event loop
root.mainloop()
