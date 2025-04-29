#!/usr/bin/env python3
# Peptide Distribution Visualization Tool
# Optimized for compact 2-3 row layout

import argparse
import os
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.colors import LinearSegmentedColormap
from Bio import SeqIO
import numpy as np
from collections import defaultdict

def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description='Visualize peptide distributions across proteins.')
    parser.add_argument('--fasta', required=True, help='Path to protein sequences FASTA file')
    parser.add_argument('--peptides', required=True, help='Path to peptides text file (one per line)')
    parser.add_argument('--mutations', type=int, default=0, help='Number of mutations allowed (default: 0)')
    parser.add_argument('--output', default='peptide_plots', help='Output directory for plots (default: peptide_plots)')
    parser.add_argument('--dpi', type=int, default=300, help='DPI for output images (default: 300)')
    parser.add_argument('--format', default='png', choices=['png', 'pdf', 'svg', 'jpg'], help='Output format (default: png)')
    parser.add_argument('--width', type=float, default=12, help='Figure width in inches (default: 12)')
    parser.add_argument('--height', type=float, default=6, help='Figure height in inches (default: 6)')
    parser.add_argument('--title', action='store_true', help='Add protein name as title')
    parser.add_argument('--color-by-mutations', action='store_true', help='Color peptides by number of mutations')
    parser.add_argument('--label-peptides', action='store_true', help='Add peptide sequence labels')
    parser.add_argument('--show-legend', action='store_true', help='Show legend (default: hidden)')
    return parser.parse_args()

def read_fasta(fasta_file):
    """Read protein sequences from FASTA file."""
    proteins = {}
    for record in SeqIO.parse(fasta_file, "fasta"):
        proteins[record.id] = str(record.seq)
    return proteins

def read_peptides(peptides_file):
    """Read peptides from text file."""
    with open(peptides_file, 'r') as f:
        return [line.strip() for line in f if line.strip()]

def count_mutations(seq1, seq2):
    """Count number of mutations between two sequences of equal length."""
    return sum(a != b for a, b in zip(seq1, seq2))

def find_peptide_positions(peptide, protein_seq, mutations_allowed=0):
    """Find positions of a peptide in a protein sequence, allowing for mutations."""
    positions = []
    peptide_len = len(peptide)
    
    # Skip if peptide is longer than protein
    if peptide_len > len(protein_seq):
        return positions
    
    # Search for matches with allowed mutations
    for i in range(len(protein_seq) - peptide_len + 1):
        substring = protein_seq[i:i+peptide_len]
        mutations = count_mutations(peptide, substring)
        
        if mutations <= mutations_allowed:
            # Record 1-based positions for consistency with common notation
            positions.append({
                'start': i + 1,
                'end': i + peptide_len,
                'mutations': mutations,
                'sequence': substring
            })
    
    return positions

