from flask import Flask, request, jsonify
import subprocess
import os

app = Flask(__name__)

@app.route('/check-code', methods=['POST'])
def check_code():
    data = request.json or {}
    user_code = data.get('code', '')

    file_path = 'temp_code.dart'
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(user_code)

    try:
        # تشغيل أداة التحليل الخاصة بـ Dart
        result = subprocess.run(['dart', 'analyze', file_path], capture_output=True, text=True, timeout=10)
        output = result.stdout + result.stderr
    except Exception as e:
        output = f"خطأ في السيرفر: {str(e)}"

    if os.path.exists(file_path):
        os.remove(file_path)

    return jsonify({'result': output})

if __name__ == '__main__':
    # Render بيحدد المنفذ (Port) تلقائياً عبر متغير البيئة PORT
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
  
