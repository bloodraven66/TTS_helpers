import os, re
from pathlib import Path
import argparse
import csv

def get_files(path, extension):
    if isinstance(path, str): path = Path(path).expanduser().resolve()
    list(path.rglob(f'*{extension}'))
    return list(path.rglob(f'*{extension}'))


def main(args):
    if not os.path.exists(args.wav_path):
        raise Exception(f'{args.wav_path} path for audio not found')
    paths = get_files(args.wav_path, args.extn)
    print('Number of audio files:', len(paths))
    if args.meta_data is not None:
        if not os.path.exists(args.meta_data):
            raise Exception(f'{args.meta_data} path for metadata not found')

        with open(args.meta_data, 'r+') as f:
            data = f.readlines()
        keys = [line.split('|')[0] for line in data]
        print('Number of transcripts:', len(keys))

        valid_files = [1 if path.stem in keys else 0 for path in paths]
        print('Number of audio-text pairs',sum(valid_files))

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Desc data')
    parser.add_argument('--wav_path', required=True)
    parser.add_argument('--meta_data', default=None)
    parser.add_argument('--extn', default='.wav')
    args = parser.parse_args()
    main(args)
