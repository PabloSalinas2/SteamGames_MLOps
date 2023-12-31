#Librerias utilizadas
from fastapi import FastAPI
import pandas as pd
import fastparquet
import pyarrow as pa
import pyarrow.parquet as pq
#from memory_profiler import profile

# Creacion de API
app= FastAPI()
app.title='Steam Games: Querys'

# Lectura de los datos
df_funcion1=pd.read_csv('Datos_procesados/funcion1.csv')
df_funcion2=pd.read_csv('Datos_procesados/funcion2.csv')
df_funcion3_4=pd.read_csv('Datos_procesados/funcion3y4.csv')
df_funcion5=pd.read_csv('Datos_procesados/funcion5.csv')
matriz_user_item=pd.read_parquet('Datos_procesados/matriz_user-item.parquet')
nombre_juegos=pd.read_parquet('Datos_procesados/nombre_juegos.parquet')


# Endpoints de la API
#@profile
@app.get("/play_time_genre/{genero}")
def PlayTimeGenre( genero : str ):
    """
    Devuelve el año con mas horas jugadas para un determinado genero

    Args:
        genre(string) : genero para el cual se calculará la cantidad de horas jugadas

    Returns:
        int: Año con mas horas jugadas 
    """
    try:
        genero=genero.title()
        valor_maximo=df_funcion1[df_funcion1['genres']==genero]['playtime_forever'].max()
        indice=df_funcion1[df_funcion1['playtime_forever']==valor_maximo].index.values
        resultado=df_funcion1['release_year'].loc[indice].values
        return {f'Año de lanzamiento con mas horas jugadas para el Género {genero}: {resultado[0]}'}
    except Exception as e:
        return {'Genero incorrecto'}

# @profile
@app.get("/user_for_genre/{genero}")
def UserForGenre( genero : str ):
    """
    Devuelve el usuario que acumula mas horas jugadas para un genero dado y una lista de horas jugadas por año

    Args:
        genero(string) : Genero del juego para el cual se mostrará el usuario con mas horas jugadas y la cantidad de horas jugadas por año

    Returns:
        tuple: contiene el nombre de usuario y una lista de diccionarios donde con datos de año y horas de juego acumuladas en el año
    """
    try:
        genero=genero.title() # independientemente de si el usuario coloca el parametro en mayuscula o minuscula, el texto introducido se convierte a un texto con la primer letra en mayusculas y las otrwas en minusculas
        df_genero=df_funcion2[df_funcion2['genres']==genero]
        tiempo_maximo=df_genero['playtime_forever'].max()
        indice_tiempo_maximo=df_genero[df_genero['playtime_forever']==tiempo_maximo].index
        usuario=df_genero['user_id'].loc[indice_tiempo_maximo].values[0]
        df_horas_por_año=df_funcion2[(df_funcion2['user_id']==usuario) & (df_funcion2['genres']==genero)]
        lista=[]
        for indice,fila in df_horas_por_año.iterrows():
            año=fila['year']
            horas_jugadas=fila['playtime_forever']
            lista.append({'Año': año, 'Horas': horas_jugadas})
        resultado=(usuario,lista)
        return {f'Usuario con más horas jugadas para el Género {genero}':resultado[0], 'Horas jugadas': resultado[1]}

    except Exception as e:
        return {'Genero incorrecto'}

# @profile
@app.get("/users_recommend/{anio}")
def UsersRecommend( year : int ): 
    """
    Devuelve el top 3 de juegos mas recomendados por usuarios para un año determinado

    Args:
        year(int): Año para el cual se determinarán los juegos mas recomendados
    
    Returns:
        list: lista de diccionarios, donde la clave indica el puesto y el valor indica el juego
    """
    try:
        df_top3=df_funcion3_4[df_funcion3_4['year']==year].nlargest(3,'recommend')
        resultado=[{'Puesto 1': df_top3['app_name'].iloc[0]},{'Puesto 2:': df_top3['app_name'].iloc[1]},{'Puesto 3:': df_top3['app_name'].iloc[2]}]
        return resultado

    except Exception:
        return {'No existen datos para el valor ingresado'}
    



