import kivy
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.spinner import Spinner
from kivy.uix.widget import Widget
from kivy.graphics import Color, Rectangle
from kivy.core.window import Window
import numpy as np

kivy.require('2.3.1')

# 全局定义色域系数
coeffs = {
    "BT601": [0.299, 0.587, 0.114],
    "BT709": [0.2126, 0.7152, 0.0722],
    "BT2020": [0.2627, 0.6780, 0.0593],
    "DCI - P3": [0.22897, 0.69174, 0.07929]
}

# 重新计算 YUV 转 RGB 系数
yuv_to_rgb_coeffs = {}
for gamut, (a1, a2, a3) in coeffs.items():
    # RGB 转 YUV 矩阵
    rgb_to_yuv_matrix = np.array([
        [a1, a2, a3],
        [-a1 / (2 * (1 - a3)), -a2 / (2 * (1 - a3)), 0.5],
        [0.5, -a2 / (2 * (1 - a1)), -a3 / (2 * (1 - a1))]
    ])
    # 求逆矩阵
    yuv_to_rgb_matrix = np.linalg.inv(rgb_to_yuv_matrix)
    yuv_to_rgb_coeffs[gamut] = yuv_to_rgb_matrix.flatten().tolist()


def range_convert_rgb(input_val, input_range, output_range, bit_depth):
    input_max = 2 ** bit_depth - 1
    if input_range == "Full Range" and output_range == "Limited Range":
        if bit_depth == 8:
            return [round((219 / 255) * val + 16) for val in input_val]
        elif bit_depth == 10:
            return [round((940 / 1023) * val + 64) for val in input_val]
        elif bit_depth == 12:
            return [round((3760 / 4095) * val + 256) for val in input_val]
    elif input_range == "Limited Range" and output_range == "Full Range":
        if bit_depth == 8:
            return [round((255 / 219) * (val - 16)) for val in input_val]
        elif bit_depth == 10:
            return [round((1023 / 940) * (val - 64)) for val in input_val]
        elif bit_depth == 12:
            return [round((4095 / 3760) * (val - 256)) for val in input_val]
    return input_val


def range_convert_yuv(input_val, input_range, output_range, bit_depth):
    input_max = 2 ** bit_depth - 1
    if input_range == "Full Range" and output_range == "Limited Range":
        if bit_depth == 8:
            y = round((219 / 255) * input_val[0] + 16)
            uv = [round((224 / 255) * val + 16) for val in input_val[1:]]
            return [y] + uv
        elif bit_depth == 10:
            y = round((940 / 1023) * input_val[0] + 64)
            uv = [round((960 / 1023) * val + 64) for val in input_val[1:]]
            return [y] + uv
        elif bit_depth == 12:
            y = round((3760 / 4095) * input_val[0] + 256)
            uv = [round((3840 / 4095) * val + 256) for val in input_val[1:]]
            return [y] + uv
    elif input_range == "Limited Range" and output_range == "Full Range":
        if bit_depth == 8:
            y = round((255 / 219) * (input_val[0] - 16))
            uv = [round((255 / 224) * (val - 16)) for val in input_val[1:]]
            return [y] + uv
        elif bit_depth == 10:
            y = round((1023 / 940) * (input_val[0] - 64))
            uv = [round((1023 / 960) * (val - 64)) for val in input_val[1:]]
            return [y] + uv
        elif bit_depth == 12:
            y = round((4095 / 3760) * (input_val[0] - 256))
            uv = [round((4095 / 3840) * (val - 256)) for val in input_val[1:]]
            return [y] + uv
    return input_val


def get_range_params(range_type, bit_depth):
    full = {8: (0, 255), 10: (0, 1023), 12: (0, 4095)}
    limited = {8: (16, 235, 16, 240), 10: (64, 940, 64, 960), 12: (256, 3760, 256, 3840)}
    if range_type == "Full Range":
        y_min, y_max = full[bit_depth]
        return y_min, y_max, y_min, y_max
    else:
        return limited[bit_depth]


