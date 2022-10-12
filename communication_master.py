import os
import sys
import select
import time
import tempfile
from typing import List, IO


class CommunicationMaster:
    def __init__(self):
        # create temp file for pipe
        tmpdir = tempfile.mkdtemp()

        # create pipe to slave
        self.__pipe_to_slave_path = os.path.join(tmpdir, 'pipe_to_slave')
        if os.path.exists(self.__pipe_to_slave_path):
            os.unlink(self.__pipe_to_slave_path)
        os.mkfifo(self.__pipe_to_slave_path)

        # create pipe to slave
        self.__pipe_from_slave_path =  os.path.join(tmpdir, 'pipe_from_slave')
        if os.path.exists(self.__pipe_from_slave_path):
            os.unlink(self.__pipe_from_slave_path)
        os.mkfifo(self.__pipe_from_slave_path)

        self.__stream_to_slave = None

        self.__stream_from_slave = os.fdopen(os.open(self.__pipe_from_slave_path, os.O_RDONLY | os.O_NONBLOCK), 'r')

    def get_answer(self, msg: str) -> List[str]:
        # open stream to slave
        if self.__stream_to_slave is None:
            # time.sleep(0.5)  # wait for other thread to open for reading
            self.__stream_to_slave = open(self.__pipe_to_slave_path, 'w')

        # count lines for header
        n_msg_lines = 0
        if msg is not None:
            n_msg_lines = len(msg.splitlines())

        # send message
        self.__stream_to_slave.write(f"{n_msg_lines}\n{msg}\n")
        self.__stream_to_slave.flush()

        # wait for answer
        select.select([self.__stream_from_slave], [], [self.__stream_from_slave])
        first_line = self.__stream_from_slave.readline()
        n_answer_lines_to_read = int(first_line)

        # read full answer message
        lines = []
        for _ in range(n_answer_lines_to_read):
            lines.append(self.__stream_from_slave.readline().rstrip())

        return lines

    @property
    def pipe_to_slave_path(self):
        return self.__pipe_to_slave_path

    @property
    def pipe_from_slave_path(self):
        return self.__pipe_from_slave_path
