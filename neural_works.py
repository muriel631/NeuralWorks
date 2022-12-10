##MATCH
##Las tablas de Match, League, Country y Team tiene toda la información para describir un partido detalladamente. Crea una query SQL para obtener la información detallada por partido uniendo las tablas Match, League, Country y Team.

SELECT *
FROM ( SELECT CL.id AS country_id, CL.name AS country_name, CL.id AS league_id, CL.name as league_name
       FROM ( SELECT * 
              FROM Country C
              LEFT JOIN League L
              ON C.id = L.country_id
             ) CL
      ) CLL
LEFT JOIN Match M 
ON M.league_id = CLL.league_id and M.country_id = CLL.country_id
LEFT JOIN ( SELECT team_api_id, team_long_name as home_team_name, team_short_name as home_team_initials
            FROM Team ) TH
ON M.home_team_api_id = TH.team_api_id
LEFT JOIN ( SELECT team_api_id, team_long_name as away_team_name, team_short_name as away_team_initials
            FROM Team ) TA
ON M.away_team_api_id = TA.team_api_id

#Me hubiera gustado despues meter la query en python para reorganizar las columnas de una forma más eficiente pero no supe como conectar la base de datos al python (en mi trabajo TI ya hizo esa conexion) y ademas me descargue SQLite Browser para ver la data de las tablas dadas entonces cada vez que se cerraba el programa se me borraban las tablas por lo que se hace más dificil conectarlo al python. Volviendo a reorganizar las columnas, como hay tantas es poco eficiente sólo escribir el listado completo pero enel orden correcto en el "SELECT ..." porque no sólo quiero reordenar sino que no quiero que se repita información, sacaría los ids de paises, ligas y equipo y dejaría los nombre de esos para reemplazarlo (junto con obviamente dejar todos las columnas de datos y detalles de los partidos). En python creo que sería más eficiente ya que uno puede usar corchetes, por lo que podría poner

datos_partidos = datos_partidos[['columna1'] + list(datos_partidos.columns)[3:]]

#datos_partidos seria el dataframe obtenido de sql con las columnas reales de sql, dentro del corchete ['columna1'], iria el listado con el orden real de las columnas que quiero mantener en la tabla (aqui sacaria los id, y reemplazaria los id por los nombres correspondiente manteniendo el orden) y después en la parte de list(datos_partidos.columns)[3:] sería para no escribir todo el resto de las columnas después de los nombres de los equipos "home" y "away" para no escribirlos todos y sólo usar indices.

##PREGUNTA
##¿Qué insights ves en la información detallada del partido? 

#Primero, cada aspecto del partido esta en detallado en una tabla distinta. 
#La tabla Country tiene los paises distintos con sus correspondientes ids. 
# La tabla League tiene las ligas distintas que analizaremos con sus ids correspondientes y con los ids de los paises de cada liga (pero sin el nombre del país por lo que uno tiene que unir las dos tablas Country con League).
# La tabla Match tiene la información de todos los partidos de cada liga analizada en la tabla anterior con el id del pais correspondiente a la liga y ahora hay un nuevo id para cada partido (entonces uno tiene que unir las dos tablas anteriores con esta para identificar los nombres de las ligas y el pais para poder entender e identificar qué partido corresponde a qué liga) entre otros detalles. Esta tabla es la que tiene más información y no sólo por la cantidad de datos/filas que tiene sino porque es la que nos entrega más detalle de cada partido ya que incluye el pais y la liga del partido sino que todos los jugadores que participaron en el partido y además el puntaje final de cada partido. Se entrega de varias formas todos los jugadores, por lo que vi se entregan con 3 diferentes ids todos los jugadores para cada partido. Aunque hay un par de partidos que no tienen la información de los jugadores. Alfinal de la tabla también hay columnas por cada equipo existente entre todas las ligas y cada columna tiene información para la mayoría de los partidos (esa información no la entendi muy bien honestamente, ya que no participan todos los equipos en cada partido).

##PREGUNTA
##Dado que queremos armar un equipo maravilloso nos interesa tener un perfil por cada jugador. Ocupa SQL y/o Python para crear un Dataframe que tenga un jugador por fila con toda la información que creas relevante.

