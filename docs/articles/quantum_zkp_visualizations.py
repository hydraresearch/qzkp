#!/usr/bin/env python3
"""
Quantum Zero-Knowledge Proof Visualizations
Creates diagrams to illustrate the probabilistic entanglement concepts
"""

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Circle, FancyBboxPatch
import matplotlib.patches as mpatches

def create_quantum_state_diagram():
    """Create a diagram showing quantum state evolution"""
    fig, ax = plt.subplots(1, 1, figsize=(12, 8))

    # Define positions for the flow
    positions = {
        'classical': (1, 4),
        'encoding': (3, 4),
        'quantum': (5, 4),
        'entanglement': (7, 4),
        'measurement': (9, 4),
        'validity': (11, 5),
        'secret': (11, 3)
    }

    # Draw boxes for each stage
    boxes = {
        'classical': FancyBboxPatch((0.5, 3.5), 1, 1, boxstyle="round,pad=0.1",
                                   facecolor='lightblue', edgecolor='blue'),
        'encoding': FancyBboxPatch((2.5, 3.5), 1, 1, boxstyle="round,pad=0.1",
                                  facecolor='lightgreen', edgecolor='green'),
        'quantum': FancyBboxPatch((4.5, 3.5), 1, 1, boxstyle="round,pad=0.1",
                                 facecolor='lightyellow', edgecolor='orange'),
        'entanglement': FancyBboxPatch((6.5, 3.5), 1, 1, boxstyle="round,pad=0.1",
                                      facecolor='lightpink', edgecolor='red'),
        'measurement': FancyBboxPatch((8.5, 3.5), 1, 1, boxstyle="round,pad=0.1",
                                     facecolor='lightgray', edgecolor='black'),
        'validity': FancyBboxPatch((10.5, 4.5), 1, 1, boxstyle="round,pad=0.1",
                                  facecolor='lightgreen', edgecolor='green'),
        'secret': FancyBboxPatch((10.5, 2.5), 1, 1, boxstyle="round,pad=0.1",
                                facecolor='lightyellow', edgecolor='orange')
    }

    # Add boxes to plot
    for box in boxes.values():
        ax.add_patch(box)

    # Add text labels
    labels = {
        'classical': 'Classical\nData',
        'encoding': 'Probabilistic\nEncoding',
        'quantum': 'Quantum\nAmplitudes',
        'entanglement': 'Logical\nEntanglement',
        'measurement': 'Quantum\nMeasurement',
        'validity': 'Validity\nResult',
        'secret': 'Secret\nPreserved'
    }

    for key, (x, y) in positions.items():
        ax.text(x, y, labels[key], ha='center', va='center', fontsize=10, fontweight='bold')

    # Draw arrows
    arrows = [
        ('classical', 'encoding'),
        ('encoding', 'quantum'),
        ('quantum', 'entanglement'),
        ('entanglement', 'measurement'),
        ('measurement', 'validity'),
        ('measurement', 'secret')
    ]

    for start, end in arrows:
        start_pos = positions[start]
        end_pos = positions[end]

        if start == 'measurement' and end == 'validity':
            ax.annotate('', xy=(end_pos[0]-0.5, end_pos[1]), xytext=(start_pos[0]+0.5, start_pos[1]+0.2),
                       arrowprops=dict(arrowstyle='->', lw=2, color='green'))
        elif start == 'measurement' and end == 'secret':
            ax.annotate('', xy=(end_pos[0]-0.5, end_pos[1]), xytext=(start_pos[0]+0.5, start_pos[1]-0.2),
                       arrowprops=dict(arrowstyle='->', lw=2, color='orange'))
        else:
            ax.annotate('', xy=(end_pos[0]-0.5, end_pos[1]), xytext=(start_pos[0]+0.5, start_pos[1]),
                       arrowprops=dict(arrowstyle='->', lw=2, color='blue'))

    ax.set_xlim(0, 12)
    ax.set_ylim(2, 6)
    ax.set_aspect('equal')
    ax.axis('off')
    ax.set_title('Quantum Zero-Knowledge Proof: Probabilistic Entanglement Flow',
                fontsize=16, fontweight='bold', pad=20)

    plt.tight_layout()
    plt.savefig('quantum_zkp_flow.png', dpi=300, bbox_inches='tight')
    plt.close()  # Close instead of show for headless operation

