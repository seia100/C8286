
# implementacion paralela de un contador de palabras


from mpi4py import MPI # comunicación entre procesos en sistemas
comm = MPI.COMM_WORLD # Crea un comunicador MPI para todos los procesos disponibles.
rank = comm.Get_rank() # Obtiene el rango (identificador) del proceso actual.
size = comm.Get_size() # Obtiene el número total de procesos.
 
# Si el proceso tiene rango 0 (es decir, es el proceso maestro): 
if rank == 0:
    with open('large_text_file.txt', 'r') as file:
        # Lee todas las líneas del archivo y las almacena en la variable lines
        lines = file.readlines()
else:
    # Si no es el proceso maestro, establece lines como None
    lines = None

# istribución de líneas entre procesos:

## Distribuye las líneas del archivo entre todos los procesos. 
lines = comm.scatter(lines, root=0) ## Cada proceso recibe una parte del archivo.

# Conteo de palabras
## Calcula el número de palabras en las líneas asignadas al proceso actual.
local_word_count = sum(len(line.split()) for line in lines) 


# Reduccoin del conteo de palabras
## Reduce los conteos locales de palabras al proceso maestro (rango 0) y calcula el total.
total_word_count = comm.reduce(local_word_count, op=MPI.SUM, root=0)

if rank == 0:
    # Si el proceso tiene rango 0, imprime el total de palabras
    print(f"Total word count: {total_word_count}")
