from Captions.TimeFormats.Nodes.INode import INode
from Captions.TimeFormats.Nodes.AbstractNodeFactory import initialize_node_factory
from Projects.SRTProject import SRTProject

STARTING_INDEX = 0
ENDING_INDEX = -1

INVALID_INDEX_ERROR = "Index out of bounds"
INVALID_LENGTH_ERROR = "Length must be greater than or equal to 0"
INVALD_LOOP_ID_ERROR = "Loop ID not found"

class LinkedList:
    # Private -----------------------------------------------------------------
    def __init__(self, data_type: str):
        self.__head = None
        self.__current = None
        self.__end = None
        self.__length = 0

        self.node_factory = initialize_node_factory(data_type)
        self.__fill_list(data_type)


    # Function is kinda gross, figure out how to refactor it
    def __fill_list(self, data_type: str) -> None:
        project = SRTProject()

        if data_type == "SPT":
            self.append_list_to_end(project.script.loops)
        elif data_type == "MRK":
            self.append_list_to_end(project.session.markers)
        elif data_type == "EDL":
            self.append_list_to_end(project.session.tracks[0].channels[0])


    def __validate_index(self, index: int) -> None:
        assert index >= 0 and index < self.__length, INVALID_INDEX_ERROR


    def __validate_not_empty(self) -> None:
        assert not self.__is_list_empty(), INVALID_LENGTH_ERROR


    def __is_list_empty(self) -> bool:
        return self.__length == 0


    def __add_node_to_empty_list(self, node: INode) -> None:
        self.__head = node
        self.__end = node
        self.__current = node
        self.__length += 1


    def __add_node_to_end(self, node: INode) -> None:
        if self.__is_list_empty():
            self.__add_node_to_empty_list(node)
        elif self.__length == 1:
            self.__head._next = node
            node._previous = self.__head
            self.__end = node
            self.__length += 1
        else:
            self.__insert_links_at_end(node)

    
    def __add_node_to_start(self, node: INode) -> None:
        if self.__is_list_empty():
            self.__add_node_to_empty_list(node)
        elif self.__length == 1:
            self.__head = node
            self.__head._next = self.__end
            self.__end._previous = self.__head
            self.__length += 1
        else:
            self.__insert_links_at_start(node)
            

    def __add_node_at_index(self, node: INode, index: int) -> None:
        self.__validate_index(index)

        if index == STARTING_INDEX:
            self.__add_node_to_start(node)
        elif index == self.__length or index == ENDING_INDEX:
            self.__add_node_to_end(node)
        else:
            self.__insert_links(node, index)


    def __insert_links(self, node: INode, index: int) -> None:
        current = self.__get_node_at_index(index)
        previous = current._previous
        
        node._next = current
        node._previous = previous

        previous._next = node
        current._previous = node

        self.__length += 1

    
    def __insert_links_at_start(self, node: INode) -> None:
        node._next = self.__head
        self.__head._previous = node
        self.__head = node
        self.__length += 1

    
    def __insert_links_at_end(self, node: INode) -> None:
        self.__end._next = node
        node._previous = self.__end
        self.__end = node
        self.__length += 1

    
    def __remove_links(self, index: int) -> None:
        current = self.__get_node_at_index(index)
        previous = current._previous
        next = current._next

        previous._next = next
        next._previous = previous

        self.__length -= 1


    def __remove_only_node(self) -> None:
        self.__head = None
        self.__end = None
        self.__current = None
        self.__length = 0

    
    def __remove_links_at_start(self) -> None:
        self.__head = self.__head._next
        self.__head._previous = None
        self.__length -= 1


    def __get_node_at_index(self, index: int) -> INode:
        self.__validate_index(index)

        current = self.__head
        for _ in range(index):
            current = current._next

        return current


    # Public ------------------------------------------------------------------
    def append_list_to_end(self, data: list) -> None:
        for item in data:
            self.create_node_at_end(item)
            

    def should_continue(self) -> bool:
        return self.__current != None


    def iterate_current_node(self) -> INode:
        if self.__current == None:
            return None
        
        current = self.__current
        self.__current = self.__current._next

        return current
    

    def reset(self) -> None:
        self.__current = self.__head


    def create_node_at_index(self, data, index: int) -> INode:
        node = self.node_factory.create_node(data)
        self.__add_node_at_index(node, index)

    
    def create_node_at_start(self, data) -> INode:
        node = self.node_factory.create_node(data)
        self.__add_node_to_start(node)


    def create_node_at_end(self, data) -> INode:
        node = self.node_factory.create_node(data)
        self.__add_node_to_end(node)


    def remove_node_at_index(self, index: int) -> None:
        self.__validate_index(index)

        if index == STARTING_INDEX:
            self.remove_node_at_start()
        elif index == self.__length or index == ENDING_INDEX:
            self.remove_node_at_end()
        else:
            self.__remove_links(index)


    def remove_node_at_start(self) -> None:
        self.__validate_not_empty()

        if self.__length == 1:
            self.__remove_only_node()
        else:
            self.__remove_links_at_start()


    def remove_node_at_end(self) -> None:
        self.__validate_not_empty()

        if self.__length == 1:
            self.__remove_only_node()
        else:
            self.__remove_links_at_start()


    def remove_node_with_loop_id(self, loop_id: str) -> None:
        index = self.get_index_from_loop_id(loop_id)
        self.remove_node_at_index(index)


    def get_index_from_loop_id(self, loop_id: str) -> int:
        current = self.__head
        for i in range(self.__length):
            if current.get_loop_id() == loop_id:
                return i
            current = current._next

        raise ValueError(INVALD_LOOP_ID_ERROR)