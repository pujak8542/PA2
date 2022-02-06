#!/usr/bin/env python
# coding: utf-8

# In[26]:


import matplotlib.pyplot as plt
import jellyfish
import itertools
import collections
import seaborn as sns
#Hexadecimal to Binary Conversion
def hex2bin(s):
    mp = {'0' : "0000",
          '1' : "0001",
          '2' : "0010",
          '3' : "0011",
          '4' : "0100",
          '5' : "0101",
          '6' : "0110",
          '7' : "0111",
          '8' : "1000",
          '9' : "1001",
          'A' : "1010",
          'B' : "1011",
          'C' : "1100",
          'D' : "1101",
          'E' : "1110",
          'F' : "1111" }
    bin = ""
    for i in range(len(s)):
        bin = bin + mp[s[i]]
    return bin
     
# Binary to hexadecimal conversion
def bin2hex(s):
    mp = {"0000" : '0',
          "0001" : '1',
          "0010" : '2',
          "0011" : '3',
          "0100" : '4',
          "0101" : '5',
          "0110" : '6',
          "0111" : '7',
          "1000" : '8',
          "1001" : '9',
          "1010" : 'A',
          "1011" : 'B',
          "1100" : 'C',
          "1101" : 'D',
          "1110" : 'E',
          "1111" : 'F' }
    hex = ""
    for i in range(0,len(s),4):
        ch = ""
        ch = ch + s[i]
        ch = ch + s[i + 1]
        ch = ch + s[i + 2]
        ch = ch + s[i + 3]
        hex = hex + mp[ch]
         
    return hex
# Binary to decimal conversion
def bin2dec(binary):
	
	binary1 = binary
	decimal, i, n = 0, 0, 0
	while(binary != 0):
		dec = binary % 10
		decimal = decimal + dec * pow(2, i)
		binary = binary//10
		i += 1
	return decimal

# Decimal to binary conversion
def dec2bin(num):
	res = bin(num).replace("0b", "")
	if(len(res)%4 != 0):
		div = len(res) / 4
		div = int(div)
		counter =(4 * (div + 1)) - len(res)
		for i in range(0, counter):
			res = '0' + res
	return res

# Permute function to rearrange the bits
def permute(k, arr, n):
	permutation = ""
	for i in range(0, n):
		permutation = permutation + k[arr[i] - 1]
	return permutation

# shifting the bits towards left by nth shifts
def shift_left(k, nth_shifts):
	s = ""
	for i in range(nth_shifts):
		for j in range(1,len(k)):
			s = s + k[j]
		s = s + k[0]
		k = s
		s = ""
	return k

# calculating xow of two strings of binary number a and b
def xor(a, b):
	ans = ""
	for i in range(len(a)):
		if a[i] == b[i]:
			ans = ans + "0"
		else:
			ans = ans + "1"
	return ans

# Table of Position of 64 bits at initial level: Initial Permutation Table
initial_perm = [58, 50, 42, 34, 26, 18, 10, 2,
				60, 52, 44, 36, 28, 20, 12, 4,
				62, 54, 46, 38, 30, 22, 14, 6,
				64, 56, 48, 40, 32, 24, 16, 8,
				57, 49, 41, 33, 25, 17, 9, 1,
				59, 51, 43, 35, 27, 19, 11, 3,
				61, 53, 45, 37, 29, 21, 13, 5,
				63, 55, 47, 39, 31, 23, 15, 7]

# Expansion D-box Table
exp_d = [32, 1 , 2 , 3 , 4 , 5 , 4 , 5,
		6 , 7 , 8 , 9 , 8 , 9 , 10, 11,
		12, 13, 12, 13, 14, 15, 16, 17,
		16, 17, 18, 19, 20, 21, 20, 21,
		22, 23, 24, 25, 24, 25, 26, 27,
		28, 29, 28, 29, 30, 31, 32, 1 ]

# Straight Permutation Table
per = [ 16, 7, 20, 21,
		29, 12, 28, 17,
		1, 15, 23, 26,
		5, 18, 31, 10,
		2, 8, 24, 14,
		32, 27, 3, 9,
		19, 13, 30, 6,
		22, 11, 4, 25 ]

