#!/bin/bash

# Configuración
endpoint="http://nginx:80/get_timestamp"  # URL del endpoint
interval=${REQUEST_TIME_SEG}  # Intervalo de tiempo en segundos (ajusta según lo que necesites)

 

for (( c=1; c<=${MAX_NUM_HTTP_REQUEST}; c++ ))
do 
    # Realiza la petición al endpoint usando curl
    response=$(curl -s $endpoint)
    
    # Imprime la respuesta
    echo "Response: $response"
    
    # Espera el tiempo especificado antes de realizar la siguiente petición
    sleep $interval
done
