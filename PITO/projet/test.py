a = r'INSERT INTO "main"."ticket_model"'
b= r'("id", "reservation", "trajet_id", "prix")'
c= r'VALUES ('
d= r', 0, '
e= r', 50);'
k=1
j=1
for i in range(60):
    print(a+'\n\t'+b+'\n\t'+c+str(i+1)+d+str(k)+e)
    j=j+1
    if j>10:
        j=1
        k=k+1