```python
import asyncio ## 
#import marshal
import pickle
from random import randint
# Codigo de Tiago Rodriguez

results = {}


async def submit_job(reader, writer): ## significa que nuesrtras funciones se 
    ## van a declarar d manera asincornas
    job_id = max(list(results.keys()) + [0]) + 1
    writer.write(job_id.to_bytes(4, 'little')) # convierte 
    writer.close()
    sleep_time = randint(1, 4)
    await asyncio.sleep(sleep_time)
    results[job_id] = sleep_time



async def get_results(reader, writer):
    job_id = int.from_bytes(await reader.read(4), 'little') # puede bloquear o permitir el resto del codigo
    # bloquear o pausar el cod
    data = pickle.dumps(results.get(job_id, None))
    writer.write(len(data).to_bytes(4, 'little'))
    writer.write(data)


async def accept_requests(reader, writer): # ansyc def son co-rutinas 
    # cuando tenemos que trabajar en partes de codigo y lo que tenemos que trabajar por policies 
    # en la que se define cuando liberar 
    # la corutina son los fragmentos de cod del que me permite ejecutar partes de cod en parte adecuado
    # cuando llamo a una corutina desde otra otra corutina desde away lo que quiero es que 

    
    op = await reader.read(1)
    if op[0] == 0:
        await submit_job(reader, writer)
    elif op[0] == 1:
        await get_results(reader, writer)


async def main():
    server = await asyncio.start_server(accept_requests, '127.0.0.1', 1936) # escucha la interfaz local y el puertp
    # 
    async with server: # esto es para que no se bloquee 
        await server.serve_forever() # atienda soliciitudes para siemrpe a nuestro servidos


# punto de entrada del codigo y 
asyncio.run(main()) #
```

# si tenemos un servidor tambien tenemos un cliente
* Repasar COOPERATIVE SHEDULING

## dill es una expension dle paquete pickell
https://dill.readthedocs.io/en/latest/

en pickle es la forma mas comun de serializar y convertir a procesos


