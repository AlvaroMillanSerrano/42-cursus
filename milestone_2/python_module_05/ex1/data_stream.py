from abc import ABC, abstractmethod
from typing import Any, List, Dict, Union, Optional


class DataStream(ABC):

    @abstractmethod
    def process_batch(self, data_batch: List[Any]) -> str:
        pass

    def filter_data(
        self,
        data_batch: List[Any],
        criteria: Optional[str] = None
    ) -> List[Any]:
        return data_batch

    def get_stats(self) -> Dict[str, Union[str, int, float]]:
        return {
            "stream_id": "",
            "processed": 0
        }


class SensorStream(DataStream):
    def __init__(self, stream_id: str):
        self.__stream_id = stream_id

    def get_id(self) -> str:
        return self.__stream_id

    def process_batch(self, data_batch: List[Any]) -> str:
        try:
            count = 0
            c_temp = 0
            temp = 0
            for data in data_batch:
                s_data = data.split(":")
                if s_data[0] == "temp":
                    c_temp += 1
                    temp += float(s_data[1])
                count += 1
            result = f"{count} readings processed, "
            result += f"avg temp: {temp/c_temp}"
        except Exception as e:
            return f"Error {e}"
        else:
            return result

    def filter_data(
        self,
        data_batch: List[Any],
        criteria: Optional[str] = None
    ) -> List[Any]:
        count = 0
        h_temps = 0
        for data in data_batch:
            count += 1
            s_data = data.split(":")
            if s_data[0] == "temp":
                if float(s_data[1]) > 49:
                    h_temps += 1
        return [count, h_temps]

    def get_stats(self) -> Dict[str, Union[str, int, float]]:
        return {
            "stream_id": self.get_id(),
            "type": "Environmental"
        }


class TransactionStream(DataStream):
    def __init__(self, stream_id: str):
        self.__stream_id = stream_id

    def get_id(self) -> str:
        return self.__stream_id

    def process_batch(self, data_batch: List[Any]) -> str:
        try:
            count = 0
            units = 0
            for data in data_batch:
                count += 1
                s_data = data.split(":")
                if s_data[0] == "buy":
                    units += int(s_data[1])
                else:
                    units -= int(s_data[1])
            result = f"{count} operation, net flow: "
            if units > -1:
                result += f"+{units} units"
            else:
                result += f"{units} units"
        except Exception as e:
            return f"Error {e}"
        else:
            return result

    def filter_data(
        self,
        data_batch: List[Any],
        criteria: Optional[str] = None
    ) -> List[Any]:
        count = 0
        l_trans = 0
        for data in data_batch:
            count += 1
            s_data = data.split(":")
            if int(s_data[1]) > 149:
                l_trans += 1
        return [count, l_trans]

    def get_stats(self) -> Dict[str, Union[str, int, float]]:
        return {
            "stream_id": self.get_id(),
            "type": "Financial"
        }


class EventStream(DataStream):
    def __init__(self, stream_id: str):
        self.__stream_id = stream_id

    def get_id(self) -> str:
        return self.__stream_id

    def process_batch(self, data_batch: List[Any]) -> str:
        try:
            count = 0
            errors = 0
            for data in data_batch:
                count += 1
                if data == "error":
                    errors += 1
            result = f"{count} events, {errors} "
            if errors == 1:
                result += "error detected"
            else:
                result += "errors detected"
        except Exception as e:
            return f"Error {e}"
        else:
            return result

    def filter_data(
        self,
        data_batch: List[Any],
        criteria: Optional[str] = None
    ) -> List[Any]:
        count = 0
        errors = 0
        for data in data_batch:
            count += 1
            if data == "error":
                errors += 1
        return [count, errors]

    def get_stats(self) -> Dict[str, Union[str, int, float]]:
        return {
            "stream_id": self.get_id(),
            "type": "System"
        }


