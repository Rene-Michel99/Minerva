circle = ""
with open("circle.txt","r",encoding='utf-8') as f:
    circle = f.readlines()

output = ""
thickness = 3
for i,line in enumerate(circle):
    if i == 0 or i == len(circle)-1:
        output += line
    else:
        new_line = ""
        passed = False
        for i in range(len(line)-thickness):
            if line[i] == " ":
                new_line += line[i]
                continue
            
            if  line[i] != " " and line[i+1] != " ":
                if not passed:
                    new_line += line[i]*thickness
                    passed = True
                else:
                    new_line += " "
            else:
                new_line = new_line[0:len(new_line)-thickness-2]
                new_line += "▓"*thickness+"     "+"\n"
                break
        output += new_line
with open("circle.txt","w",encoding='utf-8') as f:
    f.write(output)

print(output)