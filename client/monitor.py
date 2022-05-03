#! /usr/bin/env python3


import socket
import sys
import logging
import threading
from packets import PacketHeader, HEADER_FIELD_TO_PACKET_TYPE, PACKET_FILTERS


class TelemetryMonitorThread(threading.Thread):


    '''TelemetryMonitorThread receives incoming telemetry packets on specified port (F12021 default port for UDP = 20777).'''


    def __init__(self, host='', port=20777):

        super().__init__(name="monitor")
        self.host, self.port = host, port
        self.socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

        # accept udp packets from host
        self.socket.bind((self.host, self.port))

        print(f"Monitoring localhost:{self.port}\n")




    def receive(self) -> tuple:

        '''This function enables the receiving of encoded packets, and uses the UDP specification for F12021 to decode the packets into a human readable format.'''

        # every telemetry packet fits in 2048 bytes
        packet = self.socket.recv(2048)
        header = PacketHeader.from_buffer_copy(packet)

        key = (header.m_packet_format, header.m_packet_version, header.m_packet_id)

        # return packet_data, packet_type
        return HEADER_FIELD_TO_PACKET_TYPE[key].unpack(packet), HEADER_FIELD_TO_PACKET_TYPE[key]




def get_packet_name(packet_type) -> str:

    '''This function gets packet name by packet type -

    example:

    "<class 'packets.PacketExampleData'>" -> "PacketExampleData".'''

    packet_name = str(packet_type).split('.')[1][:-2]

    return packet_name




def update(packet_name, packet_data, filters=[]):

    '''This function writes to associated json file if packet_name in filters or if no filters applied.'''

    if not filters or packet_name in filters:

        with open(f"../data/{packet_name}.json", "+w") as file:
            file.write(str(packet_data))




def handle_filters(filters) -> list:

    '''This function checks if all passed arguments are valid filters and returns a list containing valid filters to be applied.
    
    Packet Filters: "PacketMotionData",
                    "PacketSessionData",
                    "PacketLapData",
                    "PacketEventData",
                    "PacketParticipantsData",
                    "PacketCarSetupData",
                    "PacketCarTelemetryData",
                    "PacketCarStatusData",
                    "PacketFinalClassificationData",
                    "PacketLobbyInfoData",
                    "PacketCarDamageData",
                    "PacketSessionHistoryData"'''


    valid_filters = []
    for filter in filters:

        # check if filter is valid
        if filter not in PACKET_FILTERS:

            logging.info('invalid filter provided: %s', filter)

            print(f"\n{filter} is not a valid filter!")

        else:

            # add filter to list of valid filters
            valid_filters.append(filter)
    
    # if one or more filters supplied
    if valid_filters:

        logging.info('filtering: %s', valid_filters)

        print(f"\nFiltering: {valid_filters}\n")
    
    return valid_filters
    



def main():


    # logging configuration
    logger = logging.getLogger()

    # initial handler
    std_out = logger.handlers[0]
    logger.setLevel(logging.DEBUG)

    # log format
    formatter = logging.Formatter("[%(asctime)-19.19s] [%(threadName)-10.10s] [%(levelname)-4.4s]: %(message)s")

    # log file handler
    file_handler = logging.FileHandler('../logs/example.log')
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    # remove initial handler (comment/remove next line if you want logs to print)
    logger.removeHandler(std_out)


    # handle filters passed as command line arguments
    valid_filters = handle_filters(sys.argv[1:])


    # start monitor thread
    monitor_thread = TelemetryMonitorThread()
    monitor_thread.start()

    try:

        logging.info('monitor thread started, listening on port:%d', monitor_thread.port)

        while True:

            packet_data, packet_type = monitor_thread.receive()
            packet_name = get_packet_name(packet_type)
            update(packet_name, packet_data, valid_filters)

            
    except KeyboardInterrupt:

        logging.info('monitor thread stopped')

        print('\nStopping...')


if __name__ == '__main__':
    main()