import numpy as np
import random

def create_random_1d_list(list_len):
    #np_array = np.arange(0,list_len,1)
    # np_array = np.zeros(list_len)
    # np_array = np.ones(list_len)
    # np_array = np.full(5,list_len)
    np_array = np.random.randint(0,10,list_len)
    return np_array

def create_randon_2d_list(rows, columns):
    np_array = np.random.randint(10, size=(rows,columns))
    return np_array

def vectorization(np_list):
    np_list = np_list.astype(np.float64)
    if np_list.ndim == 1: 
        normalized_list = (np_list - np_list.min())/(np_list.max()-np_list.min())
        return normalized_list.tolist()
    if np_list.ndim == 2:
        np_list_flattened = np_list.flatten()
        normalized_list = (np_list_flattened - np_list_flattened.min())/(np_list_flattened.max()-np_list_flattened.min())
        normalized_list = normalized_list.reshape(np_list.shape)
        return normalized_list.tolist()
    
def convert_1D_to_2D(np_list,rows,columns):
    return np_list.reshape(rows, columns)



if __name__ == "__main__":
    random_1d_list = create_random_1d_list(20)
    print(f"np 1D list : {random_1d_list}")
    print(f"Avarage: {np.average(random_1d_list)}")
    print(f"Standard devation: {np.std(random_1d_list)}")
    print(f"Variance: {np.var(random_1d_list)}")
    print(f"Vectorized 1D Normalization: {vectorization(random_1d_list)}")
    print(f"Converted to 2D \n{convert_1D_to_2D(random_1d_list,2,10)}")
    print(("="*50))
    
    random_2d_list = create_randon_2d_list(5,5)
    print(f"np 2D list : \n{random_2d_list}")
    print(f"Avarage: {np.average(random_2d_list)}")
    print(f"Standard devation: {np.std(random_2d_list)}")
    print(f"Variance: {np.var(random_2d_list)}")
    print(f"Vectorized 2D Normalization: {vectorization(random_2d_list)}")
    print(("="*50))