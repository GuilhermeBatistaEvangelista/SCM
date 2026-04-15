def convert_solution_func(data, optimal_order):
	"""Reorganiza os dados de acordo com a ordem ótima."""
	return data[optimal_order].copy()

def createVetOrder(order_samples):
	original_order = order_samples
	order_vector = [None] * len(original_order) # Initialize order_vector
	for i in range(len(original_order)):
		order_vector[i] = i # Assign value

	return order_vector

def changeOrdering(initial_order, first_variable):
	new_order = [None] * len(initial_order)
	position = 0
	new_order[position] = first_variable
	position += 1
	for i in range(len(initial_order)):
		if i not in [x for x in new_order if x is not None]:
			new_order[position] = i
			position += 1

	return new_order