from abc import ABC, abstractmethod
from typing import Any


class DataProcessor(ABC):
    @abstractmethod
    def validate(self, data: Any) -> bool:
        pass

    def format_output(self, result: str) -> str:
        return str(result)

    @abstractmethod
    def process(self, data: Any) -> str:
        pass


class NumericProcessor(DataProcessor):
    def validate(self, data: Any) -> bool:
        if isinstance(data, list):
            for num in data:
                if not isinstance(num, int):
                    return False
            return True
        else:
            return False

    def process(self, data: Any) -> str:
        try:
            if not self.validate(data):
                raise ValueError("Invalid numeric data")
            sum_res = 0
            count = 0
            for num in data:
                sum_res += num
                count += 1
            result = f"Processed {count} numeric values, "
            result += f"sum={sum_res}, avg={sum_res/count}"
        except Exception as e:
            return f"Output: [ALERT]: {e}"
        else:
            return self.format_output(result)


class TextProcessor(DataProcessor):
    def validate(self, data: Any) -> bool:
        return isinstance(data, str)

    def process(self, data: Any) -> str:
        try:
            if not self.validate(data):
                raise ValueError("Invalid text data")
            words = 0
            i = 0
            while i < len(data):
                if data[i] != ' ' and (i == 0 or data[i - 1] == ' '):
                    words += 1
                i += 1
            result = f"Processed text: {i} characters, "
            result += f"{words} words"
        except Exception as e:
            return f"Output: [ALERT]: {e}"
        else:
            return self.format_output(result)


class LogProcessor(DataProcessor):
    def validate(self, data: Any) -> bool:
        if data == "ERROR: Connection timeout":
            return False
        else:
            return True

    def process(self, data: Any) -> str:
        try:
            if not self.validate(data):
                raise ValueError("ERROR level detected: Connection timeout")
        except Exception as e:
            return f"Output: [ALERT]: {e}"
        else:
            result = "[INFO] INFO level detected: System ready"
            return self.format_output(result)


def main():
    processors = [
        NumericProcessor(),
        TextProcessor(),
        LogProcessor()
    ]

    d_streams = [
        [1, 2, 3],
        "Hello Nexus ",
        "INFO: System ready"
    ]
    print("=== CODE NEXUS - DATA PROCESSOR FOUNDATION ===")
    print("\nInitializing Numeric Processor...")
    print("Processing data: [1, 2, 3, 4, 5]")
    print("Validation: Numeric data verified")
    print("Validation: Numeric data not verified")
    print(f"Output: {processors[0].process([1, 2, 3, 4, 5])}")
    print("\nInitializing Text Processor...")
    print('Processing data: "Hello Nexus World"')
    print("Validation: Text data verified")
    print("Validation: Text data not verified")
    print(f"Output: {processors[1].process('Hello Nexus World')}")
    print("\nInitializing Log Processor...")
    print('Processing data: "ERROR: Connection timeout"')
    print("Validation: Log entry verified")
    print(f"Output: {processors[2].process('ERROR: Connection timeout')}")
    print("\n=== Polymorphic Processing Demo ===\n")
    print("Code Nexus Polymorphic Data Streams in the Digital Matrix")
    print("Processing multiple data types through same interface...")
    for i in range(len(processors)):
        print(f"Result {i + 1}: {processors[i].process(d_streams[i])}")
    print("\nFoundation systems online. Nexus ready for advanced streams.")


if __name__ == "__main__":
    main()
