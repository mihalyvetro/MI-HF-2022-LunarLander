import sys
from typing import List, IO


class CommunicationMaster:
    def __init__(self, input_stream: IO[str], output_stream: IO[str], error_stream: IO[str]):
        self.__input_stream = input_stream
        self.__output_stream = output_stream
        self.__error_stream = error_stream

    def get_answer(self, msg: str) -> List[str]:
        # count lines for header
        n_msg_lines = 0
        if msg is not None:
            n_msg_lines = len(msg.splitlines())

        # send message
        self.__input_stream.write(f"{n_msg_lines}\n{msg}\n")
        self.__input_stream.flush()

        # wait for answer
        try:
            first_line = self.__output_stream.readline()
            n_answer_lines_to_read = int(first_line)
        except ValueError:
            error_lines = self.__error_stream.readlines()
            raise RuntimeError('\n'.join(error_lines));

        # read full answer message
        lines = []
        for _ in range(n_answer_lines_to_read):
            lines.append(self.__output_stream.readline().rstrip())

        return lines
