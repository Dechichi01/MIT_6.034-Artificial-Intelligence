from production import AND, OR, NOT, PASS, FAIL, IF, THEN, \
     match, populate, simplify, variables
from zookeeper import ZOOKEEPER_RULES

# This function, which you need to write, takes in a hypothesis
# that can be determined using a set of rules, and outputs a goal
# tree of which statements it would need to test to prove that
# hypothesis. Refer to the problem set (section 2) for more
# detailed specifications and examples.

# Note that this function is supposed to be a general
# backchainer.  You should not hard-code anything that is
# specific to a particular rule set.  The backchainer will be
# tested on things other than ZOOKEEPER_RULES.

def backchain_antecedents(rules, bindings, rule):

	tree = []

	antecedents = rule.antecedent()

	if isinstance(antecedents, str): antecedents = AND(antecedents)

	for antecedent in antecedents:

		branch = simplify(backchain_support(rules, populate(antecedent, bindings)))

		if branch is None:
			tree.append(populate(antecedent, bindings))
		else:
			tree.append(branch)

	if isinstance(rule.antecedent(), AND): return simplify(AND(tree))
	else: return simplify(OR(tree))


def backchain_support(rules, hypothesis):

	tree = []

	for rule in rules:
		for consequent in rule.consequent():
			bindings = match(consequent, hypothesis)
		
			if bindings is not None:
				tree.append(populate(consequent, bindings))	
				tree.append(backchain_antecedents(rules, bindings, rule))

	if len(tree) is not 0: return simplify(OR(tree))


def backchain_to_goal_tree(rules, hypothesis):

	tree = backchain_support(rules, hypothesis)
	
	if tree is None: 
		return [hypothesis]

	return tree

    #raise NotImplementedError

# Here's an example of running the backward chainer - uncomment
# it to see it work:
print backchain_to_goal_tree(ZOOKEEPER_RULES, 'opus is a penguin')
