from api_request import get_package, send_api_request
from ui import clear_screen, pause

# Fetch my packages
def fetch_my_packages(api_key: str, tokens: dict):
    id_token = tokens.get("id_token")
    
    path = "api/v8/packages/quota-details"
    
    payload = {
        "is_enterprise": False,
        "lang": "en",
        "family_member_id": ""
    }
    
    print("Fetching my packages...")
    res = send_api_request(api_key, path, payload, id_token, "POST")
    if res.get("status") != "SUCCESS":
        print("Failed to fetch packages")
        return None
    
    quotas = res["data"]["quotas"]
    
    clear_screen()
    print("===============================")
    print("My Packages")
    print("===============================")
    num = 1
    for quota in quotas:
        quota_code = quota["quota_code"] # Can be used as option_code
        group_code = quota["group_code"]
        name = quota["name"]
        family_code = "N/A"
        
        print(f"fetching package no. {num} details...")
        package_details = get_package(api_key, tokens, quota_code)
        if package_details:
            family_code = package_details["package_family"]["package_family_code"]
        
        print("===============================")
        print(f"Package {num}")
        print(f"Name: {name}")
        print(f"Quota Code: {quota_code}")
        print(f"Family Code: {family_code}")
        print(f"Group Code: {group_code}")
        print("===============================")
        
        num += 1
        
    pause()
        