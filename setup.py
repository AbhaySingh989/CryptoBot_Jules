from setuptools import setup, find_packages

setup(
    name="trading_bot",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "requests",
        "websockets",
        "python-telegram-bot",
        "python-dotenv",
        "pandas",
        "pytest",
        "cryptography==40.0.2",
        "python-socketio==5.5.1",
        "websocket-client==1.2.3",
    ],
    entry_points={
        "console_scripts": [
            "trading_bot = trading_bot.__main__:main",
        ],
    },
)
