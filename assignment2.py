from collections import deque
"""
        ---------------------
    --- FIT 2004 ASSIGNMENT 2 --- 
        ---------------------

This file includes all the code for assignment 2. It contains code for question 1 and 2. 
It will be labeled as a comment to specify which part belongs to the specific
questions. 

"""
__author__ = "Yeoh Ming Wei"

class Graph: 
    """ A Graph class which contains number of vertices. """
    
    def __init__(self): 
        """
        A constructor to initialize a list of vertices and the amount(length) of vertices available. 
        
        Attributes
            - vertices: A list contains Vertex object
            - length: the length of the vertices list (The amount of vertex available)
        """
        self.vertices = []
        self.length = 0
        
    def __str__(self): 
            """ A toString method when Graph object is called. """
            string = ""
            for v in self.vertices: string += "{}\n".format(str(v))
            return string
    
    def getVertex(self, id): 
        """ 
        A function that that returns the specific Vertex.
        
        Input
            - id: The vertex number

        Output: The Vertex object based on num input. 

        Time complexity: O(1), where it returns a specific vertex.
        """
        return self.vertices[id]
    
    def addVertex(self, id, edge): 
        """ 
        A function to add Vertex object inside the vertices list along with the edges.
        
        Input
            - id: The vertex number
            - edge: The edge object of the vertex

        Time complexity: O(V), where V is the number of vertices
            - O(V), when the worst case is where the id given is equal to the number of vertices
        Space complexity: O(V + E), where V is the number of vertices and E is the number of edge
            - O(V + E), when we append x amount of v and add one edge. 
        """
        if self.length == 0: 
            # If the length is 0, multiply the vertices list based on the number"
            self.vertices = [None] * (id + 1)
            self.length += (id + 1) 

        if (id + 1) > self.length: 
            # If the number given is more than the length of the list, 
            # increase the list size and append None along.
            for i in range((id + 1) - self.length):
                self.vertices.append(None) 
                self.length += 1
        
        if self.vertices[id] == None: 
            # Create the Vertex object based on its id and add an edge
            self.vertices[id] = Vertex(id, edge)
        else: 
            # Add the edges if the vertex exist
            self.vertices[id].addEdge(edge)

    def addNetwork(self, tuple): 
        """
        An assignment related function.
        This function a data center and its connections into a single graph. It
        uses a tuple as representation. 
        a: ID of the data centre departs
        b: ID of the data centre arrives
        t: The capacity of the connection

        Input
            - tuple: A tuple represents the a, b, t

        Time complexity: O(|D|) where |D| is the number of data centre, it can be represent as vertex.
            - O(|D|) as we are calling the addVertex function.
        """
        a, b, t = tuple[0], tuple[1], tuple[2]
        self.addVertex(a, Edge(a, b, t))
        self.addVertex(b, Edge(a, b, t))

    def addTarget(self, targets): 
        """
        An assignment related function.
        This function update the targets attribute of the data centre. It will assign target as True
        if the data centre is the target destination. 

        Input 
            - targets: A list of integer represents the ID of data centre which is the target destination.
        
        Time complexity: O(|T|), where T is the length of target list
            - O(|T|) as we use for loop to loop through the target list
            - O(1) when we perform assignment.
        """
        for i in targets: self.vertices[i].target = True

    def addMax(self, maxIn, maxOut): 
        """
        A function to add the MaxIn and MaxOut of the data centre. Both have the same length and same
        number of data centre. 
        Time complexity: O(|D|) where |D| is the number of data centre.
            - The time complexity is O(D) because we loop through all the data centre to change
              the value.
            - The assignment is O(1).
        """
        for i in range(len(maxIn)): 
            self.vertices[i].incoming = maxIn[i]
            self.vertices[i].outgoing = maxOut[i]

    def resetDiscovered(self): 
        """
        A function to reset the discovered attribute for every data centre. This is needed when we
        reused the Breath First Search (BFS) function for path tracking. 

        Time complexity: O(|D|) where |D| is the length of the number of the data centre. 
        """
        for i in range(len(self.vertices)): self.vertices[i].discovered = False

    def bfs(self, v : int): 
        """
        A modified bfs function that allows to return a path when the origin can reach the target.
        1) The discovered for all the data centre will be reset. 
        2) Perform the normal bfs but with certain condition: 
            - If the outgoing of the origin is 0, it will return None
            - If the target is found and still can receive data, it will return a path
            - For every data centre, it will check the condition such that the received centre
              is not discovered, has outgoing and ingoing value, and the connections has remaining 
              capacity. If the condition is met, the data centre will be append inside discovered
              array
        3) Before returning the path, it will use previous from the targeted data centre
           to backtrack the path.

        Input: 
            - v: The origin of the data centre

        Output: 
            - A list of integer array if there exist a path from origin to target, otherwise return
              none when the discovered array ran out of integer. 
        Time complexity: O(|D| + |C|) where |D| is the number of data centre and |C| is number of
            connection. 
            - The first while loop has a complexity of O(|D|) and the for loop has a complexity of
              O(|C|). We go through the data centre once and the edge is also checked once only.
              Therefore, the total complexity will be O(|D| + |C|) with an addition of |D| when 
              creating the path. So, O(2|D| + |C|) -> O(|D| + |C|)
        """

        # Reset the discover attribute for every data centre
        self.resetDiscovered()

        # Set up the discover array and change the origin discovered to True
        res = []
        discovered = deque([])
        discovered.append(self.vertices[v])
        self.vertices[v].discovered = True

        # The function will loop until the length of discovered is 0
        while len(discovered) != 0: 

            # Pop left from the discovered queue
            a = discovered.popleft()

            # If the origin has no outgoing anymore, return None
            if not a.outgoing: 
                return None

            # If the pop element is a target and still can receive
            # Return a path by backtracking
            if a.target and a.incoming: 
                res.append(a.id)
                while a.previous != -1: 
                    res.append(a.previous.id)
                    a = a.previous
                res.reverse()
                
                return res
            else:  
                # Loop through all the edge for the outgoing data centre
                for e in a.edges: 

                    # v will be the incoming data centre
                    v = self.getVertex(e.b)
                          
                    # Condition to append into discovered: 
                    # 1) If v is not discovered
                    # 2) It still possible to flow in connection
                    # 3) The incoming and outgoing of the incoming data centre must have value.
                    # If it does not meet the condition, it will not go through the path
                    if not v.discovered and e.t and v.outgoing and v.incoming: 
                        discovered.append(v)
                        v.discovered = True
                        v.previous = a
        return None

    def fordFulkerson(self, origin): 
        """
        Ford Fulkerson function will calculate the maximum flow in the network. It uses 
        BFS to search a path and find the maximum flow that pass through from the path
        given. It will update the value for each of the data centre and also the flow. 
        The loop will continure until there is no path available. Lastly, it will return 
        the total flow inside the network.

        Input: 
            - origin: The origin of the data centre
        
        Output: The total flow of the network after the network has the maximum flow.
        Time complexity:  O(|D| · |C|^2) where |D| is the number of data centre and 
            |C| is number of connection. 
            - O(|D|) is from the path that we got from DFS function
            - O(|C|) for loop connection
            - O(|C|) for another loop connection.
            - Total complexity: O(|D| . |C|^2)
        """
        # Set the initial total flow as 0
        flow = 0

        # Call bfs to find the path
        path = self.bfs(origin)

        # The loop will continue until there is no path anymore, which means that 
        # the network reach maximum flow
        while path != None: 
            value = []

            # Find all the incoming, outgoing and capacity from the path
            # Append into a list
            for d in path:
                d = self.getVertex(d) 
                if d.id != origin and d.incoming != 0: 
                    value.append(d.incoming)

                if d.target == False and d.outgoing != 0: 
                    value.append(d.outgoing)
                
                for e in d.edges:
                    if d.id == e.a and e.b in path and e.t != 0 and d.target == False:
                        value.append(e.t)

            # Find the minimum value that can be flow
            value = min(value)

            # Perform update for the data centres in the path
            for d in path: 
                d = self.getVertex(d)
                for e in d.edges:
                    if d.id == e.a and e.b in path and e.t != 0:
                        u = self.getVertex(e.a)
                        v = self.getVertex(e.b)

                        u.outgoing -= value
                        v.incoming -= value
                        e.t -= value

                        if v.target == True: 
                            flow += value

            # Call the bfs function again to create another path
            path = self.bfs(origin)
            
        return flow
                