def create_orthogonal_subspaces_diagram():
    """Create a diagram showing orthogonal quantum subspaces"""
    fig, ax = plt.subplots(1, 1, figsize=(10, 8))

    # Draw the main quantum state space
    main_circle = Circle((5, 4), 3, fill=False, edgecolor='black', linewidth=3)
    ax.add_patch(main_circle)

    # Draw secret subspace
    secret_circle = Circle((3.5, 4), 1.2, fill=True, facecolor='lightcoral',
                          alpha=0.7, edgecolor='red', linewidth=2)
    ax.add_patch(secret_circle)

    # Draw validity subspace
    validity_circle = Circle((6.5, 4), 1.2, fill=True, facecolor='lightgreen',
                           alpha=0.7, edgecolor='green', linewidth=2)
    ax.add_patch(validity_circle)

    # Add labels
    ax.text(5, 7.5, 'Quantum State Space |ψ_proof⟩', ha='center', va='center',
           fontsize=14, fontweight='bold')
    ax.text(3.5, 4, 'Secret\nSubspace\n⊥', ha='center', va='center',
           fontsize=12, fontweight='bold')
    ax.text(6.5, 4, 'Validity\nSubspace\n⊥', ha='center', va='center',
           fontsize=12, fontweight='bold')

    # Add orthogonal symbol
    ax.text(5, 4, '⊥', ha='center', va='center', fontsize=20, fontweight='bold')

    # Add measurement arrows
    ax.annotate('Measure Secret\n❌ Never Done', xy=(3.5, 2.5), xytext=(1, 1),
               arrowprops=dict(arrowstyle='->', lw=2, color='red', linestyle='--'),
               fontsize=10, ha='center', color='red')

    ax.annotate('Measure Validity\n✅ Safe to Do', xy=(6.5, 2.5), xytext=(9, 1),
               arrowprops=dict(arrowstyle='->', lw=2, color='green'),
               fontsize=10, ha='center', color='green')

    # Add results
    ax.text(9, 6, 'Results:\n• Valid: P ≈ 1.0\n• Invalid: P ≈ 0.0',
           bbox=dict(boxstyle="round,pad=0.3", facecolor='lightgreen', alpha=0.7),
           fontsize=10, ha='left')

    ax.text(1, 6, 'Secret Data:\n• Preserved\n• Never Revealed',
           bbox=dict(boxstyle="round,pad=0.3", facecolor='lightcoral', alpha=0.7),
           fontsize=10, ha='left')

    ax.set_xlim(0, 10)
    ax.set_ylim(0, 8)
    ax.set_aspect('equal')
    ax.axis('off')
    ax.set_title('Orthogonal Quantum Subspaces: How Verification Preserves Secrecy',
                fontsize=14, fontweight='bold', pad=20)

    plt.tight_layout()
    plt.savefig('orthogonal_subspaces.png', dpi=300, bbox_inches='tight')
    plt.close()  # Close instead of show for headless operation

