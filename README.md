# remove_vcf_info_fields
Remove one or more INFO fields from a VCF file.

## Installation/Requirements

Python3 and the module 'parse_vcf' are required. To install the parse_vcf module run:

    pip3 install parse_vcf

## Usage

    ./remove_info_fields.py VCF field1 [field2 ... fieldN]

## Examples:

Remove the three INFO fields 'controls_AC', 'controls_AF' and  'controls_AN' from the gnomad.genomes.r2.1.sites.vcf.bgz VCF:

    ./remove_info_fields.py gnomad.genomes.r2.1.sites.vcf.bgz controls_AC controls_AF controls_AN

All output is written to STDOUT - you will probably want to redirect to a file
or pipe into bgzip.

    ./remove_info_fields.py gnomad.genomes.r2.1.sites.vcf.bgz controls_AC controls_AF controls_AN \
        | bgzip -c > output.vcf.gz


Input can be from STDIN if '-' is given as the input file.

    tabix -h gnomad.genomes.r2.1.sites.vcf.bgz 1:100000-200000 | \
        ./remove_info_fields.py - controls_AC controls_AF controls_AN | \
        bgzip -c > output.vcf.gz

Remove all INFO fields with 'neuro', 'topmed' or 'controls' in their name from gnomad 2.1 VCFs:

    ./remove_info_fields.py gnomad.genomes.r2.1.sites.vcf.bgz \
        $(tabix -H gnomad.genomes.r2.1.sites.hg38_lift.vcf.bgz | grep INFO | \
        grep -e neuro -e topmed -e controls  | cut -f 3 -d= | cut -f 1 -d,) \
        | bgzip -c > gnomad.genomes.r2.1.sites.no_topmed_no_neuro_no_controls.vcf.gz
