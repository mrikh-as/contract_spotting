import requests

url = "https://ngw.devices.sberbank.ru/api/v2/oauth"

payload = "scope=GIGACHAT_API_PERS"
headers = {
    "Content-Type": "application/x-www-form-urlencoded",
    "Accept": "application/json",
    "RqUID": "MDJjNzUyNjUtYmQxZS00ZjUzLTljNWYtNjE2YjE1MjlkZjFkOmY5YzVmNThlLWQ5YjUtNGVlNS1hMTliLWY0MTQ0OWM2N2NmMg==",
}

response = requests.request("POST", url, headers=headers, data=payload)

print(response.text)