def create_classical_vs_quantum_comparison():
    """Create a comparison diagram of classical vs quantum ZKP"""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

    # Classical ZKP
    ax1.text(0.5, 0.9, 'Classical Zero-Knowledge Proof', ha='center', va='center',
            transform=ax1.transAxes, fontsize=14, fontweight='bold')

    classical_boxes = [
        (0.5, 0.8, 'Secret Data', 'lightblue'),
        (0.5, 0.65, 'Computational\nHiding', 'lightyellow'),
        (0.5, 0.5, 'Mathematical\nProof', 'lightgreen'),
        (0.5, 0.35, 'Verification', 'lightcoral'),
        (0.5, 0.2, 'Security relies on\ncomputational assumptions', 'lightgray')
    ]

    for x, y, text, color in classical_boxes:
        bbox = FancyBboxPatch((x-0.15, y-0.05), 0.3, 0.08, boxstyle="round,pad=0.01",
                             facecolor=color, edgecolor='black', transform=ax1.transAxes)
        ax1.add_patch(bbox)
        ax1.text(x, y, text, ha='center', va='center', transform=ax1.transAxes, fontsize=9)

    # Add arrows for classical
    for i in range(len(classical_boxes)-1):
        ax1.annotate('', xy=(0.5, classical_boxes[i+1][1]+0.04),
                    xytext=(0.5, classical_boxes[i][1]-0.04),
                    xycoords='axes fraction', textcoords='axes fraction',
                    arrowprops=dict(arrowstyle='->', lw=2, color='blue'))

    # Quantum ZKP
    ax2.text(0.5, 0.9, 'Quantum Zero-Knowledge Proof', ha='center', va='center',
            transform=ax2.transAxes, fontsize=14, fontweight='bold')

    quantum_boxes = [
        (0.5, 0.8, 'Secret Data', 'lightblue'),
        (0.5, 0.65, 'Probabilistic\nEncoding', 'lightgreen'),
        (0.5, 0.5, 'Quantum\nEntanglement', 'lightpink'),
        (0.5, 0.35, 'Quantum\nMeasurement', 'lightyellow'),
        (0.5, 0.2, 'Security relies on\nquantum mechanics', 'lightgray')
    ]

    for x, y, text, color in quantum_boxes:
        bbox = FancyBboxPatch((x-0.15, y-0.05), 0.3, 0.08, boxstyle="round,pad=0.01",
                             facecolor=color, edgecolor='black', transform=ax2.transAxes)
        ax2.add_patch(bbox)
        ax2.text(x, y, text, ha='center', va='center', transform=ax2.transAxes, fontsize=9)

    # Add arrows for quantum
    for i in range(len(quantum_boxes)-1):
        ax2.annotate('', xy=(0.5, quantum_boxes[i+1][1]+0.04),
                    xytext=(0.5, quantum_boxes[i][1]-0.04),
                    xycoords='axes fraction', textcoords='axes fraction',
                    arrowprops=dict(arrowstyle='->', lw=2, color='red'))

    # Add vulnerability/strength indicators
    ax1.text(0.5, 0.05, '⚠️ Vulnerable to quantum computers', ha='center', va='center',
            transform=ax1.transAxes, fontsize=10, color='red', fontweight='bold')

    ax2.text(0.5, 0.05, '🛡️ Quantum-safe by design', ha='center', va='center',
            transform=ax2.transAxes, fontsize=10, color='green', fontweight='bold')

    for ax in [ax1, ax2]:
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
        ax.axis('off')

    plt.tight_layout()
    plt.savefig('classical_vs_quantum_zkp.png', dpi=300, bbox_inches='tight')
    plt.close()  # Close instead of show for headless operation

