from no import Node
from fila import Queue


class AVLTree():

  def __init__(self, h=[]):
    self.rootNode = None
    self.elements_count = 0
    self.rebalance_count = 0
    for el in h:
      self.insert(el)

  def height(self):
    if self.rootNode:
      return self.rootNode.height
    else:
      -1

  def find_in_subtree(self, key, node):
    if node is None:
      return None  # chave não encontrada-
    if key < node.key:
      return self.find_in_subtree(key, node.leftChild)
    elif key > node.key:
      return self.find_in_subtree(key, node.rightChild)
    else:  # chave é igual à chave do nó
      return node

  def find(self, key, node=None):
    if node is None:
      node = self.rootNode
    return self.find_in_subtree(key, node)

  def recompute_heights(self, startNode):
    changed = True
    node = startNode
    while node and changed:
      old_height = node.height
      node.height = (node.max_children_height() + 1 if
                     (node.rightChild or node.leftChild) else 0)
      changed = node.height != old_height
      node = node.parent

  def find_biggest(self):
    node = self.rootNode
    while node.rightChild:
      node = node.rightChild
    return node

  def find_smallest(self):
    node = self.rootNode
    while node.leftChild:
      node = node.leftChild
    return node

  def as_list(self, type=1): #essa função realizar a ordenação por 'in order', 'preorder', 'posordem'
    if not self.rootNode:
      return []
    assert type in [0, 1, 2], 'valor de tipo errado'

    if type == 0:
      return self.preorder(self.rootNode)
    elif type == 1:
      return self.inorder(self.rootNode)
    elif type == 2:
      return self.postorder(self.rootNode)

  def preorder(self, node, retlst=None):
    if retlst is None:
      retlst = []
    retlst += [node.key]
    if node.leftChild:
      retlst = self.preorder(node.leftChild, retlst)
    if node.rightChild:
      retlst = self.preorder(node.rightChild, retlst)
    return retlst

  def inorder(self, node, retlst=None):
    if retlst is None:
      retlst = []
    if node.leftChild:
      retlst = self.inorder(node.leftChild, retlst)
    retlst += [node.key]
    if node.rightChild:
      retlst = self.inorder(node.rightChild, retlst)
    return retlst

  def postorder(self, node, retlst=None):
    if retlst is None:
      retlst = []
    if node.leftChild:
      retlst = self.postorder(node.leftChild, retlst)
    if node.rightChild:
      retlst = self.postorder(node.rightChild, retlst)
    retlst += [node.key]
    return retlst

  def levelorder(self, nivel):
    node = self.rootNode
    queue = Queue()
    queue.push(node)
    while len(queue):
      node = queue.pop()
      if node.leftChild:
        queue.push(node.leftChild)
      if node.rightChild:
        queue.push(node.rightChild)
      print(node,'->',  end=" ")

  def add_as_child(self, parent_node, child_node):
    node_to_rebalance = None
    parent_node.size += 1
    if child_node.key < parent_node.key:

      if not parent_node.leftChild:
        parent_node.leftChild = child_node
        child_node.parent = parent_node
        if parent_node.height == 0:  # neste caso a altura das árvores pode mudar
          node = parent_node
          while node:
            node.height = node.max_children_height() + 1
            if not node.balance() in [-1, 0, 1]:
              node_to_rebalance = node
              break
            node = node.parent
      else:
        self.add_as_child(parent_node.leftChild, child_node)
    else:
      if not parent_node.rightChild:
        parent_node.rightChild = child_node
        child_node.parent = parent_node
        if parent_node.height == 0:  # neste caso a altura das árvores pode mudar
          node = parent_node
          while node:
            node.height = node.max_children_height() + 1
            if not node.balance() in [-1, 0, 1]:
              node_to_rebalance = node
              break
            node = node.parent
      else:
        self.add_as_child(parent_node.rightChild, child_node)

    if node_to_rebalance:
      self.rebalance(node_to_rebalance)

  def insert(self, key):
    new_node = Node(key)
    if not self.rootNode:
      self.rootNode = new_node
      assert self.elements_count == 0, 'Elements_count errado'
      self.elements_count += 1
    else:
      if not self.find(key):
        self.elements_count += 1
        self.add_as_child(self.rootNode, new_node)
    return self

  def remove_branch(self, node): #função que faz  balanceamento.
    
    parent = node.parent
    if (parent):
      if parent.leftChild == node:
        parent.leftChild = node.rightChild or node.leftChild
      else:
        parent.rightChild = node.rightChild or node.leftChild
      if node.leftChild:
        node.leftChild.parent = parent
      else:
        node.rightChild.parent = parent
      self.recompute_heights(parent)
    del node

    # reequilibrar
    node = parent
    while (node):
      self.resize(node)
      if not node.balance() in [-1, 0, 1]:
        self.rebalance(node)

      node = node.parent

  def remove_leaf(self, node): #função que faz o balanceamento.
    
    parent = node.parent
    if (parent):
      if parent.leftChild == node:
        parent.leftChild = None
      else:
        parent.rightChild = None
      self.recompute_heights(parent)
    else:
      self.rootNode = None
    del node

    # rebalancear
    node = parent
    while (node):
      self.resize(node)
      if not node.balance() in [-1, 0, 1]:
        self.rebalance(node)
      node = node.parent

  def remove(self, key):
    node = self.find(key)

    if not node is None:
      self.elements_count -= 1
      if node.is_leaf():
        self.remove_leaf(node)
      elif (bool(node.leftChild)) ^ (bool(node.rightChild)):
        self.remove_branch(node)
      else:
        self.swap_with_successor_and_remove(node)

  def swap_with_successor_and_remove(self, node):
    successor = self.find_smallest(node.rightChild)
    self.swap_nodes(node, successor)
    if node.height == 0:
      self.remove_leaf(node)
    else:
      self.remove_branch(node)

  def swap_nodes(self, node1, node2):
    parent1 = node1.parent
    leftChild1 = node1.leftChild
    rightChild1 = node1.rightChild
    parent2 = node2.parent
    leftChild2 = node2.leftChild
    rightChild2 = node2.rightChild

    # trocar alturas
    tmp = node1.height
    node1.height = node2.height
    node2.height = tmp

    # trocar tamanhos

    tmp = node1.size
    node1.size = node2.size
    node2.size = tmp

    if parent1:
      if parent1.leftChild == node1:
        parent1.leftChild = node2
      else:
        parent1.rightChild = node2
      node2.parent = parent1
    else:
      self.rootNode = node2
      node2.parent = None

    node2.leftChild = leftChild1
    leftChild1.parent = node2

    node1.leftChild = leftChild2
    node1.rightChild = rightChild2
    if rightChild2:
      rightChild2.parent = node1

    if not (parent2 == node1):
      node2.rightChild = rightChild1
      rightChild1.parent = node2

      parent2.leftChild = node1
      node1.parent = parent2
    else:
      node2.rightChild = node1
      node1.parent = node2

  def resize(self, node):
    node.size = 1
    if node.rightChild:
      node.size += node.rightChild.size
    if node.leftChild:
      node.size += node.leftChild.size

  def rebalance(self, node_to_rebalance):
    self.rebalance_count += 1
    A = node_to_rebalance
    F = A.parent
    if node_to_rebalance.balance() == -2:
      if node_to_rebalance.rightChild.balance() <= 0:
        """Rebalanceamento, caso RRC """
        B = A.rightChild
        C = B.rightChild
        A.rightChild = B.leftChild
        if A.rightChild:
          A.rightChild.parent = A
        B.leftChild = A
        A.parent = B
        if F is None:
          self.rootNode = B
          self.rootNode.parent = None
        else:
          if F.rightChild == A:
            F.rightChild = B
          else:
            F.leftChild = B
          B.parent = F
        self.recompute_heights(A)
        self.resize(A)
        self.resize(B)
        self.resize(C)
      else:
        """Rebalanceamento, caso RLC"""
        B = A.rightChild
        C = B.leftChild
        B.leftChild = C.rightChild
        if B.leftChild:
          B.leftChild.parent = B
        A.rightChild = C.leftChild
        if A.rightChild:
          A.rightChild.parent = A
        C.rightChild = B
        B.parent = C
        C.leftChild = A
        A.parent = C
        if F is None:
          self.rootNode = C
          self.rootNode.parent = None
        else:
          if F.rightChild == A:
            F.rightChild = C
          else:
            F.leftChild = C
          C.parent = F
        self.recompute_heights(A)
        self.recompute_heights(B)
        self.resize(A)
        self.resize(B)
        self.resize(C)

    else:
      if node_to_rebalance.leftChild.balance() >= 0:
        B = A.leftChild
        C = B.leftChild
        """Rebalanceamento, caso LLC """
        A.leftChild = B.rightChild
        if (A.leftChild):
          A.leftChild.parent = A
        B.rightChild = A
        A.parent = B
        if F is None:
          self.rootNode = B
          self.rootNode.parent = None
        else:
          if F.rightChild == A:
            F.rightChild = B
          else:
            F.leftChild = B
          B.parent = F
        self.recompute_heights(A)
        self.resize(A)
        self.resize(C)
        self.resize(B)

      else:
        B = A.leftChild
        C = B.rightChild
        """Rebalanceamento, caso LRC """
        A.leftChild = C.rightChild
        if A.leftChild:
          A.leftChild.parent = A
        B.rightChild = C.leftChild
        if B.rightChild:
          B.rightChild.parent = B
        C.leftChild = B
        B.parent = C
        C.rightChild = A
        A.parent = C
        if F is None:
          self.rootNode = C
          self.rootNode.parent = None
        else:
          if (F.rightChild == A):
            F.rightChild = C
          else:
            F.leftChild = C
          C.parent = F
        self.recompute_heights(A)
        self.recompute_heights(B)
        self.resize(A)
        self.resize(B)
        self.resize(C)

  def findkth(self, k, root=None):
    if root is None:
      root = self.rootNode
    assert k <= root.size, 'Erro, k maior que o tamanho de BST'
    leftsize = 0 if root.leftChild is None else root.leftChild.size
    if leftsize >= k:
      return self.findkth(k, root.leftChild)

    elif leftsize == k - 1:
      return root.key
    else:
      return self.findkth(k - leftsize - 1, root.rightChild)

  
    if start_node == None:
      start_node = self.rootNode
    space_symbol = r"  "
    spaces_count = 15 * 2*(self.rootNode.height)
    out_string = r""
    initial_spaces_string = space_symbol * spaces_count + "\n"
    if not start_node:
      return "A árvore está vazia"
    height = 2*(self.rootNode.height)
    level = [start_node]

    while (len([i for i in level if (not i is None)]) > 0):
      level_string = initial_spaces_string
      for i in range(len(level)):
        j = int((2 * i + 1) * spaces_count / (2 * len(level)))
        level_string = level_string[:j] + (str(level[i]) if level[i] else
                                           space_symbol) + level_string[j + 1:]
      out_string += level_string

      # criar próximo nível
      level_next = []
      for i in level:
        level_next += ([i.leftChild, i.rightChild] if i else [None, None])
      # adicionar conexão aos próximos nós
      for w in range(height - 1):
        level_string = initial_spaces_string
        for i in range(len(level)):
          if not level[i] is None:
            shift = spaces_count // (2 * len(level))
            j = (2 * i + 1) * shift
            level_string = level_string[:j - w - 1] + (
              '/' if level[i].leftChild else space_symbol) + level_string[j -
                                                                          w:]
            level_string = level_string[:j + w + 1] + (
              '\\' if level[i].rightChild else space_symbol) + level_string[j +
                                                                            w:]
        out_string += level_string
      height = height // 2
      level = level_next

    return out_string
