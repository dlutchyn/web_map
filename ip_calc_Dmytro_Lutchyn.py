def get_ip_from_raw_address(raw_address: str) -> str:
    '''
    Returns IP address from raw address.
    >>> get_ip_from_raw_address('91.124.230.205/30')
    91.124.230.205
    '''
    return raw_address.split('/')[0]


def get_network_address_from_raw_address(raw_address: str) -> str:
    '''
    Returns network address from raw address.
    >>> get_network_address_from_raw_address('91.124.230.205/30')
    91.124.230.204
    '''
    cidr = int(raw_address.split('/')[1])
    ip_address = get_ip_from_raw_address(raw_address)
    bin_ip_address = ''.join(binary_convert_ip(ip_address))
    new_bin_ip_address = bin_ip_address[:cidr] + '0'*(32 - cidr)
    network_address = [str(int(new_bin_ip_address[i:i+8], 2))
                       for i in range(0, 32, 8)]
    return '.'.join(network_address)


def get_broadcast_address_from_raw_address(raw_address: str) -> str:
    '''
    Returns broadcast address from raw address.
    >>> get_broadcast_address_from_raw_address('91.124.230.205/30')
    91.124.230.207
    '''
    cidr = int(raw_address.split('/')[1])
    ip_address = get_ip_from_raw_address(raw_address)
    bin_ip_address = ''.join(binary_convert_ip(ip_address))
    new_bin_ip_address = bin_ip_address[:cidr] + '1'*(32 - cidr)
    broadcast_address = [str(int(new_bin_ip_address[i:i+8], 2))
                         for i in range(0, 32, 8)]
    return '.'.join(broadcast_address)


def get_binary_mask_from_raw_address(raw_address: str) -> str:
    '''
    Returns binary subnet mask from raw address.
    >>> get_broadcast_address_from_raw_address('91.124.230.205/30')
    11111111.11111111.11111111.11111100
    '''
    cidr = int(raw_address.split('/')[1])
    bin_mask = '1'*cidr + '0'*(32-cidr)
    binary_subnet_mask = [bin_mask[i:i+8] for i in range(0, 32, 8)]
    return '.'.join(binary_subnet_mask)


def binary_convert_ip(ip: str) -> list:
    '''
    Returns converted ip address from int to binary form.
    >>> binary_convert_ip('91.124.230.205')
    ['01011011', '01111100', '11100110', '11001101']
    '''
    bin_ip = ip.split('.')
    for i in range(len(bin_ip)):
        bin_ip[i] = '0'*(8-len(bin(int(bin_ip[i]))[2:])) + \
            bin(int(bin_ip[i]))[2:]
    return bin_ip


def get_first_usable_ip_address_from_raw_address(raw_address: str) -> str:
    '''
    Returns first usable IP address from raw address.
    >>> get_first_usable_ip_address_from_raw_address('91.124.230.205/30')
    91.124.230.205
    '''
    network_address = get_network_address_from_raw_address(
        raw_address).split('.')
    network_address[-1] = str(int(network_address[-1]) + 1)
    return '.'.join(network_address)


def get_penultimate_usable_ip_address_from_raw_address(raw_address: str) -> str:
    '''
    Returns penultimate usable IP address from raw address.
    >>> get_penultimate_usable_ip_address_from_raw_address('91.124.230.205/30')
    91.124.230.206
    '''
    broadcast_address = get_broadcast_address_from_raw_address(
        raw_address).split('.')
    broadcast_address[-1] = str(int(broadcast_address[-1]) - 1)
    return '.'.join(broadcast_address)


def get_number_of_usable_hosts_from_raw_address(raw_address: str) -> int:
    '''
    Returns number of usable hosts from raw address.
    >>> get_penultimate_usable_ip_address_from_raw_address('91.124.230.205/30')
    2
    '''
    mask_len = int(raw_address.split('/')[1])
    host_number = 2**(32 - mask_len) - 2
    if host_number > 0:
        return host_number
    else:
        return 0


def get_ip_class_from_raw_address(raw_address: str) -> str:
    '''
    Returns IP class from raw address.
    >>> get_ip_class_from_raw_address('91.124.230.205/30')
    A
    '''
    first_value = int(get_ip_from_raw_address(raw_address)[0])
    if 1 <= first_value <= 126:
        return 'A'
    elif 128 <= first_value <= 191:
        return 'B'
    elif 192 <= first_value <= 223:
        return 'C'
    elif 224 <= first_value <= 239:
        return 'D'
    elif 240 <= first_value <= 254:
        return 'E'


def check_private_ip_address_from_raw_address(raw_address: str) -> str:
    '''
    Returns True if IP address is private and False otherwise.
    >>> check_private_ip_address_from_raw_address('91.124.230.205/30')
    False
    '''
    ip_address = get_ip_from_raw_address(raw_address)
    one_octane = ip_address.split('.')[0]
    two_octanes = ip_address.split('.')[0] + '.' + ip_address.split('.')[1]
    if one_octane == '10':
        return True
    elif two_octanes == '172.16' or two_octanes == '192.168':
        return True
    else:
        return False


def check_input(text: str) -> bool:
    '''
    Returns True if given ip address is correctly inputed and False otherwise.
    >>> check_input('text')
    Error
    False
    >>> check_input('91.124.230.205')
    Missing prefix
    False
    '''
    ip_address = text.split('/')
    new_ip_address = ip_address[0].split('.')
    for elem in new_ip_address:
        if not elem.isdigit():
            print('Error')
            return False
    if len(ip_address) != 2:
        print('Missing prefix')
        return False
    for i in range(len(new_ip_address)-1):
        if 0 <= int(elem) <= 255:
            continue
        else:
            print('None')
            return False
    if 32 < int(new_ip_address[-1]) or 0 > int(new_ip_address[-1]):
        print('None')
        return False

    return True


if __name__ == "__main__":
    raw_address = input('Enter raw address: ')
    if check_input(raw_address):
        print('IP address:', get_ip_from_raw_address(raw_address))
        print('Network Address:',
              get_network_address_from_raw_address(raw_address))
        print('Broadcast Address:',
              get_broadcast_address_from_raw_address(raw_address))
        print('Binary Subnet Mask:',
              get_binary_mask_from_raw_address(raw_address))
        print('First usable host IP:',
              get_first_usable_ip_address_from_raw_address(raw_address))
        print('Penultimate usable host IP:',
              get_penultimate_usable_ip_address_from_raw_address(raw_address))
        print('Number of usable Hosts:',
              get_number_of_usable_hosts_from_raw_address(raw_address))
        print('IP class:', get_ip_class_from_raw_address(raw_address))
        print('IP type private:',
              check_private_ip_address_from_raw_address(raw_address))
