# Python 3.11 image asosida
FROM python:3.11

# Ishchi katalogni yaratamiz va unga o'tamiz
WORKDIR /app

# Zarur bo'lgan fayllarni konteynerga nusxalaymiz
COPY requirements.txt .
COPY . .

# Python kutubxonalarini o'rnatamiz
RUN pip install --no-cache-dir -r requirements.txt

# Botni ishga tushiramiz
CMD ["python", "bot/main.py"]
