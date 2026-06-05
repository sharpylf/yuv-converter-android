#!/usr/bin/env python3
"""
YUV RGB Converter - Python Web版本
可以在手机浏览器中直接使用！
"""

import numpy as np
from flask import Flask, render_template_string, request

app = Flask(__name__)

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
    rgb_to_yuv_matrix = np.array([
        [a1, a2, a3],
        [-a1 / (2 * (1 - a3)), -a2 / (2 * (1 - a3)), 0.5],
        [0.5, -a2 / (2 * (1 - a1)), -a3 / (2 * (1 - a1))]
    ])
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
    if (input_color_space == output_color_space and
            input_gamut == output_gamut and
            input_bit_depth == output_bit_depth and
            input_range == output_range):
        return y, cb, cr

    input_max = 2 ** input_bit_depth - 1
    output_max = 2 ** output_bit_depth - 1

    if input_color_space == output_color_space:
        if input_color_space == "RGB":
            rgb_vals = [y, cb, cr]
            rgb_vals = range_convert_rgb(rgb_vals, input_range, output_range, input_bit_depth)
            y, cb, cr = rgb_vals
        else:
            yuv_vals = [y, cb, cr]
            yuv_vals = range_convert_yuv(yuv_vals, input_range, output_range, input_bit_depth)
            y, cb, cr = yuv_vals

    if input_color_space == "RGB":
        r, g, b = y, cb, cr
        if output_color_space == "YCbCr":
            a1, a2, a3 = coeffs[output_gamut]
            y_output = a1 * r + a2 * g + a3 * b
            u_output = (-a1) / (2 * (1 - a3)) * r + (-a2) / (2 * (1 - a3)) * g + 0.5 * b + 2 ** (output_bit_depth - 1)
            v_output = 0.5 * r + (-a2) / (2 * (1 - a1)) * g + (-a3) / (2 * (1 - a1)) * b + 2 ** (output_bit_depth - 1)

            y_output = max(0, min(round(y_output), 2 ** output_bit_depth - 1))
            u_output = max(0, min(round(u_output), 2 ** output_bit_depth - 1))
            v_output = max(0, min(round(v_output), 2 ** output_bit_depth - 1))

            yuv_vals = [y_output, u_output, v_output]
            if output_range != input_range:
                yuv_vals = range_convert_yuv(yuv_vals, "Full Range", output_range, output_bit_depth)
            y_output, u_output, v_output = yuv_vals
            return y_output, u_output, v_output
        elif output_color_space == "RGB" and input_gamut != output_gamut:
            a1, a2, a3 = coeffs[input_gamut]
            y_temp = a1 * r + a2 * g + a3 * b
            u_temp = (-a1) / (2 * (1 - a3)) * r + (-a2) / (2 * (1 - a3)) * g + 0.5 * b + 2 ** (output_bit_depth - 1)
            v_temp = 0.5 * r + (-a2) / (2 * (1 - a1)) * g + (-a3) / (2 * (1 - a1)) * b + 2 ** (output_bit_depth - 1)

            yuv_r1, yuv_r2, yuv_r3, yuv_g1, yuv_g2, yuv_g3, yuv_b1, yuv_b2, yuv_b3 = yuv_to_rgb_coeffs[output_gamut]
            offset = 0
            r = yuv_r1 * (y_temp - offset) + yuv_r2 * (u_temp - 2 ** (output_bit_depth - 1)) + yuv_r3 * (v_temp - 2 ** (output_bit_depth - 1))
            g = yuv_g1 * (y_temp - offset) + yuv_g2 * (u_temp - 2 ** (output_bit_depth - 1)) + yuv_g3 * (v_temp - 2 ** (output_bit_depth - 1))
            b = yuv_b1 * (y_temp - offset) + yuv_b2 * (u_temp - 2 ** (output_bit_depth - 1)) + yuv_b3 * (v_temp - 2 ** (output_bit_depth - 1))

            r = max(0, min(round(r), 2 ** output_bit_depth - 1))
            g = max(0, min(round(g), 2 ** output_bit_depth - 1))
            b = max(0, min(round(b), 2 ** output_bit_depth - 1))

            return r, g, b
    else:
        input_y_min, input_y_max, input_uv_min, input_uv_max = get_range_params(input_range, input_bit_depth)
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

        r = max(0, min(round(r), 2 ** output_bit_depth - 1))
        g = max(0, min(round(g), 2 ** output_bit_depth - 1))
        b = max(0, min(round(b), 2 ** output_bit_depth - 1))

        if output_color_space == "RGB":
            if output_range != input_range:
                rgb_vals = [r, g, b]
                rgb_vals = range_convert_rgb(rgb_vals, "Full Range", output_range, output_bit_depth)
                r, g, b = rgb_vals
            return r, g, b
        elif output_color_space == "YCbCr":
            a1, a2, a3 = coeffs[output_gamut]
            y_output = a1 * r + a2 * g + a3 * b
            u_output = (-a1) / (2 * (1 - a3)) * r + (-a2) / (2 * (1 - a3)) * g + 0.5 * b + 2 ** (output_bit_depth - 1)
            v_output = 0.5 * r + (-a2) / (2 * (1 - a1)) * g + (-a3) / (2 * (1 - a1)) * b + 2 ** (output_bit_depth - 1)

            y_output = max(0, min(round(y_output), 2 ** output_bit_depth - 1))
            u_output = max(0, min(round(u_output), 2 ** output_bit_depth - 1))
            v_output = max(0, min(round(v_output), 2 ** output_bit_depth - 1))

            yuv_vals = [y_output, u_output, v_output]
            if output_range != input_range:
                yuv_vals = range_convert_yuv(yuv_vals, "Full Range", output_range, output_bit_depth)
            y_output, u_output, v_output = yuv_vals
            return y_output, u_output, v_output

    return y, cb, cr


HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>YUV RGB Converter</title>
    <style>
        * {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
        }
        body {
            font-family: Arial, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }
        .container {
            max-width: 600px;
            margin: 0 auto;
            background: white;
            border-radius: 20px;
            padding: 30px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
        }
        h1 {
            text-align: center;
            color: #333;
            margin-bottom: 30px;
            font-size: 28px;
        }
        .section {
            margin-bottom: 25px;
            padding: 20px;
            background: #f8f9fa;
            border-radius: 10px;
        }
        .section-title {
            font-weight: bold;
            margin-bottom: 15px;
            color: #495057;
            font-size: 18px;
        }
        .form-group {
            margin-bottom: 15px;
        }
        label {
            display: block;
            margin-bottom: 5px;
            color: #495057;
            font-weight: 500;
        }
        select, input {
            width: 100%;
            padding: 12px;
            border: 2px solid #e9ecef;
            border-radius: 8px;
            font-size: 16px;
            transition: border-color 0.3s;
        }
        select:focus, input:focus {
            outline: none;
            border-color: #667eea;
        }
        button {
            width: 100%;
            padding: 15px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            border-radius: 10px;
            font-size: 18px;
            font-weight: bold;
            cursor: pointer;
            transition: transform 0.2s;
        }
        button:hover {
            transform: translateY(-2px);
        }
        button:active {
            transform: translateY(0);
        }
        .result {
            background: #e8f4f8;
            padding: 20px;
            border-radius: 10px;
            margin-top: 20px;
        }
        .result-item {
            margin: 10px 0;
            font-size: 16px;
            color: #2c3e50;
        }
        .color-preview {
            width: 100%;
            height: 100px;
            border-radius: 10px;
            margin-top: 15px;
            border: 3px solid #dee2e6;
        }
        .footer {
            text-align: center;
            margin-top: 20px;
            color: #6c757d;
            font-size: 14px;
        }
        .error {
            background: #f8d7da;
            color: #721c24;
            padding: 15px;
            border-radius: 8px;
            margin-top: 15px;
            border: 1px solid #f5c6cb;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🎨 YUV RGB 转换工具</h1>
        
        <div class="section">
            <div class="section-title">输入设置</div>
            <div class="form-group">
                <label>颜色空间:</label>
                <select name="input_color_space">
                    <option value="RGB">RGB</option>
                    <option value="YCbCr">YCbCr</option>
                </select>
            </div>
            <div class="form-group">
                <label>选择色域:</label>
                <select name="input_gamut">
                    <option value="BT601">BT601</option>
                    <option value="BT709" selected>BT709</option>
                    <option value="BT2020">BT2020</option>
                    <option value="DCI - P3">DCI - P3</option>
                </select>
            </div>
            <div class="form-group">
                <label>选择范围:</label>
                <select name="input_range">
                    <option value="Full Range" selected>Full Range</option>
                    <option value="Limited Range">Limited Range</option>
                </select>
            </div>
            <div class="form-group">
                <label>选择色深:</label>
                <select name="input_bit_depth">
                    <option value="8" selected>8bit</option>
                    <option value="10">10bit</option>
                    <option value="12">12bit</option>
                </select>
            </div>
        </div>

        <div class="section">
            <div class="section-title">输入数据</div>
            <div class="form-group">
                <label>Y (R) 值:</label>
                <input type="number" name="y_input" placeholder="0-255 (8bit)">
            </div>
            <div class="form-group">
                <label>Cb (G) 值:</label>
                <input type="number" name="cb_input" placeholder="0-255 (8bit)">
            </div>
            <div class="form-group">
                <label>Cr (B) 值:</label>
                <input type="number" name="cr_input" placeholder="0-255 (8bit)">
            </div>
        </div>

        <div class="section">
            <div class="section-title">输出设置</div>
            <div class="form-group">
                <label>颜色空间:</label>
                <select name="output_color_space">
                    <option value="RGB">RGB</option>
                    <option value="YCbCr" selected>YCbCr</option>
                </select>
            </div>
            <div class="form-group">
                <label>选择色域:</label>
                <select name="output_gamut">
                    <option value="BT601">BT601</option>
                    <option value="BT709" selected>BT709</option>
                    <option value="BT2020">BT2020</option>
                    <option value="DCI - P3">DCI - P3</option>
                </select>
            </div>
            <div class="form-group">
                <label>选择范围:</label>
                <select name="output_range">
                    <option value="Full Range" selected>Full Range</option>
                    <option value="Limited Range">Limited Range</option>
                </select>
            </div>
        </div>

        <button type="submit">🔄 转换</button>

        {% if error %}
        <div class="error">
            {{ error }}
        </div>
        {% endif %}

        {% if result %}
        <div class="result">
            <div class="section-title">输出结果</div>
            <div class="result-item">Y (R): <strong>{{ result[0] }}</strong></div>
            <div class="result-item">Cb (G): <strong>{{ result[1] }}</strong></div>
            <div class="result-item">Cr (B): <strong>{{ result[2] }}</strong></div>
            <div class="color-preview" style="background-color: {{ color }};"></div>
        </div>
        {% endif %}

        <div class="footer">
            FPGA平台 - Rev2.0
        </div>
    </div>
</body>
</html>
"""


@app.route('/', methods=['GET', 'POST'])
def index():
    result = None
    error = None
    color = '#FFFFFF'

    if request.method == 'POST':
        try:
            input_color_space = request.form.get('input_color_space', 'RGB')
            input_gamut = request.form.get('input_gamut', 'BT709')
            input_range = request.form.get('input_range', 'Full Range')
            input_bit_depth = int(request.form.get('input_bit_depth', '8'))

            output_color_space = request.form.get('output_color_space', 'YCbCr')
            output_gamut = request.form.get('output_gamut', 'BT709')
            output_range = request.form.get('output_range', 'Full Range')
            output_bit_depth = input_bit_depth

            y = int(request.form.get('y_input', 0))
            cb = int(request.form.get('cb_input', 0))
            cr = int(request.form.get('cr_input', 0))

            # 基本验证
            max_val = 2 ** input_bit_depth - 1
            if not (0 <= y <= max_val and 0 <= cb <= max_val and 0 <= cr <= max_val):
                error = f"输入值应在 0 - {max_val} 范围内"
            else:
                result_y, result_cb, result_cr = convert(
                    input_color_space, input_gamut, input_bit_depth, input_range,
                    output_color_space, output_gamut, output_bit_depth, output_range,
                    y, cb, cr
                )

                result = [result_y, result_cb, result_cr]

                # 计算颜色预览
                if output_color_space == "YCbCr":
                    output_y_min, output_y_max, output_uv_min, output_uv_max = get_range_params(output_range, output_bit_depth)
                    y_scaled = (result_y - output_y_min) / (output_y_max - output_y_min) * (2 ** output_bit_depth - 1)
                    cb_scaled = (result_cb - output_uv_min) / (output_uv_max - output_uv_min) * (2 ** output_bit_depth - 1)
                    cr_scaled = (result_cr - output_uv_min) / (output_uv_max - output_uv_min) * (2 ** output_bit_depth - 1)

                    yuv_r1, yuv_r2, yuv_r3, yuv_g1, yuv_g2, yuv_g3, yuv_b1, yuv_b2, yuv_b3 = yuv_to_rgb_coeffs[output_gamut]
                    offset = 2 ** (output_bit_depth - 1)
                    r = yuv_r1 * (y_scaled) + yuv_r2 * (cb_scaled - offset) + yuv_r3 * (cr_scaled - offset)
                    g = yuv_g1 * (y_scaled) + yuv_g2 * (cb_scaled - offset) + yuv_g3 * (cr_scaled - offset)
                    b = yuv_b1 * (y_scaled) + yuv_b2 * (cb_scaled - offset) + yuv_b3 * (cr_scaled - offset)
                else:
                    r, g, b = result_y, result_cb, result_cr

                r = max(0, min(round(r), 2 ** output_bit_depth - 1))
                g = max(0, min(round(g), 2 ** output_bit_depth - 1))
                b = max(0, min(round(b), 2 ** output_bit_depth - 1))

                max_color = 2 ** output_bit_depth - 1
                r_8bit = int(r / max_color * 255)
                g_8bit = int(g / max_color * 255)
                b_8bit = int(b / max_color * 255)

                color = f'#{r_8bit:02x}{g_8bit:02x}{b_8bit:02x}'

        except Exception as e:
            error = f"错误: {str(e)}"

    return render_template_string(HTML_TEMPLATE, result=result, error=error, color=color)


if __name__ == '__main__':
    print("🚀 YUV RGB Converter Web Server 启动中...")
    print("📱 在手机上打开: http://你的电脑IP:5000")
    print("💻 在电脑上打开: http://localhost:5000")
    print()
    
    import socket
    hostname = socket.gethostname()
    local_ip = socket.gethostbyname(hostname)
    print(f"🌐 你的电脑IP: {local_ip}")
    print()
    print("按 Ctrl+C 停止服务器")
    
    app.run(host='0.0.0.0', port=5000, debug=False)