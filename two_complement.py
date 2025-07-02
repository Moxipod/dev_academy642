def get_input():
    positive_decimal = int(input("Enter positive decimal: "))
    bit_size = int(input("Enter bit size: "))
    return positive_decimal, bit_size

def decimal_to_binary(num, bitsize):
    binary_num = bin(num)[2:]  # remove '0b'
    return binary_num.zfill(bitsize)  # pad with zeros

def two_complement(binary_num,bitsize):
    # Step 1: Flip bits
    #inverted = ''.join('1' if bit == '0' else '0' for bit in binary_num)
    flipped = ''.join('1' if bit == '0' else '0' for bit in binary_num)
    complement_int = int(flipped, 2) + 1
    return decimal_to_binary(complement_int,bitsize)

def main():
    positive_decimal, bit_size = get_input()

    binary_representation = decimal_to_binary(positive_decimal, bit_size)
    negative_binary = two_complement(binary_representation,bit_size)

    print(f"Input decimal number: {positive_decimal}")
    print(f"Binary representation: {binary_representation}")
    print(f"Two's complement (negative binary): {negative_binary}")

if __name__ == "__main__":
    main()