def convert(input_color_space, input_gamut, input_bit_depth, input_range,
            output_color_space, output_gamut, output_bit_depth, output_range, y, cb, cr):
    # 输入输出设置相同，直接返回输入值
    if (input_color_space == output_color_space and
            input_gamut == output_gamut and
            input_bit_depth == output_bit_depth and
            input_range == output_range):
        return y, cb, cr

    input_max = 2 ** input_bit_depth - 1
    output_max = 2 ** output_bit_depth - 1

    # 处理输入范围转换（若颜色空间不变，先处理范围转换）
    if input_color_space == output_color_space:
        if input_color_space == "RGB":
            rgb_vals = [y, cb, cr]
            rgb_vals = range_convert_rgb(rgb_vals, input_range, output_range, input_bit_depth)
            y, cb, cr = rgb_vals
        else:
            yuv_vals = [y, cb, cr]
            yuv_vals = range_convert_yuv(yuv_vals, input_range, output_range, input_bit_depth)
            y, cb, cr = yuv_vals

    # 颜色空间转换
    if input_color_space == "RGB":
        r, g, b = y, cb, cr
        if output_color_space == "YCbCr":
            a1, a2, a3 = coeffs[output_gamut]
            y_output = a1 * r + a2 * g + a3 * b
            u_output = (-a1) / (2 * (1 - a3)) * r + (-a2) / (2 * (1 - a3)) * g + 0.5 * b + 2 ** (output_bit_depth - 1)
            v_output = 0.5 * r + (-a2) / (2 * (1 - a1)) * g + (-a3) / (2 * (1 - a1)) * b + 2 ** (output_bit_depth - 1)

            # 四舍五入并限制范围
            y_output = max(0, min(round(y_output), 2 ** output_bit_depth - 1))
            u_output = max(0, min(round(u_output), 2 ** output_bit_depth - 1))
            v_output = max(0, min(round(v_output), 2 ** output_bit_depth - 1))

            yuv_vals = [y_output, u_output, v_output]
            # 处理输出范围转换
            if output_range != input_range:
                yuv_vals = range_convert_yuv(yuv_vals, "Full Range", output_range, output_bit_depth)
            y_output, u_output, v_output = yuv_vals
            return y_output, u_output, v_output
        elif output_color_space == "RGB" and input_gamut != output_gamut:
            # 先将输入 RGB 转换为 YCbCr（使用输入色域）
            a1, a2, a3 = coeffs[input_gamut]
            y_temp = a1 * r + a2 * g + a3 * b
            u_temp = (-a1) / (2 * (1 - a3)) * r + (-a2) / (2 * (1 - a3)) * g + 0.5 * b + 2 ** (output_bit_depth - 1)
            v_temp = 0.5 * r + (-a2) / (2 * (1 - a1)) * g + (-a3) / (2 * (1 - a1)) * b + 2 ** (output_bit_depth - 1)

            # 再将 YCbCr 转换为输出 RGB（使用输出色域）
            yuv_r1, yuv_r2, yuv_r3, yuv_g1, yuv_g2, yuv_g3, yuv_b1, yuv_b2, yuv_b3 = yuv_to_rgb_coeffs[output_gamut]
            offset = 0
            r = yuv_r1 * (y_temp - offset) + yuv_r2 * (u_temp - 2 ** (output_bit_depth - 1)) + yuv_r3 * (v_temp - 2 ** (output_bit_depth - 1))
            g = yuv_g1 * (y_temp - offset) + yuv_g2 * (u_temp - 2 ** (output_bit_depth - 1)) + yuv_g3 * (v_temp - 2 ** (output_bit_depth - 1))
            b = yuv_b1 * (y_temp - offset) + yuv_b2 * (u_temp - 2 ** (output_bit_depth - 1)) + yuv_b3 * (v_temp - 2 ** (output_bit_depth - 1))

            # 四舍五入并限制范围
            r = max(0, min(round(r), 2 ** output_bit_depth - 1))
            g = max(0, min(round(g), 2 ** output_bit_depth - 1))
            b = max(0, min(round(b), 2 ** output_bit_depth - 1))

            return r, g, b
    else:  # YCbCr 转 RGB
        input_y_min, input_y_max, input_uv_min, input_uv_max = get_range_params(input_range, input_bit_depth)
        # 处理输入值在 Limited Range 的偏移
        y = max(input_y_min, min(y, input_y_max))
        cb = max(input_uv_min, min(cb, input_uv_max))
        cr = max(input_uv_min, min(cr, input_uv_max))

        y_scaled = y
        cb_scaled = cb - input_uv_min
        cr_scaled = cr - input_uv_min

        yuv_r1, yuv_r2, yuv_r3, yuv_g1, yuv_g2, yuv_g3, yuv_b1, yuv_b2, yuv_b3 = yuv_to_rgb_coeffs[input_gamut]
        offset = input_y_min if input_range == "Limited Range" else 0
        r = yuv_r1 * (y_scaled - offset) + yuv_r2 * (cb_scaled - (input_uv_max - input_uv_min) // 2) + yuv_r3 * (cr_scaled - (input_uv_max - input_uv_min) // 2)
        g = yuv_g1 * (y_scaled - offset) + yuv_g2 * (cb_scaled - (input_uv_max - input_uv_min) // 2) + yuv_g3 * (cr_scaled - (input_uv_max - input_uv_min) // 2)
        b = yuv_b1 * (y_scaled - offset) + yuv_b2 * (cb_scaled - (input_uv_max - input_uv_min) // 2) + yuv_b3 * (cr_scaled - (input_uv_max - input_uv_min) // 2)

        # 四舍五入并限制范围
        r = max(0, min(round(r), 2 ** output_bit_depth - 1))
        g = max(0, min(round(g), 2 ** output_bit_depth - 1))
        b = max(0, min(round(b), 2 ** output_bit_depth - 1))

        if output_color_space == "RGB":
            # 处理输出范围转换
            if output_range != input_range:
                rgb_vals = [r, g, b]
                rgb_vals = range_convert_rgb(rgb_vals, "Full Range", output_range, output_bit_depth)
                r, g, b = rgb_vals
            return r, g, b
        elif output_color_space == "YCbCr":
            # 从 RGB 转换到目标色域的 YCbCr
            a1, a2, a3 = coeffs[output_gamut]
            y_output = a1 * r + a2 * g + a3 * b
            u_output = (-a1) / (2 * (1 - a3)) * r + (-a2) / (2 * (1 - a3)) * g + 0.5 * b + 2 ** (output_bit_depth - 1)
            v_output = 0.5 * r + (-a2) / (2 * (1 - a1)) * g + (-a3) / (2 * (1 - a1)) * b + 2 ** (output_bit_depth - 1)

            # 四舍五入并限制范围
            y_output = max(0, min(round(y_output), 2 ** output_bit_depth - 1))
            u_output = max(0, min(round(u_output), 2 ** output_bit_depth - 1))
            v_output = max(0, min(round(v_output), 2 ** output_bit_depth - 1))

            yuv_vals = [y_output, u_output, v_output]
            # 处理输出范围转换
            if output_range != input_range:
                yuv_vals = range_convert_yuv(yuv_vals, "Full Range", output_range, output_bit_depth)
            y_output, u_output, v_output = yuv_vals
            return y_output, u_output, v_output

    return y, cb, cr  # 兜底返回


class ColorPreview(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.size_hint = (1, None)
        self.height = 150
        with self.canvas:
            self.color = Color(1, 1, 1)
            self.rect = Rectangle(pos=self.pos, size=self.size)
        self.bind(pos=self.update_rect, size=self.update_rect)

    def update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size

    def set_color(self, r, g, b, bit_depth):
        # 根据位深归一化到0-1范围
        max_val = 2 ** bit_depth - 1
        self.color.rgba = (r / max_val, g / max_val, b / max_val, 1)


class YUVConverterApp(App):
    def build(self):
        Window.size = (500, 750)
        Window.title = "YUV与RGB转换工具"

        main_layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        # 输入设置区域
        input_frame = BoxLayout(orientation='vertical', size_hint_y=None, height=180)
        input_frame.add_widget(Label(text='输入设置', font_size=18, bold=True, size_hint_y=None, height=30))

        input_grid = GridLayout(cols=2, spacing=5, size_hint_y=None, height=150)
        input_grid.add_widget(Label(text='颜色空间:'))
        self.input_color_space = Spinner(text='RGB', values=['RGB', 'YCbCr'], size_hint_y=None, height=40)
        input_grid.add_widget(self.input_color_space)

        input_grid.add_widget(Label(text='选择色域:'))
        self.input_gamut = Spinner(text='BT709', values=['BT601', 'BT709', 'BT2020', 'DCI - P3'], size_hint_y=None, height=40)
        input_grid.add_widget(self.input_gamut)

        input_grid.add_widget(Label(text='选择范围:'))
        self.input_range = Spinner(text='Full Range', values=['Full Range', 'Limited Range'], size_hint_y=None, height=40)
        input_grid.add_widget(self.input_range)

        input_grid.add_widget(Label(text='选择色深:'))
        self.input_bit_depth = Spinner(text='8', values=['8', '10', '12'], size_hint_y=None, height=40)
        input_grid.add_widget(self.input_bit_depth)

        input_frame.add_widget(input_grid)
        main_layout.add_widget(input_frame)

        # 输出设置区域
        output_frame = BoxLayout(orientation='vertical', size_hint_y=None, height=180)
        output_frame.add_widget(Label(text='输出设置', font_size=18, bold=True, size_hint_y=None, height=30))

        output_grid = GridLayout(cols=2, spacing=5, size_hint_y=None, height=150)
        output_grid.add_widget(Label(text='颜色空间:'))
        self.output_color_space = Spinner(text='YCbCr', values=['RGB', 'YCbCr'], size_hint_y=None, height=40)
        output_grid.add_widget(self.output_color_space)

        output_grid.add_widget(Label(text='选择色域:'))
        self.output_gamut = Spinner(text='BT709', values=['BT601', 'BT709', 'BT2020', 'DCI - P3'], size_hint_y=None, height=40)
        output_grid.add_widget(self.output_gamut)

        output_grid.add_widget(Label(text='选择范围:'))
        self.output_range = Spinner(text='Full Range', values=['Full Range', 'Limited Range'], size_hint_y=None, height=40)
        output_grid.add_widget(self.output_range)

        output_frame.add_widget(output_grid)
        main_layout.add_widget(output_frame)

        # 输入数据区域
        data_frame = BoxLayout(orientation='vertical', size_hint_y=None, height=180)
        data_frame.add_widget(Label(text='输入数据 (Y/R, Cb/G, Cr/B)', font_size=16, bold=True, size_hint_y=None, height=30))

        data_grid = GridLayout(cols=2, spacing=5, size_hint_y=None, height=150)
        data_grid.add_widget(Label(text='Y (R) 值:'))
        self.y_input = TextInput(multiline=False, size_hint_y=None, height=40)
        data_grid.add_widget(self.y_input)

        data_grid.add_widget(Label(text='Cb (G) 值:'))
        self.cb_input = TextInput(multiline=False, size_hint_y=None, height=40)
        data_grid.add_widget(self.cb_input)

        data_grid.add_widget(Label(text='Cr (B) 值:'))
        self.cr_input = TextInput(multiline=False, size_hint_y=None, height=40)
        data_grid.add_widget(self.cr_input)

        data_frame.add_widget(data_grid)
        main_layout.add_widget(data_frame)

        # 转换按钮
        convert_btn = Button(text='转换', size_hint_y=None, height=50, font_size=18)
        convert_btn.bind(on_press=self.convert_data)
        main_layout.add_widget(convert_btn)

        # 输出结果区域
        output_data_frame = BoxLayout(orientation='vertical', size_hint_y=None, height=180)
        output_data_frame.add_widget(Label(text='输出结果', font_size=16, bold=True, size_hint_y=None, height=30))

        output_data_grid = GridLayout(cols=2, spacing=5, size_hint_y=None, height=150)
        output_data_grid.add_widget(Label(text='Y (R) 输出:'))
        self.y_output = TextInput(multiline=False, size_hint_y=None, height=40, readonly=True)
        output_data_grid.add_widget(self.y_output)

        output_data_grid.add_widget(Label(text='Cb (G) 输出:'))
        self.cb_output = TextInput(multiline=False, size_hint_y=None, height=40, readonly=True)
        output_data_grid.add_widget(self.cb_output)

        output_data_grid.add_widget(Label(text='Cr (B) 输出:'))
        self.cr_output = TextInput(multiline=False, size_hint_y=None, height=40, readonly=True)
        output_data_grid.add_widget(self.cr_output)

        output_data_frame.add_widget(output_data_grid)
        main_layout.add_widget(output_data_frame)

        # 颜色预览
        main_layout.add_widget(Label(text='颜色预览', font_size=16, bold=True))
        self.color_preview = ColorPreview()
        main_layout.add_widget(self.color_preview)

        # 版权信息
        footer = BoxLayout(size_hint_y=None, height=40)
        footer.add_widget(Label(text='FPGA平台', size_hint_x=0.8))
        footer.add_widget(Label(text='Rev2.0', size_hint_x=0.2))
        main_layout.add_widget(footer)

        return main_layout

    def convert_data(self, instance):
        try:
            # 输入设置
            input_color_space = self.input_color_space.text
            input_gamut = self.input_gamut.text
            input_bit_depth = int(self.input_bit_depth.text)
            input_range = self.input_range.text

            # 输出设置
            output_color_space = self.output_color_space.text
            output_gamut = self.output_gamut.text
            output_bit_depth = input_bit_depth
            output_range = self.output_range.text

            y_str = self.y_input.text.strip()
            cb_str = self.cb_input.text.strip()
            cr_str = self.cr_input.text.strip()

            # 验证输入是否为有效整数
            if not (y_str.isdigit() and cb_str.isdigit() and cr_str.isdigit()):
                self.show_error("请输入有效的十进制整数")
                return

            y = int(y_str)
            cb = int(cb_str)
            cr = int(cr_str)

            input_max = 2 ** input_bit_depth - 1

            # 输入范围验证
            if input_color_space == "RGB":
                if input_range == "Limited Range":
                    if input_bit_depth == 8:
                        if not (0 <= y <= 235 and 0 <= cb <= 235 and 0 <= cr <= 235):
                            self.show_error("RGB Limited Range 8bit 时，输入值最大为 235")
                            return
                    elif input_bit_depth == 10:
                        if not (64 <= y <= 940 and 64 <= cb <= 940 and 64 <= cr <= 940):
                            self.show_error("RGB Limited Range 10bit 时，输入值最大为 940")
                            return
                    elif input_bit_depth == 12:
                        if not (256 <= y <= 3760 and 256 <= cb <= 3760 and 256 <= cr <= 3760):
                            self.show_error("RGB Limited Range 12bit 时，输入值最大为 3760")
                            return
            else:  # YCbCr
                if input_range == "Limited Range":
                    if input_bit_depth == 8:
                        if not (16 <= y <= 235 and 16 <= cb <= 240 and 16 <= cr <= 240):
                            self.show_error("YUV Limited Range 8bit 时，Y 范围 16 - 235，U/V 范围 16 - 240")
                            return
                    elif input_bit_depth == 10:
                        if not (64 <= y <= 940 and 64 <= cb <= 960 and 64 <= cr <= 960):
                            self.show_error("YUV Limited Range 10bit 时，Y 范围 64 - 940，U/V 范围 64 - 960")
                            return
                    elif input_bit_depth == 12:
                        if not (256 <= y <= 3760 and 256 <= cb <= 3840 and 256 <= cr <= 3840):
                            self.show_error("YUV Limited Range 12bit 时，Y 范围 256 - 3760，U/V 范围 256 - 3840")
                            return

            # 验证输入值是否在位深范围内
            if not (0 <= y <= input_max and 0 <= cb <= input_max and 0 <= cr <= input_max):
                self.show_error(f"输入值应在 0 - {input_max} 范围内（当前输入色深: {input_bit_depth}bit）")
                return

            result_y, result_cb, result_cr = convert(
                input_color_space, input_gamut, input_bit_depth, input_range,
                output_color_space, output_gamut, output_bit_depth, output_range,
                y, cb, cr
            )

            self.y_output.text = str(result_y)
            self.cb_output.text = str(result_cb)
            self.cr_output.text = str(result_cr)

            # 更新颜色预览
            if output_color_space == "YCbCr":
                # 获取输出范围参数
                output_y_min, output_y_max, output_uv_min, output_uv_max = get_range_params(output_range, output_bit_depth)
                # 先将 YUV 转换到全范围
                y_scaled = (result_y - output_y_min) / (output_y_max - output_y_min) * (2 ** output_bit_depth - 1)
                cb_scaled = (result_cb - output_uv_min) / (output_uv_max - output_uv_min) * (2 ** output_bit_depth - 1)
                cr_scaled = (result_cr - output_uv_min) / (output_uv_max - output_uv_min) * (2 ** output_bit_depth - 1)

                # 使用正确的色域进行转换
                yuv_r1, yuv_r2, yuv_r3, yuv_g1, yuv_g2, yuv_g3, yuv_b1, yuv_b2, yuv_b3 = yuv_to_rgb_coeffs[output_gamut]
                offset = 2 ** (output_bit_depth - 1)
                r = yuv_r1 * (y_scaled) + yuv_r2 * (cb_scaled - offset) + yuv_r3 * (cr_scaled - offset)
                g = yuv_g1 * (y_scaled) + yuv_g2 * (cb_scaled - offset) + yuv_g3 * (cr_scaled - offset)
                b = yuv_b1 * (y_scaled) + yuv_b2 * (cb_scaled - offset) + yuv_b3 * (cr_scaled - offset)
            else:
                r, g, b = result_y, result_cb, result_cr

            # 确保 r, g, b 值在对应位深范围内
            r = max(0, min(round(r), 2 ** output_bit_depth - 1))
            g = max(0, min(round(g), 2 ** output_bit_depth - 1))
            b = max(0, min(round(b), 2 ** output_bit_depth - 1))

            self.color_preview.set_color(r, g, b, output_bit_depth)

        except Exception as e:
            self.show_error(f"发生未知错误: {str(e)}")

    def show_error(self, message):
        popup = Popup(title='错误',
                     content=Label(text=message),
                     size_hint=(0.8, 0.4))
        popup.open()


if __name__ == '__main__':
    YUVConverterApp().run()