# -*- coding: utf-8 -*-
# Сортировка пузырьком с условием Айверсона 2

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
	"""Метод, выполняющий сортировку пузырьком с условием Айверсона 2"""
	t= len(arr) - 1
	count = 4
	
	#Сортировка пузырьком с условием Айверсона 2
	while t > 0:
		bound = t
		t = 0
		count += 4
		for j in range(bound):
			count +=3
			if int(arr[j]) > int(arr[j+1]):
				arr[j], arr[j+1] = arr[j+1], arr[j]
				t = j
				count += 13
			
	print(count)
	return arr

	
def main():
	arr = input_method()
	start = time.time()
	
	arr = bubbleSort(arr)
	
	finish = time.time() - start

	print(finish)
	input()
	
main()
	
