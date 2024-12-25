# FROM python:3.8.3-alpine
# ENV PYTHONUNBUFFERED 1

# # 작업 디렉토리 생성 및 설정
# WORKDIR /app

# # 필요한 시스템 패키지 및 빌드 도구 설치
# RUN apk update && apk add --no-cache \
#     gcc \
#     musl-dev \
#     python3-dev \
#     libffi-dev \
#     libressl-dev \
#     build-base \
#     jpeg-dev \
#     zlib-dev \
#     mysql-dev \
#     curl

# # Rust 설치
# RUN curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y
# ENV PATH="/root/.cargo/bin:$PATH"

# # pip 업그레이드 및 Python 패키지 설치
# COPY requirements.txt /app/requirements.txt
# RUN pip install --upgrade pip && pip install -r requirements.txt

# # 불필요한 빌드 도구 삭제 (이미지 크기 최적화)
# RUN apk del build-base python3-dev

# # 애플리케이션 코드 복사
# COPY . /app/

# CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

FROM python:3.8.3-alpine
ENV PYTHONUNBUFFERED 1

# 작업 디렉토리 생성 및 설정
WORKDIR /app

# 필요한 시스템 패키지 및 Chrome 설치
RUN apk update && apk add --no-cache \
    gcc \
    musl-dev \
    python3-dev \
    libffi-dev \
    libressl-dev \
    build-base \
    jpeg-dev \
    zlib-dev \
    mysql-dev \
    curl \
    chromium \
    chromium-chromedriver \
    xvfb \
    libxi6 \
    libgconf-2-4 \
    dbus

RUN chromium-browser --version && chromedriver --version

# Rust 설치
RUN curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y
ENV PATH="/root/.cargo/bin:$PATH"

# Python 패키지 설치
COPY requirements.txt /app/requirements.txt
RUN pip install --upgrade pip && pip install -r requirements.txt --no-cache-dir

# 불필요한 빌드 도구 삭제 (이미지 크기 최적화)
RUN apk del build-base python3-dev

# 애플리케이션 코드 복사
COPY . /app/

# 환경 변수 추가
ENV CHROME_BIN=/usr/bin/chromium-browser
ENV CHROMEDRIVER_BIN=/usr/bin/chromedriver

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
