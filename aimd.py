import matplotlib.pyplot as plt
import math
from mpl_toolkits.mplot3d import Axes3D

#define the alpha and beta for the 2 network windows x1(x axis) and x2(y axis)

#Define the Alpha (the rate for the additive increase)
alpha_x1 = 1
alpha_x2 = 1

#Define the beta values (multiplicative decrease)
beta_x1 = 0.5
beta_x2 = 0.5

#Define the total capacity the network can handle where any value above 
#causes it to scale down based on the beta values

total_capacity = 20 #for now we just use 20 as an example

#Initial values of x1 and x2

x1 = 2 
x2 = 9

def addPeakIndex(peak_index_list, index_before_multiplicative_decrease):

    peak_index_list.append(index_before_multiplicative_decrease)
    return



#This function checks if the graph converges

def isConverged(x1_allocation, x2_allocation, peak_index_list):
    # the idea behind this algorithm to check if the graph conveges is to compare the 
    #gradient before multiplicative decrease and after -> if they are similar can be deemed
    #as converged
    length_of_index_list = len(peak_index_list)
    minimum_n_to_converge = None

    
    try:
        for i in peak_index_list:

            # 2 sets of coordinates to get gradient before MD
            peak_point_x1 = x1_allocation[i]
            peak_point_x2 =  x2_allocation[i]

            before_peak_x1 = x1_allocation[i-1]
            before_peak_x2 = x2_allocation[i-1]

            # 2 sets of coordinates to get gradient after MD

            after_peak_point_x1 = x1_allocation[i+1]
            after_peak_point_x2 =  x2_allocation[i+1]

            next_x1 = x1_allocation[i+2]
            next_x2 = x2_allocation[i+2]

            #Find the gradient

            gradient_before_MD = (peak_point_x2 - before_peak_x2) / (peak_point_x1 -before_peak_x1)
            gradient_after_MD = (peak_point_x2 - after_peak_point_x2) / (peak_point_x1 - after_peak_point_x1)
            print(f"current index peak: {i}\n")
            print(f"gradient before MD : {gradient_before_MD}\ngradient after MD :{gradient_after_MD}\n\n")
            #This sets the minimum n to converge
            if(abs(gradient_after_MD - gradient_before_MD) < 0.01 and minimum_n_to_converge == None):
                minimum_n_to_converge = i
                print(f"the minimum n to converge is {i}")
            
    except:
        print(f"error : Not enough iterations after peak")




    return minimum_n_to_converge



# This function to iterate n times
def iterate(x1, x2, alpha_x1, alpha_x2, beta_x1, beta_x2, total_capacity, n, show_graph):
    
    x1_allocation = []
    x2_allocation = []
    peak_index_list = []
    #add initial window size to the allocation array
    x1_allocation.append(x1)
    x2_allocation.append(x2)

    for i in range(n):
        #print(i)

        #increase additively if within capacity
        if(x1 + x2 <= total_capacity):
            x1 = x1 + alpha_x1
            x2 = x2 + alpha_x2
        else: 
            # multiplicative decrease
            x1 = x1 * beta_x1
            x2 = x2 * beta_x2
            print(f"x2 {x2_allocation[i]}\n")
            addPeakIndex(peak_index_list=peak_index_list, index_before_multiplicative_decrease=i)

        #add updated window size to the allocation array
        x1_allocation.append(x1)
        x2_allocation.append(x2)
    
    print(f"the window value of x1 : {x1_allocation}\n")
    print(f"the window value of x2 : {x2_allocation}\n")
    print(f"index of peaks in graph = {peak_index_list}")

    min_n_to_converge  = isConverged(x1_allocation=x1_allocation, 
                                     x2_allocation=x2_allocation,peak_index_list=peak_index_list)
    
    print(f"the minimum n to converge is at {min_n_to_converge}")
    #plot the graph to see convergence expected: alpha / 1-beta for same values
    if show_graph == True:
        # Create the plot
        plt.plot(x1_allocation, x2_allocation)

        # Customize the plot axis labels
        plt.xlabel('x1 user allocation')  # Label for the X-axis
        plt.ylabel('x2 user allocation')  # Label for the Y-axis
        plt.title('AIMD Graph')  # Title of the plot

        #plot the FAIRNESS line: y = x
        x_values_fairness_line= [0, total_capacity]  # Only two points to define the line
        y_values_fairness_line = [0, total_capacity]  # y = x for both points

        # Plot the fairness line
        plt.plot(x_values_fairness_line, y_values_fairness_line, \
                label='Indefinite Line', linestyle='--', color = 'red')

        # Set graph to start from 0 on x and y axis
        plt.xlim(0,total_capacity)
        plt.ylim(0, total_capacity)

        #Display the graph
        plt.grid(True)  # Add gridlines (optional)
        plt.show()

    return min_n_to_converge


##### UNCOMMENT THIS PART TO TEST INDIVIDUAL ALPHA AND BETA VALUES ########

#iterate(x1 = x1, x2 =x2, alpha_x1 = alpha_x1, alpha_x2 = alpha_x2, beta_x1 = beta_x1,\
#         beta_x2 = beta_x2,total_capacity = total_capacity, n = 95, show_graph=True)


# FUNCTION TO PRINT THE TABLE OF DIFFERENT STARTING VALUES
def getMinIterations(total_capacity, iterations,alpha_x1, alpha_x2, beta_x1, beta_x2):
    
    x1_index_array = []
    x2_index_array = []
    min_n_array = []
    for i in range(total_capacity+1):
        for j in range(total_capacity+1):

            min_value = iterate(x1 = i, x2 =j, alpha_x1 = alpha_x1, alpha_x2 = alpha_x2, beta_x1 = beta_x1,\
            beta_x2 = beta_x2,total_capacity = total_capacity, n = iterations, show_graph= False)
            
            if(min_value != None):
                x1_index_array.append(i)
                x2_index_array.append(j)
                min_n_array.append(min_value)

    #print(f"the actual minimum value is {min_value}")
    
    #print(min_n_array)
    for i in range(len(min_n_array)):
        print(f"x1 value: {x1_index_array[i]}, x2 value: {x2_index_array[i]}, min iterations: {min_n_array[i]} ")
    
    # Create a figure and a 3D axis
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    # Plot the data points
    ax.scatter(x1_index_array, x2_index_array, min_n_array,\
                c='r', marker='o')  # 'c' is color, 'marker' is marker style

    # Set labels and title
    ax.set_xlabel('x1 initial value')
    ax.set_ylabel('x2 initial value')
    ax.set_zlabel('min n iterations')
    ax.set_title('Minimum iterations to converge')

    # Show the plot
    plt.show()

getMinIterations(total_capacity=20, iterations=95, alpha_x1=1, alpha_x2=1, beta_x1=0.5, beta_x2=0.5)