class Vertex: 
    """A vertex class which contains a list of edges. """

    def __init__(self, id, edge):
        """
        A constructor for vertex class.

        Attribute: 
        - id: The id of the data centre
        - edges: The connection between data centres
        - discovered: Check the discoveribility of the data centres
        - previous: Keep track the previous data centres that pass through
        - incoming: The incoming value that can be received by the data centre
        - outgoing: The outgoing value that can be send by the data centre
        - target: The target destination
        """
        self.id = id
        self.edges = [edge]
        self.discovered = False
        self.previous = -1

        self.incoming = 0
        self.outgoing = 0
        self.target = False

    def __str__(self): 
        """ A toString method when Vertex object is called. """
        string = "Vertex: {}, In: {}, Out: {}, Target: {}".format(self.id, self.incoming, self.outgoing, self.target)
        for e in self.edges:
            string += " Edge: {}".format(e)
        return string
        
    
    def addEdge(self, edge): 
        """
        A function to add edge into specific vertex

        Input: 
            - edge: The edge of the vertex
        Time complexity: O(1) as append doesn't go through the whole list.
        """
        
        self.edges.append(edge)
    
'''
    EDGE CLASS
'''
class Edge: 
    """
     An edge class which contains provide the outgoing and incoming vertex, 
     along with the weight of the edge. 
     
    """
    def __init__(self, a, b, t = 0): 
        """
        A constructor to initialize the edge attributes.
        
        Attributes
            - a: ID of the data centre departs
            - b: ID of the data centre arrives
            - t: The capacity of the connection
        """
        self.a = a
        self.b = b
        self.t = t

    def __str__(self): 
        """ A toString method when Edge object is called. """
        return "({}, {}, {})".format(self.a, self.b, self.t)

