import os
cur_dir_path = os.path.dirname(os.path.abspath(__file__))
txt_path = os.path.join(cur_dir_path, "text.txt")


def count_lines(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        for count, line in enumerate(f, 1):
            return count

        
count_lines("text.txt")  


    

        