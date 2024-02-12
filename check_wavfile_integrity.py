from argparse import ArgumentParser
from typing import Sequence, Optional
from scipy.io import wavfile
from glob import glob


def main(argv: Optional[Sequence[str]] = None):
    parser = ArgumentParser('Check wavfile integrity')
    parser.add_argument('WAVDIR')
    parser.add_argument('--recursive', '-r', action='store_true')

    args = parser.parse_args(argv)

    wav_dir = args.WAVDIR
    if args.recursive:
        wav_fps = glob(wav_dir+'**/*.wav', recursive=True)
    else:
        wav_fps = glob(wav_dir+'*.wav')
    for wav_fp in wav_fps:
        check_wav_for_warning(wav_fp)
    
def check_wav_for_warning(wav_fp: str):
    print(wav_fp)
    wavfile.read(wav_fp) # for now just let warning get printed to stdout


if __name__ == '__main__':
    main()