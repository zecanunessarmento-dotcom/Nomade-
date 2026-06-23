frequencia = int (input("frequencia: "))
nota = int (input("nota: "))
if frequencia >=75:
    if nota >=60:
        print("aprovado")
    else:
        print("reprovado por nota")
else:
    print("reprovado por frequencia")    