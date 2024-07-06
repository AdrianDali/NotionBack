import requests
import json

def search_notion_pages(api_key):
    # URL de la API de Notion para realizar una búsqueda
    url = "https://api.notion.com/v1/search"

    # Encabezados necesarios para la solicitud
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "Notion-Version": "2022-06-28"
    }

    # Parámetros de búsqueda
    search_params = {"filter": {"value": "page", "property": "object"}}

    # Realizar la solicitud POST para buscar páginas
    search_response = requests.post(url, json=search_params, headers=headers)

    # Comprobando la respuesta
    if search_response.status_code == 200:
        print("Búsqueda realizada exitosamente!")
        return search_response.json()
    else:
        print("Error al realizar la búsqueda")
        print(search_response.text)
        return None

# Llamar a la función
api_key = "secret_mO0qZS4zTkRI3HfdB82DJeLc1OI9KLXIpV8nLnxcHiz"
result = search_notion_pages(api_key)

if result:
    print(json.dumps(result, indent=4))
