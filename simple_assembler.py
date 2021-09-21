# uncomment these 2 lines for taking a file as an input through console
# import sys                                    
# code = sys.stdin.read().splitlines()


# uncomment these 2 lines if you want to read your own ( custom )input file
with open('test_case1.txt') as f:  # here test_case1.txt is an input file with assembly code 
    code = f.read().splitlines()

# ACTUAL CODE STARTS FORM HERE  

#dictionary to map registers with their code
RegAddress = {
  "R0":"000",
  "R1":"001",
  "R2":"010",
  "R3":"011",
  "R4":"100",
  "R5":"101",
  "R6":"110",
  "FLAGS":"111"
}

# dictionary to map instructions with their opcode and type
operations = {
   "add":["00000","A"],
   "sub":["00001","A"],
   "mov1":["00010","B"],
   "mov2":["00011","C"],
   "ld":["00100","D"],
   "st":["00101","D"],
   "mul":["00110","A"],
   "div":["00111","C"],
   "rs":["01000","B"],
   "ls":["01001","B"],
   "xor":["01010","A"],
   "or":["01011","A"],
   "and":["01100","A"],
   "not":["01101","C"],
   "cmp":["01110","C"],
   "jmp":["01111","E"],
   "jlt":["10000","E"],
   "jgt":["10001","E"],
   "je":["10010","E"],
   "hlt":["10011","F"]
}

operations_symbol = ["add","sub","mov","ld","st","mul","div","rs","ls",
                   "xor","or","and","not","cmp","jmp","jlt","jgt","je","hlt"]

registers = [ "R0", "R1" , "R2" , "R3" , "R4" , "R5" , "R6"]
registers_flag= [ "R0", "R1" , "R2" , "R3" , "R4" , "R5" , "R6" , "FLAGS"]
labels=["hlt"]
variables=[]
error=False


#**********************************************************************************************************************************************
                               #***THIS IS ERROR HANDLING PART*** 
    # this piece of code will detect any syntax error in the input assembly code and display the error 


#*************************** THIS FUCTION CHECKS ERROR IN IMMEDIATE VALUES ********************************************#
def check_immediate(a):
    global error
    try:
        n = int(a[1:])
        if(n<0 or n>255):
            print("line no" , line_no , n ,"is not in range [0, 255] ", sep=' ')
            error=True

    except:
        print("line no" , line_no , "invalid immediate value", sep=' ')
        error=True



#**************************** THIS FUNCTION HANDLES ALL ERROR CASES OF TYPE A *******************************************#
def type_A(value):
    global error
    if(len(value)!=4):
        print("line no" , line_no , " wrong syntax used for", value[0],"instruction",sep=' ' )
        error=True
        return

    for i in range(1,len(value)):
        if(value[i]=="FLAGS"):
            print("line no" , line_no, " invalid use of flags ",sep=' ')
            error=True

        elif(value[i] not in registers):
            print("line no" , line_no ,'(',value[i],')', "is invalid register name ",sep=' ')
            error=True



#*************************** THIS FUNCTION HANDLES ALL ERROR CASES OF TYPE B ****************************************#
def type_B(value):
    global error
    if(len(value)!=3):
        print("line no" , line_no , " wrong syntax used for", value[0],"instruction",sep=' ' )
        error=True
        return   

    if(value[1]=="FLAGS"):
        print("line no" , line_no, " invalid use of flags ",sep=' ')
        error=True

    elif(value[1] not in registers):
        print("line no" , line_no ,'(',value[1],')', "is invalid register name ",sep=' ')
        error=True
        
    a = value[2]
    if(a[0]!="$"):
        print("line no", line_no , "use of " , a[0] , "is invalid" , sep=' ')
        error=True
    else:
        check_immediate(a)