# S-box Table
sbox = [[[14, 4, 13, 1, 2, 15, 11, 8, 3, 10, 6, 12, 5, 9, 0, 7],
		[ 0, 15, 7, 4, 14, 2, 13, 1, 10, 6, 12, 11, 9, 5, 3, 8],
		[ 4, 1, 14, 8, 13, 6, 2, 11, 15, 12, 9, 7, 3, 10, 5, 0],
		[15, 12, 8, 2, 4, 9, 1, 7, 5, 11, 3, 14, 10, 0, 6, 13 ]],
			
		[[15, 1, 8, 14, 6, 11, 3, 4, 9, 7, 2, 13, 12, 0, 5, 10],
			[3, 13, 4, 7, 15, 2, 8, 14, 12, 0, 1, 10, 6, 9, 11, 5],
			[0, 14, 7, 11, 10, 4, 13, 1, 5, 8, 12, 6, 9, 3, 2, 15],
		[13, 8, 10, 1, 3, 15, 4, 2, 11, 6, 7, 12, 0, 5, 14, 9 ]],

		[ [10, 0, 9, 14, 6, 3, 15, 5, 1, 13, 12, 7, 11, 4, 2, 8],
		[13, 7, 0, 9, 3, 4, 6, 10, 2, 8, 5, 14, 12, 11, 15, 1],
		[13, 6, 4, 9, 8, 15, 3, 0, 11, 1, 2, 12, 5, 10, 14, 7],
			[1, 10, 13, 0, 6, 9, 8, 7, 4, 15, 14, 3, 11, 5, 2, 12 ]],
	
		[ [7, 13, 14, 3, 0, 6, 9, 10, 1, 2, 8, 5, 11, 12, 4, 15],
		[13, 8, 11, 5, 6, 15, 0, 3, 4, 7, 2, 12, 1, 10, 14, 9],
		[10, 6, 9, 0, 12, 11, 7, 13, 15, 1, 3, 14, 5, 2, 8, 4],
			[3, 15, 0, 6, 10, 1, 13, 8, 9, 4, 5, 11, 12, 7, 2, 14] ],
		
		[ [2, 12, 4, 1, 7, 10, 11, 6, 8, 5, 3, 15, 13, 0, 14, 9],
		[14, 11, 2, 12, 4, 7, 13, 1, 5, 0, 15, 10, 3, 9, 8, 6],
			[4, 2, 1, 11, 10, 13, 7, 8, 15, 9, 12, 5, 6, 3, 0, 14],
		[11, 8, 12, 7, 1, 14, 2, 13, 6, 15, 0, 9, 10, 4, 5, 3 ]],
	
		[ [12, 1, 10, 15, 9, 2, 6, 8, 0, 13, 3, 4, 14, 7, 5, 11],
		[10, 15, 4, 2, 7, 12, 9, 5, 6, 1, 13, 14, 0, 11, 3, 8],
			[9, 14, 15, 5, 2, 8, 12, 3, 7, 0, 4, 10, 1, 13, 11, 6],
			[4, 3, 2, 12, 9, 5, 15, 10, 11, 14, 1, 7, 6, 0, 8, 13] ],
		
		[ [4, 11, 2, 14, 15, 0, 8, 13, 3, 12, 9, 7, 5, 10, 6, 1],
		[13, 0, 11, 7, 4, 9, 1, 10, 14, 3, 5, 12, 2, 15, 8, 6],
			[1, 4, 11, 13, 12, 3, 7, 14, 10, 15, 6, 8, 0, 5, 9, 2],
			[6, 11, 13, 8, 1, 4, 10, 7, 9, 5, 0, 15, 14, 2, 3, 12] ],
		
		[ [13, 2, 8, 4, 6, 15, 11, 1, 10, 9, 3, 14, 5, 0, 12, 7],
			[1, 15, 13, 8, 10, 3, 7, 4, 12, 5, 6, 11, 0, 14, 9, 2],
			[7, 11, 4, 1, 9, 12, 14, 2, 0, 6, 10, 13, 15, 3, 5, 8],
			[2, 1, 14, 7, 4, 10, 8, 13, 15, 12, 9, 0, 3, 5, 6, 11] ] ]

