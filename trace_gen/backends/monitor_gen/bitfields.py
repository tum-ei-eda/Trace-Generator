from m2isar.backends.etiss.fields_code import FieldsCode
# TODO: get width and data type from m2isar

def main(tracemodel):
    fields_code = ""
    for instr_i in tracemodel.getAllInstructions():
        # fields_code += f'{instr_i.name}\n'
        for bf_i in instr_i.getAllBitfields():
            fc = FieldsCode(bf_i.name, bf_i.getDataType())
            for br_i in bf_i.getAllBitRanges():
                fc.addFieldsCode(br_i.offset, br_i.msb, br_i.lsb)
                fields_code += fc.getFieldsCode()
    return fields_code
