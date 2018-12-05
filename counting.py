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
	"""Метод, выполняющий сортировку подсчетом"""
	
	b = [0] * 10001
	count = 20002
	for i in arr:
		b[int(i)] += 1
		count += 3
	
	m = 0
	count += 1
	
	for i in range(len(b)):
		count += 4
		while b[i] > 0:
			arr[m] = i
			m+=1
			b[i] -= 1
			count += 9
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
	