# @profile
@app.get("/users_not_recommend/{anio}")
def UsersNotRecommend( year : int ):
    """
    Devuelve el top 3 de juegos menos recomendados por usuarios para un año determinado

    Args:
        year(int): Año para el cual se determinarán los juegos menos recomendados
    
    Returns:
        list: lista de diccionarios, donde la clave indica el puesto y el valor indica el juego
    """
    try:
        df_top3=df_funcion3_4[df_funcion3_4['year']==year].nsmallest(3,'recommend')
        resultado=[{'Puesto 1': df_top3['app_name'].iloc[0]},{'Puesto 2:': df_top3['app_name'].iloc[1]},{'Puesto 3:': df_top3['app_name'].iloc[2]}]
        return resultado
    except Exception:
        return {'No existen datos para el valor ingresado'}
 




# @profile
@app.get("/sentiment_analysis/{anio}")
def sentiment_analysis( year : int ):
    """
    Devuelve un diccionario que muestra la cantidad de comentarios positivos, negativos y neutros para un determinado año

    Args:
        year(int): Año para el cual se mostrarán la cantidad de comentarios positivos, negativos y neutros dentro de la plataforma Steam Games
    
    Returns:
        Dict: Diccionario donde figuran la cantidad de comentarios positivos, negativos y neutros

    """
    positivos=0
    negativos=0
    neutros=0
    for i in df_funcion5['year']:
        if i==0:
            negativos+=1
        elif i==1:
            neutros+=1
        elif i==2:
            positivos+=1
    resultado={'Negative': negativos, 'Neutral': neutros,'Positive':positivos}
    return resultado


# @profile
@app.get("/recommend_system/{user}")
def sistema_recomendacion(usuario_objetivo):
    """
    Devuelve una lista de juegos recomendados para un usuario determinado

    Args:
        usuario_objetivo(string): Usuario para el cual se devolverá una lista de juegos recomendados.

    Returns:
        list: Lista de juegos recomendados para el usuario_objetivo
    """
    # Ruta al archivo Parquet
    parquet_file_path = 'Datos_procesados/matriz_utilidad.parquet'
    # Configurar el lector Parquet
    parquet_file = pq.ParquetFile(parquet_file_path)
    num_rows_groups=(parquet_file.num_row_groups)-1
    # Iterar sobre los chunks
    for i in range(0, num_rows_groups):
        table = parquet_file.read_row_group(i)
        #Convertir la tabla a un DataFrame de Pandas
        matriz_utilidad= table.to_pandas()
        # Matris con usuarios similares
        matriz_similares=matriz_utilidad.loc[:,['index',usuario_objetivo]]
        matriz_similares=matriz_similares.sort_values(by=usuario_objetivo,ascending=False).reset_index(drop=True)
        matriz_similares=matriz_similares.iloc[1:,:].reset_index(drop=True)
        # Lista de juegos usuario objetivo
        usuario_similar=matriz_similares['index'][0] # cambiar esto
        lista_1=matriz_user_item.columns[matriz_user_item.loc[usuario_objetivo]==True].to_list()
        #Lista de juegos jugados por usuario similar
        lista_2=matriz_user_item.columns[matriz_user_item.loc[usuario_similar]==True].to_list()
        recomendaciones= [int(juego) for juego in lista_2 if juego not in lista_1]
        resultado=list(nombre_juegos[nombre_juegos['item_id'].isin(recomendaciones)]['item_name'])
        return resultado[0:5]


# if __name__ == '__main__':
#     print(PlayTimeGenre('action'))
#     print(UserForGenre('action'))
#     print(UsersRecommend(2011))
#     print(UsersNotRecommend(2011))
#     print(sentiment_analysis('2011'))
#     print(sistema_recomendacion('Whitts'))