def create_mermaid_style_flow():
    """Create a PNG version of the Mermaid flow diagram"""
    fig, ax = plt.subplots(1, 1, figsize=(14, 8))

    # Define positions for nodes (matching Mermaid layout)
    positions = {
        'classical': (2, 6),
        'encoding': (2, 4.5),
        'amplitudes': (2, 3),
        'entanglement': (2, 1.5),
        'proof_state': (6, 1.5),
        'measurement': (10, 1.5),
        'validity': (12, 3),
        'secret': (12, 0.5)
    }

    # Define node styles (matching Mermaid colors)
    node_styles = {
        'classical': {'color': '#e1f5fe', 'edge': '#0277bd'},
        'encoding': {'color': '#e8f5e8', 'edge': '#2e7d32'},
        'amplitudes': {'color': '#fff3e0', 'edge': '#f57c00'},
        'entanglement': {'color': '#f3e5f5', 'edge': '#7b1fa2'},
        'proof_state': {'color': '#f3e5f5', 'edge': '#7b1fa2'},
        'measurement': {'color': '#fafafa', 'edge': '#424242'},
        'validity': {'color': '#e8f5e8', 'edge': '#2e7d32'},
        'secret': {'color': '#fff3e0', 'edge': '#f57c00'}
    }

    # Draw nodes
    node_size = 1.2
    for node, (x, y) in positions.items():
        style = node_styles[node]
        rect = FancyBboxPatch((x-node_size/2, y-0.4), node_size, 0.8,
                             boxstyle="round,pad=0.1",
                             facecolor=style['color'],
                             edgecolor=style['edge'],
                             linewidth=2)
        ax.add_patch(rect)

    # Add text labels
    labels = {
        'classical': 'Classical Data',
        'encoding': 'Probabilistic\nEncoding',
        'amplitudes': 'Quantum\nAmplitudes',
        'entanglement': 'Logical\nEntanglement',
        'proof_state': 'Entangled\nProof State',
        'measurement': 'Quantum\nMeasurement',
        'validity': 'Validity Result',
        'secret': 'Secret Remains\nHidden'
    }

    for node, (x, y) in positions.items():
        ax.text(x, y, labels[node], ha='center', va='center',
               fontsize=10, fontweight='bold')

    # Draw arrows
    arrows = [
        ('classical', 'encoding'),
        ('encoding', 'amplitudes'),
        ('amplitudes', 'entanglement'),
        ('entanglement', 'proof_state'),
        ('proof_state', 'measurement'),
        ('measurement', 'validity'),
        ('measurement', 'secret')
    ]

    for start, end in arrows:
        start_pos = positions[start]
        end_pos = positions[end]

        if start == 'measurement' and end == 'validity':
            # Arrow going up-right
            ax.annotate('', xy=(end_pos[0]-0.6, end_pos[1]),
                       xytext=(start_pos[0]+0.6, start_pos[1]+0.2),
                       arrowprops=dict(arrowstyle='->', lw=2.5, color='#2e7d32'))
        elif start == 'measurement' and end == 'secret':
            # Arrow going down-right
            ax.annotate('', xy=(end_pos[0]-0.6, end_pos[1]),
                       xytext=(start_pos[0]+0.6, start_pos[1]-0.2),
                       arrowprops=dict(arrowstyle='->', lw=2.5, color='#f57c00'))
        elif start == 'entanglement' and end == 'proof_state':
            # Horizontal arrow
            ax.annotate('', xy=(end_pos[0]-0.6, end_pos[1]),
                       xytext=(start_pos[0]+0.6, start_pos[1]),
                       arrowprops=dict(arrowstyle='->', lw=2.5, color='#7b1fa2'))
        elif start == 'proof_state' and end == 'measurement':
            # Horizontal arrow
            ax.annotate('', xy=(end_pos[0]-0.6, end_pos[1]),
                       xytext=(start_pos[0]+0.6, start_pos[1]),
                       arrowprops=dict(arrowstyle='->', lw=2.5, color='#424242'))
        else:
            # Vertical arrows
            ax.annotate('', xy=(end_pos[0], end_pos[1]+0.4),
                       xytext=(start_pos[0], start_pos[1]-0.4),
                       arrowprops=dict(arrowstyle='->', lw=2.5, color='#1976d2'))

    # Add title and styling
    ax.set_xlim(0, 14)
    ax.set_ylim(-0.5, 7)
    ax.set_aspect('equal')
    ax.axis('off')
    ax.set_title('Quantum Zero-Knowledge Proof: Probabilistic Entanglement Flow',
                fontsize=16, fontweight='bold', pad=20)

    # Add subtle background
    ax.set_facecolor('#fafafa')

    plt.tight_layout()
    plt.savefig('probabilistic_entanglement_flow.png', dpi=300, bbox_inches='tight',
                facecolor='white', edgecolor='none')
    plt.close()

