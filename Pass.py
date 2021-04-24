##########################################################################################################################
####################### PUF BASED PASSWORD GENERATOR USING IMPROVED PROTOCOL #############################################
##########################################################################################################################
import numpy as np
from itertools import permutations
import hashlib

print("++++++++++++++ WELCOME TO NAU PASSWORD MANAGER +++++++++++++++++ \n ");
print("++++++++++++++ PRESS 1.ENROLLMENT 2.AUTHENTICATION +++++++++++++++++ \n ");

enroll_auth_id= input()
if enroll_auth_id == '1':
    print("Enrollment")
#defined hash function(sha256)
def hash(number):
    Hash= hashlib.sha256(str(number).encode())
    HashDigest = Hash.hexdigest()
    return HashDigest

#No_of_Oscillations = np.random.randint(low=100, high=1000, size=16)
No_of_Oscillations =[782, 421, 637, 261, 926, 379, 723, 847, 373, 882, 999, 930, 383, 791, 131, 711]
type(No_of_Oscillations);
print("the type of oscillations ",type(No_of_Oscillations))


print("PUF with Ring Oscillators \n",No_of_Oscillations)
perm = permutations(No_of_Oscillations,2)     # permutations of the pairs selecting two at a time and considering the order.
my_list = list(perm)
my_array = np.array(my_list)
print("Combinations of pairs \n",my_array)
print("Dimension of the permutations considering the order \n",my_array.shape)

dataStream=np.zeros(len(my_array))
dataStream = dataStream.astype(int)

for i in range(0, len(my_array)):
    if my_array[i, 0] > my_array[i, 1]:
        dataStream[i]=1
    else:
        dataStream[i]=0

print("The data stream at Server end \n\n", (dataStream).tolist())

user_id=int(input("Enter the USERID :  \n"))
password=int(input("Enter the PASSWORD : \n"))

xor_pass_rn= user_id ^ password
print("The XOR output of USERID and PASSWORD : \n",xor_pass_rn)
md_userPass=hash(xor_pass_rn)
print("The MESSAGE DIGEST of hash(USERID XOR PASSWORD) used to fetch location to store CHALLENGE RESPONSE in the DATABASE : \n",md_userPass)
addr_locator=md_userPass[0:2]

print("ROW and COLOUMN location to store CHALLENGE RESPONSE(OF PUF) into the DATABASE : \n",addr_locator)

md_hash_pass=hash(password)
bit_selector= int(md_hash_pass[0:2],16)
PUF_bit_selector= md_hash_pass[0:2]
print("Hash of the Password is used to generate the challenge responses of the PUF : \n",md_hash_pass)
print("First two values of Message Digest (Hash of the Password)  : \n",PUF_bit_selector)

limit=bit_selector%128
print("Starting index of a bit in the datastream : \n",limit)
print("Ending index of a bit in the datastream : \n",limit+128)

Puff_password=np.zeros(128)
Puff_password = Puff_password.astype(int)
Puff_password=dataStream[limit: limit+128]

print("The PUF CHALLENGE RESPONSE generated using Hash of the password : \n",Puff_password.tolist())

s = Puff_password.tolist()
out_arr = ' '.join([str(elem) for elem in s])

import mysql.connector
import mysql
mydb = mysql.connector.connect(host="localhost",user="root",passwd="11AAaa@@",database="NAU_sk2292")
mycursor = mydb.cursor()

z=(addr_locator.upper())
L= z[0];
M = z[1];

if enroll_auth_id == '1':
    print("Enrollment")
    if L in ["0", "1","2","3","4","5","6","7","8","9"]:
         cant = "C";
         L=cant+L;
         mycursor.execute("UPDATE pass_manager SET "+L+"=\""+out_arr+"\" WHERE XY = \""+M+"\"")
         print("\nCREDENTIALS ENTERED ARE SAVED INTO DB ----> ENROLLED  \n\n")
         mydb.commit()
    else:
           mycursor.execute("UPDATE pass_manager SET "+L+"=\""+out_arr+"\" WHERE XY = \""+M+"\"")
           print("\nCREDENTIALS ENTERED ARE SAVED INTO DB ----> ENROLLED  \n\n")
           mydb.commit()

if enroll_auth_id == '2':
    print("AUTHENTICATING.......")
    if L in ["0", "1","2","3","4","5","6","7","8","9"]:
         cant = "C";
         L=cant+L;
         mycursor.execute("SELECT "+L+" FROM pass_manager WHERE XY = \""+M+"\"")
         myresult = mycursor.fetchone()

         def convertTuple(tup):
             str = ''.join(tup)
             return str
         str = convertTuple(myresult)
         #print("The value of tuple", type(str))
         if(str == out_arr):
             print("\nCREDENTIALS ENTERED ARE PRESENT IN DB ----> AUTHENTICATION SUCCESS \n\n")
         else:
             print("\nCREDENTIALS ENTERED ARE NOT PRESENT IN DB ----> AUTHENTICATION FAILED \n\n")
    else:
        mycursor.execute("SELECT " + L + " FROM pass_manager WHERE XY = \"" + M + "\"")
        myresult = mycursor.fetchone()
        print(myresult)
        def convertTuple(tup):
            str = ''.join(tup)
            return str

        str = convertTuple(myresult)
        #print("The value of tuple", type(str))
        if (str == out_arr):
            print("\nYOUR CREDENTIALS ARE PRESENT AND AUTHENTICATED\n\n")
        else:
            print("\nCREDENTIALS ENTERED ARE NOT PRESENT IN DB ----> AUTHENTICATION FAILED \n\n")

#mycursor.execute("select * from pass_manager ")
#result = mycursor.fetchall()
#for i in result:
  #  print(i)
mycursor.close()





