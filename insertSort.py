# -*- coding: utf-8 -*-
# Сортировка простыми вставками

from io import open
import time

def input_method():
	"""Метод для считывания массива из файла""" 
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
	"""Метод выполняет сортировка простыми вставками"""
	count  = 0
	for i in range(1, len(arr)):
		j = i - 1
		value = int(arr.pop(i))
		count += 11
		while (j >= 0) and (int(arr[j]) > value):
			j -= 1
			count += 5
		arr.insert(j + 1, value)
		count += 5
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
	