#*************************** THIS FUNCTION HANDLES ALL ERROR CASES OF TYPE C ****************************************#
def type_C(value):
    global error
    if(len(value)!=3):
        print("line no" , line_no , " wrong syntax used for type C instruction",sep=' ' )
        error=True
        return

    if(value[1]=="FLAGS"):
        print("line no" , line_no, " invalid use of flags ",sep=' ')
        error=True

    elif(value[1] not in registers):
        print("line no" , line_no ,'(',value[1],')', "is invalid register name ",sep=' ')
        error=True

    if(value[0]=="mov2" and value[2] not in registers_flag):
        print("line no" , line_no , " invalid register or flag name ",sep=' ')
        error=True

    elif value[0]!="mov2" and value[2] not in registers:
        print("line no",line_no,"invalid register name",sep=' ')
        error=True



#*************************** THIS FUNCTION HANDLES ALL ERROR CASES OF TYPE D *****************************************#
def type_D(value):
    global error
    if(len(value)!=3):
        print("line no" , line_no , " wrong syntax used for", value[0],"instruction",sep=' ' )
        error=True
        return
        
    if(value[2] in labels):
        print("line no", line_no , "labels cannot be used inplace of variables", sep=' ')
        error=True

    elif(value[2] not in variables):
        print("line no" , line_no , '(',value[2] ,')'," is undefined variable",sep=' ')
        error=True



#*************************** THIS FUNCTION HANDLES ALL ERROR CASES OF TYPE E *******************************************#
def type_E(value):
    global error
    if(len(value)!=2):
        print("line no" , line_no , " wrong syntax used for", value[0],"instruction",sep=' ' )
        error=True
        return

    if(value[1] in variables):
        print("line no", line_no , "variables cannot be used inplace of labels", sep=' ')
        error=True
            
    elif(value[1] not in labels):
        print("line no" , line_no , '(',value[1],')' ," is undefined label ",sep=' ')
        error=True



#*************************** THIS FUNCTION HANDLES ALL ERROR CASES OF TYPE F *********************************************#
def type_F(value):
    if(line_no!=len(code)):
        print("line no", line_no , "hlt must be at the end",sep=' ')
        error=True

    elif(len(value)!=1):
        print("line no" , line_no , " wrong syntax used for", value[0],"instruction",sep=' ' )
        error=True



#***************************** THIS IS HELPER FUNCTION TO HANDLE CASES OF VARIABLES ***************************************#
def handle_variables(value):
    global error
    global flag
    if(value[0]!="var"):
        flag=1

    if value[0]=="var" and len(value)!=2:
        print("line no",line_no,"invalid syntax",sep=' ')
        error=True
        return

    if value[0]=="var":
        if(flag==1):
            print("line no", line_no , "variable not decalared in the beginning of code ",sep=' ')
            error=True
        if(value[1] in variables):
            print("line no", line_no , "mulitiple declaration of variable " , value[1] , sep=' ')
            error = True
        else:
            variables.append(value[1])   


#*********************************THIS HELPER FUNCTION TO HANDLE CASES OF LABELS ********************************#
def handle_labels(value):
    global error
    if(value[0][-1]==":"):
        if(value[0][0:-1] in labels):
            print("line no", line_no , "multiple definations of label " ,'(', value[0],')',sep=' ')
            error=True
        else:
            labels.append(value[0][0:-1])


#**********************************THIS IS HELPER FUNCTION TO HANDLE HALT *********************************************#
def handle_hlt(value):
    global error
    if(len(value)==2 ):
        if value[1]!="hlt":
            print("line no" ,line_no +1 ," no hlt instruction at the end ", sep=' ')
            error=True

    elif(value[0]!="hlt"):
        print("line no" ,line_no +1 ," no hlt instruction at the end ", sep=' ')
        error=True



#HANDLING ALL CASES OF VARIABLES 
line_no =0 
flag=0
for line in code:                                               
    line_no+=1
    if(len(line)==0):
        continue
    value = list(line.split())
    handle_variables(value)



# HANDLING ALL CASES OF LABELES 
line_no=0                                                         
for line in code:              
    line_no+=1
    if(len(line)==0):
        continue
    value = list(line.split())
    handle_labels(value)



 # HANDLING ALL CASES OF NORMAL INSTRUCTIONS
