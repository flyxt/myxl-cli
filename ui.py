import os
import json
import sys
from datetime import datetime
from api_request import get_otp, submit_otp, save_tokens, get_package, purchase_package

def clear_screen():
    print("clearing screen...")
    os.system('cls' if os.name == 'nt' else 'clear')

def pause():
    input("\nTekan Enter untuk lanjut...")
    
def show_banner():
    print("--------------------------")
    print("Dor XL by Flyxt9")
    print("--------------------------")
    
def show_main_menu(user_data):
    clear_screen()
    if not user_data["is_logged_in"]:
        print("--------------------------")
        print("Anda belum login")
        print("--------------------------")
        print("Menu:")
        print("1. Login")
        print("99. Tutup aplikasi")
        print("--------------------------")
    else:
        phone_number = user_data["phone_number"]
        remaining_balance = user_data["balance"]
        expired_at = user_data["balance_expired_at"]
        expired_at_dt = datetime.fromtimestamp(expired_at).strftime("%Y-%m-%d %H:%M:%S")
        
        print("--------------------------")
        print("Informasi Akun")
        print(f"Nomor: {phone_number}")
        print(f"Pulsa: Rp {remaining_balance}")
        print(f"Masa aktif: {expired_at_dt}")
        print("--------------------------")
        print("Menu:")
        print("1. Login/Ganti akun")
        print("2. Paket XUT")
        print("99. Tutup aplikasi")
        print("--------------------------")
        
def show_login_menu():
    clear_screen()
    print("--------------------------")
    print("Login ke MyXL")
    print("--------------------------")
    print("1. Request OTP")
    print("2. Submit OTP")
    print("99. Tutup aplikasi")
    print("--------------------------")
    
def login_prompt():
    clear_screen()
    print("--------------------------")
    print("Request OTP")
    print("--------------------------")
    print("Masukan nomor XL Prabayar (Contoh 6281234567890):")
    phone_number = input("Nomor: ")

    if not phone_number.startswith("628") or len(phone_number) < 10 or len(phone_number) > 14:
        print("Nomor tidak valid. Pastikan nomor diawali dengan '628' dan memiliki panjang yang benar.")
        return None

    try:
        subscriber_id = get_otp(phone_number)
        if not subscriber_id:
            return None
        print("OTP Berhasil dikirim ke nomor Anda.")
        
        otp = input("Masukkan OTP yang telah dikirim: ")
        if not otp.isdigit() or len(otp) != 6:
            print("OTP tidak valid. Pastikan OTP terdiri dari 6 digit angka.")
            pause()
            return None
        
        tokens = submit_otp(phone_number, otp)
        if not tokens:
            print("Gagal login. Periksa OTP dan coba lagi.")
            pause()
            return None
        
        save_tokens(tokens)
        print("Berhasil login!")
        
        return phone_number
    except Exception as e:
        return None
    
def show_package_menu(tokens, packages):
    in_package_menu = True
    while in_package_menu:
        clear_screen()
        print("--------------------------")
        print("Paket Tersedia")
        print("--------------------------")
        for pkg in packages:
            print(f"{pkg['number']}. {pkg['name']} - Rp {pkg['price']}")
        print("99. Kembali ke menu utama")
        print("--------------------------")
        pkg_choice = input("Pilih paket (nomor): ")
        if pkg_choice == "99":
            in_package_menu = False
            return None
        selected_pkg = next((p for p in packages if p["number"] == int(pkg_choice)), None)
        if not selected_pkg:
            print("Paket tidak ditemukan. Silakan masukan nomor yang benar.")
            continue
        
        is_done = show_package_details(tokens, selected_pkg["code"])
        if is_done:
            in_package_menu = False
            return None
    
def show_package_details(tokens, package_option_code):
    clear_screen()
    print("--------------------------")
    print("Detail Paket")
    print("--------------------------")
    package = get_package(tokens, package_option_code)
    if not package:
        print("Failed to load package details.")
        pause()
        return False
    name2 = package.get("package_detail_variant", "").get("name","") #For Xtra Combo
    price = package["package_option"]["price"]
    detail = package["package_option"]["tnc"]
    detail = detail.replace("<p>", "").replace("</p>", "").replace("<strong>", "").replace("</strong>", "").replace("<br>", "").replace("<br />", "").strip()
    name3 = package.get("package_option", {}).get("name","") #Vidio
    name1 = package.get("package_family", {}).get("name","") #Unlimited Turbo
    
    title = f"{name1} {name2} {name3}".strip()
    

    print(f"Nama: {title}")
    print(f"Harga: Rp {price}")
    print(f"SnK MyXL:\n{detail}")
    print("--------------------------")
    print("Pastikan pulsa mencukupi sebelum membeli paket.")
    choice = input("Apakah Anda yakin membeli paket ini? (y/t): ")
    if choice.lower() == 'y':
        purchase_package(tokens, package_option_code)
        input("Silahkan cek hasil pembelian di aplikasi MyXL. Tekan Enter untuk kembali.")
        return True
    else:
        print("Purchase cancelled.")
        return False
    pause()
    sys.exit(0)
