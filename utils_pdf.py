


def coordinate_transfer(input_cors: list or tuple) -> list or tuple:
    """
    基于 300 dpi的坐标转换

    At first, transfer pdf file to images :

            from pdf2image import convert_from_path
            convert_from_path(file_in, 300, file_out, fmt="png", output_file='image', last_page=20, thread_count=4)

    Secondary, extract raw chars with coordinates :

            import pdfplumber
            file_name = '4126600.pdf'
            pdf = pdfplumber.open(file_name)
            sheet = pdf.pages[0]
            chars = sheet.chars
        in chars, x0 is left border and x1 is right border with axis from left to right, y0 is top border and y1 is bottom border, but
        y axis starts from bottom to top(numpy array stars from top to bottom)

    Thirdly, deliver the four coordinates into this function in order [x0, x1, y0, y1] you can get the relative coordinates in 300 dpi png image
            newx0, newx1, newy0, newy1 = coordinate_transfer([x0, x1, y0, y1])


    :param input_cors:
    :return:
    """

    x0_rate = 4.1
    x1_rate = 4.2
    y0_rate = 4.15
    y1_rate = 4.18
    cv_width_x = 2481
    cv_height_y = 3508

    cv_x0, cv_x1, cv_y0, cv_y1 = input_cors
    return [cv_x0 * x0_rate, cv_x1 * x1_rate, cv_height_y - cv_y1 * y1_rate, cv_height_y - cv_y0 * y0_rate]


print(coordinate_transfer([193.370, 229.370, 678.802, 696.80]))