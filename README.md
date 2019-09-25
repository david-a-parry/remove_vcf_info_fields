# remove_vcf_info_fields
Remove one or more INFO fields from a VCF file.

## Installation/Requirements

Python3 and the modules 'parse_vcf' is required. The 'biopython' module is
required to write BGZIP compressed output. To install via pip run:

    pip3 install parse_vcf
    pip3 install biopython

## Usage

    usage: remove_info_fields.py [-h] -i VCF_INPUT [-o OUTPUT]
                                 (-r REMOVE_FIELDS [REMOVE_FIELDS ...] | -k KEEP_FIELDS [KEEP_FIELDS ...])

    Remove specific INFO fields from a VCF file.

    optional arguments:
      -h, --help            show this help message and exit
      -i VCF_INPUT, --vcf_input VCF_INPUT, --vcf VCF_INPUT
                            Input VCF file
      -o OUTPUT, --output OUTPUT
                            Output VCF file. If the given filename ends with '.gz'
                            or '.bgz' the output will be written compressed via
                            BGZIP.
      -r REMOVE_FIELDS [REMOVE_FIELDS ...], --remove_fields REMOVE_FIELDS [REMOVE_FIELDS ...]
                            One or more INFO fields to remove.
      -k KEEP_FIELDS [KEEP_FIELDS ...], --keep_fields KEEP_FIELDS [KEEP_FIELDS ...]
                            One or more INFO fields to retain. All other INFO
                            fields will be removed as long as they are defined in
                            the VCF header.
