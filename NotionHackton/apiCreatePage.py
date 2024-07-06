import requests
import json

def create_notion_page( new_title, new_groups):
    page_id = "d3096f18-d46f-49f1-813e-e9d8d106bba5"
    # URL de la API de Notion para actualizar una página
    url = f"https://api.notion.com/v1/pages/{page_id}"
    api_key = "secret_mO0qZS4zTkRI3HfdB82DJeLc1OI9KLXIpV8nLnxcHiz"
    
    # Encabezados necesarios para la solicitud
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "Notion-Version": "2022-06-28"
    }

    # Datos para actualizar la página
    update_page_body = {
        "properties": {
            "Requerimiento": {
                "title": [
                    {
                        "type": "text",
                        "text": {
                            "content": new_title
                        }
                    }
                ]
            },
            "Grupo": {
                "multi_select": [
                    {"name": group} for group in new_groups
                ]
            }
        }
    }

    # Haciendo la solicitud PATCH para actualizar la página
    response = requests.patch(url, headers=headers, json=update_page_body)

    # Comprobando la respuesta
    if response.status_code == 200:
        print("Página actualizada exitosamente!")
        return response.json()
    else:
        print("Error al actualizar la página")
        print(response.text)
        return None

# Llamar a la función

# new_title = "tema uno actualizado"
# new_groups = ["Calidades", "Nuevo Grupo"]

# result = create_notion_page( new_title, new_groups)

# if result:
#     print(json.dumps(result, indent=4))
