
#mult_scalar
def mult_scalar(matrix, scale):
	local_matrix = [[]*len(matrix[0]) for i in range(len(matrix))]

	for i in range(len(matrix)):
		for j in range(len(matrix[i])):
			local_matrix[i].append(scale * matrix[i][j])
	return local_matrix

#mult_matrix
def mult_matrix(a, b):
	if len(a[0]) != len(b):
		return None
	else:
		# to initialize a matrix with all zero elements in the form of a result matrix
		result = [[0 for i in range(len(b[0]))] for j in range(len(a))]
		
		for i in range(len(a)):
			for j in range(len(b[0])):
				for k in range(len(a[0])):
					result[i][j] += a[i][k] * b[k][j]

	return result

#euclidean
def euclidean_dist(a,b):
	result = 0
	for i in range(len(a[0])):
		result += (a[0][i] - b[0][i])**2

	result = result**0.5

	return result

