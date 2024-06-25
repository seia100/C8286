# Algoritmo de paxos
# Algoritmo propuesto en clase
# Profesor: Cesar Lara - parallel computing

class Proposer:
    def __init__(self, proposer_id, acceptors):
        self.proposer_id = proposer_id
        self.acceptors = acceptors
        self.proposal_number = 0
        self.proposal_value = None

    def prepare(self):
        self.proposal_number += 1
        promises = []
        for acceptor in self.acceptors:
            promise = acceptor.receive_prepare(self.proposal_number)
            if promise:
                promises.append(promise)
        if len(promises) > len(self.acceptors) / 2:
            self.propose()

    def propose(self):
        for acceptor in self.acceptors:
            acceptor.receive_propose(self.proposal_number, self.proposal_value)

class Acceptor:
    def __init__(self, acceptor_id):
        self.acceptor_id = acceptor_id
        self.promised_proposal_number = 0
        self.accepted_proposal_number = 0
        self.accepted_value = None

    def receive_prepare(self, proposal_number):
        if proposal_number > self.promised_proposal_number:
            self.promised_proposal_number = proposal_number
            return (self.accepted_proposal_number, self.accepted_value)
        return None

    def receive_propose(self, proposal_number, value):
        if proposal_number >= self.promised_proposal_number:
            self.promised_proposal_number = proposal_number
            self.accepted_proposal_number = proposal_number
            self.accepted_value = value
            return True
        return False

# # Ejemplo de uso
# acceptors = [Acceptor(i) for i in range(5)]
# proposer = Proposer(1, acceptors)
# proposer.prepare()

# ALgoritmod ebully
class Node:
    def __init__(self, node_id, nodes):
        self.node_id = node_id
        self.nodes = nodes
        self.leader = None

    def start_election(self):
        print(f"Nodo {self.node_id} inicia una eleccion.")
        higher_nodes = [node for node in self.nodes if node.node_id > self.node_id]
        if not higher_nodes:
            self.become_leader()
        else:
            for node in higher_nodes:
                if node.alive:
                    node.receive_election_message(self.node_id)

    def receive_election_message(self, sender_id):
        print(f"Nodo {self.node_id} recive mensaje de eleccion desde el Nodo {sender_id}.")
        if self.node_id > sender_id:
            self.start_election()

    def become_leader(self):
        print(f"Nodo {self.node_id} llega a ser el lider the leader.")
        self.leader = self.node_id
        for node in self.nodes:
            if node.node_id != self.node_id:
                node.leader = self.node_id

    @property
    def alive(self):
        return True

# nodes = [Node(i, []) for i in range(5)]
# for node in nodes:
#     node.nodes = [n for n in nodes if n != node]

# nodes[2].start_election()

## relojes vectoriales

class VectorClock:
    def __init__(self, num_nodes, node_id):
        if not (0 <= node_id < num_nodes):
            raise ValueError(f"node_id {node_id} is out of valid range 0 to {num_nodes-1}")
        self.clock = [0] * num_nodes
        self.node_id = node_id

    def tick(self):
        self.clock[self.node_id] += 1

    def send_event(self):
        self.tick()
        return self.clock[:]

    def receive_event(self, received_vector):
        for i in range(len(self.clock)):
            self.clock[i] = max(self.clock[i], received_vector[i])
        self.clock[self.node_id] += 1

# # Ejemplo de uso
# num_nodes = 3
# node1 = VectorClock(num_nodes, 0)
# node2 = VectorClock(num_nodes, 1)
# node3 = VectorClock(num_nodes, 2)

# # Evento en el nodo 1
# node1.tick()
# print(f" Reloj Nodo 1 : {node1.clock}")

# # Nodo 1 envía un mensaje a nodo 2
# msg = node1.send_event()
# node2.receive_event(msg)
# print(f"Reloj Nodo 2 despues de recibir: {node2.clock}")

# # Evento en el nodo 3
# node3.tick()
# print(f"Reloj Nodo 3 : {node3.clock}")


# Recolector de basura

class CheneyCollector:
    def __init__(self, size):
        self.size = size
        self.from_space = [None] * size
        self.to_space = [None] * size
        self.free_ptr = 0

    def allocate(self, obj):
        if self.free_ptr >= self.size:
            self.collect()
        addr = self.free_ptr
        self.from_space[addr] = obj
        self.free_ptr += 1
        return addr

    def collect(self):
        self.to_space = [None] * self.size
        self.free_ptr = 0
        for obj in self.from_space:
            if obj is not None:
                self.copy(obj)
        self.from_space, self.to_space = self.to_space, self.from_space

    def copy(self, obj):
        addr = self.free_ptr
        self.to_space[addr] = obj
        self.free_ptr += 1
        return addr

# # Ejemplo de uso
# collector = CheneyCollector(10)
# addr1 = collector.allocate("obj1")
# print(f"Asignado obj1 en: {addr1}")
# collector.collect()
# print("Recoleccion de basura completa")



########################################
##MODULO PARA EL EJERCICIO 4

# Algoritmo de raft
import threading
import time

class Node:
    def __init__(self, node_id, peers):
        self.node_id = node_id
        self.peers = peers
        self.term = 0
        self.voted_for = None
        self.state = "follower"
        self.log = []
        self.commit_index = 0
        self.last_applied = 0

    def start_election(self):
        self.state = "candidate"
        self.term += 1
        self.voted_for = self.node_id
        votes = 1
        for peer in self.peers:
            if peer.request_vote(self.term, self.node_id):
                votes += 1
        if votes > len(self.peers) / 2:
            self.state = "leader"
            self.lead()

    def request_vote(self, term, candidate_id):
        if term > self.term:
            self.term = term
            self.voted_for = candidate_id
            return True
        return False

    def lead(self):
        while self.state == "leader":
            self.send_heartbeats()
            time.sleep(1)

    def send_heartbeats(self):
        for peer in self.peers:
            peer.receive_heartbeat(self.term, self.node_id)

    def receive_heartbeat(self, term, leader_id):
        if term >= self.term:
            self.term = term
            self.state = "follower"

