# 10 Desafios Simples de Lógica de Programação em Python

# =====================================================
# DESAFIO 1: Números Pares
# Crie um programa que verifique se um número é par ou ímpar
# =====================================================
numero = int(input("Digite um número: "))
if numero % 2 == 0:
    print(f"{numero} é par")
else:
    print(f"{numero} é ímpar")

print("-" * 50)

# =====================================================
# DESAFIO 2: Maior de Três Números
# Determine qual dos três números é o maior
# =====================================================
a = int(input("Digite o primeiro número: "))
b = int(input("Digite o segundo número: "))
c = int(input("Digite o terceiro número: "))

if a >= b and a >= c:
    print(f"O maior número é: {a}")
elif b >= a and b >= c:
    print(f"O maior número é: {b}")
else:
    print(f"O maior número é: {c}")

print("-" * 50)

# =====================================================
# DESAFIO 3: Tabuada
# Mostre a tabuada de um número digitado pelo usuário
# =====================================================
n = int(input("Digite um número para ver a tabuada: "))
for i in range(1, 11):
    print(f"{n} x {i} = {n * i}")

print("-" * 50)

# =====================================================
# DESAFIO 4: Soma de 1 até N
# Calcule a soma de todos os números de 1 até N
# =====================================================
n = int(input("Digite um número: "))
soma = sum(range(1, n + 1))
print(f"A soma de 1 até {n} é: {soma}")

print("-" * 50)

# =====================================================
# DESAFIO 5: Fatorial
# Calcule o fatorial de um número
# =====================================================
n = int(input("Digite um número para calcular o fatorial: "))
fatorial = 1
for i in range(1, n + 1):
    fatorial *= i
print(f"{n}! = {fatorial}")

print("-" * 50)

# =====================================================
# DESAFIO 6: Fibonacci
# Mostre os N primeiros números da sequência de Fibonacci
# =====================================================
n = int(input("Quantos números da Fibonacci deseja ver? "))
a, b = 0, 1
for i in range(n):
    print(a, end=" ")
    a, b = b, a + b
print()

print("-" * 50)

# =====================================================
# DESAFIO 7: Palíndromo
# Verifique se uma palavra é um palíndromo
# =====================================================
palavra = input("Digite uma palavra: ")
if palavra == palavra[::-1]:
    print(f"{palavra} é um palíndromo!")
else:
    print(f"{palavra} não é um palíndromo")

print("-" * 50)

# =====================================================
# DESAFIO 8: Números Primos
# Verifique se um número é primo
# =====================================================
n = int(input("Digite um número para verificar se é primo: "))
if n > 1:
    for i in range(2, n):
        if n % i == 0:
            print(f"{n} não é primo")
            break
    else:
        print(f"{n} é primo!")
else:
    print(f"{n} não é primo")

print("-" * 50)

# =====================================================
# DESAFIO 9: Inverter Número
# Inverta os dígitos de um número
# =====================================================
numero = input("Digite um número: ")
numero_invertido = numero[::-1]
print(f"Número invertido: {numero_invertido}")

print("-" * 50)

# =====================================================
# DESAFIO 10: Média de Notas
# Calcule a média de 5 notas e mostre se o aluno foi aprovado
# =====================================================
notas = []
for i in range(5):
    nota = float(input(f"Digite a {i+1}ª nota: "))
    notas.append(nota)

media = sum(notas) / len(notas)
print(f"Média: {media:.2f}")

if media >= 7:
    print("Aprovado!")
elif media >= 5:
    print("Em recuperação")
else:
    print("Reprovado")

print("-" * 50)
print("Fim dos 10 Desafios de Lógica!")
