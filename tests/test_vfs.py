"""Тесты виртуальной файловой системы (VFS)."""

import pytest

from src.vfs import VFS


def test_load_vfs(tmp_path):
    """Проверка загрузки VFS из CSV."""
    csv_file = tmp_path / "test.csv"
    csv_file.write_text(
        "path,type,content\n/,dir,\n/home,dir,\n/home/test.txt,file,Hello",
        encoding="utf-8",
    )
    vfs = VFS(str(csv_file))
    assert vfs.root.name == "/"
    assert "home" in vfs.root.children


def test_get_node(tmp_path):
    """Проверка поиска узла по пути."""
    csv_file = tmp_path / "test.csv"
    csv_file.write_text(
        "path,type,content\n/,dir,\n/home,dir,\n/home/test.txt,file,Hello",
        encoding="utf-8",
    )
    vfs = VFS(str(csv_file))
    node = vfs.get_node("/home/test.txt")
    assert node is not None
    assert node.name == "test.txt"
    assert node.content == "Hello"


def test_change_dir(tmp_path):
    """Проверка смены директории."""
    csv_file = tmp_path / "test.csv"
    csv_file.write_text(
        "path,type,content\n/,dir,\n/home,dir,\n", encoding="utf-8"
    )
    vfs = VFS(str(csv_file))
    vfs.change_dir("/home")
    assert vfs.cwd.name == "home"


def test_list_dir(tmp_path):
    """Проверка вывода списка файлов."""
    csv_file = tmp_path / "test.csv"
    csv_file.write_text(
        "path,type,content\n/,dir,\n/home,dir,\n/home/test.txt,file,Hello",
        encoding="utf-8",
    )
    vfs = VFS(str(csv_file))
    files = vfs.list_dir("/home")
    assert "test.txt" in files


def test_file_not_found():
    """Проверка ошибки при отсутствии файла."""
    with pytest.raises(FileNotFoundError):
        VFS("nonexistent.csv")
