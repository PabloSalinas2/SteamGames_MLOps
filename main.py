from fastapi import FastAPI
import pandas as pd


df_funcion1=pd.read_csv('funcion1.csv')
df_funcion2=pd.read_csv('funcion2.csv')
df_funcion3_4=pd.read_csv('funcion3y4.csv')
df_funcion5=pd.read_csv('funcion5.csv')

app= FastAPI()
app.title='Steam Games: Querys'




@app.get("/play_time_genre/{genre}")
def PlayTimeGenre( genre : str ): #  Debe devolver año con mas horas jugadas para dicho género.
    # pasar a dataframe dentro de la funcion ?
    try:
        genre=genre.title()
        valor_maximo=df_funcion1[df_funcion1['genres']==genre]['playtime_forever'].max()
        indice=df_funcion1[df_funcion1['playtime_forever']==valor_maximo].index
        resultado=df_funcion1['release_year'].loc[indice].values
        return {f'Año de lanzamiento con mas horas jugadas para el Género {genre}:':resultado[0]}
    except Exception as e:
        print('Genero incorrecto')

# Ejemplo de retorno: {"Año de lanzamiento con más horas jugadas para Género X" : 2013}

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





@app.get("/users_recommend/{anio}")
def UsersRecommend( year : int ): # Devuelve el top 3 de juegos MÁS recomendados por usuarios para el año dado. (reviews.recommend = True y comentarios positivos/neutrales)
    try:
        df_top3=df_funcion3_4[df_funcion3_4['year']==year].nlargest(3,'recommend')
        return [{'Puesto 1': df_top3['app_name'].iloc[0]},{'Puesto 2:': df_top3['app_name'].iloc[1]},{'Puesto 3:': df_top3['app_name'].iloc[2]}]

    except Exception:
        return {'No existen datos para el valor ingresado'}
    
#Ejemplo de retorno: [{"Puesto 1" : X}, {"Puesto 2" : Y},{"Puesto 3" : Z}]
    



@app.get("/users_not_recommend/{anio}")
def UsersNotRecommend( year : int ): # Devuelve el top 3 de juegos MENOS recomendados por usuarios para el año dado. (reviews.recommend = False y comentarios negativos)
    try:
        df_top3=df_funcion3_4[df_funcion3_4['year']==year].nsmallest(3,'recommend')
        return [{'Puesto 1': df_top3['app_name'].iloc[0]},{'Puesto 2:': df_top3['app_name'].iloc[1]},{'Puesto 3:': df_top3['app_name'].iloc[2]}]

    except Exception:
        return {'No existen datos para el valor ingresado'}
 
# Ejemplo de retorno: [{"Puesto 1" : X}, {"Puesto 2" : Y},{"Puesto 3" : Z}]





@app.get("/sentiment_analysis/{anio}")
def sentiment_analysis( year : int ): # Según el año de lanzamiento, se devuelve una lista con la cantidad de registros de reseñas de usuarios que se encuentren categorizados con un análisis de sentimiento.
    df_año=df_funcion5[df_funcion5['release_year']==year]
    positivos=0
    negativos=0
    neutros=0
    for i in df_año['sentiment_analysis'].values:
        if i==0:
            negativos+=1
        elif i==1:
            neutros+=1
        elif i==2:
            positivos+=1

    return {'Negative': negativos, 'Neutral': neutros,'Positive':positivos}

# Ejemplo de retorno: {Negative = 182, Neutral = 120, Positive = 278}


