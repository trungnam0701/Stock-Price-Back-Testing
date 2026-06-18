# 📈 Dự Án Phân Tích & Backtest Chiến Lược Giao Dịch Chứng Khoán VN5

Dự án này tập trung vào việc phân tích dữ liệu lịch sử, làm sạch dữ liệu, tính toán các chỉ báo kỹ thuật và mô phỏng giao dịch chứng khoán (Backtesting) dựa trên nhóm cổ phiếu VN5 (bao gồm **FPT**, **HPG**, **VCB**, **TCB**, và **MWG**) kết hợp với chỉ số thị trường **VNINDEX** từ năm 2019 đến năm 2026.

Chúng tôi đã thử nghiệm và đánh giá ba chiến lược giao dịch khác nhau từ cổ điển (Phân tích kỹ thuật) đến hiện đại (Học máy và Mô hình Chuỗi thời gian SARIMAX).

---

## 📋 1. Mô Tả Dự Án

Dự án được triển khai qua 4 bước chính:

1. **Thu thập & Xử lý dữ liệu**:
   - Tải dữ liệu lịch sử của nhóm cổ phiếu từ Yahoo Finance (`yfinance`) và chỉ số VNINDEX từ `vnstock`.
   - Làm sạch dữ liệu, xử lý các giá trị trống (`NaN`) và giá trị bằng `0` do các ngày nghỉ lễ tại Việt Nam (sử dụng thư viện `holidays` để đối chiếu và phân loại).
   - Nội suy (Interpolation) và chuẩn hóa dữ liệu lưu dưới dạng `raw_data.xlsx`.

2. **Kỹ thuật tính toán Chỉ báo Kỹ thuật (Feature Engineering)**:
   - Xây dựng lớp tính toán các chỉ báo kỹ thuật cơ bản và nâng cao: Đường trung bình động đơn giản/lũy thừa (**SMA/EMA**), Chỉ số sức mạnh tương đối (**RSI**), Đường trung bình hội tụ phân kỳ (**MACD**), Dải Bollinger (**Bollinger Bands**), Tỷ suất sinh lời hằng ngày (**Daily Return**), và Biến động lịch sử (**Volatility**).

3. **Phát triển Chiến lược Giao dịch (Strategy Development)**:
   - **SMA Crossover**: Mua khi SMA ngắn hạn (20 ngày) vượt lên trên SMA dài hạn (50 ngày) và bán khi cắt xuống dưới.
   - **Machine Learning Classifier**: Sử dụng các mô hình học máy (Logistic Regression, Random Forest, XGBoost) để phân loại xu hướng và tạo tín hiệu mua/bán từ các chỉ báo kỹ thuật.
   - **SARIMAX với Rolling Validation**: Áp dụng mô hình chuỗi thời gian SARIMAX với cơ chế xác thực cuộn (Rolling Validation) cập nhật liên tục để dự đoán xu hướng giá đóng cửa và tạo tín hiệu giao dịch.

4. **Kiểm thử Lịch sử (Backtesting)**:
   - Đo lường hiệu suất chiến lược so với thị trường (phương pháp Mua & Nắm giữ - Buy & Hold) thông qua các chỉ số tài chính cốt lõi: **Tổng lợi nhuận (Total Return)**, **Hệ số Sharpe (Sharpe Ratio)**, và **Mức sụt giảm tối đa (Max Drawdown)**.
   - Trực quan hóa giá trị danh mục đầu tư theo thời gian.

---

## 📂 2. Cấu Trúc Thư Mục Dự Án

Dự án được tổ chức theo dạng mô-đun hóa, giúp dễ dàng chuyển đổi từ các thử nghiệm trên Jupyter Notebook sang mã chạy thực tế (production scripts):

```text
StockPrice/
├── data/                            # Thư mục lưu trữ dữ liệu đầu vào và đầu ra
│   ├── VN5_Close_Volume.xlsx        # Dữ liệu giá đóng cửa và khối lượng VN5 gốc
│   ├── VNINDEX.xlsx                 # Dữ liệu lịch sử chỉ số VNINDEX
│   └── raw_data.xlsx                # Dữ liệu đã làm sạch và hợp nhất sau tiền xử lý
│
├── notebook/                        # Thư mục chứa các tệp Jupyter Notebook nghiên cứu
│   ├── market_analyst.ipynb         # Phân tích dữ liệu gốc, đối chiếu ngày lễ, xử lý khuyết thiếu
│   ├── ml.ipynb                     # Thử nghiệm so sánh nội suy, tạo biến và xây dựng nhãn tín hiệu
│   └── strategy_and_backtest.ipynb  # Phát triển và kiểm thử 3 chiến lược (MA, ML, SARIMAX)
│
├── scripts/                         # Các mô-đun mã nguồn Python chính
│   ├── data_handle.py               # Lớp Technical_Indicators tính toán các chỉ báo kỹ thuật
│   ├── strategy.py                  # Lớp Strategy chứa thuật toán tạo tín hiệu giao dịch (MA Crossover)
│   ├── back_testing.py              # Lớp Back_Testing mô phỏng giao dịch, tính chỉ số & vẽ biểu đồ
│   └── get_data.py                  # CLI script tải dữ liệu thực tế, chạy quy trình từ đầu đến cuối
│
└── README.md                        # Tài liệu mô tả dự án
```

