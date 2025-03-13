# Use Python 3.10 base image
FROM python:3.10

# Set up a non-root user
RUN useradd -m -u 1000 user
USER user

# Ensure ~/.local/bin is in PATH
ENV PATH="/home/user/.local/bin:$PATH"

# Set working directory
WORKDIR /app

# Copy requirements file
COPY --chown=user ./requirements.txt requirements.txt

# Upgrade pip
RUN pip install --no-cache-dir --upgrade pip

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --upgrade peft



# Copy application files
COPY --chown=user . /app

# Set the command to run FastAPI
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "7860"]