select P.player_name, *
from Player_Attributes PA
left join Player P
on PA.player_fifa_api_id = P.player_fifa_api_id
WHERE player_name not null

#Otra información relevante sería contar cuántos partidos ha jugado cada jugador en los años presentados y además en cuántos ha estado en el equipo ganador. Se podría haber hecho esto mediante una query de SQL pero muy largo y tediosa, pero con muchos left join de forma similar como lo hice para obtener los nombres de los equipos "home" y "away" en la query de la pregunta de arriba. Ahi sólo fueron dos left join porque quería transformar dos ids en nombres, aquí en este caso la cantidad de left joins utilizados sería la cantidad de jugadores en total en away y home. Otra forma de obtener esa información es en Python, reemplazando los ids directamente en la tabla de Matches con los nombres de los jugadores, se podría obtener un dataframe de SQL donde en la primera columna esta el id y la segunda el nombre del jugador (como la tabla Players) correspondiente y pasar por ese dataframe con un for index, row in dataframe.iterrows() y dentro del for usar el script de replace un valor por otro en todo el dataframe. Como haciendo dataframe.replace('nombre_jugador': id), y así pasar por el dataframe. 

#Siguiendo esta línea de identificar cuándo el jugador ha sido home o away, no logre definir los equipos de cada jugador pero lo podría haber identificado usando el mecanismo explicado en el parrafo anterior.

#Encuentro que también hubiera sido valioso capaz sacar el promedio de todas las cualidades de los jugadores por cada año, o en general (parecido a como lo hice en la pregunta bonus, pero no sólo del overall_rating) porque tener ese puntaje por partido no lo encuentro tan valioso ya que son demasiados datos y hace el análisis mucho más extenso de lo que debería (pensando en que capaz que el mirar esos detalles por partido no sea mucho más importante o preciso que mirar el promedio por temporada o año).


##PREGUNTA
##¿Qué insights ves en el perfil por jugador? ¿Qué data crees que es relevante para elegir a los mejores jugadores? 

#Hay dos tablas especiales para la información de los jugadores.
#La tabla Player tiene la infromación básica de los jugadores, sus nombres, sus diferentes ids, su altura, peso y fecha de nacimiento. Información que no nos dice mucho de cómo juegan sino que información general de la persona.
#Las cifras y detalles importante sobre cómo juega cada jugador estan en la tabla Player_Attributes donde salen muchas cifras de cómo jugaron en cada partido. En general son muchas columnas con cifras numericas, por lo que observe se puede asumir que en general si las cifras de esas columnas como de sus reflejos, saltos, pases, posicionamiento, etc. son mayores significa que el jugador tiene un ranking más alto en la columna overall_rating. Yo creo que esos numeros son también parte de un ranking, no la cantidad de reflejos, saltos, etc. que hace en un partido.

#Observé las lineas con id 8 y 11 de Player_Attributes que tenian el mismo overall_rating pero diferente potential para entender qué se toma en cuenta para calcular esos valores y conclui que uno de los factores para calcular el potential es el valor de long_shots y que es mejor tener menos long_shot para un mejor puntaje en potential (ya que los valores de todas las otras cualidades eran iguales para los dos ids) y probablemente tiene muy poca importancia o cero importancia para calcular el overall_rating. 
#Se podría hacer un análisis más profundo de qué factores aportan la calificación del overall_rating y potential pero ese es uno de los factores que encontre, con el tiempo limitado de la prueba y considerando el no desviarme tanto de la pregunta inicial.

#Observando en general los datos de Player_Attributes, un jugador puede tener distintas evaluaciones de overall_raiting y potential para cada partido, por lo que yo tomare el promedio de overall_rating de cada jugador para sólo tener un puntaje final de overall_rating y potential para cada jugador y así el análisis de cada jugador se hace un poco más facil para lo que se esta pidiendo en esta tarea.

#Dada la información dada por cada jugador, encuentro relevante la progresión del puntaje de overall_rating de un jugador, si va decayendo capaz que en algun minuto fue muy bueno en algun minuto pero ya esta empeorando en el juego mediante el paso de los años. Se supone que el overall_rating toma en cuenta todos los detalles como sus pases, reflejos, etc. asi que no los miraría tanto y tampoco creo que es tan útil para elegir a los mejores jugadores, creo que son más relevantes para armar un equipo como para que funcionen mejor los jugadores juntos y trabajen mejor en equipo y se complementen.

