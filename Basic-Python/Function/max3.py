# define the max function to find maximum number
def maxNum(num1, num2, num3):
    if(num1 > num2 and num1 > num3):
        return f"The max number is {num1}"
    elif(num2 > num1 and num2 > num3):
        return f"The max number is {num2}"
    else:
        return f"The max number is {num3}"
# input number
a = input("Enter your first number \n")
b = input("Enter your second number \n")
c = input("Enter your last number \n")

print(maxNum(a, b, c))