def maxThroughput(connections, maxIn, maxOut, origin, targets): 
    """
    An assignment related question. 
    The maxThroughput function a combination of multiple function to find
    the maximum flow of the network based on the connections, maxIn, maxOut, origin
    and targets. It will return the result which is the total flow of the network from
    origin to the targets. 
    1) Create a graph
    2) Create a network flow from the graph (or residual network)
    3) Add the maximum, minimum and the target
    4) Perform Ford Fulkerson algorithm
    5) Return the total flow

    Input: 
    - connections: The connections between data centre (Can be represent as edge)
    - maxIn: The maximum incoming / receive of the data centre, 
    - maxOut: The maximum outgoing / send of the data centre
    - origin: The data centre that in charge of sending
    - targets: The destination that data centre will receive

    Output: 
    - The total or maximum flow of the network

    Time complexity: O(|D| · |C|^2) where |D| is the number of data centre and 
            |C| is number of connection. 
            - The time complexity is O(|D| · |C|^2) due to the usage of fordFulkerson
            function. 
    """
    g = Graph()
    for i in connections: g.addNetwork(i)
    g.addMax(maxIn, maxOut)
    g.addTarget(targets)
    res = g.fordFulkerson(origin)
    return res

####################################################################
class Node: 
    """
    A node class is a point that contains data that is needed for storing any type of
    data. It is used to create a data structure with multiple nodes, and node is used
    for the Trie structure. 
    """
    def __init__(self, count = 0): 
        """
        A constructor for the node class to initialize data that is neccessary for the
        Trie structure.
        - Link: An array that has a size of 27 as we include all the 26 lower case letters
                with a dollar sign
        - Count: The number of words
        - fWord (or frequent word): The most frequent word
        - fCount (or frequent count): The number of the most frequent word

        Input: 
            - count - The number of word, the default count is 0 without input
        Time complexity: O(1) as both variables assigning values only
        """
        self.link = [None] * 27
        self.count = count
        self.fWord = None
        self.fCount = 0
         
