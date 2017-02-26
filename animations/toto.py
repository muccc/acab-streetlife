#!/usr/bin/env python3

import urllib.request
import argparse
import json
import logging
import os
import effects

from time import sleep

TEST_PAYLOAD="""txt|col:#blue|msg:hallo|rep:1\\nseq|id:5\\nblink|col:#red"""
TEST_PAYLOAD_II="""seq|id:rain\\nseq|id:23\\nblink"""
TEST_SEARCH = [
    """[
        {
            "name": "acab",
            "payload": "%s",
            "ts": 123
        }, {
            "name": "acab",
            "payload": "%s",
            "ts": 124
        }
    ]""" % (TEST_PAYLOAD, TEST_PAYLOAD_II)
]

logger = logging.getLogger()
formatter = logging.Formatter(
        "%(asctime)s - %(levelname)-8s - %(message)s"
        )

stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)
logger.addHandler(stream_handler)

logger.setLevel(logging.WARNING)

def hexColourToTuple(colour):
    if colour.startswith("#"):
        colour = colour[1:]
    try:
        int(colour,16)
    except ValueError:
        colourMapping = {
            "blue": "0000CC",
            "red": "CC0000",
            "green": "00CC00",
            "white": "CCCCCC",
            "black": "000000",
            "yellow": "CCCC00",
        }
        if colour in colourMapping:
            colour = colourMapping[colour]
        else:
            colour = "000000"
    result = []
    for i in range(3):
        result.append(int(colour[i*2:i*2+2],16))
    return tuple(result)

class Handler:
    def __init__(self, base_url, key, secret, debug = False):
        self.base_url = base_url
        self.key = key
        self.secret = secret
        self.last = None
        self.debug = debug

    def parsePayload(self, payload):
        instructions = []
        for line in payload.splitlines():
            line = line.split("|")
            if not line:
                continue
            command = line.pop(0)
            instructions.append({"cmd": command})
            for arg in line:
                key,value = arg.split(":")
                instructions[-1][key] = value
        logging.debug(instructions)
        return instructions

    def apiGet(self, url, **params):
        query = "%s%s?key=%s&secret=%s" % ( self.base_url, url, self.key, self.secret ) + \
            "".join(["&%s=%s" % ( key, value ) for key, value in params.items()])
        logger.debug("api query '%s'", query)
        response = urllib.request.urlopen(query).read().decode("utf-8")
        logger.debug("api response '%s'", response)
        json_obj = json.loads(response)
        return json_obj

    def getLast(self, since=None):
        return self.apiGet("/last")["ts"]

    def getSearch(self, since = None):
        if self.debug:
            return json.loads(TEST_SEARCH[0])
        else:
            return self.apiGet("/search", since = since if since else self.last)

    def initiateLast(self):
        self.last = self.getLast()

    def search(self):
        search_result = self.getSearch()
        playlist = []
        logger.debug("search result: %s", search_result)
        for item in search_result:
            self.last = item["ts"]
            playlist.append(self.parsePayload(item["payload"]))
        return playlist

    def processTXT(self, msg, col = "#002A2A", rep = 1):
        col = hexColourToTuple(col)
        effects.text(msg, int(rep), col)

    def processSEQ(self, seq_id):
        logger.debug(seq_id)
        if seq_id == "rain":
            effects.rain()

    def processBlink(self, col = "#blue", rep = 1, dur = 1):
        col = hexColourToTuple(col)
        effects.blink(col, int(rep), int(dur))

    def processPlaylist(self, playlist):
        if not playlist:
            logger.debug("empty playlist")
            return
        logger.info("new playlist: %s" % str(playlist))
        for action in playlist:
            for instruction in action:
                cmd = instruction.pop("cmd")
                if cmd == "txt":
                    self.processTXT(**instruction)
                elif cmd == "seq":
                    if "id" in instruction:
                        instruction["seq_id"] = instruction.pop("id")
                    self.processSEQ(**instruction)
                elif cmd == "blink":
                    self.processBlink(**instruction)

    def loop(self, interval):
        self.initiateLast()

        try:
            while True:
                try:
                    playlist = self.search()
                    logger.debug("new playlist: %s", playlist)
                    self.processPlaylist(playlist)

                    sleep(interval)
                except Exception as e:
                    if self.debug:
                        raise e
                    logger.error(e)
                    sleep(interval)
        except KeyboardInterrupt:
            logger.info("exiting")


if __name__=="__main__":
    parser = argparse.ArgumentParser(description='TOTO ACAB Actuator')
    parser.add_argument('--verbose', '-v', action='store_true', help='Verbose mode')
    parser.add_argument('--debug', '-d', action='store_true', help='Debug mode')
    parser.add_argument('--simulate', '-s', action='store_true', help='Use predefined responses')
    parser.add_argument('--log', '-l', help='Logfile')
    parser.add_argument('--base-url', default='https://example', help='Base URL for TOTO server')
    parser.add_argument('--check-interval', default=1, type=int, help='Interval in seconds for checking backend for new payloads')
    parser.add_argument('key', help='API Key')
    parser.add_argument('secret', help='API Secret')
    args = parser.parse_args()

    if args.log:
        file_handler = logging.FileHandler(args.log,"a")
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)


    if args.verbose:
        logger.setLevel(logging.INFO)
    if args.debug:
        logger.setLevel(logging.DEBUG)

    handler = Handler(args.base_url, args.key, args.secret, args.simulate)
    handler.loop(args.check_interval)