# Otra data relevante, que no esta incluida en mi query, pero explique en la pregunta anterior como lo obtendría es la cantidad de partidos que ha jugado cada jugador y además la cantidad de veces ha estado en el equipo "home" o "away" porque creo que tambien es relevante mirar si un jugador mantiene su status y buen rendimiento cuando juega fuera de su estadio o país. Toca bastante que un equipo no siempre juega en su estadio o pais natal entonces uno busca un jugador que no baje mucho su rendimiento y concentración en un lugar ajeno. Por si no queda claro, no sólo es importante ver la cantidad de veces que ha sido el equipo home o away sino que las ganancias que ha tenido siendo home o away.

##BONUS: ¿Cuál es tu sugerencia de jugadores para armar el mejor equipo de la historia? Argumenta tu respuesta.

#La pregunta bonus me pide armar el mejor equipo de la historia, lo cual se da para varias interpretaciones. Yo voy a tomarlo como crear el mejor equipo en tiempo presente, porque se podria tomar jugadores muy buenos pero que tenian muy buen overall_raiting en años distintos o todos en el mismo año pero que fue hace tiempo y actualmente no se si sería el mismo equipo y tend´rían el mejor rendimiento. Como por ejemplo se podría hipoteticamente hacer un equipo con Alexis Sanches, Chupete Suazo, Bravo, etc. jugadores estrellas chilenos que en su minuto eran increibles y sacaron adelante a la selección Chilena pero actualmente no serían parte de el mejor equipo de la historia porque ya no rinden así como para seguir jugando y ser los mejores.

#Todo eso fue sólo para explicar mi razonamiento y cómo voy a tomar los bonus. Mi idea es sacar un promedio de los overall rating de cada año (ya que se me hacía muy dificil hacerlo por temporada) e ir revisando mediante un código de python si cada año iba mejorando el rating o empeorando. No sería ideal armar un equipo con un jugador sabiendo que el jugador va decayendo cada año, no sería muy duradero el jugador ni el rendimiento progresivo del equipo. 

###AVISO en mi trabajo actual, la conexion entre nuestros jupyter notebooks y la base de datos que usamos ya existe entonces uno normalmente tiene un codigo habitual que usamos para conectar:

params = {'dbname': 'cron_stock',
        'user': 'cron_stock',
        'password': 'fVNJ5V2q8QHkjLUe',
        'host': 'stock.cvropcx09k2v.us-west-1.rds.amazonaws.com',
        'port': 5432
         }

dbconn = psycopg2.connect(**params)
dbconn.autocommit = True
cursor = dbconn.cursor()

query = (
    '''
    '''
    )

cursor.execute(query,)
df = pd.DataFrame(cursor.fetchall(), columns = [~escribir listado de columnas aca~])

#no supe hacer esa conexion entre este codigo y sqlite como explique antes, entonces lo que hice para poder seguir trabajando con la data fue ejecutar la query en SQLite Browser:
select P.player_name, PA.player_fifa_api_id, strftime('%Y', PA.date) as year, AVG(PA.overall_rating), AVG(PA.potential)
from Player_Attributes PA
left join Player P
on PA.player_fifa_api_id = P.player_fifa_api_id
WHERE player_name not null
group by P.player_name, PA.player_fifa_api_id, year

#Copiar esa información entregada a una planilla y de ahi leer esa planilla desde el jupyter (usando un función que ya uso actualmente en mi trabajo, porque nuevamente TI ya nos dejo lista esa conexión) entonces por eso hay tantas paqueterías que podrían parecer extrañas pero las puse igual para que se entienda lo que hice después capaz.
#la planilla que use para leer los datos es esta: https://docs.google.com/spreadsheets/d/1jcLUoV-sY0-ArLS78Go9rpbUSNRUH9zG03vz8O94GCo/edit#gid=0 
# Hice esta parte del código en un jupyter notebook porque se me hace más fácil, pero después lo pegue aca abajo como código normal python.

