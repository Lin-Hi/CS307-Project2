from Project2 import function, crud_staff, crud_center, crud_model, crud_enterprise

if __name__ == '__main__':
    product_number_list = ['A50L172']
    contract_number_list = ['CSE0000106', 'CSE0000209', 'CSE0000306']
    function.oneStepImport()
    f = open('my_output.txt', 'w', encoding='utf-8')
    f.write(function.oneStepExport(product_number_list, contract_number_list))
    f.close()
    function.end()
