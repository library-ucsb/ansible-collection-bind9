



def process_zonefile(zonesrc):
    with open(zonesrc, 'r') as f:
        lines = f.readlines()

    # The number of subnet octets to truncate, so the value of 1 would cut 10.3.3 to 10.3 
    strip_octets = 1

    cleanset = []
    for line in lines:

        # Skip over blank lines
        if str(line).strip() == "":
            continue

        # Strip newline and tab characters, then split on spaces
        clean_raw = line.replace('\n', '').replace('\t', ' ').split(' ')

        # if the array begins with a comment, skip
        if clean_raw[0].strip() == ";;":
            continue

        # drop any empty entries inside the array
        clean_filtered_empty = []
        for entry in clean_raw:
            if not str(entry).strip() == "":
                clean_filtered_empty.append(entry)

        # Get rid of trailing comments in the last column
        if clean_filtered_empty[-1].startswith(';;'):
            clean_filtered_empty = clean_filtered_empty[0:-2]

        # Just take the first three columns
        clean_filtered_empty = clean_filtered_empty[:3]

        # strip octects specified ( 0 is none )
        if strip_octets > 0:
            split_val = clean_filtered_empty[0].split('.')[ 0:(-1 * strip_octets) ]
            new_val   = '.'.join(split_val)
            clean_filtered_empty[0] = new_val

        clean_final = clean_filtered_empty

        # ensure that we have at least 3 columns, then append
        if (len(clean_final) == 3):
            cleanset.append(
                {
                    'label': clean_final[0],
                    'type': clean_final[1],
                    'rdata': clean_final[-1]
                }
            )

    return cleanset

def print_yaml(zonesrc_array, path):
    print(f"{path}")
    for entry in zonesrc_array:
        print(f" - {entry}")

def write_yaml(dest, zonesrc_array):
    f = open(dest, "w")
    
    nl = '\n'
    f.write(f"rrs:{nl}")
    for entry in zonesrc_array:
        f.write(f"  - {entry}{nl}")



def main():
    zonesrc_dir = '/home/josh/docs/projects/ucsb/lib/infrastructure/ansible/plays/library-ansible-plays-dns-bind9/files/bind/zones/internal/'

    zonesrc_files_relative = [
        '3.10.in-addr.arpa.clean.dns',
        '11.10.in-addr.arpa.clean.dns',
        '12.10.in-addr.arpa.clean.dns'
    ]
    
    for zonesrc_file in zonesrc_files_relative:
        zonesrc_full_path = zonesrc_dir + zonesrc_file

        zone = process_zonefile(zonesrc_full_path)
        write_yaml(zonesrc_full_path + ".yml", zone)
        print_yaml(zone, zonesrc_file)

if __name__ == "__main__":
    main()