from fastapi import FastAPI
import pandas as pd
import fastparquet
import pyarrow as pa
import pyarrow.parquet as pq
from memory_profiler import profile




df_funcion1=pd.read_csv('Datos_procesados/funcion1.csv')
df_funcion2=pd.read_csv('Datos_procesados/funcion2.csv')
df_funcion3_4=pd.read_csv('Datos_procesados/funcion3y4.csv')
df_funcion5=pd.read_csv('Datos_procesados/funcion5.csv')
matriz_user_item=pd.read_parquet('Datos_procesados/matriz_user-item.parquet')
nombre_juegos=pd.read_parquet('Datos_procesados/nombre_juegos.parquet')

# Lectura del archivo "matriz_utiilidad.parquet"
# Tamaño del chunk
chunksize = 100
# Ruta al archivo Parquet
parquet_file_path = 'Datos_procesados/matriz_utilidad.parquet'
# Configurar el lector Parquet
parquet_file = pq.ParquetFile(parquet_file_path)
num_rows = parquet_file.num_row_groups
# Iterar sobre los chunks
for i in range(0, num_rows, chunksize):
    # Calcular el rango de filas para el chunk actual
    start_row = i
    end_row = min(i + chunksize, num_rows)
    # Leer el chunk
    table = pq.read_table(parquet_file_path)# row_groups=list(range(start_row, end_row)))
    # Convertir la tabla a un DataFrame de Pandas
    matriz_utilidad= table.to_pandas()




    #matriz_utilidad=pd.read_parquet('Datos_procesados/matriz_utilidad.parquet')

app= FastAPI()
app.title='Steam Games: Querys'

#@profile
@app.get("/play_time_genre/{genero}")
def PlayTimeGenre( genero : str ): #  Debe devolver año con mas horas jugadas para dicho género.
    try:
        genero=genero.title()
        valor_maximo=df_funcion1[df_funcion1['genres']==genero]['playtime_forever'].max()
        indice=df_funcion1[df_funcion1['playtime_forever']==valor_maximo].index.values
        resultado=df_funcion1['release_year'].loc[indice].values
        return {f'Año de lanzamiento con mas horas jugadas para el Género {genero}: valor maximo: {resultado}'}
    except Exception as e:
        return {'Genero incorrecto'}

#@profile
@app.get("/user_for_genre/{genero}")
def UserForGenre( genero : str ): #Debe devolver el usuario que acumula más horas jugadas para el género dado y una lista de la acumulación de horas jugadas por año.
    try:
        genero=genero.title() # independientemente de si el usuario coloca el parametro en mayuscula o minuscula, el texto introducido se convierte a un texto con la primer letra en mayusculas y las otrwas en minusculas
        df_genero=df_funcion2[df_funcion2['genres']==genero]
        tiempo_maximo=df_genero['playtime_forever'].max()
        indice_tiempo_maximo=df_genero[df_genero['playtime_forever']==tiempo_maximo].index
        resultado=df_genero['user_id'].loc[indice_tiempo_maximo].values[0]

        df_horas_por_año=df_funcion2[(df_funcion2['user_id']==resultado) & (df_funcion2['genres']==genero)]
        lista=[]
        for indice,fila in df_horas_por_año.iterrows():
            año=fila['year']
            horas_jugadas=fila['playtime_forever']
            lista.append({'Año': año, 'Horas': horas_jugadas})

        return {f'Usuario con más horas jugadas para el Género {genero}':resultado, 'Horas jugadas': lista}

    except Exception as e:
        return {'Genero incorrecto'}

# Ejemplo de retorno: {"Usuario con más horas jugadas para Género X" : us213ndjss09sdf, "Horas jugadas":[{Año: 2013, Horas: 203}, {Año: 2012, Horas: 100}, {Año: 2011, Horas: 23}]}


#@profile
@app.get("/users_recommend/{anio}")
def UsersRecommend( year : int ): # Devuelve el top 3 de juegos MÁS recomendados por usuarios para el año dado. (reviews.recommend = True y comentarios positivos/neutrales)
    try:
        df_top3=df_funcion3_4[df_funcion3_4['year']==year].nlargest(3,'recommend')
        return [{'Puesto 1': df_top3['app_name'].iloc[0]},{'Puesto 2:': df_top3['app_name'].iloc[1]},{'Puesto 3:': df_top3['app_name'].iloc[2]}]

    except Exception:
        return {'No existen datos para el valor ingresado'}
    
#Ejemplo de retorno: [{"Puesto 1" : X}, {"Puesto 2" : Y},{"Puesto 3" : Z}]
    

#@profile
@app.get("/users_not_recommend/{anio}")
def UsersNotRecommend( year : int ): # Devuelve el top 3 de juegos MENOS recomendados por usuarios para el año dado. (reviews.recommend = False y comentarios negativos)
    try:
        df_top3=df_funcion3_4[df_funcion3_4['year']==year].nsmallest(3,'recommend')
        return [{'Puesto 1': df_top3['app_name'].iloc[0]},{'Puesto 2:': df_top3['app_name'].iloc[1]},{'Puesto 3:': df_top3['app_name'].iloc[2]}]

    except Exception:
        return {'No existen datos para el valor ingresado'}
 
# Ejemplo de retorno: [{"Puesto 1" : X}, {"Puesto 2" : Y},{"Puesto 3" : Z}]



#@profile
@app.get("/sentiment_analysis/{anio}")
def sentiment_analysis( year : int ): # Según el año de lanzamiento, se devuelve una lista con la cantidad de registros de reseñas de usuarios que se encuentren categorizados con un análisis de sentimiento.
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

    return {'Negative': negativos, 'Neutral': neutros,'Positive':positivos}

# Ejemplo de retorno: {Negative = 182, Neutral = 120, Positive = 278}

@profile
@app.get("/recommend_system/{user}")
def sistema_recomendacion(usuario_objetivo):
    # Lectura parcial de matriz utilidad 
    chunksize = 100
    # Ruta al archivo Parquet
    parquet_file_path = 'Datos_procesados/matriz_utilidad.parquet'
    # Configurar el lector Parquet
    parquet_file = pq.ParquetFile(parquet_file_path)
    num_rows = parquet_file.num_row_groups
    # Iterar sobre los chunks
    for i in range(0, num_rows, chunksize):
        # Calcular el rango de filas para el chunk actual
        start_row = i
        end_row = min(i + chunksize, num_rows)
        # Leer el chunk
        table = pq.read_table(parquet_file_path)# row_groups=list(range(start_row, end_row)))
        # Convertir la tabla a un DataFrame de Pandas
        matriz_utilidad= table.to_pandas()



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
#     PlayTimeGenre('action')
#     UserForGenre('action')
#     UsersRecommend('2011')
#     UsersNotRecommend('2011')
#     sentiment_analysis('2011')
#     # sistema_recomendacion('Whitts')