import site
import requests
import psycopg2
import psycopg2.extras
from datetime import date, datetime, timedelta
from googleapiclient.discovery import build
import pandas as pd
import numpy as np
import sys
import matplotlib.pyplot as plt
sys.path.append("/home/ubuntu/jupyter/Logistica/")
from ForkSpreadSheet import Utils
sys.path.append("/home/ubuntu/jupyter/Utils/")

from ForkSpreadsheet import ForkSpreadsheet,Owner
fss = ForkSpreadsheet(Owner.MURIEL)
from IPython.core.display import display, HTML

def get_data_spreadsheet(sheet_name, range_name, link, columnas = None):
    if columnas:
        df = pd.DataFrame(data=fss.readRange(link, sheet_name+'!'+range_name), columns = columnas)
        
    else:
        spread = fss.readRange(link, sheet_name +'!'+ range_name)
        df = pd.DataFrame(data=spread[1:], columns = spread[0])
    
    return df


datos_jugadores = get_data_spreadsheet('datos_jugadores', 'A1:E', '1jcLUoV-sY0-ArLS78Go9rpbUSNRUH9zG03vz8O94GCo')
datos_jugadores = datos_jugadores.astype({'overall_rating': 'float', 'potential': 'float'})

#PRIMER FILTRO
datos_jugadores_group = datos_jugadores.groupby(['player_name'])
final_jugadores = []

def get_best(group_name, df_group, vueltas):
    contador = 0
    for index, row in df_group.iterrows():
        if contador == 0:
            valor_first_year = row.overall_rating
            contador = contador + 1
        else:
            valor_second_year = row.overall_rating
            if valor_second_year >= valor_first_year:
                contador = contador + 1
                if contador == vueltas:
                    final_jugadores.append(group_name)
                    break
            else:
                break

for group_name, df_group in datos_jugadores_group:
    vueltas = len(df_group)
    get_best(group_name, df_group, vueltas)
    
datos_jugadores = datos_jugadores[datos_jugadores['player_name'].isin(final_jugadores)]

#SEGUNDO FILTRO
def last_year(group_name, df_group, vueltas):
    contador = 1
    for index, row in df_group.iterrows():
        if contador == vueltas:
            if row.overall_rating >= 85:
                final_jugadores2.append(group_name)
        else:
            contador = contador + 1

datos_jugadores_group = datos_jugadores.groupby(['player_name'])
final_jugadores2 = []

for group_name, df_group in datos_jugadores_group:
    vueltas = len(df_group)
    last_year(group_name, df_group, vueltas)

#mi lista final de mejores jugadores para seguir con los filtros de abajo es la lista final_jugadores2.

#El proceso consiste en hacer esas revisiones haciendo un groupby del dataframe grande de datos clasificandolos por el jugador, entonces corro por el dataframe viendo los ratings de cada año y si el siguiente año es pero que el anterior no entra en mi lista de los mejores jugadores, si es que sí, sí entra.
#Después armo un nuevo dataframe donde sólo tengo los jugadores de esa lista. Este nuevo dataframe va tender promediado la columna overall_rating de cada jugador y esto es para filtrar 
#Cabe destacar que mi creación del equipo es plenamente mirando estadística pero despuées se tendría que tomar en cuenta las posiciones que juga cada jugador, no sirve de nada tener sólamente delanteros o lo que sea la posición, esta información me faltó y por eso no hice ese extra paso pero yo pienso que así seguiría el análisis. Sería como un segundo filtro para crear el mejor equipo despues de ya tener los mejores jugadores que progresivamente van aumentando su overall_rating.
#En algún minuto consideré también utilizar el factor de edad para elegir a los mejores pero puede pasar que un jugador ya esté en sus "últimos años" o más "viejos" por la cantidad de años que lleva jugando, y juegue igual de bien que siempre o siga mejorando cada año. Puede pasar también lo contrario, la velocidad baja, los reflejos y años que seguirá jugando pero es un análisis que se tiene que hacer de cada caso por lo que no lo inclui como factor.
# Como también he mencionado anteriormente y el razonamiento por detras, influye también la cantidad de partidos que ha jugado en los años presentados y la cantidad de veces que ha estado en el partido home y away y sus ganacias siendo home y away.