# Final Permutation Table
final_perm = [ 40, 8, 48, 16, 56, 24, 64, 32,
			39, 7, 47, 15, 55, 23, 63, 31,
			38, 6, 46, 14, 54, 22, 62, 30,
			37, 5, 45, 13, 53, 21, 61, 29,
			36, 4, 44, 12, 52, 20, 60, 28,
			35, 3, 43, 11, 51, 19, 59, 27,
			34, 2, 42, 10, 50, 18, 58, 26,
			33, 1, 41, 9, 49, 17, 57, 25 ]

def encrypt(pt, rkb, rk):
	
	# Initial Permutation
    plain=[]
    pt = permute(pt, initial_perm, 64)
    #print("After initial permutation", pt)
    old,cur=pt,""
    
	# Splitting
    left = pt[0:32]
    right = pt[32:64]
    for i in range(0, 16):
		# Expansion D-box: Expanding the 32 bits data into 48 bits
        right_expanded = permute(right, exp_d, 48)
		
		# XOR RoundKey[i] and right_expanded
        xor_x = xor(right_expanded, rkb[i])

		# S-boxex: substituting the value from s-box table by calculating row and column
        sbox_str = ""
        for j in range(0, 8):
            row = bin2dec(int(xor_x[j * 6] + xor_x[j * 6 + 5]))
            col = bin2dec(int(xor_x[j * 6 + 1] + xor_x[j * 6 + 2] + xor_x[j * 6 + 3] + xor_x[j * 6 + 4]))
            val = sbox[j][row][col]
            sbox_str = sbox_str + dec2bin(val)
			
		# Straight D-box: After substituting rearranging the bits
        sbox_str = permute(sbox_str, per, 32)
		
		# XOR left and sbox_str
        result = xor(left, sbox_str)
        left = result
		
		# Swapper
        if(i != 15):
            left, right = right, left
            x=str(left)
            y=str(right)
            x+=y
           
            cur=x
            
        
       # print("Round ", i + 1, " ", left, " ", right)
        plain.append(cur)
        ct=0
        
        
        le=0
        while le<64:
            if cur[le]!=old[le]:
                ct+=1
            le+=1
        
        ct=0
        
	
	# Combination
    combine = left + right
	
	# Final permutation: final rearranging of bits to get cipher text
    cipher_text = permute(combine, final_perm, 64)
    return cipher_text,plain
#For 5 different plain texts their 5 different perturbed texts with hamming distance of 1 between them
pl_text1="1100000010110111101010001101000001011111001110101000001010011100"
ch_text1="1100001010110111101010001101000001011111001110101000001010011100"
pl_text2="0000000010110111101010001001000001011111001110101000001010011100"
ch_text2="0000000010110101101010001001000001011111001110101000001010011100"
pl_text3="1100000010110111101010001101000001010001001110101010001011111100"
ch_text3="1100001010110111101010001101000001010001001110101010001011111100"
pl_text4="1100000010110111101010001101000001000000001110101000001010010011"
ch_text4="1100000010110111101010001101000001001000001110101000001010010011"
pl_text5="1111000010110111101010001101001001011111001110101000001010011111"
ch_text5="0111000010110111101010001101001001011111001110101000001010011111"
#Plain texts with different hamming distances between them(i.e hamming distance =1,2,3,4,5)
pt = "1100000010110111101010001101000001011111001110101000001010011100"
pt2="1100100010110111101010001101000001011111001110101000001010011100"
pt3="1100001000110111101010001101000001011111001110101000001010011100"
pt4="1100000010100111101010001101000011011111001110101000011010011100"
pt5="1101000010110111101011001101010001011111001110101001001010011100"
pt6="1100000010110111101011111101000101011101001110101000001010011100"
#5 different secret keys
key = "1010101010111011000010010001100000100111001101101100110011011101"
key2="1010101010111011000010010001101000100111001101101100110011011101"
key3="1010101010111010100010010001100000100111001101101100110011011101"
key4="1010101010111011000010010001101100100110001101101100110011011101"
key5="1010101010111011001110010001100000100001001101101100110011011101"
# --parity bit drop table
keyp = [57, 49, 41, 33, 25, 17, 9,
		1, 58, 50, 42, 34, 26, 18,
		10, 2, 59, 51, 43, 35, 27,
		19, 11, 3, 60, 52, 44, 36,
		63, 55, 47, 39, 31, 23, 15,
		7, 62, 54, 46, 38, 30, 22,
		14, 6, 61, 53, 45, 37, 29,
		21, 13, 5, 28, 20, 12, 4 ]

