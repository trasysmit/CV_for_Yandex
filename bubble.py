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

		
def bubbleSort(arr):
	"""Метод, выполняющий сортировку пузырьком"""
	
	i = len(arr)
	count = 3
	#Сортировка пузырьком
	while i > 0:
		count += 1
		for j in range(i - 1):
			count += 4
			if int(arr[j]) > int(arr[j+1]):
				count += 8
				arr[j], arr[j+1] = arr[j+1], arr[j]
		i -=1
		count += 1

	print('count = ' + str(count))
	return arr

	
def main():
	arr = input_method()
	start = time.time()
	
	arr = bubbleSort(arr)
	
	finish = time.time() - start

	print(finish)
	input()
	
main()
	