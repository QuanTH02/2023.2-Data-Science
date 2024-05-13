str1 = '"Roman J. Israel, Esq.",1.0,2018.0,,,,'

a = str1.split("\"")

b = a[2].split(",")

print(b[1])