# getting 56 bit key from 64 bit using the parity bits
key = permute(key, keyp, 56)
key2=permute(key2,keyp,56)
key3=permute(key3,keyp,56)
key4=permute(key4,keyp,56)
key5=permute(key5,keyp,56)

# Number of bit shifts
shift_table = [1, 1, 2, 2,
				2, 2, 2, 2,
				1, 2, 2, 2,
				2, 2, 2, 1 ]

# Key- Compression Table : Compression of key from 56 bits to 48 bits
key_comp = [14, 17, 11, 24, 1, 5,
			3, 28, 15, 6, 21, 10,
			23, 19, 12, 4, 26, 8,
			16, 7, 27, 20, 13, 2,
			41, 52, 31, 37, 47, 55,
			30, 40, 51, 45, 33, 48,
			44, 49, 39, 56, 34, 53,
			46, 42, 50, 36, 29, 32 ]

# Splitting
left = key[0:28] # rkb for RoundKeys in binary
right = key[28:56] # rk for RoundKeys in hexadecimal

rkb = []
rk = []
for i in range(0, 16):
	# Shifting the bits by nth shifts by checking from shift table
	left = shift_left(left, shift_table[i])
	right = shift_left(right, shift_table[i])
	
	# Combination of left and right string
	combine_str = left + right
	
	# Compression of key from 56 to 48 bits
	round_key = permute(combine_str, key_comp, 48)

	rkb.append(round_key)
	rk.append(round_key)
p1,p2,p3,p4,p5=[],[],[],[],[]
c1,c2,c3,c4,c5=[],[],[],[],[]
ct1,p1 = encrypt(pl_text1, rkb, rk)
ct2,p2 = encrypt(pl_text2, rkb, rk)
ct3,p3 = encrypt(pl_text3, rkb, rk)
ct4,p4 = encrypt(pl_text4, rkb, rk)
ct5,p5 = encrypt(pl_text5, rkb, rk)
ct6,c1 = encrypt(ch_text1, rkb, rk)
ct7,c2 = encrypt(ch_text2, rkb, rk)
ct8,c3 = encrypt(ch_text3, rkb, rk)
ct9,c4 = encrypt(ch_text4, rkb, rk)
ct10,c5 = encrypt(ch_text5, rkb, rk)
H_D1,H_D2,H_D3,H_D4,H_D5=[],[],[],[],[]
#Storing the hamming distance of 16 rounds of cipher texts in 5 lists. Each list contains the hamming distance between two cipher texts for each of the 16 rounds
for i in range (0,16):
    H_D1.append(jellyfish.damerau_levenshtein_distance(p1[i], c1[i]))
    H_D2.append(jellyfish.damerau_levenshtein_distance(p2[i], c2[i]))
    H_D3.append(jellyfish.damerau_levenshtein_distance(p3[i], c3[i]))
    H_D4.append(jellyfish.damerau_levenshtein_distance(p4[i], c4[i]))
    H_D5.append(jellyfish.damerau_levenshtein_distance(p5[i], c5[i]))
