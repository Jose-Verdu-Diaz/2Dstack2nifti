import os
import json
import numpy as np
from PIL import Image, ImageTk
import tkinter as tk
import nibabel as nib
from tkinter import filedialog

config = {
    'default_input_dir': '.',
    'voxel_mult': 0.2
    }

def update_config(new_config):
    for k in new_config: config[k] = new_config[k]
    with open('config.json', 'w') as f: json.dump(config, f)


def display_image(img):
    root = tk.Tk()
    img = ImageTk.PhotoImage(image=Image.fromarray(img))
    tk.Label(
        root,
        image=img
    ).pack()
    root.mainloop()

def create_coronal(img):
    rows = []
    middle = int(img.shape[1] / 2)
    n = int(1 / config['voxel_mult'])
    print(n)
    print(img.shape[2])
    for i in range(img.shape[2]):
        for j in range(n): rows.insert(0, img[middle, :, i])
    img_new = np.array(rows)
    return img_new


def select_input():
    root = tk.Tk()
    input_dir = filedialog.askdirectory(title='Select an input directory', initialdir=config['default_input_dir'])
    root.destroy()
    assert os.path.isdir(input_dir), f'{input_dir} is not a directory'
    print (f'Input Dir: {input_dir}')

    update_config({'default_input_dir': os.path.split(input_dir)[0]})

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


def auto_contrast(img):
    print(f'Min/Max values before auto contrast: {img.min()}/{img.max()}')
    img = img / 255
    update_contrast = lambda x, a, b: (x - a) / (b - a)
    img_cont = update_contrast(img, img.min(), img.max())
    img_cont = np.where(img_cont > 0, img_cont, 0)
    img_cont = np.where(img_cont < 1, img_cont, 1)
    img_cont = np.array(img_cont * 255, dtype=np.uint8)
    print(f'Min/Max values after auto contrast:  {img_cont.min()}/{img_cont.max()}')

    return img_cont


def transform_data(stacked):
    transformed = np.moveaxis(stacked, 0, 1)
    transformed = np.flip(transformed, 1)
    print(f'Transformed shape: {transformed.shape}')
    return transformed


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
    input_dir = select_input()
    files = read_data(input_dir)
    stacked = load_data(files)
    coronal = create_coronal(stacked)
    display_image(coronal)
    img_cont = auto_contrast(stacked)
    transformed = transform_data(img_cont)
    save_nifti(input_dir, transformed)


if __name__ == '__main__':
    if not os.path.isdir('output'): os.makedirs('output')
    if not os.path.isfile('config.json'): update_config({})
    with open('config.json', 'r') as f: config = json.load(f)
    main()