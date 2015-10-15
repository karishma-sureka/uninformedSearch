import sys
import Queue

def read_input_data(textFile):
	cityPipesMap = dict()
	task = textFile.readline().strip()
	source = textFile.readline().strip()
	destinations = set(textFile.readline().split())
	middleNodes = textFile.readline().split()

	allnodes = list()

	cityPipesMap[source] = list()
	allnodes.append(source)

	for i in destinations:
		cityPipesMap[i] = list()
		allnodes.append(i)
	for i in middleNodes:
		cityPipesMap[i] = list()
		allnodes.append(i)

	pipes = int(textFile.readline())
	for pipe in range(pipes):
		cityPipesMap = build_graph_info(textFile.readline(), cityPipesMap)
	startTime = int(textFile.readline())
	return (task, source, destinations, startTime, cityPipesMap, allnodes)

class CityPipe:
	
	def setPeriod(self, startPeriod, endPeriod):
		for time in range(startPeriod, endPeriod + 1):
			self.timeList.add(time)
	
	def __init__(self, start, end, length, periods):
		self.start = start
		self.end = end
		self.length = length
		self.timeList = set()
		for period in periods:
			timeRanges = period.split()
			for timeRange in timeRanges:
				self.setPeriod(int(timeRange.split('-')[0]), int(timeRange.split('-')[1]))
	
	def getStart(self):
		return self.start
	
	def getEnd(self):
		return self.end
	
	def getLength(self):
		return self.length

	def getTimeList(self):
		return self.timeList

	def __repr__(self):
		return "start:" + self.start + " end:" + self.end + " length:" + str(self.length) + " timeList:" + str(self.timeList)

def build_graph_info(graphData, cityPipesMap):
	pipeInfo = graphData.split()
	cityPipe = CityPipe(pipeInfo[0], pipeInfo[1], int(pipeInfo[2]), pipeInfo[4:])
	start = cityPipe.getStart()
	cityPipesMap[start].append(cityPipe)
	return cityPipesMap

def uninformed_search(task, source, destinations, startTime, cityPipesMap, allnodes):	
	if(task == "BFS"):
		destination, time = BFS(source, destinations, startTime, cityPipesMap)
	elif(task == "DFS"):
		destination, time = DFS(source, destinations, startTime, cityPipesMap)
	else: 
		destination, time = UCS(source, destinations, startTime, cityPipesMap, allnodes)
	return(destination, time)

def BFS(source, destinations, startTime, cityPipesMap):
	if cityPipesMap[source]:
		start = cityPipesMap[source][0].getStart()
	else:
		return (-1, -1)
	expandedNode = list()
	q = Queue.Queue()
	cost = 0
	q.put((start, cost))
	destination = None

	while not q.empty():
		endList = []
		startNode = q.get()
		if(startNode[0] not in expandedNode):
			expandedNode.append(startNode[0])
			cost = startNode[1]
			if(startNode[0] in destinations):
				destination = startNode[0]
				break
			if cityPipesMap[startNode[0]]:
				for pipe in cityPipesMap[startNode[0]]:
					endList.append((pipe.getEnd(), cost + 1))
				q = insertListAlphabeticallyInQueue(q, endList)	
	if(destination):
		return (destination, (cost + startTime)%24)
	else:
		return (-1, -1)

def insertListAlphabeticallyInQueue(queue, destinationList):
	destinationList.sort()
	for destination in destinationList:
		queue.put(destination)
	return queue

def DFS(source, destinations, startTime, cityPipesMap):
	nodeLevelMap = {}
	expandedNode = list()
	if cityPipesMap[source]:
		start = cityPipesMap[source][0].getStart()
	else:
		return (-1, -1)
	nodeLevelMap[start] = 0
	stack = list()
	stack.append(start)
	cost = 0
	destination = None

	while not stack == []:
		endList = []
		start = stack.pop()
		if(start not in expandedNode):
			expandedNode.append(start)
			if(start in destinations):
				destination = start
				break
			if cityPipesMap[startNode[0]]:
				for pipe in cityPipesMap[start]:
					endList.append(pipe.getEnd())
					nodeLevelMap[pipe.getEnd()] = nodeLevelMap[start] + 1
				stack = insertListReverseAlphabeticallyInStack(stack, endList)
	if(destination):
		return (destination, (nodeLevelMap[destination] + startTime)%24)
	else:
		return(-1, -1)

