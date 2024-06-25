import random
from mod_algorithms import Proposer, Acceptor, Node as BullyNode, VectorClock, CheneyCollector

class InventoryRecord:
    def __init__(self, item_id, quantity):
        self.item_id = item_id
        self.quantity = quantity

class InventoryNode(BullyNode):
    def __init__(self, node_id, nodes):
        super().__init__(node_id, nodes)
        self.inventory = {}
        self.vector_clock = VectorClock(len(nodes), node_id)
        self.gc = CheneyCollector(100)  # Inicializa el recolector de basura
        self.acceptor = Acceptor(node_id)
        self.proposer = Proposer(node_id, [node.acceptor for node in nodes])

    def update_inventory(self, item_id, quantity):
        # Propone una actualización usando Paxos
        self.proposer.proposal_value = (item_id, quantity)
        self.proposer.prepare()
        
        # Si la propuesta es aceptada, actualiza el inventario
        if self.acceptor.accepted_value == (item_id, quantity):
            self.inventory[item_id] = self.gc.allocate(InventoryRecord(item_id, quantity))
            self.vector_clock.tick()
            print(f"Nodo {self.node_id} actualizó el inventario: Item {item_id}, Cantidad {quantity}")
            print(f"Vector Clock: {self.vector_clock.clock}")

    def receive_update(self, sender_id, item_id, quantity, sender_clock):
        # Verifica la causalidad usando relojes vectoriales
        if all(sender_clock[i] <= self.vector_clock.clock[i] for i in range(len(self.vector_clock.clock))):
            self.inventory[item_id] = self.gc.allocate(InventoryRecord(item_id, quantity))
            self.vector_clock.receive_event(sender_clock)
            print(f"Nodo {self.node_id} recibió actualización: Item {item_id}, Cantidad {quantity}")
            print(f"Vector Clock: {self.vector_clock.clock}")
        else:
            print(f"Nodo {self.node_id} detectó violación de causalidad, actualizaci")

# Configuración del sistema
num_nodes = 5
nodes = [InventoryNode(i, []) for i in range(num_nodes)]
for node in nodes:
    node.nodes = [n for n in nodes if n != node]
    node.initialize_vector_clock(num_nodes)  # Inicializa el VectorClock aquí


# Simulación de operaciones
def simulate_operations():
    for _ in range(10):
        node = random.choice(nodes)
        item_id = random.randint(1, 10)
        quantity = random.randint(1, 100)
        node.update_inventory(item_id, quantity)
        
        # Simula la propagación de la actualización a otros nodos
        for other_node in nodes:
            if other_node != node:
                other_node.receive_update(node.node_id, item_id, quantity, node.vector_clock.clock)

        # Simula la elección de un nuevo líder
        if random.random() < 0.2:
            random.choice(nodes).start_election()

        # Ejecuta el recolector de basura en el nodo líder
        leader = next(node for node in nodes if node.leader == node.node_id)
        leader.gc.collect()

# Ejecutar la simulación
simulate_operations()