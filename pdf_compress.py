#!/usr/bin/env python3

from os.path import basename, dirname, realpath, splitext, exists, getsize
from os import makedirs, chdir, system, listdir
from sys import argv

size_after = 0
size_before = 0

def change_dir(path):
    if path.endswith('.pdf'):
        dir = dirname(path)
    else:
        dir = path
    if not exists(dir):
        print(f'{dir}: Not found')
        exit(1)
    else:
        chdir(dir)

def compress_pdf(input_file, output_file):
    makedirs('.tmp', exist_ok=True)
    system('cp \'{}\' .tmp/input.pdf'.format(realpath(input_file)))
    system('gs -q -sDEVICE=pdfwrite -dCompatibilityLevel=1.4 -dPDFSETTINGS=/ebook -dNOPAUSE -dQUIET -dBATCH -sOutputFile=.tmp/output.pdf .tmp/input.pdf')
    input_size = getsize('.tmp/input.pdf')
    output_size = getsize('.tmp/output.pdf')
    print(f'({output_size/input_size:.2%} of original) => {basename(input_file)}')
    system('mv .tmp/output.pdf \'{}\''.format(realpath(output_file)))
    system('rm -rf .tmp')
    global size_after
    size_after += input_size
    global size_before
    size_before += output_size

def main():
    if len(argv) >= 2:
        file_inp = realpath(argv[1])
    if len(argv) >= 3:
        file_out = realpath(argv[2])

    if len(argv) == 3 and argv[1].endswith('.pdf') and argv[2].endswith('.pdf'):
        change_dir(file_out)
        compress_pdf(f'{file_inp}', f'{file_out}')
    elif len(argv) == 2 and argv[1].endswith('.pdf'):
        change_dir(file_inp)
        f, e = splitext(basename(file_inp))
        compress_pdf(f'{f}{e}', f'{f}_compressed{e}')
    elif len(argv) == 2 and not argv[1].endswith('.pdf'):
        change_dir(file_inp)
        for filename in listdir('.'):
            if filename.endswith('.pdf'):
                makedirs('compressed', exist_ok=True)
                compress_pdf(f'{filename}', f'compressed/{filename}')
    else:
        print(f'Usage: {argv[0]} [<path>|input.pdf output.pdf]')
        exit(1)
    print(f'Total: {size_after}Kb => {size_before}Kb (Compressed: {round((size_after-size_before)/size_after*100, 2)}%)')

if __name__ == '__main__':
    main()
