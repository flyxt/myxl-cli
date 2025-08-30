import os, json
import sys

from api_request import *
from ui import *

def load_token(api_key: str):
    if os.path.exists("tokens.json"):
        with open("tokens.json", "r", encoding="utf8") as f:
            tokens = json.load(f)
        print("Tokens loaded successfully.")
        
        refresh_token = tokens.get("refresh_token")
        tokens = get_new_token(refresh_token)
        
        id_token = tokens.get("id_token")
        access_token = tokens.get("access_token")
        
        profile = get_profile(api_key, access_token, id_token)
        if not profile:
            print("Failed to fetch profile. Please check your tokens.")
            sys.exit(1)
        
        phone_number = profile.get("profile").get("msisdn")
        
        balance = get_balance(api_key, id_token)
        balance_remaining = balance.get("remaining")
        balance_expired_at = balance.get("expired_at")
        
        return {
            "tokens": tokens,
            "is_logged_in": True,
            "phone_number": phone_number,
            "balance": balance_remaining,
            "balance_expired_at": balance_expired_at,
        }
    
    return None

# Load API key from text file named api.key
def load_api_key() -> str:
    if os.path.exists("api.key"):
        with open("api.key", "r", encoding="utf8") as f:
            api_key = f.read().strip()
        if api_key:
            print("API key loaded successfully.")
            return api_key
        else:
            print("API key file is empty.")
            return ""
    else:
        print("API key file not found.")
        return ""
    
def save_api_key(api_key: str):
    with open("api.key", "w", encoding="utf8") as f:
        f.write(api_key)
    print("API key saved successfully.")
    
def delete_api_key():
    if os.path.exists("api.key"):
        os.remove("api.key")
        print("API key file deleted.")
    else:
        print("API key file does not exist.")

def verify_api_key(api_key: str, *, timeout: float = 10.0) -> bool:
    """
    Returns True iff the verification endpoint responds with HTTP 200.
    Any network error or non-200 is treated as invalid.
    """
    try:
        url = f"https://crypto.mashu.lol/api/verify?key={api_key}"
        resp = requests.get(url, timeout=timeout)
        if resp.status_code == 200:
            json_resp = resp.json()
            print(f"API key is valid.\nId: {json_resp.get('user_id')}\nOwner: @{json_resp.get('username')}")
            return True
        else:
            print(f"API key is invalid. Server responded with status code {resp.status_code}.")
            return False
    except requests.RequestException as e:
        print(f"Failed to verify API key: {e}")
        return False


def ensure_api_key() -> str:
    """
    Load api.key if present; otherwise prompt the user.
    Always verifies the key. Saves only if valid.
    Exits the program if invalid or empty.
    """
    # Try to load an existing key
    current = load_api_key()
    if current:
        if verify_api_key(current):
            return current
        else:
            print("Existing API key is invalid. Please enter a new one.")

    # Prompt user if missing or invalid
    api_key = input("Masukkan API key: ").strip()
    if not api_key:
        print("API key tidak boleh kosong. Menutup aplikasi.")
        sys.exit(1)

    if not verify_api_key(api_key):
        print("API key tidak valid. Menutup aplikasi.")
        delete_api_key()
        sys.exit(1)

    save_api_key(api_key)
    return api_key