class CatsTrie:
    """
    CatsTrie is a data structure that contains all the cat sentences and contains a function
    such that when you provide a prompt, it will auto complete the sentences based on the 
    frequency of words. For example, if we prompt "ab" and the most frequent word is "abc",
    it will return "abc" as output. Unless "ab" is the most frequent word, it will return "ab"
    as output. More detail description can be seen inside the functions. 
    """
    def __init__(self, sentences):
        """
        A constructor for CatsTrie class. The root will be initialized first and an array of
        sentences will be insert inside the Tries structure. 
        - Root: The highest level of the structure. The one and only node.
        - insertSentence(sentences): A method that insert all the sentences into the Tries structure

        Input: 
            sentences: A list of cat sentences
        Time complexity: O(NM), where N is the number of sentences and M is the number of characters
                         in the longer sentences. 
            - The complexity is O(NM) as we used insertSentence function.
        Space complexity: O(NM), same as above
            - We need to store the words as long as each of the characters in the word. 
        
        """
        self.root = Node()
        self.insertSentence(sentences)
    
    def insert(self, word): 
        """
        A function that insert every characters inside a word into the Tries structure. When a new
        word needs to be added into the Tries structure, it will create new Nodes inside the node link
        and further extend the depth of the Tries structure. The value or data will be save when all the
        characters have been gone through the data is reused and running the same path from top to bottom
        to modify the value if the word is more frequent than the other word stored inside the data.

        Input: 
            word - The cat sentence word
        Time complexity: O(2M) -> O(M), where M is the number of characters in the longest sentence.
            - As mentioned above, the worst case occurs when the sentence is the longest and we perform
              loop of every character inside the word. 
        """

        # Set the current node, the root node. 
        currentNode = self.root

        # Loop every character inside the word and convert the character into an index that can be used
        # to refer the linked array inside the Node. If the element inside is None, which means that
        # the character doesn't exist. So, the index that we had got from the character is used to refer
        # the link array and create a Node if the element is None.
        for char in word: 
            index = self.getIndex(char)

            if currentNode.link[index] == None: 
                currentNode.link[index] = Node()
                
            currentNode = currentNode.link[index]     

        # Lets say that we have "abc", the current node now is "c" and we add 1 into the count data inside the node       
        currentNode.count += 1

        # Save the count value inside a variable
        count = currentNode.count

        # Return back to the first node
        checkNode = self.root

        # Compare the frequency of the word with the current frequent word inside the data
        self.checkFrequency(count, checkNode, word)
        
        # Similar method as the method where we add the node, using back the example above, we traverse "abc" and
        # compare the frequency of the word with the current frequent word inside the data for every node available.
        for char in word: 
            
            index = self.getIndex(char)
            checkNode = checkNode.link[index]
            self.checkFrequency(count, checkNode, word)

    def getIndex(self, c): 
        """
        A function that returns the value that will refer to the link index array in the Node.

        Input: 
            c - One of the character in the word
        Time complexity: O(1) as its just a simple operation
        """
        return ord(c) - 97 + 1
    
    def checkFrequency(self, count, checkNode, word):
        """
        A function that compare the current word in the function and the word that is inside the
        data of the node. The word that has the most frequency by comparing the number of count
        will be replaced as the most frequent word and count. 
        
        Input: 
            count: The number count of the current word
            checkNode: The current node that we are checking
            word: The current word in the function
        Time complexity: O(1) as there is only condition checking with assignments
        """
        if count > checkNode.fCount or (count == checkNode.fCount and word < checkNode.fWord): 
            checkNode.fWord = word 
            checkNode.fCount = count


    def insertSentence(self, sentences): 
        """
        A function that perform insertion into the Tries structure for every word in the sentence.
        It will loop all the word in the sentences and call the insert function for every word.

        Input: 
            sentences: A list of sentences that contains word 
        Time complexity: O(2NM) -> O(NM) where N is the number of words in a sentence and M is the number of characters
                         in the longer sentences. 
            - The time complexity is O(NM) is because we loop N times of words in the sentence and called insert
              function which has a complexity of O(M). 
            - Total time complexity = O(N) * O(M) = O(NM)
        """
        for word in sentences: 
            self.insert(word)
      
    def autoComplete(self, prompt):
        """
        An assignment related function.
        Based on the prompt that you input, it will return the most frequent word by going through the nodes and obtain the
        value inside the node. It will return None if there is a character that is not existed inside the link array of the
        node.

        Input: 
            prompt: The message that you inputted
        Output: The most frequent word, it will return None if the word doesn't exist. 
        Time complexity: O(X), where X is the length of the prompt. 
            - It is O(X) as it only requires to go through all the character inside the prompt and return the word in the value
              of the current node.
           *- The reason why it is not O(X + Y) is because I go through all the character in the prompt and straight return a full
              word. I did not perform any method to get additional characters. 
        """

        # Set the current node, the root node.
        currentNode = self.root

        ## Loop through every character in prompt
        for char in prompt: 
            index = self.getIndex(char)

            # If the element inside the link based on the index is not None, set the node as the node inside the link array.
            # Otherwise, return none. Which means that the word doesn't exist.
            if currentNode.link[index] is not None:
                currentNode = currentNode.link[index]
            else:
                return None
        
        # Return the word inside the value of the node.
        return currentNode.fWord


