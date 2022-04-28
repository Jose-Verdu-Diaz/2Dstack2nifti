import os
import json
import numpy as np
import tkinter as tk
import nibabel as nib
from PIL import Image
from tkinter import filedialog

from utils import Color, input_yes_no, input_number
from image import auto_contrast, create_coronal, display_image

config = {
    'default_input_dir': '.',
    'voxel_mult': 0.2
    }

clr = Color()


def update_config(new_config):
    for k in new_config: config[k] = new_config[k]
    with open('config.json', 'w') as f: json.dump(config, f)


def select_input_dir():
    root = tk.Tk()
    input_dir = filedialog.askdirectory(title='Select an input directory', initialdir=config['default_input_dir'])
    root.destroy()
    assert os.path.isdir(input_dir), f'{input_dir} is not a directory'
    print(f'{clr.GREY}Input Dir: {input_dir}{clr.ENDC}')
    update_config({'default_input_dir': os.path.split(input_dir)[0]})

    return input_dir


def select_input_files():
    root = tk.Tk()
    files = list(filedialog.askopenfilenames(title='Select an input directory', initialdir=config['default_input_dir']))
    root.destroy()

    assert len(files), 'Length of files is 0'

    for i, f in enumerate(files):
        if not i: extension = f.split('.')[-1]
        assert os.path.isfile(f), f'{f} is not a file'
        assert f.endswith(extension), f'Expected {extension}, found {f.split(".")[-1]}'

    input_dir = os.path.split(files[0])[0]
    update_config({'default_input_dir': os.path.split(input_dir)[0]})

    return input_dir, files


def read_directory(input_dir):
    files = []
    for f in os.listdir(input_dir):
        path = os.path.join(input_dir, f)
        if not len(files): extension = f.split('.')[-1]
        assert os.path.isfile(path), f'{path} is not a file'
        assert f.endswith(extension), f'Expected {extension}, found {f.split(".")[-1]}'
        files.append(path)
    files = sorted(files)

    return files


def load_data(files):
    images = [np.array(Image.open(f).convert('L'), dtype='uint8') for f in files]
    stacked = np.stack(images, axis=2)
    print(f'{clr.GREY}Data shape: {stacked.shape}{clr.ENDC}')

    return stacked


def transform_data(stacked):
    transformed = np.moveaxis(stacked, 0, 1)
    transformed = np.flip(transformed, 1)
    return transformed


def save_nifti(input_dir, transformed):
    s = config['voxel_mult']
    aff = np.array([
        [s,0,0,0],
        [0,s,0,0],
        [0,0,1,0],
        [0,0,0,1],
    ])
    output_name = f'{input_dir.split("/")[-1]}.nii.gz'
    nifti = nib.Nifti1Image(transformed, affine=aff)
    nib.save(nifti, os.path.join('output', output_name))
    print(f'{clr.GREEN}Data saved at: output/{output_name}{clr.ENDC}')


def main():

    if input_number('Enter 0 to load a folder or 1 to load files', [0,1], 'int'):
        input_dir, files = select_input_files()
    else:
        print(f'{clr.CYAN}Opening folder dialog, please choose an input folder...{clr.ENDC}')
        input_dir = select_input_dir()
        files = read_directory(input_dir)
        
    stacked = load_data(files)

    while True:
        coronal = create_coronal(stacked, config['voxel_mult'])
        print(f'{clr.CYAN}Displaying coronal image, close window to continue...{clr.ENDC}')
        display_image(coronal)
        print(f'{clr.CYAN}Current voxel multiplier: {config["voxel_mult"]}{clr.ENDC}')
        vm = input(f'{clr.PURPLE}Enter a new voxel multiplier or press Enter to continue:{clr.ENDC}')
        if vm:
            try:
                vm = float(vm)
            except ValueError:
                print(f'{clr.RED}{vm} is not a number{clr.ENDC}')
            assert 0 < vm <= 1, 'Voxel multiplier must be between 0 and 1'
            update_config({'voxel_mult': vm})
        else: break

    img_cont = auto_contrast(stacked)
    transformed = transform_data(img_cont)
    
    save_nifti(input_dir, transformed)


if __name__ == '__main__':
    if not os.path.isdir('output'): os.makedirs('output')
    if not os.path.isfile('config.json'): update_config({})
    with open('config.json', 'r') as f: config = json.load(f)
    main()