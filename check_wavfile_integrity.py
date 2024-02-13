from argparse import ArgumentParser
from scipy.io import wavfile
from glob import glob
import os
import warnings
from tqdm import tqdm

warnings.filterwarnings("error")

def main():
    parser = ArgumentParser('Check wavfile integrity')
    parser.add_argument('WAVDIR')
    parser.add_argument('--recursive', '-r', action='store_true')

    args = parser.parse_args()

    wav_dir = args.WAVDIR
    if args.recursive:
        wav_fps = glob(os.path.join(wav_dir, '**/*.wav'), recursive=True)
    else:
        wav_fps = glob(os.path.join(wav_dir, '*.wav'))
    for wav_fp in tqdm(wav_fps, desc='wav files discovered'):
        check_wav_for_warning(wav_fp)
    
def check_wav_for_warning(wav_fp: str):
    try:
        wavfile.read(wav_fp) # for now just let warning get printed to stdout
    except wavfile.WavFileWarning:
        print(f"Error with {wav_fp}")

if __name__ == '__main__':
    main()