from functions.run_python import run_python_file

# Test 1
print("Result for current directory:")
result1 = run_python_file("calculator", "main.py")
print(result1)

# Test 2  
print("\nResult for 'pkg' directory:")
result2 = run_python_file("calculator", "tests.py")

print(result2)

# Test 3
print("\nResult for '/bin' directory:")
result3 = run_python_file("calculator", "../main.py")
print(result3)

result4 = run_python_file("calculator", "nonexistent.py")
print(result4)