# # Ejemplo de uso
# nodes = [Node(i, []) for i in range(5)]
# for node in nodes:
#     node.peers = [n for n in nodes if n != node]

# leader = nodes[0]
# thread = threading.Thread(target=leader.start_election)
# thread.start()


## Algoritmo de Chandy-Lamport

import threading
import time
from collections import defaultdict

class Process:
    def __init__(self, process_id):
        self.process_id = process_id
        self.state = None
        self.channels = defaultdict(list)
        self.neighbors = []
        self.marker_received = {}
        self.local_snapshot = None
        self.lock = threading.Lock()

    def set_neighbors(self, neighbors):
        self.neighbors = neighbors
        for neighbor in neighbors:
            self.marker_received[neighbor.process_id] = False

    def initiate_snapshot(self):
        with self.lock:
            self.local_snapshot = self.state
            print(f"Process {self.process_id} taking local snapshot: {self.local_snapshot}")
            self.send_marker_messages()

    def send_marker_messages(self):
        for neighbor in self.neighbors:
            self.send_message(neighbor, 'MARKER')

    def send_message(self, neighbor, message_type, content=None):
        message = (message_type, self.process_id, content)
        neighbor.receive_message(message)

    def receive_message(self, message):
        message_type, sender_id, content = message
        with self.lock:
            if message_type == 'MARKER':
                if not self.marker_received[sender_id]:
                    self.marker_received[sender_id] = True
                    if self.local_snapshot is None:
                        self.local_snapshot = self.state
                        print(f"Process {self.process_id} taking local snapshot: {self.local_snapshot}")
                        self.send_marker_messages()
                    else:
                        self.channels[sender_id].append(content)
                else:
                    self.channels[sender_id].append(content)
            else:
                if self.local_snapshot is not None:
                    self.channels[sender_id].append(content)
                else:
                    self.process_message(message)

    def process_message(self, message):
        # Simulate processing of a normal message
        print(f"Process {self.process_id} received message from Process {message[1]}: {message[2]}")

    def update_state(self, new_state):
        self.state = new_state

# # Ejemplo de uso
# processes = [Process(i) for i in range(3)]
# for i, process in enumerate(processes):
#     neighbors = [p for j, p in enumerate(processes) if i != j]
#     process.set_neighbors(neighbors)

# # Simulate state updates
# processes[0].update_state("State A")
# processes[1].update_state("State B")
# processes[2].update_state("State C")

# # Initiate snapshot from process 0
# processes[0].initiate_snapshot()

# # Simulate message passing
# time.sleep(1)
# processes[1].send_message(processes[0], 'MESSAGE', "Message 1 from P1 to P0")
# time.sleep(1)
# processes[2].send_message(processes[0], 'MESSAGE', "Message 2 from P2 to P0")
# time.sleep(1)
# processes[2].send_message(processes[1], 'MESSAGE', "Message 3 from P2 to P1")

# ALgoritmo de maekawa
class MaekawaMutex:
    def __init__(self, node_id, quorum):
        self.node_id = node_id
        self.quorum = quorum
        self.voted = False
        self.votes_received = 0

    def request_access(self):
        self.votes_received = 0
        for node in self.quorum:
            node.receive_request(self)

    def receive_request(self, requester):
        if not self.voted:
            self.voted = True
            requester.receive_vote(self)

    def receive_vote(self, voter):
        self.votes_received += 1
        if self.votes_received == len(self.quorum):
            self.enter_critical_section()

    def enter_critical_section(self):
        print(f"Nodo {self.node_id} ingresando a la seccion critica")
        # Critical section code here
        self.leave_critical_section()

    def leave_critical_section(self):
        print(f"Nodo {self.node_id} dejando la seccion critica")
        for node in self.quorum:
            node.release_vote(self)

    def release_vote(self, requester):
        self.voted = False

# # Ejemplo de uso
# num_nodes = 3
# quorum = [
#     [0, 1],
#     [1, 2],
#     [0, 2]
# ]
# nodes = [MaekawaMutex(i, [nodes[j] for j in q if j != i]) for i, q in enumerate(quorum)]

# # Simulate node 0 requesting access
# nodes[0].request_access()
# time.sleep(2)
# nodes[0].leave_critical_section()

# Algoritmode  recolector d esemiespacio
class SemispaceCollector:
    def __init__(self, size):
        self.size = size
        self.from_space = [None] * size
        self.to_space = [None] * size
        self.free_ptr = 0

    def allocate(self, obj):
        if self.free_ptr >= self.size:
            self.collect()
        addr = self.free_ptr
        self.from_space[addr] = obj
        self.free_ptr += 1
        return addr

    def collect(self):
        self.to_space = [None] * self.size
        self.free_ptr = 0
        for obj in self.from_space:
            if obj is not None:
                self.copy(obj)
        self.from_space, self.to_space = self.to_space, self.from_space

    def copy(self, obj):
        addr = self.free_ptr
        self.to_space[addr] = obj
        self.free_ptr += 1
        return addr

# # Ejemplo de uso
# collector = SemispaceCollector(10)
# addr1 = collector.allocate("obj1")
# print(f"Asignado el obj1 en: {addr1}")
# collector.collect()
# print("Recoleccion de basura completa")
