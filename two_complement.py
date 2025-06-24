def get_input():
    positive_decimal = int(input("Enter positive decimal: "))
    bit_size = int(input("Enter bit size: "))
    return positive_decimal, bit_size

def decimal_to_binary(num, bitsize):
    binary_num = bin(num)[2:]  # remove '0b'
    return binary_num.zfill(bitsize)  # pad with zeros

def two_complement(binary_num):
    # Step 1: Flip bits
    inverted = ''.join('1' if bit == '0' else '0' for bit in binary_num)
    
    # Step 2: Add 1 manually
    result = list(inverted)
    carry = 1
    for i in range(len(result)-1, -1, -1):
        if result[i] == '1' and carry == 1:
            result[i] = '0'
        elif result[i] == '0' and carry == 1:
            result[i] = '1'
            carry = 0
            break
    if carry == 1:
        result.insert(0, '1')  # overflow for full addition
    return ''.join(result[-len(binary_num):])  # keep same bit length

def main():
    positive_decimal, bit_size = get_input()

    binary_representation = decimal_to_binary(positive_decimal, bit_size)
    negative_binary = two_complement(binary_representation)

    print(f"Input decimal number: {positive_decimal}")
    print(f"Binary representation: {binary_representation}")
    print(f"Two's complement (negative binary): {negative_binary}")

if __name__ == "__main__":
    main()
