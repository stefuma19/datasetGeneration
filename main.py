import datasetgen
import sys
import skyline

"""
Main
To run: "python main.py generation_method number_of_samples_ dim output_filename compute_skyline", where:
        method: the method through which the datasets will be generated
        number_of_samples: the number of rows of the output dataset 
        dim: the number of columns of the output dataset
        output_filename: the name of the output file. The name needs to end with ".csv"
        compute_skyline: if equal to 1 the skyline of the dataset will be computed and saved 
    
The output consists in a CSV file containing the generated dataset. The resulting dataset will be normalized.
    Note: the dimensions of the output file will be of the type x1, x2, ..., xn
It is possible to optionally save the skyline of the generated dataset if compute_skyline is set to 1
"""
if __name__ == '__main__':
    method = sys.argv[1]
    number_of_samples = int(sys.argv[2])
    dim = int(sys.argv[3])
    output_filename = sys.argv[4]
    compute_skyline = sys.argv[5]

    if method == 'uniform':
        dataset = datasetgen.generate_uniform(number_of_samples, dim)
    elif method == 'normal':
        dataset = datasetgen.generate_normal(number_of_samples, dim)
    elif method == 'exponential':
        dataset = datasetgen.generate_exponential(number_of_samples, dim)
    elif method == 'multivariate_normal':
        mean = [1, 1]
        cov = [[1, 0], [0, 1]]
        dataset = datasetgen.generate_multivariate_normal(number_of_samples, mean=mean, cov=cov)
    elif method == 'cor_neg':
        mean = [1, 1]
        cov = [[1, -0.8], [-0.8, 1]]
        dataset = datasetgen.generate_multivariate_normal(number_of_samples, mean=mean, cov=cov)
    elif method == 'cor_pos':
        mean = [1, 1]
        cov = [[1, 0.8], [0.8, 1]]
        dataset = datasetgen.generate_multivariate_normal(number_of_samples, mean=mean, cov=cov)

    datasetgen.save_dataset_to_csv(dataset, output_filename)
    if compute_skyline == '1':
        skyline.create_and_save_skyline(output_filename)
