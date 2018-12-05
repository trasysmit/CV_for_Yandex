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

		
def mergeSort(arr, left, right):
	"""Метод для сортировки слияниями"""
	if right - left >= 1:#если есть более 1 элемента
		split = int((left + right)/2)# индекс, по которому делим массив
		mergeSort(arr, left, split)#сортируем левую половину 
		mergeSort(arr, split+1, right)#сортируем правую половину
		return merge(arr, left, split, right)#сливаем результаты в общий массив
		
	

		
def merge(arr, left, split, right):
	"""Метод для сливания 2х массивов в один"""
	
	#Слияние упорядоченных частей массива в буфер temp
	#с дальнейшим переносом содержимого temp в arr[left]...arr[right]

	#текущая позиция чтения из первой последовательности arr[left]...arr[split]
	pos1=left
	 
	#текущая позиция чтения из второй последовательности arr[split+1]...arr[right]
	pos2=split+1
	 
	#текущая позиция записи в temp
	pos3=0
	
	count = 7
	
	#Объявляем список temp
	temp = [i for i in range(right-left+1)]
	
	count += len(range(right-left+1)) * 4
	 
	#идет слияние, пока есть хоть один элемент в каждой последовательности
	while pos1 <= split and pos2 <= right:
		count += 2
		if arr[pos1] < arr[pos2]:
			temp[pos3] = arr[pos1]
			pos1+=1
			pos3+=1
			count += 8
			
		else:
			temp[pos3] = arr[pos2]
			pos2+=1
			pos3+=1
			count += 5
	 
	#одна последовательность закончилась - 
	#копировать остаток другой в конец буфера 
	while pos2 <= right:   #пока вторая последовательность непуста 
		temp[pos3] = arr[pos2]
		pos3+=1
		pos2+=1
		count += 6
		
	while pos1 <= split:  #пока первая последовательность непуста
		temp[pos3] = arr[pos1]
		pos3+=1
		pos1+=1
		count += 6
		
	#скопировать буфер temp в arr[left]...arr[right]
	arr[left:right+1] = temp
	count += 3 * (right + 1 - left)
	
	print(count)
	
	return arr

	
def main():
	arr = input_method()
	start = time.time()
	
	arr = mergeSort(arr, 0, len(arr) - 1)
	
	finish = time.time() - start

	print(finish)
	input()
	
main()
	