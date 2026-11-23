"""Виртуальная файловая система (VFS) на основе CSV."""

import csv
import os


class VFSNode:
    """Узел файловой системы."""

    def __init__(self, name, is_dir, content=""):
        """Инициализация узла."""
        self.name = name
        self.is_dir = is_dir
        self.content = content
        self.children = {}


class VFS:
    """Виртуальная файловая система в памяти."""

    def __init__(self, csv_path):
        """Создать VFS."""
        self.root = VFSNode("/", is_dir=True)
        self.cwd = self.root
        self._load_from_csv(csv_path)

    def _load_from_csv(self, csv_path):
        """Читает CSV."""
        if not os.path.exists(csv_path):
            raise FileNotFoundError(f"Файл VFS не найден: {csv_path}")

        with open(csv_path, mode="r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                path = row["path"].strip()
                is_dir = row["type"].strip() == "dir"
                content = row.get("content", "")

                if path != "/":
                    self._create_node(path, is_dir, content)

    def _create_node(self, path, is_dir, content):
        """Создать узел."""
        parts = [p for p in path.split("/") if p]
        current = self.root
        for i, part in enumerate(parts):
            is_last = (i == len(parts) - 1)
            if part not in current.children:
                current.children[part] = VFSNode(
                    part, is_dir if is_last else True
                )

            if not is_last:
                current = current.children[part]
            else:
                if is_dir:
                    current.children[part].is_dir = True
                else:
                    current.children[part].is_dir = False
                    current.children[part].content = content

    def get_node(self, path):
        """Найти узел."""
        if not path or path == ".":
            return self.cwd

        if path.startswith("/"):
            parts = [p for p in path.split("/") if p]
            current = self.root
        else:
            parts = [p for p in path.split("/") if p]
            current = self.cwd

        for part in parts:
            if part == "..":
                current = self._find_parent(self.root, current) or current
            elif part != ".":
                current = self._get_child(current, part)
                if not current:
                    return None
        return current

    def _get_child(self, node, part):
        """Получить ребенка."""
        if part in node.children:
            return node.children[part]
        return None

    def _find_parent(self, start_node, target_node):
        """Найти родителя."""
        if start_node == target_node:
            return None
        for child in start_node.children.values():
            if child == target_node:
                return start_node
            parent = self._find_parent(child, target_node)
            if parent:
                return parent
        return None

    def list_dir(self, path=""):
        """Список файлов."""
        node = self.get_node(path)
        if not node or not node.is_dir:
            raise ValueError("Not a directory")
        return sorted(list(node.children.keys()))

    def change_dir(self, path):
        """Сменить директорию."""
        node = self.get_node(path)
        if not node or not node.is_dir:
            raise ValueError("No such directory")
        self.cwd = node
