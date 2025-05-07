#!/usr/bin/env python3

import matplotlib.pyplot as plt
import warnings

"""
Bayesian Network is a probabilistic graphical model reasoning system.
It represents a set of variables and their conditional dependencies via a directed acyclic graph (DAG).
The nodes represent the variables, and the edges represent the conditional dependencies.
The Bayesian network is used to model the relationships between different variables and to perform probabilistic inference.

This scenario covers a Bayesian network with nodes representing various factors related to climate change and sustainability.
"""

class BayesianNetwork:
    def __init__(self):
        print("Bayesian Network start.\n")
        # Defining positions for each node (x, y) for visualization
        self.positions = {
            'SE': (20, 0),   # SocioEconomic
            'PI': (0, 0),    # PoliticalInitiative
            'U':  (20, 20),  # Urbanisation
            'JM': (17, 5),   # JobMarket
            'CP': (4, 2),    # ClimatePolicy
            'CEA':(11, 1),   # CleanEnergyAdoption
            'TI': (12, 6),   # TechInnovation
            'CE': (7, 20),   # CarbonEmissions
            'EF': (13, 15)   # EcologicalFootprint
        }
        # Defining categories for color-coding nodes
        self.node_category = {
            'SE': 'Social development',
            'PI': 'Social development',
            'U':  'Ecology',
            'JM': 'Social development',
            'CP': 'Social development',
            'CEA':'Sustainability',
            'TI': 'Sustainability',
            'CE': 'Ecology',
            'EF': 'Ecology'
        }
        # Assigning colors to each category
        self.category_colors = {
            'Ecology': 'lightgreen',
            'Sustainability': 'lightskyblue',
            'Social development': 'lightcoral'
        }
        # Directed edges: (parent, child)
        self.edges = [
            ('SE', 'U'), ('SE', 'JM'), ('SE', 'CEA'),
            ('PI', 'CP'), ('CP', 'CE'), ('CP', 'CEA'),
            ('U', 'CE'), ('U', 'EF'), ('CEA', 'TI'),
            ('CEA', 'CE'), ('JM', 'TI'), ('TI', 'CE'),
            ('TI', 'EF'), ('CE', 'EF')
        ]
        # Conditional Probability Tables (CPTs) - values are predefined for simplicity
        # Range of 0 to 1 means probability %
        self.cpt = {
            # Prior probabilities for root nodes
            'SE': {'High': 0.6, 'Low': 0.4},
            'PI': {'Stable': 0.7, 'Unstable': 0.3},
            # P(CP | PI)
            'CP': {
                ('Stable', 'Strict'): 0.8,
                ('Stable', 'Average'): 0.2,
                ('Unstable', 'Strict'): 0.3,
                ('Unstable', 'Average'): 0.7
            },
            # P(CEA | SE, CP)
            'CEA': {
                ('High', 'Strict', 'High'): 0.85,
                ('High', 'Strict', 'Low'):  0.15,
                ('High', 'Average', 'High'):0.6,
                ('High', 'Average', 'Low'): 0.4,
                ('Low',  'Strict', 'High'): 0.5,
                ('Low',  'Strict', 'Low'):  0.5,
                ('Low',  'Average', 'High'):0.2,
                ('Low',  'Average', 'Low'): 0.8
            },
            # P(CE | CEA, CP)
            'CE': {
                ('High', 'Strict', 'Low'): 0.9,
                ('Low',  'Strict', 'High'):0.7,
                ('High', 'Average', 'Low'):0.3,
                ('Low',  'Average', 'High'):0.2
            }
        }
        self.print_cpt()

    def print_cpt(self):
        # Print the Conditional Probability Tables (CPTs)
        print("Conditional Probability Tables:")
        for node, table in self.cpt.items():
            print(f"\nNode: {node}")
            for condition, prob in table.items():
                # Format condition: string or tuple
                cond_str = condition if isinstance(condition, str) else ", ".join(condition)
                print(f"P({node} | {cond_str}) = {prob}")

    def d_separation(self, node1, node2, given):
        """
        Check simplified d-separation for example cases:
        - PI and CE are independent given CP
        - SE and CE are independent given CEA
        """
        if node1 == 'PI' and node2 == 'CE' and 'CP' in given:
            print("D-separation: PI and CE are independent given CP.")
            return True
        if node1 == 'SE' and node2 == 'CE' and 'CEA' in given:
            print("D-separation: SE and CE are independent given CEA.")
            return True
        print(f"No d-separation found between {node1} and {node2} given {given}.")
        return False

    def query(self):
        """
        Computation of P(CE=Low | SE=High, PI=Stable) step by step:
        1. Use CPTs to get P(CP | PI)
        2. Get P(CEA=High | SE, CP)
        3. Multiply by prior P(CP) and sum
        4. Finally get P(CE=Low | CEA, CP)
        """
        print("\nQuery: P(CE=Low | SE=High, PI=Stable)\n")
        # Check conditional independencies
        self.d_separation('PI', 'CE', ['CP'])
        self.d_separation('SE', 'CE', ['CEA'])
        # Step 1: Probabilities for CP given PI=Stable
        p_cp_strict  = self.cpt['CP'][('Stable', 'Strict')]
        p_cp_average = self.cpt['CP'][('Stable', 'Average')]
        # Step 2: Probabilities for CEA=High given SE=High and CP
        p_cea_high_if_strict  = self.cpt['CEA'][('High', 'Strict', 'High')]
        p_cea_high_if_average = self.cpt['CEA'][('High', 'Average', 'High')]
        # Marginalize over CP to get P(CEA=High)
        p_cea_high = p_cea_high_if_strict*p_cp_strict + p_cea_high_if_average*p_cp_average
        # Step 3: P(CE=Low | CEA=High, CP=Strict)
        p_ce_low_if = self.cpt['CE'][('High', 'Strict', 'Low')]
        # Final probability
        p_ce_low = p_ce_low_if * p_cea_high
        print(f"P(CE=Low | SE=High, PI=Stable) = {p_ce_low:.3f}")
        return p_ce_low

    def plot(self):
        # Visualize the Bayesian Network
        added = set()
        # Draw nodes
        for node, (x, y) in self.positions.items():
            cat = self.node_category[node]
            color = self.category_colors[cat]
            label = cat if cat not in added else None
            plt.scatter(x, y, s=900, c=color, label=label)
            plt.text(x, y, node, fontsize=14, ha='center', va='center')
            added.add(cat)
        # Draw edges
        for parent, child in self.edges:
            x1,y1 = self.positions[parent]
            x2,y2 = self.positions[child]
            plt.annotate('', xy=(x2,y2), xytext=(x1,y1),
                         arrowprops=dict(arrowstyle='-|>', color='gray'))
        plt.axis('off')
        # Show or save plot
        with warnings.catch_warnings(record=True) as caught:
            warnings.simplefilter("always")
            plt.show()
            if any(isinstance(w.message, UserWarning) for w in caught):
                plt.savefig("bayesian_network.png")
                print("\nWarning: could not display plot interactively; saved to 'bayesian_network.png'.")
            else:
                print("\nGraph was generated and displayed.")
        print("\n Bayesian Network end.\n" + "="*40 + "\n")


if __name__ == "__main__":
    bn = BayesianNetwork()
    bn.query()
    bn.plot()