print("1)Taking Five plaintexts and for each plain text there is a pertubed text with a hamming distance of 1 between them:")
print("")
print("For plain text:",bin2hex(pl_text1)," and perturbed text :",bin2hex(ch_text1))    
print("Hamming Distance between cipher text for round 1 to 16: ",H_D1)
print("")
print("For plain text:",bin2hex(pl_text2)," and perturbed text :",bin2hex(ch_text2))
print("Hamming Distance between cipher text for round 1 to 16: ",H_D2)
print("")
print("For plain text:",bin2hex(pl_text3)," and perturbed text :",bin2hex(ch_text3))
print("Hamming Distance between cipher text for round 1 to 16: ",H_D3)
print("")
print("For plain text:",bin2hex(pl_text4)," and perturbed text :",bin2hex(ch_text4))
print("Hamming Distance between cipher text for round 1 to 16: ",H_D4)  
print("")
print("For plain text:",bin2hex(pl_text5)," and perturbed text :",bin2hex(ch_text5))
print("Hamming Distance between cipher text for round 1 to 16: ",H_D5)    
round1, round2, round3, round4,round5,round6,round7,round8,round9,round10,round11,round12,round13,round14,round15,round16 = ([], ) * 16
mul_list_dict3 = collections.defaultdict(list)
#Seperating the hamming distance of cipher texts for different rounds with each round having 5 hamming distances corresponding to 5 cipher texts
for i in range(0,16):
    mul_list_dict3['round'+str((i+1))].append(H_D1[i])
    mul_list_dict3['round'+str((i+1))].append(H_D2[i])
    mul_list_dict3['round'+str((i+1))].append(H_D3[i])
    mul_list_dict3['round'+str((i+1))].append(H_D4[i])
    mul_list_dict3['round'+str((i+1))].append(H_D5[i]) 
data=[mul_list_dict3['round1'],mul_list_dict3['round2'],mul_list_dict3['round3'],mul_list_dict3['round4'],mul_list_dict3['round5'],mul_list_dict3['round6'],mul_list_dict3['round7'],mul_list_dict3['round8'],mul_list_dict3['round9'],mul_list_dict3['round10'],mul_list_dict3['round11'],mul_list_dict3['round12'],mul_list_dict3['round13'],mul_list_dict3['round14'],mul_list_dict3['round15'],mul_list_dict3['round16']]
fig = plt.figure(figsize =(10, 7))
 
# Creating axes instance
ax = fig.add_axes([1, 0.5, 1, 0.5])
ax.set_title("Using Five different plaintexts")
ax.set_xlabel("Rounds")
ax.set_ylabel("Hamming Distance of cipher texts")
# Creating plot
bp = ax.boxplot(data)
 
# show plot
plt.show()   
#Encrypting of plaintext
plaint_text1=[]
plaint_text2=[]
plaint_text3=[]
plaint_text4=[]
plaint_text5=[]
plaint_text6=[]
print("2)Taking 5 different hamming distances")
print("")
cipher_text,plaint_text1 = encrypt(pt, rkb, rk)
#print("Cipher Text : ",cipher_text)
cipher_text2,plaint_text2 = encrypt(pt2, rkb, rk)
#print("Cipher Text : ",cipher_text2)


cipher_text3,plaint_text3 = encrypt(pt3, rkb, rk)
#print("Cipher Text : ",cipher_text3)
cipher_text4,plaint_text4 = encrypt(pt4, rkb, rk)
#print("Cipher Text : ",cipher_text4)

cipher_text5,plaint_text5 = encrypt(pt5, rkb, rk)
cipher_text6,plaint_text6 = encrypt(pt6, rkb, rk)
#print("Cipher Text : ",cipher_text5)
dist1=[]
dist2=[]
dist3=[]
dist4=[]
dist5=[]
#calculating the hamming distance of cipher texts for each round
for i in range (0,16):
   # print("p=:"+str(i+1))
    dist1.append(jellyfish.damerau_levenshtein_distance(plaint_text1[i], plaint_text2[i]))
    #print("dis="+str(dist))
    dist2.append(jellyfish.damerau_levenshtein_distance(plaint_text1[i], plaint_text3[i]))
    dist3.append(jellyfish.damerau_levenshtein_distance(plaint_text1[i], plaint_text4[i]))
    dist4.append(jellyfish.damerau_levenshtein_distance(plaint_text1[i], plaint_text5[i]))
    dist5.append(jellyfish.damerau_levenshtein_distance(plaint_text1[i], plaint_text6[i]))
