# SteamGames_MLOps

### Introducción.

El presente proyecto tiene como finalidad mostrar el proceso de desarrollo de una API con FastAPI, la cual será deployada en render, la misma contará con 5 endopoints encargados de consultar datos de distintos datasets, además se llevará a cabo el desarrollo de un sistema de recomendación de VideoJuegos.

Datos: Se trabajará con datos provenientes de la plataforma Steam Games.


### 1) ETL. 

Se realizará un proceso de ETL (Extraction, Transform and Load) de los datos, en esta etapa se realizará un ETL simple, efectuandose las trasformaciones necesarios para el desarrollo de las funciones, No nos concentraremos en la transformación de Datos no reelevanes para el desarrollo del proyecto.

![imagen de etl](imagenes/etl%20imagen.jpg)


### 2) Desarrollo de Funciones.

A partir de los datos transformados se extraerán datasets mas chicos optimizados para cada función, esto permitirá tener un mejor rendimiento y optima utilización de los recursos 
gratuitos proporcionados por render.com.


### 3) EDA y Modelo de Recomendación.

Una vez los datos están limpios se efectuará un modelo de recomendación de juegos, el mismo se desarrollará bajo un filtrado colaborativo basado en el usuario, esto significa que la recomendación de juegos a cada usuario estará determinada por la simililitud existentente entre usuarios, para encontrar la similitud entre usuarios se utilizará la técnica de similitud del coseno 

Previo a lo descripto se efectuará un EDA, con la finalidad de entender los datos, la relación entre sus variables, captar patrones para desarrollar el modelo de recomendación

![sistema de recomendacion con filtrado colaborativo basado en el usuario](imagenes/Diagramas_recomendados.png)


### 4) Construcción de API y despliegue del modelo.

La construcción de la API será llevada a cabo con la librería FastApi, gracias a su simplicidad podemos montar una API en poco tiempo y de manera sencilla.
La API constará de 6 endopoints, compuestas por 5 funciones encargadas de hacer consultas sobre los datos y un sistema de recomendacion de juegos. 
La misma será desplegada en render.com.
