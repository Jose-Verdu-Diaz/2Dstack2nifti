import os
import numpy as np
import tkinter as tk
from tkinter import filedialog
from PIL import Image
import nibabel as nib


def select_input():
    root = tk.Tk()
    input_dir = filedialog.askdirectory(title='Select an input directory')
    root.destroy()
    assert os.path.isdir(input_dir), f'{input_dir} is not a directory'
    print (f'Input Dir: {input_dir}')

    return input_dir


def read_data(input_dir):
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
    print(f'Data shape: {stacked.shape}')

    return stacked


def transform_data(stacked):
    transformed = np.moveaxis(stacked, 0, 1)
    transformed = np.flip(transformed, 1)
    print(f'Transformed shape: {transformed.shape}')


def save_nifti(input_dir, transformed):
    s = 0.1
    aff = np.array([
        [s,0,0,0],
        [0,s,0,0],
        [0,0,1,0],
        [0,0,0,1],
    ])
    output_name = f'{input_dir.split("/")[-1]}.nii.gz'
    nifti = nib.Nifti1Image(transformed, affine=aff)
    nib.save(nifti, os.path.join('output', output_name))
    print(f'Data saved at: output/{output_name}')


def main():
    if not os.path.isdir('output'): os.makedirs('output')

    input_dir = select_input()
    files = read_data(input_dir)
    stacked = load_data(files)
    transformed = transform_data(stacked)
    save_nifti(input_dir, transformed)


if __name__ == '__main__':
    main()