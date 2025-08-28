import json
from api_request import send_api_request, get_family
from ui import clear_screen, show_package_details

def get_packages_by_family(api_key: str, tokens: dict, family_code: str):
    packages = []
    
    data = get_family(api_key, tokens, family_code)
    if not data:
        print("Failed to load family data.")
        return None
    
    
    in_package_menu = True
    while in_package_menu:
        clear_screen()
        print("--------------------------")
        print("Paket Tersedia")
        print("--------------------------")
        
        family_name = data['package_family']["name"]
        print(f"Family Name: {family_name}")
        
        package_variants = data["package_variants"]
        
        option_number = 1
        variant_number = 1
        
        for variant in package_variants:
            variant_name = variant["name"]
            print(f" Variant {variant_number}: {variant_name}")
            for option in variant["package_options"]:
                option_name = option["name"]
                
                packages.append({
                    "number": option_number,
                    "name": option_name,
                    "price": option["price"],
                    "code": option["package_option_code"]
                })
                
                print(f"{option_number}. {option_name} - Rp {option['price']}")
                
                option_number += 1
            variant_number += 1

        print("99. Kembali ke menu sebelumnya")
        pkg_choice = input("Pilih paket (nomor): ")
        if pkg_choice == "99":
            in_package_menu = False
            return None
        selected_pkg = next((p for p in packages if p["number"] == int(pkg_choice)), None)
        
        if not selected_pkg:
            print("Paket tidak ditemukan. Silakan masukan nomor yang benar.")
            continue
        
        is_done = show_package_details(api_key, tokens, selected_pkg["code"])
        if is_done:
            in_package_menu = False
            return None
        
    return packages