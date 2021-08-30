import os
from pathlib import Path

def get_files(path, extension):
    if isinstance(path, str): path = Path(path).expanduser().resolve()
    list(path.rglob(f'*{extension}'))
    return list(path.rglob(f'*{extension}'))

def validate_paths(*paths):
    for path in paths:
        if not os.path.exists(path):
            raise Exception(f'{path} path not found')

def read_metadata(metadata):
    with open(metadata, 'r') as f:
        data = f.readlines()
    return data

def extract_key_text(data, delim):
    return {line.split(delim)[0]:line.split(delim)[-1] for line in data}

def extract_valid_pairs(audio_paths, extn, metadata, delim):
    text_keys = read_metadata(metadata)
    text_keys = extract_key_text(text_keys, delim)
    audio_paths = get_files(audio_paths, extn)
    valid_paths = {str(path): text_keys[path.stem] for path in audio_paths if path.stem in text_keys}
    return valid_paths

def save_splits(args, all_keys, split_dct):
    print([f'{len(split_dct[key])} {key} saved' for key in split_dct])
    for key in split_dct:

        path = os.path.join(args.save_path, args.save_prefix+key+args.save_extn)
        with open(path, 'w') as f:
            for path in split_dct[key]:
                line = path + args.delim + all_keys[path]
                f.write(line)
