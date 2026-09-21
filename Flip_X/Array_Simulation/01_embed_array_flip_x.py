import numpy as np
from qiskit import QuantumCircuit, QuantumRegister

def get_qubit_counts(size):
    return int(np.ceil(np.log2(size)))

def apply_binary_address(qc, q_reg, value, n):
    binary_str = format(value, f'0{n}b')
    for i in range(n):
        if binary_str[n - 1 - i] == '0':
            qc.x(q_reg[i])

def prepare_neqr_state(qc, q_y, q_x, q_c, q_w, cover, wm, n, size):
    qc.barrier(label="Superposition")
    qc.h(q_y)
    qc.h(q_x)
    
    controls = list(q_y) + list(q_x)
    
    for y in range(size):
        for x in range(size):
            cover_val = int(cover[y, x]) & 254
            wm_val = int(wm[y, x])
            
            apply_binary_address(qc, q_y, y, n)
            apply_binary_address(qc, q_x, x, n)
            
            cover_bin = format(cover_val, '08b')
            for i in range(8):
                if cover_bin[7 - i] == '1':
                    qc.mcx(controls, q_c[i])
                    
            if wm_val == 1:
                qc.mcx(controls, q_w[0])
                
            apply_binary_address(qc, q_y, y, n)
            apply_binary_address(qc, q_x, x, n)

def embed_watermark(qc, q_c, q_w):
    qc.barrier(label="Embedding")
    qc.cx(q_w[0], q_c[0])

def apply_flip_x(qc, q_y, n):
    qc.barrier(label="Flip X")
    for i in range(n):
        qc.x(q_y[i])

def build_flip_x_stego_circuit(cover=None, wm=None):
    if cover is None:
        cover = np.array([[1, 2], [7, 4]])
    if wm is None:
        wm = np.array([[1, 0], [1, 1]])
    size = cover.shape[0]
    n = get_qubit_counts(size)
    
    q_y = QuantumRegister(n, 'y')
    q_x = QuantumRegister(n, 'x')
    q_c = QuantumRegister(8, 'c')
    q_w = QuantumRegister(1, 'w')
    qc = QuantumCircuit(q_w, q_c, q_x, q_y, name="Flip X Stego")
    
    prepare_neqr_state(qc, q_y, q_x, q_c, q_w, cover, wm, n, size)
    embed_watermark(qc, q_c, q_w)
    apply_flip_x(qc, q_y, n)
    
    return qc, q_y, q_x, q_c, q_w, n, size, wm

if __name__ == "__main__":
    qc, _, _, _, _, n, size, _ = build_flip_x_stego_circuit()
    try:
        fig = qc.draw(output='mpl', style='clifford', fold=50)
        fig.savefig('../../outputs/Array_1_Embedding_and_Attack_Circuit_FlipX.png', bbox_inches="tight", dpi=300)
        print("Circuit successfully built and saved to outputs/1_stego_flip_x.png!")
    except Exception as e:
        pass

    # Classical Stego Matrix Representation
    try:
        import numpy as np
        cover_mat = np.array([[1, 2], [7, 4]])
        wm_mat = np.array([[1, 0], [1, 1]])
        stego_classical = (cover_mat & 254) | wm_mat
        if 'FlipX' == 'FlipX': stego_attacked = np.flipud(stego_classical)
        elif 'FlipX' == 'FlipY': stego_attacked = np.fliplr(stego_classical)
        elif 'FlipX' == '90_Deg': stego_attacked = np.rot90(stego_classical, -1)
        elif 'FlipX' == '180_Deg': stego_attacked = np.rot90(stego_classical, -2)
        elif 'FlipX' == '270_Deg': stego_attacked = np.rot90(stego_classical, -3)
        print("\n--- Attacked Stego Matrix ---")
        print(stego_attacked)
    except Exception as e:
        pass