def create_formula_images():
    """Create PNG images of the mathematical formulas for Medium"""

    # Formula 1: Probabilistic Encoding
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.text(0.5, 0.8, r'Probabilistic Encoding Formula',
            fontsize=18, fontweight='bold', ha='center', transform=ax.transAxes)

    ax.text(0.5, 0.6, r'For classical data $D = \{d_1, d_2, \ldots, d_n\}$, we create quantum amplitudes:',
            fontsize=14, ha='center', transform=ax.transAxes)

    ax.text(0.5, 0.4, r'$\alpha_i = \sqrt{P(d_i)} \times e^{i\phi_i}$',
            fontsize=20, ha='center', transform=ax.transAxes,
            bbox=dict(boxstyle="round,pad=0.5", facecolor='lightblue', alpha=0.8))

    ax.text(0.5, 0.25, r'where $P(d_i)$ = normalized probability, $\phi_i$ = phase encoding',
            fontsize=12, ha='center', transform=ax.transAxes)

    ax.text(0.5, 0.1, r'$\sum_i |\alpha_i|^2 = 1$ (normalization constraint)',
            fontsize=12, ha='center', transform=ax.transAxes)

    ax.axis('off')
    plt.tight_layout()
    plt.savefig('formula_probabilistic_encoding.png', dpi=300, bbox_inches='tight',
                facecolor='white', edgecolor='none')
    plt.close()

    # Formula 2: Quantum State
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.text(0.5, 0.7, r'Quantum State Formation',
            fontsize=18, fontweight='bold', ha='center', transform=ax.transAxes)

    ax.text(0.5, 0.4, r'$|\psi_{\text{data}}\rangle = \sum_i \alpha_i |i\rangle$',
            fontsize=20, ha='center', transform=ax.transAxes,
            bbox=dict(boxstyle="round,pad=0.5", facecolor='lightgreen', alpha=0.8))

    ax.text(0.5, 0.15, r'Classical data becomes quantum superposition',
            fontsize=12, ha='center', transform=ax.transAxes)

    ax.axis('off')
    plt.tight_layout()
    plt.savefig('formula_quantum_state.png', dpi=300, bbox_inches='tight',
                facecolor='white', edgecolor='none')
    plt.close()

    # Formula 3: Entanglement
    fig, ax = plt.subplots(figsize=(10, 4))
    ax.text(0.5, 0.7, r'Logical Entanglement',
            fontsize=18, fontweight='bold', ha='center', transform=ax.transAxes)

    ax.text(0.5, 0.4, r'$|\psi_{\text{proof}}\rangle = U_{\text{entangle}}(|\psi_{\text{data}}\rangle \otimes |\psi_{\text{witness}}\rangle)$',
            fontsize=18, ha='center', transform=ax.transAxes,
            bbox=dict(boxstyle="round,pad=0.5", facecolor='lightpink', alpha=0.8))

    ax.text(0.5, 0.15, r'Creates correlations without revealing individual amplitudes',
            fontsize=12, ha='center', transform=ax.transAxes)

    ax.axis('off')
    plt.tight_layout()
    plt.savefig('formula_entanglement.png', dpi=300, bbox_inches='tight',
                facecolor='white', edgecolor='none')
    plt.close()

    # Formula 4: Verification
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.text(0.5, 0.7, r'Quantum Verification',
            fontsize=18, fontweight='bold', ha='center', transform=ax.transAxes)

    ax.text(0.5, 0.4, r'$P(\text{valid}) = |\langle\psi_{\text{expected}}|\psi_{\text{proof}}\rangle|^2$',
            fontsize=18, ha='center', transform=ax.transAxes,
            bbox=dict(boxstyle="round,pad=0.5", facecolor='lightyellow', alpha=0.8))

    ax.text(0.5, 0.15, r'Binary result without exposing original data encoding',
            fontsize=12, ha='center', transform=ax.transAxes)

    ax.axis('off')
    plt.tight_layout()
    plt.savefig('formula_verification.png', dpi=300, bbox_inches='tight',
                facecolor='white', edgecolor='none')
    plt.close()

    # Formula 5: Entangled Proof State
    fig, ax = plt.subplots(figsize=(12, 4))
    ax.text(0.5, 0.7, r'Entangled Proof State',
            fontsize=18, fontweight='bold', ha='center', transform=ax.transAxes)

    ax.text(0.5, 0.4, r'$|\psi_{\text{proof}}\rangle = \alpha|\text{secret},\text{valid}\rangle + \beta|\text{secret},\text{invalid}\rangle + \gamma|\text{other states}\rangle$',
            fontsize=16, ha='center', transform=ax.transAxes,
            bbox=dict(boxstyle="round,pad=0.5", facecolor='lightcyan', alpha=0.8))

    ax.text(0.5, 0.15, r'Superposition of secret data with validity states',
            fontsize=12, ha='center', transform=ax.transAxes)

    ax.axis('off')
    plt.tight_layout()
    plt.savefig('formula_entangled_proof_state.png', dpi=300, bbox_inches='tight',
                facecolor='white', edgecolor='none')
    plt.close()

    # Formula 6: Quantum Interference Verification
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.text(0.5, 0.85, r'Quantum Interference Verification',
            fontsize=18, fontweight='bold', ha='center', transform=ax.transAxes)

    ax.text(0.5, 0.65, r'$\text{Validity} = |\langle\psi_{\text{expected}}|\psi_{\text{proof}}\rangle|^2$',
            fontsize=18, ha='center', transform=ax.transAxes,
            bbox=dict(boxstyle="round,pad=0.5", facecolor='lightsteelblue', alpha=0.8))

    ax.text(0.5, 0.45, r'This gives us:',
            fontsize=14, fontweight='bold', ha='center', transform=ax.transAxes)

    ax.text(0.5, 0.3, r'$P(\text{valid}) \approx 1.0$ if the prover knows the secret',
            fontsize=14, ha='center', transform=ax.transAxes,
            bbox=dict(boxstyle="round,pad=0.3", facecolor='lightgreen', alpha=0.6))

    ax.text(0.5, 0.15, r'$P(\text{valid}) \approx 0.0$ if the prover is guessing',
            fontsize=14, ha='center', transform=ax.transAxes,
            bbox=dict(boxstyle="round,pad=0.3", facecolor='lightcoral', alpha=0.6))

    ax.axis('off')
    plt.tight_layout()
    plt.savefig('formula_quantum_interference.png', dpi=300, bbox_inches='tight',
                facecolor='white', edgecolor='none')
    plt.close()

    # Formula 7: Observable Types
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.text(0.5, 0.9, r'Two Different Quantum Observables',
            fontsize=18, fontweight='bold', ha='center', transform=ax.transAxes)

    # Secret Observable
    ax.text(0.25, 0.7, r'Secret Observable',
            fontsize=16, fontweight='bold', ha='center', transform=ax.transAxes,
            bbox=dict(boxstyle="round,pad=0.3", facecolor='lightcoral', alpha=0.8))

    ax.text(0.25, 0.55, r'Measures actual data content',
            fontsize=12, ha='center', transform=ax.transAxes)

    ax.text(0.25, 0.4, r'❌ NEVER MEASURED',
            fontsize=14, fontweight='bold', ha='center', transform=ax.transAxes, color='red')

    ax.text(0.25, 0.25, r'Would reveal the secret',
            fontsize=10, ha='center', transform=ax.transAxes, style='italic')

    # Validity Observable
    ax.text(0.75, 0.7, r'Validity Observable',
            fontsize=16, fontweight='bold', ha='center', transform=ax.transAxes,
            bbox=dict(boxstyle="round,pad=0.3", facecolor='lightgreen', alpha=0.8))

    ax.text(0.75, 0.55, r'Measures proof correctness',
            fontsize=12, ha='center', transform=ax.transAxes)

    ax.text(0.75, 0.4, r'✅ SAFE TO MEASURE',
            fontsize=14, fontweight='bold', ha='center', transform=ax.transAxes, color='green')

    ax.text(0.75, 0.25, r'Preserves secrecy',
            fontsize=10, ha='center', transform=ax.transAxes, style='italic')

    # Orthogonal symbol
    ax.text(0.5, 0.5, r'⊥', fontsize=30, ha='center', transform=ax.transAxes, fontweight='bold')
    ax.text(0.5, 0.1, r'Quantum mechanically orthogonal',
            fontsize=12, ha='center', transform=ax.transAxes, style='italic')

    ax.axis('off')
    plt.tight_layout()
    plt.savefig('formula_observables.png', dpi=300, bbox_inches='tight',
                facecolor='white', edgecolor='none')
    plt.close()

    # Formula 8: Mathematical Proof
    fig, ax = plt.subplots(figsize=(12, 8))
    ax.text(0.5, 0.95, r'The Mathematical Proof',
            fontsize=18, fontweight='bold', ha='center', transform=ax.transAxes)

    # Define variables
    ax.text(0.5, 0.85, r'Let $|\text{secret}\rangle$ be the hidden information',
            fontsize=14, ha='center', transform=ax.transAxes)

    ax.text(0.5, 0.8, r'Let $|\text{witness}\rangle$ be the proof of knowledge',
            fontsize=14, ha='center', transform=ax.transAxes)

    ax.text(0.5, 0.75, r'Let $U_{\text{entangle}}$ be our entanglement operation',
            fontsize=14, ha='center', transform=ax.transAxes)

    # Main proof state equation
    ax.text(0.5, 0.65, r'$|\psi_{\text{proof}}\rangle = U_{\text{entangle}}(|\text{secret}\rangle \otimes |\text{witness}\rangle)$',
            fontsize=16, ha='center', transform=ax.transAxes,
            bbox=dict(boxstyle="round,pad=0.5", facecolor='lightblue', alpha=0.8))

    # Verification measurement
    ax.text(0.5, 0.5, r'Verification measures: $\langle\text{validity\_check}|\psi_{\text{proof}}\rangle$',
            fontsize=14, ha='center', transform=ax.transAxes,
            bbox=dict(boxstyle="round,pad=0.3", facecolor='lightgreen', alpha=0.6))

    # Orthogonal spaces
    ax.text(0.5, 0.35, r'Secret remains in: $\text{span}\{|\text{secret}\rangle\} \perp \text{span}\{|\text{validity\_check}\rangle\}$',
            fontsize=14, ha='center', transform=ax.transAxes,
            bbox=dict(boxstyle="round,pad=0.3", facecolor='lightyellow', alpha=0.6))

    # Conclusion
    ax.text(0.5, 0.2, r'Since these spaces are orthogonal, measuring validity',
            fontsize=14, ha='center', transform=ax.transAxes, fontweight='bold')

    ax.text(0.5, 0.15, r"doesn't collapse the secret subspace.",
            fontsize=14, ha='center', transform=ax.transAxes, fontweight='bold')

    # Add QED symbol
    ax.text(0.5, 0.05, r'∎', fontsize=20, ha='center', transform=ax.transAxes, fontweight='bold')

    ax.axis('off')
    plt.tight_layout()
    plt.savefig('formula_mathematical_proof.png', dpi=300, bbox_inches='tight',
                facecolor='white', edgecolor='none')
    plt.close()

