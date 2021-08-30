import os, sys, re
from pathlib import Path
import argparse
import random
sys.path.append('../common')
from utils import *

def main(args):
    validate_paths(args.audio_path, args.meta_data, args.save_path)
    valid_paths = extract_valid_pairs(args.audio_path,
                                    args.extn,
                                    args.meta_data,
                                    args.delim)
    all_keys = list(valid_paths.keys())
    random.shuffle(all_keys)
    test_keys = all_keys[:args.num_test]
    val_keys = all_keys[args.num_test:args.num_test+args.num_val]
    train_keys = all_keys[args.num_test+args.num_val:]
    dct = {'train':train_keys, 'val':val_keys , 'test':test_keys}
    save_splits(args, valid_paths, dct)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Restructure metadata')
    parser.add_argument('--audio_path', required=True)
    parser.add_argument('--extn', default='.wav')
    parser.add_argument('--meta_data', required=True)
    parser.add_argument('--save_path', required=True)
    parser.add_argument('--save_prefix', default='glowtts_')
    parser.add_argument('--save_extn', default='.txt')
    parser.add_argument('--delim', default='|')
    parser.add_argument('--random_splits', default=True)
    parser.add_argument('--num_val', default=200)
    parser.add_argument('--num_test', default=500)
    args = parser.parse_args()
    main(args)
