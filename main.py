import requests
import io
import pandas as pd

def main():
 

  # Obteniendo la url de los datos desde la terminal
  url = input("Introduzca la url de los datos: ")

  # Descargando los datos
  response = requests.get(url)
  contenido = response.content

  # Creando un archivo de texto plano con extensión csv
  with io.open("datos.csv", "w", encoding="utf-8") as archivo:
    # Escribiendo el contenido de la respuesta en el archivo
    archivo.write(contenido.decode("utf-8"))

  # Convirtiendo el archivo csv a un DataFrame
  df = pd.read_csv("datos.csv")

  # Limpiando los datos
  df = limpiar_datos(df)

  # Categorizando los datos
  df["edad_categoria"] = df["age"].apply(edad_categoria)

  # Exportando los datos limpios
  df.to_csv("datos_limpios.csv", index=False)


def limpiar_datos(df):

  # Verificando que no existan valores faltantes

  if df.isnull().values.any():
    raise ValueError("El DataFrame contiene valores faltantes")

  # Verificando que no existan filas repetidas

  if df.duplicated().values.any():
    raise ValueError("El DataFrame contiene filas repetidas")

  # Verificando si existen valores atípicos y los eliminamos

  for col in df.columns:
    if df[col].dtype.name == "float32":
      # Calculando los límites inferior y superior del 99% de los datos
      Q1 = df[col].quantile(0.25)
      Q3 = df[col].quantile(0.75)
      IQR = Q3 - Q1

      # Eliminando los valores que se encuentran fuera de los límites
      df = df.loc[(df[col] >= Q1 - 1.5 * IQR) & (df[col] <= Q3 + 1.5 * IQR)]

  # Creando una columna que categorice por edades

  def edad_categoria(edad):
    if edad <= 12:
      return "Niño"
    elif edad <= 19:
      return "Adolescente"
    elif edad <= 39:
      return "Jóvenes adulto"
    elif edad <= 59:
      return "Adulto"
    else:
      return "Adulto mayor"

  df["edad_categoria"] = df["age"].apply(edad_categoria)

  return df


def edad_categoria(edad):
 

  if edad <= 12:
    return "Niño"
  elif edad <= 19:
    return "Adolescente"
  elif edad <= 39:
    return "Jóvenes adulto"
  elif edad <= 59:
    return "Adulto"
  else:
    return "Adulto mayor"


if __name__ == "__main__":
  main()
