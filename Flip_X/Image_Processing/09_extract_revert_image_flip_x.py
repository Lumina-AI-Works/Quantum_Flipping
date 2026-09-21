import cv2
from qiskit import ClassicalRegister, transpile
from qiskit_aer import Aer
import numpy as np
import importlib

embed_module = importlib.import_module("07_embed_image_flip_x")

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

def build_approach_2(cover=None, wm=None):
    qc, q_y, q_x, q_c, q_w, n, size, original_wm = embed_module.build_flip_x_stego_circuit(cover, wm)
    qc.name = "Approach 2 (Flip X Reversion)"
    
    c_y = ClassicalRegister(n, 'c_y')
    c_x = ClassicalRegister(n, 'c_x')
    c_val = ClassicalRegister(1, 'c_val')
    qc.add_register(c_y, c_x, c_val)
    
    qc.barrier(label="Revert State")
    # Mathematical inverse of Flip X is another Flip X
    for i in range(n):
        qc.x(q_y[i])
        
    qc.barrier(label="Standard Measurement")
    qc.measure(q_c[0], c_val)
    qc.measure(q_y, c_y)
    qc.measure(q_x, c_x)
    return qc, n, size, original_wm

if __name__ == "__main__":
    qc2, n, size, original_wm = build_approach_2()
    try:
        fig2 = qc2.draw(output='mpl', style='clifford', fold=50)
        fig2.savefig('../../outputs/Image_4_Revert_Extraction_Circuit_FlipX.png', bbox_inches="tight", dpi=300)
    except Exception as e:
        print(f'Notice: Circuit diagram too large to draw/save ({type(e).__name__}). Skipping circuit image.')
        
    wm2 = simulate_and_reconstruct(qc2, n, size, "Approach 2 Revert Flip X")
    print("Approach 2 Match:", np.array_equal(wm2, original_wm))

    cv2.imwrite('../../outputs/Image_5_Output_Watermark_Revert_FlipX.png', wm2 * 255)
    print('Saved extracted watermark to outputs/Image_5_Output_Watermark_Revert_FlipX.png')