def create_gantt_chart():
    """Create a PNG version of the IBM Quantum execution timeline"""
    import matplotlib.dates as mdates
    from datetime import datetime, timedelta

    fig, ax = plt.subplots(figsize=(12, 6))

    # Define the tasks and their dates
    tasks = [
        ('Bell State Preparation', datetime(2025, 5, 22), 1, '#4CAF50'),
        ('QZKP Circuit Testing', datetime(2025, 5, 23), 1, '#2196F3'),
        ('128-bit Secure Proof', datetime(2025, 5, 24), 0.5, '#FF9800'),
        ('256-bit Ultra-Secure Proof', datetime(2025, 5, 24, 12), 0.5, '#F44336'),
        ('Text Message Conversion', datetime(2025, 5, 25), 0.33, '#9C27B0'),
        ('Binary/Unicode Conversion', datetime(2025, 5, 25, 8), 0.33, '#673AB7'),
        ('Cryptographic Hash Conversion', datetime(2025, 5, 25, 16), 0.33, '#3F51B5')
    ]

    # Create the Gantt chart
    y_pos = range(len(tasks))

    for i, (task, start_date, duration, color) in enumerate(tasks):
        ax.barh(i, duration, left=start_date, height=0.6,
               color=color, alpha=0.8, edgecolor='black')

        # Add task labels
        ax.text(start_date + timedelta(hours=duration*12), i, task,
               va='center', ha='left', fontsize=10, fontweight='bold')

    # Format the chart
    ax.set_yticks(y_pos)
    ax.set_yticklabels([])
    ax.set_xlabel('Date (May 2025)', fontsize=12, fontweight='bold')
    ax.set_title('IBM Quantum Execution Timeline\nQuantum Backend: IBM ibm_brisbane (127 qubits)',
                fontsize=16, fontweight='bold', pad=20)

    # Format x-axis
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %d'))
    ax.xaxis.set_major_locator(mdates.DayLocator())

    # Set date range
    ax.set_xlim(datetime(2025, 5, 21, 12), datetime(2025, 5, 26))

    # Add grid
    ax.grid(True, alpha=0.3)

    # Add job IDs as annotations
    job_ids = [
        'd0smnrfvx7bg00819cx0',
        'd0smx1wvx7bg00819dm0',
        'd0smxp6vx7bg00819dqg',
        'd0sn3b54mb60008xb2qg',
        'd0sn57m1wej00088rhn0',
        'd0sn59x1wej00088rhpg',
        'd0sn5c57qc70008r9c1g'
    ]

    for i, job_id in enumerate(job_ids):
        ax.text(0.02, 0.95 - i*0.12, f'{i+1}. {job_id}',
               transform=ax.transAxes, fontsize=8,
               bbox=dict(boxstyle="round,pad=0.2", facecolor='lightgray', alpha=0.7))

    plt.tight_layout()
    plt.savefig('ibm_quantum_timeline.png', dpi=300, bbox_inches='tight',
                facecolor='white', edgecolor='none')
    plt.close()

if __name__ == "__main__":
    print("Creating Quantum ZKP visualizations...")

    # Create all diagrams
    create_quantum_state_diagram()
    create_orthogonal_subspaces_diagram()
    create_classical_vs_quantum_comparison()
    create_mermaid_style_flow()
    create_formula_images()
    create_gantt_chart()

    print("All visualizations saved to current directory!")
    print("Generated files:")
    print("- quantum_zkp_flow.png")
    print("- orthogonal_subspaces.png")
    print("- classical_vs_quantum_zkp.png")
    print("- probabilistic_entanglement_flow.png")
    print("- formula_probabilistic_encoding.png")
    print("- formula_quantum_state.png")
    print("- formula_entanglement.png")
    print("- formula_verification.png")
    print("- formula_entangled_proof_state.png")
    print("- formula_quantum_interference.png")
    print("- formula_observables.png")
    print("- formula_mathematical_proof.png")
    print("- ibm_quantum_timeline.png")
