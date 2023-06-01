import itertools
import logging
import random
import re
from collections import deque
from dataclasses import dataclass
from typing import Optional

logger = logging.getLogger("tree_walk")


@dataclass
class BinaryTreeNode:
    val: int
    left: Optional["BinaryTreeNode"] = None
    right: Optional["BinaryTreeNode"] = None

    def __repr__(self):
        return f"<BinaryTreeNode[{self.val}]>"


def walk(root: BinaryTreeNode):
    queue = deque([root])

    while queue:
        node = queue.popleft()

        logger.info(f"Visiting {node!r}")

        if node.left:
            logger.debug(
                f"{node!r} left is not empty. Adding {node.left!r} to the queue"
            )
            queue.append(node.left)

        if node.right:
            logger.debug(
                f"{node!r} right is not empty. Adding {node.right!r} to the queue"
            )
            queue.append(node.right)


counter = itertools.count(random.randint(1, 10 ** 6))


def get_tree(max_depth: int, level: int = 1) -> Optional[BinaryTreeNode]:
    if max_depth == 0:
        return None

    node_left = get_tree(max_depth - 1, level=level + 1)
    node_right = get_tree(max_depth - 1, level=level + 1)
    node = BinaryTreeNode(val=next(counter), left=node_left, right=node_right)

    return node


def restore_tree(path_to_log_file: str) -> BinaryTreeNode:
    """
    The function receives path to source log file
    and returns the binary tree root.
    :param path_to_log_file: path to the source log file
    """

    # Step 1: Read the log file and extract visited node values:
    with open(path_to_log_file, "r", encoding="utf-8") as file:
        log_lines = file.readlines()

    visited_nodes = []
    for line in log_lines:
        if "Visiting" in line:
            node_val = int(re.findall(r"\d+", line)[0])
            visited_nodes.append(node_val)

    # Step 2: Create a dictionary of {node_value: node_object}
    node_dict = {}

    # Step 3: Create BinaryTreeNode objects for each visited node value
    for node_val in visited_nodes:
        node_object = BinaryTreeNode(val=node_val)
        node_dict[node_val] = node_object

    # Step 4: Link the nodes together based on relationships using the node_dict
    for line in log_lines:
        if "left is not empty" in line:
            values_list = re.findall(r"\d+", line)
            parent_val = int(values_list[0])
            child_val = int(values_list[1])

            parent_node = node_dict[parent_val]
            child_node = node_dict[child_val]
            parent_node.left = child_node

        elif "right is not empty" in line:
            values_list = re.findall(r"\d+", line)
            parent_val = int(values_list[0])
            child_val = int(values_list[1])

            parent_node = node_dict[parent_val]
            child_node = node_dict[child_val]
            parent_node.right = child_node

    # Step 5: Return the root node of the restored binary tree
    return node_dict[visited_nodes[0]]


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(levelname)s:%(message)s",
        filename="walk_log_4.txt",
    )

    root = get_tree(7)
    walk(root)

    restored_root = restore_tree("walk_log_4.txt")
    print(restored_root)