class StreamProcessor():
    def __init__(self):
        self.__streams: List[DataStream] = []

    def add_stream(self, stream: DataStream) -> None:
        self.__streams.append(stream)

    def get_streams(self) -> List[DataStream]:
        return self.__streams

    def process_all(self, batches: Dict[str, List[Any]]) -> str:
        try:
            h_temps = 0
            l_trans = 0
            errors = 0
            analytics = "Batch 1 Results:\n"
            for stream_id, data in batches.items():
                for stream in self.get_streams():
                    if stream.get_id() == stream_id:
                        c_stream = stream.get_stats()
                        c_stats = stream.filter_data(data)
                        if c_stream["type"] == "Environmental":
                            analytics += "- Sensor data: "
                            if c_stats[0] > 1:
                                analytics += (
                                    f"{c_stats[0]} readings processed\n"
                                )
                            else:
                                analytics += (
                                    f"{c_stats[0]} reading processed\n"
                                )
                            h_temps += c_stats[1]
                        elif c_stream["type"] == "Financial":
                            analytics += "- Transaction data: "
                            if c_stats[0] > 1:
                                analytics += (
                                    f"{c_stats[0]} operations processed\n"
                                )
                            else:
                                analytics += (
                                    f"{c_stats[0]} operation processed\n"
                                )
                            l_trans += c_stats[1]
                        elif c_stream["type"] == "System":
                            analytics += "- Event data: "
                            if c_stats[0] > 1:
                                analytics += f"{c_stats[0]} events processed\n"
                            else:
                                analytics += f"{c_stats[0]} event processed\n"
                            errors += c_stats[1]
            analytics += "\nStream filtering active: High-priority data only\n"
            analytics += "Filtered results: "
            if h_temps > 0:
                if h_temps > 1:
                    analytics += f"{h_temps} critical sensor alerts"
                else:
                    analytics += f"{h_temps} critical sensor alert"
            if l_trans > 0:
                if l_trans > 1:
                    analytics += f", {l_trans} large transactions"
                else:
                    analytics += f", {l_trans} large transaction"
            if errors > 0:
                if errors > 1:
                    analytics += f", {errors} system errors"
                else:
                    analytics += f", {errors} system error"
        except Exception as e:
            return (e)
        else:
            return analytics


def main() -> None:
    s_stream = SensorStream("SENSOR_001")
    t_stream = TransactionStream("TRANS_001")
    e_stream = EventStream("EVENT_001")
    s_processor = StreamProcessor()
    s_processor.add_stream(s_stream)
    s_processor.add_stream(t_stream)
    s_processor.add_stream(e_stream)
    datas = {
        "SENSOR_001": ["temp:100.5", "humidity:65", "temp:800"],
        "TRANS_001": ["buy:150", "sell:100", "buy:75", "buy:10"],
        "EVENT_001": ["login", "ls", "logout"]
    }
    print("=== CODE NEXUS - POLYMORPHIC STREAM SYSTEM ===")
    print("\nInitializing Sensor Stream...")
    print("Stream ID: SENSOR_001, Type: Environmental Data")
    print("Processing sensor batch: [temp:22.5, humidity:65, pressure:1013]")
    sensor_batch = ['temp:22.5', 'humidity:65', 'pressure:1013']
    print(
        f"Sensor analysis: "
        f"{s_stream.process_batch(sensor_batch)}"
    )
    print("\nInitializing Transaction Stream...")
    print("Stream ID: TRANS_001, Type: Financial Data")
    print("Processing transaction batch: [buy:100, sell:150, buy:75]")
    print(
        f"Transaction analysis: "
        f"{t_stream.process_batch(['buy:100', 'sell:150', 'buy:75'])}"
    )
    print("\nInitializing Event Stream...")
    print("Stream ID: EVENT_001, Type: System Events")
    print("Processing event batch: [login, error, logout]")
    print(
        f"Event analysis: "
        f"{e_stream.process_batch(['login', 'error', 'logout'])}"
    )
    print("=== Polymorphic Stream Processing ===")
    print("Processing mixed stream types through unified interface...\n")
    print(s_processor.process_all(datas))
    print("\nAll streams processed successfully. Nexus throughput optimal.")


if __name__ == "__main__":
    main()
