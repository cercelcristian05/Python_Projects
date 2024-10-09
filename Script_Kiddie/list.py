import requests

url = "https://cdn-0.reconshell.com/wp-content/uploads/2021/12/party-768x432.png"
file_name = "phishing_diagram.png"

response = requests.get(url)
if response.status_code == 200:
    with open(file_name, 'wb') as f:
        f.write(response.content)
    print("Imagine descărcată cu succes!")
else:
    print("Eroare la descărcare:", response.status_code)
