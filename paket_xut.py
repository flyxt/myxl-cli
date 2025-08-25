import json
from api_request import send_api_request, get_family

PACKAGE_FAMILY_CODE = "08a3b1e6-8e78-4e45-a540-b40f06871cfe"

def get_package_xut(tokens: dict):
    packages = []
    
    data = get_family(tokens, PACKAGE_FAMILY_CODE)
    package_variants = data["package_variants"]
    start_number = 1
    for variant in package_variants:
        if variant["name"] == "For Xtra Combo":
            for option in variant["package_options"]:
                if option["name"].lower() in ["vidio", "iflix", "basic"]:
                    friendly_name = option["name"]
                    
                    if friendly_name.lower() == "basic":
                        friendly_name = "Xtra Combo Unli Turbo Basic"
                    if friendly_name.lower() == "vidio":
                        friendly_name = "Unli Turbo Vidio 30 Hari"
                    if friendly_name.lower() == "iflix":
                        friendly_name = "Unli Turbo Iflix 30 Hari"
                        
                    packages.append({
                        "number": start_number,
                        "name": friendly_name,
                        "price": option["price"],
                        "code": option["package_option_code"]
                    })
                    
                    start_number += 1
    return packages