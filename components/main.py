# coding=utf-8

import suanpan
from suanpan.app import app
from suanpan.app.arguments import String, Json
from modules.apis import socketapi
from suanpan.log import logger

app.modules.register("socketapi", socketapi)


@app.input(String(key="inputData1"))
@app.output(String(key="outputData1"))
def main(context):
    args = context.args
    logger.info(args["inputData1"])
    socketapi.sendData(args["inputData1"])
    return args["inputData1"]


if __name__ == "__main__":
    suanpan.run(app)