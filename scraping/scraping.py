import requests
from bs4 import BeautifulSoup
import pandas as pd

URL = "http://books.toscrape.com/"

try:
    response = requests.get(URL)
    response.raise_for_status()
except requests.exceptions.RequestException as e:
    print(f"Error al acceder a la URL: {e}")
    exit()

soup = BeautifulSoup(response.content, 'html.parser')

datos_libros = []
articulos = soup.find_all('article', class_='product_pod')

for libro in articulos:
    titulo = libro.h3.a.get('title')
    
    precio_str = libro.find('p', class_='price_color').text.strip()
    precio = float(precio_str[1:])
    
    rating_clase = libro.find('p', class_='star-rating').get('class')[1]
    
    datos_libros.append({
        'Titulo': titulo,
        'Precio': precio,
        'Rating': rating_clase 
    })

df = pd.DataFrame(datos_libros)
df.to_csv('datos_libros.csv', index=False)

print("✅ Datos extraídos y guardados en 'datos_libros.csv'.")