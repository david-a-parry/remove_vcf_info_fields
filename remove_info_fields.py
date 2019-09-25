#!/usr/bin/env python3
import sys
import re
import argparse
from parse_vcf import VcfReader

info_re = re.compile(r"""\#\#INFO
                      =<ID=(\S+?)          #captures metadata ID
                      (,(.*))*             #capture remaining keys/values
                      >""",                #dict line should end with a >
                      re.X)
def get_options():
    parser = argparse.ArgumentParser(description='''Remove specific INFO fields
    from a VCF file.''')
    parser.add_argument("-i", "--vcf_input", "--vcf", required=True,
                        help='Input VCF file')
    parser.add_argument("-o", "--output", help='''Output VCF file. If the given
                        filename ends with '.gz' or '.bgz' the output will be
                        written compressed via BGZIP (required biopython
                        module to be installed).''')
    keep_or_remove = parser.add_mutually_exclusive_group(required=True)
    keep_or_remove.add_argument('-r', '--remove_fields', nargs='+',
                                help='One or more INFO fields to remove.')
    keep_or_remove.add_argument('-k', '--keep_fields', nargs='+',
                                help='''One or more INFO fields to retain. All
                                other INFO fields will be removed as long as
                                they are defined in the VCF header.''')
    return parser

def main(vcf_input, output, remove_fields=[], keep_fields=[]):
    '''
        Remove INFO fields from VCF.

        Args:
            vcf_input:  input VCF file

            output:     VCF output file. Will write to STDOUT if not
                        provided.

            remove_fields:
                        One or more INFO fields to remove. Can not be
                        used in conjunction with keep_fields argument.

            keep_fields:
                        One or more INFO fields to keep. All other INFO
                        fields defined in the VCF header will be removed.
                        Can not be used in conjunction with remove_fields
                        argument.

    '''
    if remove_fields and keep_fields:
        raise RuntimeError("remove_fields and keep_fields arguments are " +
                           "mutually exclusive.")
    vcf = VcfReader(vcf_input)
    if output is None:
        vcf_writer = sys.stdout
    elif output.endswith(('.gz', '.bgz')):
        from Bio import bgzf
        vcf_writer = bgzf.BgzfWriter(output)
    else:
        vcf_writer = open(output, 'w')
    new_head = []
    if keep_fields:
        remove_fields = [x for x in vcf.header.metadata['INFO'].keys() if x not
                         in keep_fields]
    for h in vcf.header.meta_header:
        match = info_re.match(h)
        if not match or match.group(1) not in remove_fields:
            new_head.append(h)
    vcf_writer.write("\n".join(new_head) + "\n")
    vcf_writer.write("\t".join(vcf.col_header) + "\n")
    for record in vcf:
        record.remove_info_fields(remove_fields)
        vcf_writer.write(str(record) + "\n")
    vcf_writer.close()

if __name__ == '__main__':
    argparser = get_options()
    args = argparser.parse_args()
    main(**vars(args))
