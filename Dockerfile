# 使用pytorch的CPU版本
FROM pytorch/pytorch:latest

# 設置工作目錄
WORKDIR /myapp

# 複製PyTorch檔案到容器中
COPY test.py .

# 安裝其他必要的Python套件
RUN pip install pandas matplotlib scikit-learn schedule

# 指定容器啟動時運行的命令
CMD [ "python", "test.py" ]
