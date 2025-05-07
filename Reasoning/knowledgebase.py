import random

"""
This code scenario demonstrates a simple knowledge base system that uses logical reasoning to infer new facts based on existing ones.
The knowledge base contains facts about family relationships and eye color inheritance.
Family facts are:
- Alice and Bob are parents of Carol and Dave.
- Carol is a parent of Frank.
- Eve is a spouse of Dave.
- Carol has blue eyes.
- Frank's blue eyes are inherited from Carol with a 50% probability.
"""

class KnowledgeBase:
    def __init__(self):
        # Set of facts: tuples of the form (predicate, arg1, arg2, …)
        self.facts = set()
        # List of rules: each rule is ((head_predicate, [head_arguments]), body_list)
        self.rules = []
        self._define_rules()
        self._add_initial_facts()

        # Probabilistic inheritance of blue eyes for Frank
        self.frank_has_blue_eyes = False
        if random.random() < 0.5:
            # Add fact about inheritance
            self.add_fact('Inherits_blue_eyes', 'Frank', 'Carol')
            self.add_fact('Has_blue_eyes', 'Frank')
            self.frank_has_blue_eyes = True
            print("Probabilistic inheritance result: Frank inherited blue eyes from Carol.")
        else:
            print("Probabilistic inheritance result: Frank did not inherit blue eyes from Carol.")

        # Trigger inference of all derivable facts (forward chaining)
        self._infer_all()

    def add_fact(self, pred, *args):
        # Add a fact to the knowledge base
        self.facts.add((pred,) + args)

    def add_rule(self, head_pred, head_args, body):
        # Add a rule to the knowledge base
        # Rule means: if body is true, then head_pred with head_args is true
        self.rules.append(((head_pred, head_args), body))

    def _define_rules(self):
        """Define all logical rules."""
        # Parent(x,y) => Ancestor(x,y)
        self.add_rule('Ancestor', ['x','y'], [('Parent', ['x','y'])])
        # Parent(x,z) & Ancestor(z,y) => Ancestor(x,y)
        self.add_rule('Ancestor', ['x','y'], [('Parent', ['x','z']), ('Ancestor', ['z','y'])])
        # Parent(p,x) & Parent(p,y) => Sibling(x,y)
        self.add_rule('Sibling', ['x','y'], [('Parent', ['p','x']), ('Parent', ['p','y'])])
        # Parent(p1,x) & Parent(p2,y) & Sibling(p1,p2) => Cousin(x,y)
        self.add_rule('Cousin', ['x','y'], [
            ('Parent', ['p1','x']), 
            ('Parent', ['p2','y']), 
            ('Sibling', ['p1','p2'])
        ])
        # Parent(p,c) & Has_blue_eyes(p) => Inherits_blue_eyes(c,p)
        self.add_rule('Inherits_blue_eyes', ['c','p'], [
            ('Parent', ['p','c']), 
            ('Has_blue_eyes', ['p'])
        ])
        # Inherits_blue_eyes(c,p) => Has_blue_eyes(c)
        self.add_rule('Has_blue_eyes', ['c'], [('Inherits_blue_eyes', ['c','p'])])
        # Ancestor(x,y) & Has_blue_eyes(x) => Has_ancestor_with_blue_eyes(y)
        self.add_rule('Has_ancestor_with_blue_eyes', ['y'], [
            ('Ancestor', ['x','y']), 
            ('Has_blue_eyes', ['x'])
        ])

    def _add_initial_facts(self):
        # Add initial facts to the knowledge base
        facts = [
            ('Parent', 'Alice','Carol'), ('Parent','Bob','Carol'),
            ('Parent','Alice','Dave'),  ('Parent','Bob','Dave'),
            ('Parent','Carol','Frank'),
            ('Spouse','Eve','Dave'),     ('Spouse','Dave','Eve'),
            ('Has_blue_eyes','Carol')
        ]
        for pred, *args in facts:
            self.add_fact(pred, *args)

    def _infer_all(self):
        # Perform forward chaining to infer all possible facts
        added = True
        while added:
            added = False
            for (head_pred, head_args), body in self.rules:
                # Find all possible substitutions that satisfy the rule body
                for theta in self._find_thetas(body, {}):
                    # Create a new fact based on the rule head
                    head = (head_pred,) + tuple(theta.get(var, var) for var in head_args)
                    if head not in self.facts:
                        self.facts.add(head)
                        added = True

    def _find_thetas(self, body, theta):
        # Recursively find all substitutions that satisfy the body of a rule
        if not body:
            yield theta
            return
        pred, args = body[0]
        for fact in list(self.facts):
            if fact[0] != pred or len(fact)-1 != len(args):
                continue
            theta2 = self._unify(args, fact[1:], theta)
            if theta2 is not None:
                yield from self._find_thetas(body[1:], theta2)

    def _unify(self, atom_args, fact_args, theta):
        """
        Attempt to unify the arguments of an atom and a fact given the current substitution.
        atom_arg, ie ['x','y'], fact_args: ['Alice','Carol']
        theta: {'x':'Alice'}
        """
        theta = theta.copy()
        for a, f in zip(atom_args, fact_args):
            if a.islower():
                # a is a variable
                if a in theta:
                    if theta[a] != f:
                        return None
                else:
                    theta[a] = f
            else:
                # a is a constant
                if a != f:
                    return None
        return theta

    def query(self, pred, *args):
        # Query the knowledge base for a predicate with given arguments.
        fc = (pred,) + args in self.facts
        # Check if the predicate is a fact by backward chaining
        bc = self._backward(pred, list(args), {})
        return fc, bc

    def _backward(self, pred, args, theta):
        # Support backward chaining function to check if a predicate can be derived from the knowledge base
        # Check if it can be a fact
        for fact in self.facts:
            if fact[0] == pred:
                if self._unify(args, fact[1:], theta) is not None:
                    return True
        # Try applying a rule
        for (head_pred, head_args), body in self.rules:
            if head_pred != pred or len(head_args) != len(args):
                continue
            theta2 = self._unify(head_args, args, theta)
            if theta2 is None:
                continue
            # Check all atoms in the rule body
            ok = True
            for bpred, bargs in body:
                bargs_inst = [theta2.get(v, v) for v in bargs]
                if not self._backward(bpred, bargs_inst, theta2):
                    ok = False
                    break
            if ok:
                return True
        return False


# Implementing a simple logical reasoning system using a knowledge base.
class LogicalReasoning:
    def __init__(self):
        print("Logical Reasoning start.\n")
        self.kb = KnowledgeBase()

    def task1(self):
        print("Task 1: Does Frank have blue eyes?", self.kb.frank_has_blue_eyes)

    def task2(self):
        print("Task 2: Does Frank have an ancestor with blue eyes?")
        result, _ = self.kb.query('Has_ancestor_with_blue_eyes', 'Frank')
        print("Result:", result)

    def task3(self):
        print("Task 3: Are Carol and Eve cousins?")
        result, _ = self.kb.query('Cousin', 'Carol', 'Eve')
        print("Result:", result)

    def task4(self):
        print("Task 4: List ancestor relationships:")
        people = ['Alice', 'Bob', 'Carol', 'Dave', 'Frank']
        for ancestor in people:
            for descendant in people:
                if ancestor != descendant:
                    result, _ = self.kb.query('Ancestor', ancestor, descendant)
                    if result:
                        print(f"- {ancestor} is an ancestor of {descendant}")
        print("\nLogical Reasoning end.\n")
        print("==========================================\n")

# Main
if __name__ == "__main__":
    lr = LogicalReasoning()
    lr.task1()
    lr.task2()
    lr.task3()
    lr.task4()
