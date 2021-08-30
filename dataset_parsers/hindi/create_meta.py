import os, re
from pathlib import Path
import argparse
import csv

class Extract():
    def __init__(self, args):
        self.path = args.path
        self.save = args.save_name
        self.split_lengths = {}
        self.second_split_lengths = {}
        self.text_dct = {}
        self.file_name_keys = {}

    def get_files(self, path, extension):
        if isinstance(path, str): path = Path(path).expanduser().resolve()
        list(path.rglob(f'*{extension}'))
        return list(path.rglob(f'*{extension}'))

    def clean_text(self, text):
        text = text.replace('\n', '')
        text = text.replace('\x00', '')
        text = text.replace('//', '')
        text = text.replace("'", '')
        text = re.sub(r'[a-zA-Z]', '', text)
        return text

    def parse_three(self, line, file_name):
        split = line.split('_')
        for idx, char in enumerate(split[2]):
            if not char.isnumeric():
                end_num=idx
                break
        if len(split[2])>3:
            key = split[0]+'_'+split[1]+'_'+split[2][:end_num]
            value = split[2][end_num:].replace('\t', '')
            return key, value
        else:
            return None, None

    def parse_one(self, line, file_name):
        split = line.split('.')
        if len(split) in self.second_split_lengths: self.second_split_lengths[len(split)] += 1
        else: self.second_split_lengths[len(split)] = 1
        if len(split) == 2:
            key_prefix=file_name.stem

            if key_prefix not in self.file_name_keys:
                self.file_name_keys[key_prefix] = 1
            else:
                self.file_name_keys[key_prefix] += 1
            key = key_prefix+'_'+str(self.file_name_keys[key_prefix])
            value = split[1]
            return key, value
        else:
            return None, None

    def parse_line(self, line, file_name):
        split = line.split('_')
        if len(split) in self.split_lengths: self.split_lengths[len(split)] += 1
        else: self.split_lengths[len(split)] = 1
        if len(split) == 3:
            fn = self.parse_three
        else:
            fn = self.parse_one
        key, value = fn(line, file_name)
        return key, value

    def save_dict_to_csv(self):
        with open(self.save, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile, delimiter='|')
            for key, val in self.text_dct.items():
                writer.writerow([key, val.strip()])

    def clean_files(self, files):
        for file_name in files:
            with open(file_name, 'r') as f:
                data = f.readlines()
            for line in data:
                line = self.clean_text(line)
                if len(line)>0:
                    key, value = self.parse_line(line, file_name)
                    if key is not None or value is not None:
                        self.text_dct[key] = value

    def run(self):
        files = self.get_files(self.path, '.txt')
        self.clean_files(files)
        self.save_dict_to_csv()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Restructure metadata')
    parser.add_argument('--path', default='../data/hindiData/')
    parser.add_argument('--save_name', default='metadata.csv')
    args = parser.parse_args()
    extract = Extract(args)
    extract.run()
    print(extract.split_lengths)
    print(extract.second_split_lengths)
    print('extracted:', len(extract.text_dct))
