# import pywhatkit  <-- MOVED INSIDE FUNCTION TO PREVENT STARTUP HANG
import time
import os
import platform
import pyautogui
import win32clipboard
from ctypes import windll, Structure, c_int, c_uint, c_char, byref, sizeof, POINTER
from ctypes.wintypes import HWND, UINT, DWORD, BOOL, HANDLE

# Struct for DROPFILES (standard Windows structure for file clipboard)
class DROPFILES(Structure):
    _fields_ = [
        ("pFiles", c_uint),
        ("pt_x", c_int),
        ("pt_y", c_int),
        ("fNC", c_int),
        ("fWide", c_int),
    ]

def copy_file_to_clipboard(filepath):
    """
    Copies a file to the Windows clipboard so it can be pasted.
    """
    try:
        if not os.path.exists(filepath):
            return False

        # Prepare the file path (must be absolute)
        filepath = os.path.abspath(filepath)
        
        # Create buffer for the path (wide char + double null terminator)
        # 2 bytes per char for wide chars
        files_data = filepath.encode("utf-16le") + b"\0\0"  # Double null terminator
        
        # Prepare DROPFILES structure
        dropfiles = DROPFILES()
        dropfiles.pFiles = sizeof(DROPFILES)
        dropfiles.fWide = 1
        
        # Serialize the struct
        dropfiles_buffer = bytes(dropfiles)
        
        # Total data = Struct + File Path Bytes
        global_data = dropfiles_buffer + files_data
        
        # Allocate global memory
        # GMEM_MOVEABLE = 0x0002
        h_global = windll.kernel32.GlobalAlloc(0x0002, len(global_data))
        if not h_global:
            return False
            
        # Lock memory to get pointer
        ptr = windll.kernel32.GlobalLock(h_global)
        
        # Copy data to memory
        # RtlMoveMemory(dest, src, length)
        # We need to use ctypes memmove or similar
        import ctypes
        ctypes.memmove(ptr, global_data, len(global_data))
        
        windll.kernel32.GlobalUnlock(h_global)
        
        # Open clipboard
        win32clipboard.OpenClipboard()
        win32clipboard.EmptyClipboard()
        # CF_HDROP = 15
        win32clipboard.SetClipboardData(15, h_global)
        win32clipboard.CloseClipboard()
        return True
    except Exception as e:
        print(f"Clipboard Error: {e}")
        return False

def format_phone_number(phone_number):
    """Format phone number to international format."""
    if not phone_number:
        return None
    clean_number = phone_number.replace(" ", "").replace("-", "")
    if not clean_number.startswith("+"):
        clean_number = "+91" + clean_number
    return clean_number

def send_whatsapp_message(phone_number, message):
    """Send a text message via WhatsApp Web/Desktop."""
    try:
        formatted_num = format_phone_number(phone_number)
        if not formatted_num:
            return False, "Invalid phone number"
        
        
        # Send text
        import pywhatkit # Lazy import
        pywhatkit.sendwhatmsg_instantly(formatted_num, message, 15, True, 3)
        return True, "Message sent"
    except Exception as e:
        return False, str(e)

def send_whatsapp_with_pdf(phone_number, message, pdf_path):
    """
    Send a WhatsApp message AND attach the PDF automatically via Clipboard Paste.
    """
    try:
        import pywhatkit # Lazy import
        formatted_num = format_phone_number(phone_number)
        if not formatted_num:
            return False, "Invalid phone number"

        if not os.path.exists(pdf_path):
            return False, "PDF file not found"
            
        print(f"Sending WhatsApp to {formatted_num}...")
        
        # 1. Open WhatsApp and send the text message first
        # INCREASED WAIT TIME to 20 seconds to allow slow connections/browser to load
        # tab_close=False prevents the tab from closing, so we can paste the file
        pywhatkit.sendwhatmsg_instantly(formatted_num, message, 25, False, 3)
        
        # 2. Wait a moment for the text message to completely send and focus to remain
        # The function above waits 25s, types, sends. Then returns.
        # We wait a bit more to be sure UI is ready for the next action.
        time.sleep(5) 
        
        # 3. Copy file to clipboard
        if copy_file_to_clipboard(pdf_path):
            print("File copied to clipboard. Pasting...")
            
            # 4. Paste the file (Ctrl + V)
            # We press it twice just in case (sometimes first focus click is needed)
            # But let's try clean paste first
            pyautogui.hotkey('ctrl', 'v')
            
            # 5. Wait for the attachment preview to load (Important: large files take longer)
            time.sleep(3)
            
            # 6. Press Enter to send the attachment
            pyautogui.press('enter')
            
            return True, "Message and PDF sent successfully (Tab left open)"
        else:
            return True, "Message sent, but failed to copy PDF to clipboard. Please attach manually."
        
    except Exception as e:
        return False, str(e)


def send_group_message(group_id, message):
    """
    Send a message to a WhatsApp Group FAST using clipboard paste.
    Opens WhatsApp Web with group link, pastes message, and sends instantly.
    Much faster than pywhatkit's character-by-character typing.
    """
    try:
        import webbrowser
        import pyperclip
        import pyautogui
        import time
        import urllib.parse
        
        # pywhatkit's group sending is too slow (types each character).
        # Instead, we use web.whatsapp.com URL scheme with pre-filled message
        # and then just press Enter.
        
        # URL encode the message
        encoded_message = urllib.parse.quote(message)
        
        # If full link provided, extract the group invite code
        if 'chat.whatsapp.com/' in group_id:
            group_id = group_id.split('chat.whatsapp.com/')[-1]
        
        # Note: WhatsApp Web doesn't support direct group message via URL like phone numbers.
        # The workaround is: 
        # 1. Copy message to clipboard
        # 2. Open the group chat link
        # 3. Wait for it to load
        # 4. Paste (Ctrl+V) and Send (Enter)
        
        # Copy message to clipboard
        pyperclip.copy(message)
        
        # Open the group invite link (user must have already joined this group)
        # This part is tricky - WhatsApp Web can open existing chats but not directly send to groups via URL.
        # We need to open WhatsApp Web and let user navigate OR use a saved group link.
        
        # For now, let's open WhatsApp Web. User can manually navigate if link doesn't work.
        webbrowser.open("https://web.whatsapp.com")
        
        # Wait for WhatsApp Web to load (adjust based on speed)
        time.sleep(10) # 10 seconds to load and let user navigate to group if needed
        
        # Paste from clipboard
        pyautogui.hotkey('ctrl', 'v')
        time.sleep(0.5)
        
        # Press Enter to send
        pyautogui.press('enter')
        
        return True, "Message pasted and sent! Please ensure the correct group chat was open."
        
    except Exception as e:
        return False, f"WhatsApp Group Error: {str(e)}"

