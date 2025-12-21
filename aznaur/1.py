import os
cur_dir_path = os.path.dirname(os.path.abspath(__file__))
txt_path = os.path.join(cur_dir_path, "text.txt")


def count_lines(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        return len(f.readlines())

def count_words(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        return len(f.read().split())

print(count_lines(txt_path))
print(count_words(txt_path))