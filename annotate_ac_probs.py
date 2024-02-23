from argparse import ArgumentParser
from typing import Sequence, Optional
from scipy.io import wavfile
from glob import glob
from zugubul.models.infer import infer
from pympi import Elan
import os
from tqdm import tqdm


def main(argv: Optional[Sequence[str]] = None):
    parser = ArgumentParser('Annotate directory of eaf files with AC probabilities for each annotation')
    parser.add_argument('EAFDIR')
    parser.add_argument('OUTDIR')
    parser.add_argument('--recursive', '-r', action='store_true')
    parser.add_argument('--tier', '-t')
    parser.add_argument('--tgt_lang')
    parser.add_argument('--model', '-m')

    args = parser.parse_args(argv)

    eaf_dir = args.EAFDIR
    out_dir = args.OUTDIR

    if args.recursive:
        eaf_fps = glob(os.path.join(eaf_dir, '**/*.eaf'), recursive=True)
    else:
        eaf_fps = glob(os.path.join(eaf_dir, '*.eaf'))
    for eaf_fp in tqdm(eaf_fps, desc="Annotating eafs"):
        eaf_obj = Elan.Eaf(eaf_fp)
        media_paths = [x['MEDIA_URL'] for x in eaf_obj.media_descriptors]
        media = media_paths[0]
        # trim prefix added by ELAN
        # have to keep initial / on posix systems
        # and remove on Windows
        if os.name == 'nt':
            media = media.replace('file:///', '')
        else:
            media = media.replace('file://', '')
        eaf_out = infer(
            source = media,
            eaf = eaf_obj,
            inference_method='local',
            return_ac_probs=True,
            model='/mnt/cube/home/AD/mjsimmons/markjosims/wav2vec2-large-mms-1b-tira-lid-2cat-tira-finetune',
            task='LID',
            max_len=20,
            tier=args.tier,
            tgt_lang=args.tgt_lang,
            model=args.model,
        )
        eaf_stem = os.path.basename(eaf_fp)
        out_fp = os.path.join(out_dir, eaf_stem)
        eaf_out.to_file(out_fp)



if __name__ == '__main__':
    main()