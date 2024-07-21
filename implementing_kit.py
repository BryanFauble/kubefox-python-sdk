"""Test running the Python Kit SDK"""


from kit import Kit
import logging

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s [%(module)s:%(lineno)d - %(levelname)s]: %(message)s",
    datefmt='%Y-%m-%d %H:%M:%S'
)

if __name__ == "__main__":
    instance = Kit.new()
    instance.start()