round1, round2, round3, round4,round5,round6,round7,round8,round9,round10,round11,round12,round13,round14,round15,round16 = ([], ) * 16
mul_list_dict = collections.defaultdict(list)
for i in range(0,16):
    mul_list_dict['round'+str((i+1))].append(dist1[i])
    mul_list_dict['round'+str((i+1))].append(dist2[i])
    mul_list_dict['round'+str((i+1))].append(dist3[i])
    mul_list_dict['round'+str((i+1))].append(dist4[i])
    mul_list_dict['round'+str((i+1))].append(dist5[i])
    

print("Plain text: "+bin2hex(pt)," Perturbed text :",bin2hex(pt2)," Hamming Distance : 1")
print("Hamming Distance between cipher text for round 1 to 16: ",dist1)
print("")
print("Plain text: "+bin2hex(pt)," Perturbed text :",bin2hex(pt3)," Hamming Distance : 2")
print("Hamming Distance between cipher text for round 1 to 16: ",dist2)
print("")
print("Plain text: "+bin2hex(pt)," Perturbed text :",bin2hex(pt4)," Hamming Distance : 3")

print("Hamming Distance between cipher text for round 1 to 16: ",dist3)
print("")
print("Plain text: "+bin2hex(pt)," Perturbed text :",bin2hex(pt5)," Hamming Distance : 4")

print("Hamming Distance between cipher text for round 1 to 16: ",dist4)
print("")
print("Plain text: "+bin2hex(pt)," Perturbed text :",bin2hex(pt6)," Hamming Distance : 5")
print("Hamming Distance between cipher text for round 1 to 16: ",dist5)
print("")


left2 = key2[0:28] # rkb for RoundKeys in binary
right2 = key2[28:56] # rk for RoundKeys in hexadecimal

rkb2 = []
rk2 = []
for i in range(0, 16):
	# Shifting the bits by nth shifts by checking from shift table
	left2 = shift_left(left2, shift_table[i])
	right2 = shift_left(right2, shift_table[i])
	
	# Combination of left and right string
	combine_str = left2 + right2
	
	# Compression of key from 56 to 48 bits
	round_key = permute(combine_str, key_comp, 48)

	rkb2.append(round_key)
	rk2.append(round_key)
cipher_text6,plaint_text6 = encrypt(pt, rkb2, rk2)  
left3 = key3[0:28] # rkb for RoundKeys in binary
right3 = key3[28:56] # rk for RoundKeys in hexadecimal

rkb3 = []
rk3 = []
for i in range(0, 16):
	# Shifting the bits by nth shifts by checking from shift table
	left3 = shift_left(left3, shift_table[i])
	right3 = shift_left(right3, shift_table[i])
	
	# Combination of left and right string
	combine_str = left3 + right3
	
	# Compression of key from 56 to 48 bits
	round_key = permute(combine_str, key_comp, 48)

	rkb3.append(round_key)
	rk3.append(round_key)
cipher_text7,plaint_text7 = encrypt(pt, rkb3, rk3)
left4= key4[0:28] # rkb for RoundKeys in binary
right4 = key4[28:56] # rk for RoundKeys in hexadecimal

rkb4 = []
rk4 = []
for i in range(0, 16):
	# Shifting the bits by nth shifts by checking from shift table
	left4 = shift_left(left4, shift_table[i])
	right4 = shift_left(right4, shift_table[i])
	
	# Combination of left and right string
	combine_str = left4 + right4
	
	# Compression of key from 56 to 48 bits
	round_key = permute(combine_str, key_comp, 48)

	rkb4.append(round_key)
	rk4.append(round_key)
cipher_text8,plaint_text8 = encrypt(pt, rkb4, rk4)
left5 = key5[0:28] # rkb for RoundKeys in binary
right5 = key5[28:56] # rk for RoundKeys in hexadecimal

rkb5 = []
rk5= []
for i in range(0, 16):
	# Shifting the bits by nth shifts by checking from shift table
	left5= shift_left(left5, shift_table[i])
	right5 = shift_left(right5, shift_table[i])
	
	# Combination of left and right string
	combine_str = left5 + right5
	
	# Compression of key from 56 to 48 bits
	round_key = permute(combine_str, key_comp, 48)

	rkb5.append(round_key)
	rk5.append(round_key)
