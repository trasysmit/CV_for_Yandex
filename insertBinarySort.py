# -*- coding: utf-8 -*-

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
	count = 0
	for i in range(1, len(arr)):
		count += 4
		if (arr[i-1] > arr[i]):
			
			lf = 0
			rg = i - 1
			count += 7
			while (lf <= rg):
				c = int((lf + rg)/2)
				count += 4
				if (arr[c] < arr[i]):
					lf = c + 1
					count += 4
				else:
					rg = c - 1
					count += 4
		
			k = i
			p = arr[i]
			count += 3
			
			while k > lf:
				arr[k] = arr[k-1]
				k = k - 1
				count += 7
			arr[lf] = p
			count += 2
	print(count)
	return arr

	
def main():
	arr = input_method()
	start = time.time()
	
	arr = sort(arr)
	
	finish = time.time() - start

	print(finish)
	input()
	
main()
	