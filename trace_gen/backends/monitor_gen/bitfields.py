# from m2isar.backends.etiss.instruction_generator import common_function

# def main(tracemodel):
#     bitfields_code = ""
#     for instr_i in tracemodel.getAllInstructions():
#         for bf_i in instr_i.getAllBitfields():
#             bitfields_code += f'int {bf_i.name} = 0;'
#             for br_i in bf_i.getAllBitRanges():
#                 bitfields_code += common_function(bf_i.name, br_i.msb, br_i.lsb, br_i.offset)
#     return bitfields_code
