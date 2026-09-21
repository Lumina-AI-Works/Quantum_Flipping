from qiskit import ClassicalRegister, transpile
from qiskit_aer import Aer
import numpy as np
import importlib

embed_module = importlib.import_module("04_embed_array_flip_y")

def simulate_and_reconstruct(qc, n, size, name=""):
    simulator = Aer.get_backend('qasm_simulator')
    compiled_circuit = transpile(qc, simulator)
    job = simulator.run(compiled_circuit, shots=100000)
    result = job.result()
    counts = result.get_counts(compiled_circuit)
    
    extracted_wm = np.zeros((size, size), dtype=np.uint8)
    
    for bitstring, count in counts.items():
        parts = bitstring.split(' ')
        val = int(parts[0], 2)
        x = int(parts[1], 2)
        y = int(parts[2], 2)
        extracted_wm[y, x] = val
        
    print(f"\n--- {name} ---")
    print("Reconstructed Matrix:")
    print(extracted_wm)
    return extracted_wm

def build_approach_1(cover=None, wm=None):
    qc, q_y, q_x, q_c, q_w, n, size, original_wm = embed_module.build_flip_y_stego_circuit(cover, wm)
    qc.name = "Approach 1 (Flip Y)"
    
    c_y = ClassicalRegister(n, 'c_y')
    c_x = ClassicalRegister(n, 'c_x')
    c_val = ClassicalRegister(1, 'c_val')
    qc.add_register(c_y, c_x, c_val)
    
    qc.barrier(label="Measurement Direct")
    qc.measure(q_c[0], c_val)

    # Inverse classical mapping for Flip Y: x -> 1 - x
    for i in range(n):
        qc.x(q_x[i])
        
    qc.measure(q_y, c_y)
    qc.measure(q_x, c_x)
    return qc, n, size, original_wm

if __name__ == "__main__":
    qc1, n, size, original_wm = build_approach_1()
    try:
        fig1 = qc1.draw(output='mpl', style='clifford', fold=50)
        fig1.savefig('../../outputs/Array_2_Direct_Extraction_Circuit_FlipY.png', bbox_inches="tight", dpi=300)
    except Exception as e:
        pass
        
    wm1 = simulate_and_reconstruct(qc1, n, size, "Approach 1 Direct Flip Y")
    print("Approach 1 Match:", np.array_equal(wm1, original_wm))
