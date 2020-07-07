# T = int(input().strip())
# while T != 0:
#     N, K, A = map(int, input().split())
#     num = list(map(int, input().split()))
#     op = input()
#     if K == 0:
#         print(A)
#     else:
#         if op == "AND":
#             for j in num:
#                 A = A & j
#             print(A)
#         elif op == "OR":
#             for j in num:
#                 A = A | j
#             print(A)
#         elif op == "XOR":
#             if (K % 2) == 0:
#                 pass
#             else:
#                 for j in num:
#                     A = A ^ j
#             print(A)
#     T -= 1
import pandas as pd
df = pd.read_excel('C:/Users/Usman Khan/Desktop/Accession Register.xls')
for index,row in df.iterrows():
    print(row[0])
    print(row[1])
