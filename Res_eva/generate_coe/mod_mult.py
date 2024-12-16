def generate_coe_for_banks(bank_size, bit_width, file_prefix):
    """
    根据要求生成两个 COE 文件，每个文件对应一个 ROM Bank。

    :param bank_size: 每个 Bank 的大小（数据个数）
    :param bit_width: 每个数据的位宽(bit)
    :param file_prefix: 生成文件的前缀
    """
    # 确保位宽为32位
    if bit_width != 32:
        raise ValueError("Currently only 32-bit data is supported.")

    # 每个 Bank 的数据范围
    bank0_data = range(0, bank_size)
    bank1_data = range(bank_size, 2 * bank_size)

    # 准备 Bank 数据
    banks = [("bank0", bank0_data), ("bank1", bank1_data)]

    for bank_name, data in banks:
        file_name = f"{file_prefix}_{bank_name}.coe"

        # COE 文件头
        coe_header = "memory_initialization_radix=16;\n"
        coe_header += "memory_initialization_vector=\n"

        # 数据转换为 16 进制字符串
        data_strings = [f"{x:08X}" for x in data]  # 每个数据占8个字符，32位

        # 用逗号分隔数据，最后一个数据以分号结束
        coe_data = ",\n".join(data_strings) + ";"

        # 写入文件
        with open(file_name, "w") as file:
            file.write(coe_header)
            file.write(coe_data)

        print(f"COE file '{file_name}' generated successfully!")


if __name__ == "__main__":
    # 配置 ROM Bank 参数
    BANK_SIZE = 512  # 每个 Bank 包含 512 个数据
    BIT_WIDTH = 32   # 每个数据 32 位宽
    FILE_PREFIX = "rom"  # 生成文件的前缀

    # 生成两个 Bank 的 COE 文件
    generate_coe_for_banks(BANK_SIZE, BIT_WIDTH, FILE_PREFIX)