cipher_text9,plaint_text9 = encrypt(pt, rkb5, rk5)
dist5=[]
dist6=[]
dist7=[]
dist8=[]
#calculating the hamming distance of cipher texts for each round
for i in range (0,16):
    dist5.append(jellyfish.damerau_levenshtein_distance(plaint_text1[i], plaint_text6[i]))
    dist6.append(jellyfish.damerau_levenshtein_distance(plaint_text1[i], plaint_text7[i]))
    dist7.append(jellyfish.damerau_levenshtein_distance(plaint_text1[i], plaint_text8[i]))
    dist8.append(jellyfish.damerau_levenshtein_distance(plaint_text1[i], plaint_text9[i]))
data=[mul_list_dict['round1'],mul_list_dict['round2'],mul_list_dict['round3'],mul_list_dict['round4'],mul_list_dict['round5'],mul_list_dict['round6'],mul_list_dict['round7'],mul_list_dict['round8'],mul_list_dict['round9'],mul_list_dict['round10'],mul_list_dict['round11'],mul_list_dict['round12'],mul_list_dict['round13'],mul_list_dict['round14'],mul_list_dict['round15'],mul_list_dict['round16']]
fig = plt.figure(figsize =(10, 7))
 
# Creating axes instance
ax = fig.add_axes([1, 0.5, 1, 0.5])
ax.set_xlabel("Rounds")
ax.set_ylabel("Hamming Distance of cipher texts")
ax.set_title("Using Five Different Hamming distances")
# Creating plot
bp = ax.boxplot(data)
 
# show plot
plt.show()
print("3)Taking 5 different secret keys")
print("")
print("Fixed Plain text:",bin2hex(pt),"\n\nKey1: ",bin2hex(key))
print("Cipher Text:",bin2hex(cipher_text6))
print("")
print("Key2: ",bin2hex(key))
print("Cipher Text:",bin2hex(cipher_text6))
print("")
print("Hamming distance of cipher text for round 1 to 16 corresponding key1 and key2: ",dist5)
print("")
print("Key3: ",bin2hex(key))
print("Cipher Text:",bin2hex(cipher_text7))
print("")
print("Hamming distance of cipher text for round 1 to 16 corresponding key1 and key3: ",dist6)
print("")
print("Key4: ",bin2hex(key))
print("Cipher Text:",bin2hex(cipher_text8))
print("")
print("Hamming distance of cipher text for round 1 to 16 corresponding key1 and key4: ",dist7)
print("")
print("Key5: ",bin2hex(key))
print("Cipher Text:",bin2hex(cipher_text9))
print("")
print("Hamming distance of cipher text for round 1 to 16 corresponding key1 and key5: ",dist8)
print("")
round1, round2, round3, round4,round5,round6,round7,round8,round9,round10,round11,round12,round13,round14,round15,round16 = ([], ) * 16
mul_list_dict2 = collections.defaultdict(list)
for i in range(0,16):
    mul_list_dict2['round'+str((i+1))].append(dist5[i])
    mul_list_dict2['round'+str((i+1))].append(dist6[i])
    mul_list_dict2['round'+str((i+1))].append(dist7[i])
    mul_list_dict2['round'+str((i+1))].append(dist8[i])
    data=[mul_list_dict2['round1'],mul_list_dict2['round2'],mul_list_dict2['round3'],mul_list_dict2['round4'],mul_list_dict2['round5'],mul_list_dict2['round6'],mul_list_dict2['round7'],mul_list_dict2['round8'],mul_list_dict2['round9'],mul_list_dict2['round10'],mul_list_dict2['round11'],mul_list_dict2['round12'],mul_list_dict2['round13'],mul_list_dict2['round14'],mul_list_dict2['round15'],mul_list_dict2['round16']]
fig = plt.figure(figsize =(10, 7))
 
# Creating axes instance
ax = fig.add_axes([1, 0.5, 1, 0.5])
ax.set_title("Using 5 different Secret Keys")
ax.set_xlabel("Rounds")
ax.set_ylabel("Hamming Distance of cipher texts")
# Creating plot
bp = ax.boxplot(data)
 
# show plot
plt.show()
    


# In[ ]:




