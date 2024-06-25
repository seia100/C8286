import random
from mod_algorithms import Node as RaftNode, Process as ChandyLamportProcess, MaekawaMutex, SemispaceCollector

class BankAccount:
    def __init__(self, account_id, balance):
        self.account_id = account_id
        self.balance = balance

class BankNode(RaftNode, ChandyLamportProcess):
    def __init__(self, node_id, peers):
        RaftNode.__init__(self, node_id, peers)
        ChandyLamportProcess.__init__(self, node_id)
        self.accounts = {}
        self.mutex = MaekawaMutex(node_id, peers)
        self.gc = SemispaceCollector(100)  # Inicializa el recolector de semiespacio

    def create_account(self, account_id, initial_balance):
        self.accounts[account_id] = self.gc.allocate(BankAccount(account_id, initial_balance))

    def perform_transaction(self, account_id, amount):
        self.mutex.request_access()
        # La sección crítica comienza aquí
        if account_id in self.accounts:
            account = self.accounts[account_id]
            account.balance += amount
            print(f"Nodo {self.node_id} realizó transacción: Cuenta {account_id}, Monto {amount}")
            self.replicate_transaction(account_id, amount)
        else:
            print(f"Cuenta {account_id} no encontrada en el nodo {self.node_id}")
        self.mutex.leave_critical_section()

    def replicate_transaction(self, account_id, amount):
        # Usa Raft para replicar la transacción a otros nodos
        if self.state == "leader":
            self.log.append((account_id, amount))
            for peer in self.peers:
                peer.receive_transaction(self.term, self.node_id, account_id, amount)

    def receive_transaction(self, term, leader_id, account_id, amount):
        if term >= self.term:
            self.term = term
            self.state = "follower"
            if account_id in self.accounts:
                self.accounts[account_id].balance += amount
                print(f"Nodo {self.node_id} replicó transacción: Cuenta {account_id}, Monto {amount}")

    def take_snapshot(self):
        self.initiate_snapshot()
        snapshot = {account_id: account.balance for account_id, account in self.accounts.items()}
        print(f"Nodo {self.node_id} tomó instantánea: {snapshot}")
        return snapshot

# Configuración del sistema
num_nodes = 5
nodes = [BankNode(i, []) for i in range(num_nodes)]
for node in nodes:
    node.set_neighbors([n for n in nodes if n != node])
    node.peers = [n for n in nodes if n != node]

# Simulación de operaciones bancarias
def simulate_banking_operations():
    # Crear algunas cuentas iniciales
    for i in range(10):
        account_id = f"ACC-{i}"
        initial_balance = random.randint(1000, 10000)
        for node in nodes:
            node.create_account(account_id, initial_balance)

    # Realizar transacciones
    for _ in range(20):
        node = random.choice(nodes)
        account_id = f"ACC-{random.randint(0, 9)}"
        amount = random.randint(-1000, 1000)
        node.perform_transaction(account_id, amount)

        # Tomar instantáneas periódicamente
        if random.random() < 0.2:
            random.choice(nodes).take_snapshot()

        # Simular elección de líder periódicamente
        if random.random() < 0.1:
            random.choice(nodes).start_election()

        # Ejecutar el recolector de basura periódicamente
        if random.random() < 0.1:
            leader = next(node for node in nodes if node.state == "leader")
            leader.gc.collect()

# Ejecutar la simulación
simulate_banking_operations()