line_no=0                                                      
for line in code:
    line_no+=1
    if(len(line)==0):
        continue

    value = list(line.split())

    if line_no==len(code):
        handle_hlt(value)

    if(value[0]=="var"):
        continue

    if(value[0][0:-1] in labels):
        value.pop(0)

    if(len(value)==0):
        print("line no", line_no , "invalid defnation of labels",sep=' ')
        error=True
        continue
    
    if(value[0] not in operations_symbol):
        print("line no",line_no , '(',value[0],')'," is invalid instruction name ", sep=' ')
        error=True
        continue

    if(value[0]=="mov" and len(value)>=2):
        c = value[2][0]
        if(65<=ord(c)<=90 or 97<=ord(c)<=122):
            value[0]="mov2"
        else:
            value[0]="mov1"
    
    if (operations[value[0]][1] == "A"):
        type_A(value)
            
    elif (operations[value[0]][1] == "C"):
        type_C(value)
        
    elif (operations[value[0]][1] == "B"):
        type_B(value)

    elif (operations[value[0]][1] == "D"):
        type_D(value)
    
    elif (operations[value[0]][1] == "E"):
        type_E(value)

    elif (operations[value[0]][1] == "F"):
        type_F(value)

    else:
        print("line no",line_no,"invalid syntax",sep=' ')
        error=True


                          # this is printing the binary code part 
#********************************************************************************************************************************************
              # THIS IS ASSEMBLER THIS WILL RUN ONLY WHEN THERE ARE NO ERRORS IN THE ASSEMBLY CODE 
              

labels={}
variables={}

t=1
address=-1

if(error==True):
    exit()


#*********************************THIS LOOP WILL STORE THE ADDRESS OF ALL VARIABLES IN DICTIONARY*********************
for line in code:
    if len(line)==0:
        continue
    value = list(line.split())
    
    if(value[0] in operations_symbol):
        address+=1

    if value[0]=="hlt":
        labels[value[0]+":"]=address

    if(value[0][-1]==":"):
        address+=1
        labels[value[0]]=address
        

#********************************* THIS LOOP WILL STORE THE ADDRESS OF ALL LABELS IN DICTIONARY ***********************
for line in code:
    if(len(line)==0):
        continue
    value = list(line.split())
    if value[0]=="var" and len(value)==2:
        variables[value[1]]=t+address
        t+=1


#********************************* THIS IS MAIN LOOP TO COVERT ASSEMBLY INTO BINARY CODE *******************************
for line in code:

    if(len(line)==0):
        continue

    value = list(line.split())
    if( len(value)>1 and value[0] in labels and value[1] in operations_symbol):
        value.pop(0)

    if (value[0] in operations_symbol):

        if(value[0]=="mov" ):
            if(value[2][0]=="$"):
                value[0]="mov1"
            else:
                value[0]="mov2"

        if (operations[value[0]][1] == "B"):
            a = value[1]
            b = value[2][1:]
            b1 = bin(int(b))[2:]
            s = operations[value[0]][0] + RegAddress[a] + (8-len(b1))*"0" + b1

        elif (operations[value[0]][1] == "A"):
            a = value[1]
            b = value[2]
            c = value[3]
            s = operations[value[0]][0] + "00" + RegAddress[a] + RegAddress[b] + RegAddress[c]
    
        elif (operations[value[0]][1] == "C"):
            a = value[1]
            b = value[2]
            s = operations[value[0]][0] + "00000" + RegAddress[a] + RegAddress[b]

        elif (operations[value[0]][1] == "D"):
            a = value[1]
            b = bin(variables[value[2]])[2:]
            s = operations[value[0]][0] + RegAddress[a] + (8 - len(b)) * "0" + b

        elif (operations[value[0]][1] == "E"):
            a=value[1]
            b=bin(labels[a+":"])[2:]
            s=operations[value[0]][0] + "000" + (8 - len(b)) * "0" + b

        elif (operations[value[0]][1] == "F"):
            s = operations[value[0]][0] + "00000000000"

        print(s)


# ********************************THE END*********************************************************************