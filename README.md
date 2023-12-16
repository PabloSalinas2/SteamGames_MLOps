# SteamGames_MLOps


A partir de datos extraidos de la plataforma SteamGames se desarrollará un sistema de recomendación de juegos, el cual se montará en una API la cual será despleguada en el servicio brindador por Render. 


El proyecto en cuestion consta de las siguientes etapas: 

### 1- ETL 

Se realizar un proceso de ETL (Extraction, Transform and Load) de los datos, en esta etapa se realiza un ETL simple, efectuandose las trasformaciones necesariosa para el desarrollo de las funciones, No nos concentraremos en la transformación de Datos no reelevanes para el desarrollo del proyecto.


### 2- Desarrollo de Funciones

A partir de los datos transformados se extraerán datasets mas chicos optimizados para cada función, esto permitirá tener un mejor rendimiento y optima utilización de los recursos 
gratuitos proporcionados por Render.


### 3- EDA y Modelo de Recomendación 

Una vez los datos están limpios se efectuará un modelo de recomendación de juegos, el mismo se desarrollará bajo un filtrado colaborativo basado en el usuario, esto significa que la recomendacion de juegos a cada usuario estará determinada por la simililitud existentente entre usuarios, para encontrar la similitud entre usuarios se utilizará la tecnica de similitud del coseno 

Previo a lo descripto se efectuará un EDA, con la finalidad de entender los datos, la relación entre sus variables, captar patrones para desarrollar el modelo de recomendación


### 4- Construccion de API y despliegue del modelo 

La construcción de la API será llevada a cabo con la librería FastApi, gracias a su simplicidad podemos montar una API en poco tiempo y de manera sencilla.
La API constará de 6 endopoints, compuestas por 5 funciones encargadas de hacer consultas sobre los datos y un sistema de recomendacion de juegos. 
La misma será desplegada en render
