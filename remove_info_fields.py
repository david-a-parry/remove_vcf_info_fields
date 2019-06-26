#!/usr/bin/env python3
import sys
import re
from parse_vcf import VcfReader


info_re = re.compile(r"""\#\#INFO
                      =<ID=(\S+?)          #captures metadata ID
                      (,(.*))*             #capture remaining keys/values
                      >""",                #dict line should end with a >
                      re.X)

def main(vcf_file, fields):
    ''' Remove given INFO fields from VCF '''
    vcf = VcfReader(vcf_file)
    new_head = []
    for h in vcf.header.meta_header:
        match = info_re.match(h)
        if not match or match.group(1) not in fields:
            new_head.append(h)
    print("\n".join(new_head))
    print("\t".join(vcf.col_header))
    for record in vcf:
        record.remove_info_fields(fields)
        print(record)

usage = '''
Usage: {} VCF field1 [field2 ... fieldN]

Removes one or more INFO fields from a VCF. Input can be from STDIN if '-' is
given as the input file.

All output is written to STDOUT - you will probably want to redirect to a file
or pipe into bgzip.

Examples:

    {} gnomad.genomes.r2.1.sites.vcf.bgz controls_AC controls_AF controls_AN

    tabix -h gnomad.genomes.r2.1.sites.vcf.bgz 1:100000-200000 | {} - controls_AC controls_AF controls_AN

'''.format(sys.argv[0], sys.argv[0], sys.argv[0])

if __name__ == '__main__':
    if len(sys.argv) < 3:
        sys.exit(usage)
    main(sys.argv[1], sys.argv[2:])