def insertListReverseAlphabeticallyInStack(destinationStack, subList):
	return destinationStack + sorted(subList, reverse = True)

def isAcceptablePipe(start, time, cityPipesMap):
	for cityPipe in cityPipesMap[start[2]]:
		if(cityPipe.getEnd() == start[1]): #pipe from parent to this node
			if(time in cityPipe.getTimeList()):
				return False
	return True

def insertTupleIntoPriorityQueue(q, endList):
	for end in endList:
		q.put(end)
	return q

def setTime(time):
	return (time)

def setParent(node, source):
	if(node == source): #source has no parent
		return None
	else:
		return node

def isSource(start, source):
	if(start[1] == source):
		return True
	else:
		return False

def updateNodeCostInList(cost, node, parent, priorityQueue):
	newPriorityQueue = Queue.PriorityQueue()
	while not priorityQueue.empty():
		state = priorityQueue.get()
		if(state[1] == node):
			newPriorityQueue.put((cost, state[1], state[2]))
		else:
			newPriorityQueue.put(state)
	return newPriorityQueue

def UCS(source, destinations, startTime, cityPipesMap, allnodes):
	priorityQueue = Queue.PriorityQueue() 
	nodeTracker = dict()
	for node in allnodes:
		nodeTracker[node] = -2 #-2 => Not visited
	if cityPipesMap[source]:
		startNode = cityPipesMap[source][0].getStart()
	else:
		return (-1, -1)
	time = startTime
	priorityQueue.put((startTime, startNode, None))
	nodeTracker[startNode] = startTime
	destination = None
	
	while priorityQueue.qsize():
		endList = []
		currentNode = priorityQueue.get()
		nodeTracker[currentNode[1]] = -1 #to denote that the node has been visited
		time = currentNode[0]
		if(currentNode[1] in destinations):
			destination = currentNode[1]
			break
		if cityPipesMap[currentNode[1]]:
			for pipe in cityPipesMap[currentNode[1]]: #adding all the points that connect(can be reached) from the current node
				#check if the point already exists, update if shorter
				cost = pipe.getLength()+currentNode[0] 
				newNode = (cost, pipe.getEnd(), currentNode[1])
				if( nodeTracker[pipe.getEnd()] !=- 2 ): #visited or has a cost which can get updated
					if(nodeTracker[pipe.getEnd()] != -1 and isAcceptablePipe(newNode, (currentNode[0])%24, cityPipesMap)): #visited node, not to be added to the queue
						if(nodeTracker[pipe.getEnd()] > cost): #value needs to be updated
							nodeTracker[pipe.getEnd()] = cost
							priorityQueue = updateNodeCostInList(cost, pipe.getEnd(), currentNode[1], priorityQueue)
				else:
					if(isAcceptablePipe(newNode, (currentNode[0])%24, cityPipesMap)):
						nodeTracker[pipe.getEnd()] = cost
						priorityQueue.put(newNode)
	if(destination):
		return (destination, time%24)
	else:
		return (-1, -1)

def citySearch():
	textFile = open(sys.argv[2], "r")
	testCases = int(textFile.readline())
	outputFile = open("output_new.txt", "w")
	for i in range(testCases):
		task, source, destinations, startTime, cityPipesMap, allnodes = read_input_data(textFile)
		if not cityPipesMap:
			outputFile.write("None" + '\n')
		else:
			try: 
				destination, time = uninformed_search(task, source, destinations, startTime, cityPipesMap, allnodes)
			except:
				destination, time = (-1, -1)
			if(destination != -1):
				outputFile.write(str(destination) + ' ' + str(time) + '\n')
			else:
				outputFile.write("None" + '\n')
		textFile.readline()
	textFile.close()
	outputFile.close()

citySearch()
