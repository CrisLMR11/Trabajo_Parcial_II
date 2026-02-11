import requests
import pandas as pd
import time

GITHUB_TOKEN = "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"

# Repositorio a analizar
OWNER = "pallets"
REPO = "flask"
# Cantidad de Issues/PRs a revisar
LIMIT_ISSUES = 100

def get_headers():
    return {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json"
    }

def obtener_comentarios(issue_number):
    """Descarga los comentarios individuales de un issue/PR."""
    url = f"https://api.github.com/repos/{OWNER}/{REPO}/issues/{issue_number}/comments"
    try:
        response = requests.get(url, headers=get_headers())
        if response.status_code == 200:
            return response.json()
    except Exception as e:
        print(f"Error obteniendo comentarios del issue {issue_number}: {e}")
    return []

def main():
    print(f"- Iniciando recolección de datos del repo: {OWNER}/{REPO} -")

    dataset = []

    base_url = f"https://api.github.com/repos/{OWNER}/{REPO}/issues"
    params = {
        "state": "all",
        "per_page": 100,
        "sort": "updated",
        "direction": "desc"
    }

    page = 1
    issues_procesados = 0

    while issues_procesados < LIMIT_ISSUES:
        print(f"Procesando página {page}...")
        params["page"] = page

        response = requests.get(base_url, headers=get_headers(), params=params)

        if response.status_code != 200:
            print(f"Error de conexión: {response.status_code}")
            print(response.text)
            break

        items = response.json()
        if not items:
            break # No hay más datos

        for item in items:
            if issues_procesados >= LIMIT_ISSUES:
                break

            # Identificar si es Issue o PR
            tipo_fuente = "Pull Request" if "pull_request" in item else "Issue"
            id_ref = item['number']

            # 1. Guardar el Título
            dataset.append({
                "repo": REPO,
                "id_referencia": id_ref,
                "tipo_origen": tipo_fuente,
                "tipo_mensaje": "Titulo",
                "texto": item['title']
            })

            # 2. Guardar la Descripción (Body)
            if item.get('body'):
                dataset.append({
                    "repo": REPO,
                    "id_referencia": id_ref,
                    "tipo_origen": tipo_fuente,
                    "tipo_mensaje": "Descripcion",
                    "texto": item['body']
                })

            # 3. Descargar y guardar Comentarios asociados
            comentarios = obtener_comentarios(id_ref)
            for com in comentarios:
                if com.get('body'):
                    dataset.append({
                        "repo": REPO,
                        "id_referencia": id_ref,
                        "tipo_origen": tipo_fuente,
                        "tipo_mensaje": "Comentario",
                        "texto": com['body']
                    })

            issues_procesados += 1
            time.sleep(0.5)

        page += 1

    # Convertir a DataFrame y guardar CSV
    df = pd.DataFrame(dataset)
    nombre_archivo = "dataset_github.csv"
    df.to_csv(nombre_archivo, index=False, encoding="utf-8")

    print(f"\n- Recolección finalizada -")
    print(f"Se procesaron {issues_procesados} Issues/PRs.")
    print(f"Total de mensajes (filas) recolectados: {len(df)}")
    print(f"Archivo guardado como: {nombre_archivo}")
    print("\nVista previa de los datos:")
    print(df.head())

if __name__ == "__main__":
    main()
