FROM odoo:19.0

USER root

# Cài đặt các gói cần thiết cho PDF printing và fonts
RUN apt-get update && apt-get install -y --no-install-recommends \
    wkhtmltopdf \
    xvfb \
    xfonts-75dpi \
    xfonts-base \
    fontconfig \
    fonts-liberation \
    fonts-dejavu-core \
    fonts-dejavu \
    fonts-liberation2 \
    locales \
    tzdata \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Cài đặt locale tiếng Việt
RUN sed -i '/vi_VN.UTF-8/s/^# //g' /etc/locale.gen && \
    locale-gen vi_VN.UTF-8

# Thiết lập timezone Việt Nam
ENV TZ=Asia/Ho_Chi_Minh
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

# Tạo thư mục cho fonts
RUN mkdir -p /usr/share/fonts/truetype/vietnamese

# Tải và cài đặt font Times New Roman và các font tiếng Việt
# Cài đặt msttcorefonts (bao gồm Times New Roman)
RUN echo "ttf-mscorefonts-installer msttcorefonts/accepted-mscorefonts-eula select true" | debconf-set-selections && \
    apt-get update && \
    apt-get install -y --no-install-recommends ttf-mscorefonts-installer || \
    (curl -L https://gist.githubusercontent.com/maxwelleite/10774746/raw/ttf-mscorefonts-installer_3.6_all.deb -o /tmp/ttf-installer.deb && \
     dpkg -i /tmp/ttf-installer.deb || apt-get install -yf) && \
    rm -rf /var/lib/apt/lists/* /tmp/*

# Tải font tiếng Việt bổ sung từ Google Fonts (Roboto, Open Sans hỗ trợ tiếng Việt tốt)
RUN mkdir -p /tmp/vn-fonts && \
    cd /tmp/vn-fonts && \
    curl -L "https://github.com/google/fonts/raw/main/ofl/roboto/Roboto-Regular.ttf" -o Roboto-Regular.ttf 2>/dev/null || true && \
    curl -L "https://github.com/google/fonts/raw/main/ofl/opensans/OpenSans-Regular.ttf" -o OpenSans-Regular.ttf 2>/dev/null || true && \
    if [ -f Roboto-Regular.ttf ]; then cp Roboto-Regular.ttf /usr/share/fonts/truetype/vietnamese/; fi && \
    if [ -f OpenSans-Regular.ttf ]; then cp OpenSans-Regular.ttf /usr/share/fonts/truetype/vietnamese/; fi && \
    rm -rf /tmp/vn-fonts

# Cập nhật font cache
RUN fc-cache -f -v

# Tạo wrapper script cho wkhtmltopdf với xvfb
RUN echo '#!/bin/bash\n\
xvfb-run -a --server-args="-screen 0, 1024x768x24" /usr/bin/wkhtmltopdf "$@"' > /usr/local/bin/wkhtmltopdf-wrapper && \
    chmod +x /usr/local/bin/wkhtmltopdf-wrapper

# Tạo symlink để Odoo sử dụng
RUN ln -sf /usr/local/bin/wkhtmltopdf-wrapper /usr/local/bin/wkhtmltopdf-custom || true

# Thiết lập locale mặc định
ENV LANG=vi_VN.UTF-8
ENV LC_ALL=vi_VN.UTF-8
ENV LANGUAGE=vi_VN:en_US:en

# Tạo thư mục log
RUN mkdir -p /var/log/odoo && chown -R odoo:odoo /var/log/odoo

# Chuyển về user odoo
USER odoo