def create_plot(protein_name, protein_seq, peptide_matches, args):
    """Create a visualization of peptide distribution across a protein."""
    fig, ax = plt.figure(figsize=(args.width, args.height)), plt.gca()
    
    protein_length = len(protein_seq)
    max_peptides = len(peptide_matches)
    
    # Publication-quality colors
    protein_color = '#FFE6E6'  # Light pink for protein background
    exact_match_color = '#DD2222'  # Red for peptide bars, matching example
    mutation_color = '#FFAA22'  # Orange for mutations
    
    # Create colormap for mutations if needed
    if args.color_by_mutations and args.mutations > 0:
        cmap = LinearSegmentedColormap.from_list(
            "mutation_cmap", [exact_match_color, "#FF7722", mutation_color], N=args.mutations+1)
    
    # Set clean, white background
    ax.set_facecolor('white')
    fig.patch.set_facecolor('white')
    
    # Configure axes for publication quality
    for spine in ax.spines.values():
        spine.set_linewidth(0.5)
        spine.set_color('#999999')
    
    # Plot protein track at the bottom of the plot with thicker outline
    ax.add_patch(plt.Rectangle((0, 0), protein_length, 0.8, 
                              facecolor=protein_color, edgecolor='#FFCCCC', 
                              linewidth=0.5, zorder=1))
    
    # Add protein position markers
    tick_positions = list(range(0, protein_length+1, max(1, protein_length // 10)))
    ax.set_xticks(tick_positions)
    ax.set_xticklabels([str(pos) for pos in tick_positions], fontsize=9)
    ax.tick_params(axis='x', which='both', width=0.5, length=3, pad=2, colors='#333333')
    
    # Eliminate the gap between axis and bars
    ax.spines['left'].set_position(('data', 0))
    ax.spines['bottom'].set_position(('data', 0))
    
    # Maximum number of rows to use (2 rows as shown in example)
    max_rows = 2
    
    # Organize peptides into rows with minimal overlap
    rows = [[] for _ in range(max_rows)]
    row_end_positions = [0] * max_rows
    
    # Sort matches by start position first, then by length (shorter first)
    # This helps with more efficient packing
    sorted_matches = sorted(peptide_matches, key=lambda x: (x['start'], x['end'] - x['start']))
    
    # Assign peptides to rows
    for match in sorted_matches:
        start_pos = match['start'] - 1  # Convert to 0-based for plotting
        end_pos = match['end'] - 1
        
        # Find suitable row
        assigned = False
        for row_idx in range(max_rows):
            # Check if there's enough space in this row
            if start_pos > row_end_positions[row_idx] + 10:  # Add small gap between peptides
                rows[row_idx].append(match)
                row_end_positions[row_idx] = end_pos
                assigned = True
                break
        
        # If all rows are occupied at this position, use the row with the earliest ending position
        if not assigned:
            best_row = min(range(max_rows), key=lambda i: row_end_positions[i])
            rows[best_row].append(match)
            row_end_positions[best_row] = max(row_end_positions[best_row], end_pos)
    
    # Plot peptides by row - using thinner bars as requested
    for row_idx, row_matches in enumerate(rows):
        y_position = 1.2 + row_idx * 0.7  # Position above the protein track with consistent spacing
        
        for match in row_matches:
            start_pos = match['start'] - 1  # Convert to 0-based for plotting
            peptide_length = match['end'] - match['start'] + 1
            
            # Use thinner peptide bars (half height) as requested
            peptide_height = 0.4
            
            # Determine color based on mutations
            if args.color_by_mutations and args.mutations > 0:
                color = cmap(match['mutations'] / args.mutations)
            else:
                color = exact_match_color if match['mutations'] == 0 else mutation_color
            
            # Add peptide rectangle
            rect = plt.Rectangle((start_pos, y_position), peptide_length, peptide_height,
                               facecolor=color, edgecolor=color, linewidth=0, zorder=2)
            ax.add_patch(rect)
            
            # Add peptide label if requested
            if args.label_peptides:
                label_text = f"{match['peptide']}"
                if match['mutations'] > 0:
                    label_text += f" ({match['mutations']} mut)"
                label_text += f" [{match['start']}-{match['end']}]"
                
                ax.text(start_pos + peptide_length + 5, y_position + (peptide_height/2), 
                       label_text, fontsize=8, va='center', color='#333333')
    
    # Set plot limits and labels with no padding after protein end
    ax.set_xlim(0, protein_length)  # Remove gap after protein end
    ax.set_ylim(-0.2, 1.2 + (max_rows * 0.7) + 0.2)  # Adjust height based on max rows
    
    # Make the axis labels more publication-worthy
    ax.set_xlabel('Amino Acid Position', fontsize=10, labelpad=4, color='#333333')
    
    # Custom y-axis label with proper rotation
    if max_rows >= 2:
        ax.text(-protein_length*0.03, 1.5 + (max_rows * 0.7)/2, 'Peptides', 
               rotation=90, va='center', ha='center', fontsize=10, color='#333333')
    
    # Remove y-axis ticks and labels
    ax.set_yticks([])
    for spine in ['top', 'right', 'left']:
        ax.spines[spine].set_visible(False)
    
    # Add title if requested
    if args.title:
        ax.set_title(f"{protein_name}", fontsize=12, pad=10, color='#333333')
    
    # Add protein name label on the protein bar if not showing title
    if not args.title:
        ax.text(protein_length/2, 0.4, protein_name, 
               ha='center', va='center', fontsize=10, color='#333333', weight='bold')
    
    # Add legend only if requested
    if args.show_legend:
        legend_patches = []
        legend_patches.append(mpatches.Patch(color=exact_match_color, label='Exact Match'))
        
        if args.mutations > 0:
            if args.color_by_mutations:
                for i in range(1, args.mutations + 1):
                    color = cmap(i / args.mutations)
                    legend_patches.append(mpatches.Patch(color=color, label=f'{i} Mutation{"s" if i > 1 else ""}'))
            else:
                legend_patches.append(mpatches.Patch(color=mutation_color, label='With Mutations'))
        
        ax.legend(handles=legend_patches, loc='upper right', frameon=False, fontsize=9)
    
    # Adjust layout
    plt.tight_layout()
    
    return fig

def main():
    """Main function to process files and create visualizations."""
    args = parse_args()
    
    # Set publication quality defaults for matplotlib
    plt.rcParams['svg.fonttype'] = 'none'  # Ensures text remains editable in SVG
    plt.rcParams['pdf.fonttype'] = 42  # Ensures text remains editable in PDF
    plt.rcParams['font.family'] = 'sans-serif'
    plt.rcParams['font.sans-serif'] = ['Arial', 'Helvetica', 'DejaVu Sans']
    plt.rcParams['axes.linewidth'] = 0.5
    plt.rcParams['xtick.major.width'] = 0.5
    plt.rcParams['ytick.major.width'] = 0.5
    
    # Create output directory if it doesn't exist
    if not os.path.exists(args.output):
        os.makedirs(args.output)
    
    # Read input files
    proteins = read_fasta(args.fasta)
    peptides = read_peptides(args.peptides)
    
    print(f"Loaded {len(proteins)} proteins and {len(peptides)} peptides")
    print(f"Searching with {args.mutations} mutations allowed")
    
    # Process each protein
    for protein_name, protein_seq in proteins.items():
        print(f"Processing {protein_name} ({len(protein_seq)} aa)")
        
        # Find all peptide matches
        all_matches = []
        
        for peptide in peptides:
            matches = find_peptide_positions(peptide, protein_seq, args.mutations)
            
            for match in matches:
                all_matches.append({
                    'peptide': peptide,
                    **match
                })
        
        # Sort by start position
        all_matches.sort(key=lambda x: x['start'])
        # Remove duplicates
        
        print(f"  Found {len(all_matches)} peptide matches")
        
        if all_matches:
            # Create and save visualization
            fig = create_plot(protein_name, protein_seq, all_matches, args)
            
            # Adjust figure to remove external padding
            plt.subplots_adjust(left=0.05, right=0.98, top=0.95, bottom=0.1)
            
            # Save the figure
            output_path = os.path.join(args.output, f"{protein_name}_peptide_distribution.{args.format}")
            fig.savefig(output_path, dpi=args.dpi, bbox_inches='tight', pad_inches=0.1,
                       facecolor='white', edgecolor='none', transparent=False)
            plt.close(fig)
            
            print(f"  Saved plot to {output_path}")
    
    print("Done!")

if __name__ == "__main__":
    main()