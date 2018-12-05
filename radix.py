# -*- coding: utf-8 -*-
# Поразрядная сортировка

from io import open
import time

def input_method():
	"""Метод для считывания массива из файла или его автоматичекой генерации""" 
	arr = []
	f = open('c:/input.txt', 'r', encoding='utf-8')
	
	arr = f.readlines()
	f.close()
	for x in arr:
		if ('\n' in x):
			j = arr.index(x)
			arr.remove(x)
			arr.insert(j, x[:x.find('\n')])

	return arr
	

	
def output_method(arr):
	"""Метод для вывода массива"""
	
	#Вывод отсортированного массива
	for x in arr:
		print(x)

		
def sort(arr):
	"""Метод, выполняющий поразрядную сортировку"""
	
	RADIX = 10000
	maxLength = False
	tmp , placement = -1, 1
	count = 4
	 
	while not maxLength:
		maxLength = True
		# declare and initialize buckets
		buckets = [list() for _ in range( RADIX )]
		count += 1 + 30000
	 
	# split arr between lists
	for  i in arr:
		tmp = int(i) / placement
		buckets[int(tmp % RADIX)].append( int(i) )
		count += 5
		if maxLength and tmp > 0:
			maxLength = False
			count += 4
	 
	# empty lists into arr array
	a = 0
	count += 1
	for b in range( RADIX ):
		buck = buckets[b]
		count += 30000 + 2
		for i in buck:
			arr[a] = int(i)
			a += 1
			count += 8
			
	 
	# move to next digit
	placement *= RADIX
	
	count += 2
	print(count)
	
	return arr

	
def main():
	arr = input_method()
	start = time.time()
	
	arr = sort(arr)
	
	finish = time.time() - start
	output_method(arr)
	print(finish)
	input()
	
main()
	