---

## 📊 3. Kết Quả Backtesting Chi Tiết

Dưới đây là bảng tổng hợp kết quả kiểm thử lịch sử của **3 chiến lược** trên **5 mã cổ phiếu** mục tiêu trong thời gian nghiên cứu:

| Cổ phiếu | Chỉ số Đánh giá | Chiến lược SMA Crossover | Chiến lược Machine Learning | Chiến lược SARIMAX Rolling |
| :---: | :--- | :---: | :---: | :---: |
| **FPT** | Tổng lợi nhuận (Total Return)<br>Hệ số Sharpe (Sharpe Ratio)<br>Sụt giảm tối đa (Max Drawdown) | -26.58%<br>-1.38<br>-30.36% | -37.03%<br>-1.40<br>-39.51% | -31.86%<br>-1.19<br>-39.18% |
| **HPG** | Tổng lợi nhuận (Total Return)<br>Hệ số Sharpe (Sharpe Ratio)<br>Sụt giảm tối đa (Max Drawdown) | -4.90%<br>-0.03<br>-20.97% | +5.56%<br>+0.37<br>-7.11% | **+27.25%**<br>**+0.93**<br>**-10.02%** |
| **VCB** | Tổng lợi nhuận (Total Return)<br>Hệ số Sharpe (Sharpe Ratio)<br>Sụt giảm tối đa (Max Drawdown) | -36.56%<br>-0.78<br>-39.29% | -32.84%<br>-0.62<br>-48.60% | -24.24%<br>-0.36<br>-34.54% |
| **TCB** | Tổng lợi nhuận (Total Return)<br>Hệ số Sharpe (Sharpe Ratio)<br>Sụt giảm tối đa (Max Drawdown) | **+27.96%**<br>**+0.76**<br>**-18.95%** | **+22.00%**<br>**+0.74**<br>**-13.11%** | **+26.84%**<br>**+0.77**<br>**-20.81%** |
| **MWG** | Tổng lợi nhuận (Total Return)<br>Hệ số Sharpe (Sharpe Ratio)<br>Sụt giảm tối đa (Max Drawdown) | -17.22%<br>-0.32<br>-27.20% | +8.00%<br>+0.44<br>-14.49% | **+27.37%**<br>**+0.86**<br>**-14.46%** |

### 💡 Nhận Xét Kết Quả:
1. **Mã cổ phiếu TCB**: Đây là cổ phiếu đạt hiệu quả giao dịch tốt nhất một cách đồng đều trên cả 3 chiến lược. Lợi nhuận mang về dao động ổn định từ **22.00% đến 27.96%**, Sharpe Ratio đạt mức cao (~0.76) và Max Drawdown tương đối thấp.
2. **Chiến lược SARIMAX với Rolling Validation**: Đây là phương pháp mang lại hiệu năng cao và cải thiện vượt trội nhất đối với các cổ phiếu có tính chu kỳ và biến động mạnh như **HPG** (lợi nhuận tăng từ -4.90% lên **27.25%**) và **MWG** (lợi nhuận tăng từ -17.22% lên **27.37%**).
3. **Mã cổ phiếu FPT & VCB**: Ghi nhận hiệu suất âm trên cả 3 chiến lược thử nghiệm. Điều này chỉ ra rằng các chỉ báo kỹ thuật ngắn hạn hoặc mô hình xu hướng đơn giản chưa bắt kịp đà chuyển động của 2 mã này, hoặc cấu trúc thị trường của chúng thiên về Mua & Nắm giữ lâu dài (Buy & Hold) hơn là giao dịch ngắn hạn theo tín hiệu.

---

## 🚀 4. Hướng Dẫn Cài Đặt & Chạy Dự An

### Yêu cầu hệ thống
* Python 3.10 trở lên.
* Cài đặt các thư viện cần thiết bằng pip:

```bash
pip install pandas numpy yfinance vnstock holidays scikit-learn xgboost statsmodels matplotlib seaborn openpyxl
```
